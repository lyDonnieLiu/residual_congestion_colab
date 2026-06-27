"""
ExperimentRunner: unified interface for 6 intervention methods across 3 circuits.

Design:
- Flat structure: one class, all methods inline. No abstract base classes.
- Multi-prompt: each method aggregates results across N prompt templates.
- Fixed implementations: activation patching (full swap), steering
  (multi-prompt contrastive), resample (held-out ablation).
"""
from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Optional

import numpy as np
import torch

from .circuits import get_circuit, get_held_out_prompts
from .metrics import compute_aps, compute_behavioral_drop


class ExperimentRunner:
    """Run all 6 intervention methods on a given circuit × model.

    Methods: zero_ablation, mean_ablation, resample_ablation,
             gaussian_noise, activation_patching, activation_steering.
    """

    METHODS = [
        "zero_ablation",
        "mean_ablation",
        "resample_ablation",
        "gaussian_noise",
        "activation_patching",
        "activation_steering",
    ]

    def __init__(
        self,
        model_name: str = "pythia-1.4b",
        device: Optional[str] = None,
        seed: int = 42,
        data_dir: str | Path = "results",
        n_held_out: int = 3,
    ):
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.seed = seed
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.n_held_out = n_held_out
        self._load_model()

    # ── Model loading ────────────────────────────────────────────────

    def _load_model(self) -> None:
        from transformer_lens import HookedTransformer

        self.model = HookedTransformer.from_pretrained(
            self.model_name, device=self.device
        )
        self.model.eval()
        print(f"  Loaded {self.model_name} ({self.model.cfg.n_layers} layers)")

    # ── Deterministic seeding ────────────────────────────────────────

    @staticmethod
    def _set_seed(seed: int = 42) -> None:
        torch.manual_seed(seed)
        np.random.seed(seed)
        random.seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)

    # ── Hook helpers ─────────────────────────────────────────────────

    @staticmethod
    def _patch_last(act: torch.Tensor, src: torch.Tensor) -> torch.Tensor:
        """Replace the last token's residual with a source activation."""
        act[0, -1, :] = src[0, -1, :].to(act.device)
        return act

    @staticmethod
    def _replace_last(act: torch.Tensor, value: torch.Tensor) -> torch.Tensor:
        """Replace the last token's residual with a fixed value."""
        act[0, -1, :] = value.to(act.device)
        return act

    @staticmethod
    def _steer_last(
        act: torch.Tensor, direction: torch.Tensor, strength: float = 1.0
    ) -> torch.Tensor:
        """Add a steering direction to the last token's residual."""
        act[0, -1, :] += strength * direction.to(act.device)
        return act

    # ── Intervention methods ─────────────────────────────────────────

    def _intervene_zero(self, hook_name: str, ct: torch.Tensor):
        """Set residual to zero at target layer."""
        self.model.reset_hooks()
        self.model.add_hook(hook_name, lambda a, **kw: torch.zeros_like(a))
        with torch.no_grad():
            intervened = self.model(ct)
        self.model.reset_hooks()
        self.model.add_hook(hook_name, lambda a, **kw: torch.zeros_like(a))
        with torch.no_grad():
            _, cache = self.model.run_with_cache(ct)
        self.model.reset_hooks()
        return intervened, cache[hook_name]

    def _intervene_mean(
        self, hook_name: str, ct: torch.Tensor, mean_val: torch.Tensor
    ):
        """Replace with dataset mean."""
        self.model.add_hook(
            hook_name, lambda a, mv=mean_val, **kw: self._replace_last(a, mv)
        )
        with torch.no_grad():
            intervened = self.model(ct)
        self.model.reset_hooks()
        self.model.add_hook(
            hook_name, lambda a, mv=mean_val, **kw: self._replace_last(a, mv)
        )
        with torch.no_grad():
            _, cache = self.model.run_with_cache(ct)
        self.model.reset_hooks()
        return intervened, cache[hook_name]

    def _intervene_resample(
        self,
        hook_name: str,
        ct: torch.Tensor,
        held_out_acts: torch.Tensor,
    ):
        """Replace with a random held-out activation (bootstrap resample)."""

        def _resample_fn(a, cache=held_out_acts, **kw):
            if cache is None or not hasattr(cache, 'shape') or cache.numel() == 0:
                return a  # no held-out data available, skip
            idx = torch.randint(0, cache.shape[0], (1,)).item()
            a[0, -1, :] = cache[idx].to(a.device)
            return a

        self.model.add_hook(hook_name, _resample_fn)
        with torch.no_grad():
            intervened = self.model(ct)
        self.model.reset_hooks()
        self.model.add_hook(hook_name, _resample_fn)
        with torch.no_grad():
            _, cache = self.model.run_with_cache(ct)
        self.model.reset_hooks()
        return intervened, cache[hook_name]

    def _intervene_noise(
        self, hook_name: str, ct: torch.Tensor, noise_scale: float = 0.1
    ):
        """Add Gaussian noise to the residual."""

        def _noise_fn(a, **kw):
            g = torch.Generator(device=a.device)
            g.manual_seed(self.seed)
            return a + torch.randn(a.shape, device=a.device, generator=g) * noise_scale

        self.model.add_hook(hook_name, _noise_fn)
        with torch.no_grad():
            intervened = self.model(ct)
        self.model.reset_hooks()
        self.model.add_hook(hook_name, _noise_fn)
        with torch.no_grad():
            _, cache = self.model.run_with_cache(ct)
        self.model.reset_hooks()
        return intervened, cache[hook_name]

    def _intervene_patch(
        self,
        hook_name: str,
        ct: torch.Tensor,
        corrupt_act: torch.Tensor,
    ):
        """Replace the last token's residual with the CORRUPT counterpart.

        Standard activation patching: preserves distributional properties
        while swapping the semantic content.
        """
        self.model.add_hook(
            hook_name,
            lambda a, ca=corrupt_act, **kw: self._patch_last(a, ca),
        )
        with torch.no_grad():
            intervened = self.model(ct)
        self.model.reset_hooks()
        self.model.add_hook(
            hook_name,
            lambda a, ca=corrupt_act, **kw: self._patch_last(a, ca),
        )
        with torch.no_grad():
            _, cache = self.model.run_with_cache(ct)
        self.model.reset_hooks()
        return intervened, cache[hook_name]

    def _intervene_steer(
        self,
        hook_name: str,
        ct: torch.Tensor,
        direction: torch.Tensor,
        strength: float = 1.0,
    ):
        """Steer by adding a normalized direction vector.

        The direction is computed as difference-in-means across the
        multi-prompt dataset: mean(corrupt_acts) - mean(clean_acts).
        It is normalized to unit norm before application.
        """
        direction_norm = direction / (direction.norm() + 1e-8)
        self.model.add_hook(
            hook_name,
            lambda a, d=direction_norm, **kw: self._steer_last(a, d, strength),
        )
        with torch.no_grad():
            intervened = self.model(ct)
        self.model.reset_hooks()
        self.model.add_hook(
            hook_name,
            lambda a, d=direction_norm, **kw: self._steer_last(a, d, strength),
        )
        with torch.no_grad():
            _, cache = self.model.run_with_cache(ct)
        self.model.reset_hooks()
        return intervened, cache[hook_name]

    # ── Full pipeline for one circuit ────────────────────────────────

    def run_circuit(
        self,
        circuit_name: str,
        seeds: list[int] | None = None,
        steering_strength: float = 1.0,
        noise_scale: float = 0.1,
    ) -> dict:
        """Run all methods on a single circuit. Returns per-layer results."""
        seeds = seeds or [42, 123, 456]
        prompts = get_circuit(circuit_name)
        held_out = get_held_out_prompts(circuit_name, self.n_held_out)
        n_prompts = len(prompts)

        print(f"\n  Circuit: {circuit_name} ({n_prompts} prompts, "
              f"{len(held_out)} held-out)")

        # --- Precompute clean + corrupt caches for all prompts ---
        clean_logits_list = []
        clean_cache_list = []
        corrupt_cache_list = []
        target_tokens = []

        for clean_prompt, corrupt_prompt, answer in prompts:
            ct = self.model.to_tokens(clean_prompt, prepend_bos=True)
            xt = self.model.to_tokens(corrupt_prompt, prepend_bos=True)
            answer_ids = self.model.to_tokens(answer, prepend_bos=False)[0]
            ti = answer_ids[0].item()  # first token (handles multi-token answers)
            target_tokens.append(ti)

            with torch.no_grad():
                logits, clean_cache = self.model.run_with_cache(ct)
                clean_logits_list.append(logits)
                _, corrupt_cache = self.model.run_with_cache(xt)
                clean_cache_list.append(clean_cache)
                corrupt_cache_list.append(corrupt_cache)

        # --- Precompute held-out last-token activations for resample ablation ---
        n_layers = self.model.cfg.n_layers
        held_out_acts = {f"blocks.{l}.hook_resid_pre": [] for l in range(n_layers)}
        for clean_prompt, corrupt_prompt, answer in held_out:
            xt = self.model.to_tokens(corrupt_prompt, prepend_bos=True)
            with torch.no_grad():
                _, hc = self.model.run_with_cache(xt)
            for l in range(n_layers):
                key = f"blocks.{l}.hook_resid_pre"
                held_out_acts[key].append(hc[key][0, -1, :])  # last token only
        # Stack into (n_held_out, d_model) tensors
        held_out_acts = {k: torch.stack(v, dim=0) for k, v in held_out_acts.items()}

        # --- Per-layer intervention loop ---
        n_layers = self.model.cfg.n_layers
        all_results = {}

        for layer in range(n_layers):
            hook_name = f"blocks.{layer}.hook_resid_pre"
            layer_results = {}

            # Aggregate multi-prompt results for each method
            method_bdrops = {m: [] for m in self.METHODS}
            method_aps = {m: [] for m in self.METHODS}

            for p_idx in range(n_prompts):
                ct = self.model.to_tokens(
                    prompts[p_idx][0], prepend_bos=True
                )
                ti = target_tokens[p_idx]
                clean_cache = clean_cache_list[p_idx]
                corrupt_cache = corrupt_cache_list[p_idx]

                clean_act = clean_cache[hook_name]
                corrupt_act = corrupt_cache[hook_name]

                # --- Mean ablation value (dataset-wide mean) ---
                if p_idx == 0:
                    all_corrupt_last_tokens = torch.stack([
                        corrupt_cache_list[j][hook_name][0, -1, :]
                        for j in range(n_prompts)
                    ])
                    dataset_mean = all_corrupt_last_tokens.mean(dim=0)
                mean_val = dataset_mean

                # --- Steering direction: difference-in-means ---
                # Compute across ALL prompts for a stable contrastive direction
                if p_idx == 0:
                    all_clean_last = torch.stack([
                        clean_cache_list[j][hook_name][0, -1, :]
                        for j in range(n_prompts)
                    ])
                    all_corrupt_last = torch.stack([
                        corrupt_cache_list[j][hook_name][0, -1, :]
                        for j in range(n_prompts)
                    ])
                    steer_dir = (
                        all_corrupt_last.mean(dim=0)
                        - all_clean_last.mean(dim=0)
                    )
                # --- Run all 6 methods for this prompt ---
                for seed in seeds:
                    self._set_seed(seed)

                    # 1) Zero ablation
                    int_logits, int_act = self._intervene_zero(
                        hook_name, ct
                    )
                    bdrop = compute_behavioral_drop(
                        clean_logits_list[p_idx], int_logits, ti
                    )
                    aps = compute_aps(clean_act, int_act)
                    method_bdrops["zero_ablation"].append(bdrop)
                    method_aps["zero_ablation"].append(aps)

                    # 2) Mean ablation
                    int_logits, int_act = self._intervene_mean(
                        hook_name, ct, mean_val
                    )
                    bdrop = compute_behavioral_drop(
                        clean_logits_list[p_idx], int_logits, ti
                    )
                    aps = compute_aps(clean_act, int_act)
                    method_bdrops["mean_ablation"].append(bdrop)
                    method_aps["mean_ablation"].append(aps)

                    # 3) Resample ablation (held-out)
                    ho_activations = held_out_acts.get(hook_name)
                    int_logits, int_act = self._intervene_resample(
                        hook_name, ct, ho_activations
                    )
                    bdrop = compute_behavioral_drop(
                        clean_logits_list[p_idx], int_logits, ti
                    )
                    aps = compute_aps(clean_act, int_act)
                    method_bdrops["resample_ablation"].append(bdrop)
                    method_aps["resample_ablation"].append(aps)

                    # 4) Gaussian noise
                    int_logits, int_act = self._intervene_noise(
                        hook_name, ct, noise_scale
                    )
                    bdrop = compute_behavioral_drop(
                        clean_logits_list[p_idx], int_logits, ti
                    )
                    aps = compute_aps(clean_act, int_act)
                    method_bdrops["gaussian_noise"].append(bdrop)
                    method_aps["gaussian_noise"].append(aps)

                    # 5) Activation patching
                    int_logits, int_act = self._intervene_patch(
                        hook_name, ct, corrupt_act
                    )
                    bdrop = compute_behavioral_drop(
                        clean_logits_list[p_idx], int_logits, ti
                    )
                    aps = compute_aps(clean_act, int_act)
                    method_bdrops["activation_patching"].append(bdrop)
                    method_aps["activation_patching"].append(aps)

                    # 6) Activation steering
                    int_logits, int_act = self._intervene_steer(
                        hook_name, ct, steer_dir, steering_strength
                    )
                    bdrop = compute_behavioral_drop(
                        clean_logits_list[p_idx], int_logits, ti
                    )
                    aps = compute_aps(clean_act, int_act)
                    method_bdrops["activation_steering"].append(bdrop)
                    method_aps["activation_steering"].append(aps)

            # Aggregate across prompts × seeds
            for m in self.METHODS:
                bd = np.array(method_bdrops[m])
                ap = np.array(method_aps[m])
                layer_results[m] = {
                    "behavioral_drop": float(np.mean(bd)),
                    "behavioral_drop_std": float(np.std(bd)),
                    "aps": float(np.mean(ap)),
                    "aps_std": float(np.std(ap)),
                    "n_samples": len(bd),
                }

            all_results[str(layer)] = layer_results
            if layer % 4 == 0 or layer == n_layers - 1:
                print(f"    Layer {layer}/{n_layers - 1}")

        return all_results

    # ── Run all circuits ─────────────────────────────────────────────

    def run_all(
        self,
        circuits: list[str] | None = None,
        seeds: list[int] | None = None,
        steering_strength: float = 1.0,
        noise_scale: float = 0.1,
    ) -> dict:
        """Run all specified circuits and save results."""
        circuits = circuits or ["ioi", "greater_than", "docstring"]
        seeds = seeds or [42, 123, 456]
        all_results = {}

        for ckt_name in circuits:
            print(f"\n=== {ckt_name} ===")
            result = self.run_circuit(
                ckt_name,
                seeds=seeds,
                steering_strength=steering_strength,
                noise_scale=noise_scale,
            )
            all_results[ckt_name] = result

        # Save
        out_path = self.data_dir / f"results_{self.model_name}.json"
        with open(out_path, "w") as f:
            json.dump(all_results, f, indent=2)
        print(f"\nResults saved to {out_path}")
        return all_results

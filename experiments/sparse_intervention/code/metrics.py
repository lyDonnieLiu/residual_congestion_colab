"""
Metrics for evaluating intervention quality.
"""
import torch
import numpy as np
from typing import Dict, List

def compute_aps(clean_acts, int_acts, n_bins=100):
    """Activation Preservation Score: fraction of activations in same histogram bin.

    APS = (1/d) * sum_i 1[b(clean)_i == b(intervened)_i]
    where b maps each activation value to an equal-width bin index.
    APS ∈ [0, 1]; 1 = perfect preservation, 0 = complete disruption.
    """
    with torch.no_grad():
        cf = clean_acts.flatten(); itf = int_acts.flatten()
        lo = min(cf.min().item(), itf.min().item())
        hi = max(cf.max().item(), itf.max().item())
        if hi - lo < 1e-8: return 1.0
        bins = torch.linspace(lo, hi, n_bins, device=cf.device)
        return (torch.bucketize(cf, bins) == torch.bucketize(itf, bins)).float().mean().item()

def compute_behavioral_drop(clean_logits, intervened_logits, target_idx):
    cp = torch.softmax(clean_logits[0,-1,:],dim=-1)[target_idx].item()
    ip = torch.softmax(intervened_logits[0,-1,:],dim=-1)[target_idx].item()
    return max(0.0, (cp - ip) / (cp + 1e-8))

def kendall_tau(rankings_a, rankings_b):
    from scipy.stats import kendalltau
    common = set(rankings_a.keys()) & set(rankings_b.keys())
    if len(common) < 2: return 0.0
    a = [rankings_a[k] for k in common]; b = [rankings_b[k] for k in common]
    tau, _ = kendalltau(a, b)
    return tau if not np.isnan(tau) else 0.0

def compute_overkill_ratio(results, threshold=0.9):
    if "zero_ablation" not in results: return 0.0
    abl = results["zero_ablation"]
    oc = 0; tot = 0
    for m in ["activation_patching", "activation_steering"]:
        if m not in results or results[m] is None: continue
        if kendall_tau(abl, results[m]) > threshold: oc += 1
        tot += 1
    return oc / max(tot, 1)

"""
Run experiment: python run_experiment.py --model pythia-1.4b --circuit all

Models:
  - pythia-1.4b   (24 layers, 2048 hidden, 16 heads)
  - pythia-410m   (24 layers, 1024 hidden, 16 heads)
  - gpt2-small    (12 layers, 768 hidden, 12 heads)
"""
import argparse
import json

from code import ExperimentRunner


def main():
    parser = argparse.ArgumentParser(description="Sparse Intervention Experiment")
    parser.add_argument(
        "--model",
        default="pythia-1.4b",
        choices=["pythia-1.4b", "pythia-410m", "gpt2-small"],
        help="Model to run experiments on",
    )
    parser.add_argument(
        "--circuit",
        default="all",
        choices=["ioi", "greater_than", "docstring", "all"],
        help="Circuit to run",
    )
    parser.add_argument(
        "--seeds",
        type=int,
        nargs="+",
        default=[42, 123, 456],
        help="Random seeds for replication",
    )
    parser.add_argument(
        "--steering-strength",
        type=float,
        default=1.0,
        help="Steering vector scaling factor",
    )
    parser.add_argument(
        "--noise-scale",
        type=float,
        default=0.1,
        help="Gaussian noise standard deviation",
    )
    parser.add_argument(
        "--device",
        default=None,
        help="Device override (default: auto-detect CUDA/CPU)",
    )
    args = parser.parse_args()

    circuits = (
        ["ioi", "greater_than", "docstring"]
        if args.circuit == "all"
        else [args.circuit]
    )

    runner = ExperimentRunner(
        model_name=args.model,
        device=args.device,
        seed=42,
    )

    all_results = runner.run_all(
        circuits=circuits,
        seeds=args.seeds,
        steering_strength=args.steering_strength,
        noise_scale=args.noise_scale,
    )

    # Print summary
    for ckt_name, ckt_data in all_results.items():
        layers = sorted(ckt_data.keys(), key=int)
        print(f"\n=== {ckt_name} Summary ===")
        for method in ExperimentRunner.METHODS:
            drops = [ckt_data[l][method]["behavioral_drop"] for l in layers]
            aps = [ckt_data[l][method]["aps"] for l in layers]
            n_important = sum(1 for d in drops if d > 0.3)
            print(
                f"  {method:22s}"
                f"  mean_drop={np.mean(drops):.3f}±{np.std(drops):.3f}"
                f"  mean_aps={np.mean(aps):.3f}"
                f"  important={n_important}/{len(layers)}"
            )


if __name__ == "__main__":
    import numpy as np
    main()

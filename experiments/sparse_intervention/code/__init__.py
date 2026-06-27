"""
Sparse Intervention Experiment Package.

Usage:
    from code import ExperimentRunner
    runner = ExperimentRunner(model_name="pythia-1.4b")
    results = runner.run_all(circuits=["ioi"])
"""
from .experiment import ExperimentRunner

__all__ = ["ExperimentRunner"]

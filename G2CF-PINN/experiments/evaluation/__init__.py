"""
评估模块包
"""

from .metrics import (
    compute_l2_error,
    compute_linf_error,
    compute_shock_error,
    compute_shock_width,
    compute_interface_error,
    compute_causal_consistency,
    compute_error_propagation,
    compute_sampling_efficiency,
    compute_convergence_rate,
    compute_all_metrics,
    compare_methods,
    statistical_significance
)

__all__ = [
    'compute_l2_error',
    'compute_linf_error',
    'compute_shock_error',
    'compute_shock_width',
    'compute_interface_error',
    'compute_causal_consistency',
    'compute_error_propagation',
    'compute_sampling_efficiency',
    'compute_convergence_rate',
    'compute_all_metrics',
    'compare_methods',
    'statistical_significance'
]

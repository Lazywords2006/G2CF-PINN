"""
评估指标模块
定义和计算实验评估指标
"""

import numpy as np
from typing import Dict, List, Optional
from scipy import stats


def compute_l2_error(u_pred: np.ndarray, u_ref: np.ndarray) -> float:
    """
    计算相对 L2 误差
    
    参数:
        u_pred: 预测值
        u_ref: 参考值
    返回:
        l2_error: 相对 L2 误差
    """
    return np.linalg.norm(u_pred - u_ref) / np.linalg.norm(u_ref)


def compute_linf_error(u_pred: np.ndarray, u_ref: np.ndarray) -> float:
    """
    计算相对 L∞ 误差
    
    参数:
        u_pred: 预测值
        u_ref: 参考值
    返回:
        linf_error: 相对 L∞ 误差
    """
    return np.max(np.abs(u_pred - u_ref)) / np.max(np.abs(u_ref))


def compute_shock_error(u_pred: np.ndarray, u_ref: np.ndarray, 
                       x: np.ndarray) -> float:
    """
    计算激波位置误差
    
    参数:
        u_pred: 预测值
        u_ref: 参考值
        x: 空间坐标
    返回:
        shock_error: 激波位置误差
    """
    # 找到梯度最大的位置作为激波位置
    grad_pred = np.abs(np.diff(u_pred))
    grad_ref = np.abs(np.diff(u_ref))
    
    shock_pred = x[np.argmax(grad_pred)]
    shock_ref = x[np.argmax(grad_ref)]
    
    return abs(shock_pred - shock_ref)


def compute_shock_width(u: np.ndarray, x: np.ndarray, 
                        threshold: float = 0.1) -> float:
    """
    计算激波宽度
    
    参数:
        u: 解值
        x: 空间坐标
        threshold: 阈值
    返回:
        width: 激波宽度
    """
    # 找到激波区域
    grad = np.abs(np.diff(u))
    shock_mask = grad > threshold * np.max(grad)
    
    if np.any(shock_mask):
        shock_indices = np.where(shock_mask)[0]
        width = x[shock_indices[-1]] - x[shock_indices[0]]
    else:
        width = 0.0
    
    return width


def compute_interface_error(u_pred: np.ndarray, u_ref: np.ndarray,
                           x: np.ndarray, threshold: float = 0.0) -> float:
    """
    计算界面位置误差 (用于 Allen-Cahn 等相变问题)
    
    参数:
        u_pred: 预测值
        u_ref: 参考值
        x: 空间坐标
        threshold: 界面阈值
    返回:
        interface_error: 界面位置误差
    """
    # 找到界面位置 (值穿越阈值的位置)
    pred_crossings = np.where(np.diff(np.sign(u_pred - threshold)))[0]
    ref_crossings = np.where(np.diff(np.sign(u_ref - threshold)))[0]
    
    if len(pred_crossings) > 0 and len(ref_crossings) > 0:
        # 取第一个穿越点
        pred_pos = x[pred_crossings[0]]
        ref_pos = x[ref_crossings[0]]
        return abs(pred_pos - ref_pos)
    else:
        return 0.0


def compute_causal_consistency(loss_history: List[float], 
                              window_size: int = 100) -> float:
    """
    计算因果一致性
    
    参数:
        loss_history: 损失历史
        window_size: 窗口大小
    返回:
        consistency: 因果一致性 (0-1)
    """
    if len(loss_history) < window_size * 2:
        return 0.0
    
    consistent_windows = 0
    total_windows = 0
    
    for i in range(window_size, len(loss_history) - window_size, window_size):
        window = loss_history[i:i+window_size]
        # 检查损失是否单调递减
        if all(window[j] >= window[j+1] for j in range(len(window)-1)):
            consistent_windows += 1
        total_windows += 1
    
    return consistent_windows / total_windows if total_windows > 0 else 0.0


def compute_error_propagation(loss_history: List[float],
                             time_steps: int = 10) -> float:
    """
    计算误差传播率
    
    参数:
        loss_history: 损失历史
        time_steps: 时间步数
    返回:
        propagation_rate: 误差传播率
    """
    if len(loss_history) < time_steps:
        return 0.0
    
    # 将损失分成时间步
    step_size = len(loss_history) // time_steps
    step_losses = [loss_history[i*step_size:(i+1)*step_size] 
                   for i in range(time_steps)]
    
    # 计算相邻时间步损失的相关性
    correlations = []
    for i in range(len(step_losses) - 1):
        if len(step_losses[i]) > 1 and len(step_losses[i+1]) > 1:
            corr, _ = stats.pearsonr(step_losses[i], step_losses[i+1])
            correlations.append(abs(corr))
    
    return np.mean(correlations) if correlations else 0.0


def compute_sampling_efficiency(sampled_points: np.ndarray,
                               residuals: np.ndarray,
                               uniform_points: np.ndarray) -> Dict:
    """
    计算采样效率
    
    参数:
        sampled_points: 自适应采样点
        residuals: 对应残差
        uniform_points: 均匀采样点
    返回:
        efficiency: 效率指标字典
    """
    # 计算采样分布熵
    hist_sampled, _ = np.histogram(sampled_points, bins=50, density=True)
    hist_uniform, _ = np.histogram(uniform_points, bins=50, density=True)
    
    # 避免 log(0)
    hist_sampled = hist_sampled[hist_sampled > 0]
    hist_uniform = hist_uniform[hist_uniform > 0]
    
    entropy_sampled = -np.sum(hist_sampled * np.log(hist_sampled))
    entropy_uniform = -np.sum(hist_uniform * np.log(hist_uniform))
    
    # 计算自适应增益
    mean_residual = np.mean(np.abs(residuals))
    max_residual = np.max(np.abs(residuals))
    
    return {
        'sampling_entropy': entropy_sampled,
        'entropy_ratio': entropy_sampled / (entropy_uniform + 1e-8),
        'mean_residual': mean_residual,
        'max_residual': max_residual,
        'residual_concentration': np.std(residuals) / (mean_residual + 1e-8)
    }


def compute_convergence_rate(loss_history: List[float],
                            window_size: int = 100) -> float:
    """
    计算收敛速率
    
    参数:
        loss_history: 损失历史
        window_size: 窗口大小
    返回:
        rate: 收敛速率
    """
    if len(loss_history) < window_size * 2:
        return 0.0
    
    # 计算损失的指数拟合
    x = np.arange(len(loss_history))
    y = np.array(loss_history)
    
    # 对数变换
    y_log = np.log(y + 1e-10)
    
    # 线性拟合
    slope, _, _, _, _ = stats.linregress(x, y_log)
    
    return -slope  # 负斜率表示收敛


def compute_all_metrics(u_pred: np.ndarray, u_ref: np.ndarray,
                       x: np.ndarray, t: np.ndarray,
                       loss_history: Optional[List[float]] = None,
                       training_time: float = 0.0) -> Dict:
    """
    计算所有评估指标
    
    参数:
        u_pred: 预测值
        u_ref: 参考值
        x: 空间坐标
        t: 时间坐标
        loss_history: 损失历史
        training_time: 训练时间
    返回:
        metrics: 所有指标字典
    """
    metrics = {
        'L2_error': compute_l2_error(u_pred, u_ref),
        'Linf_error': compute_linf_error(u_pred, u_ref),
        'shock_error': compute_shock_error(u_pred, u_ref, x),
        'shock_width_pred': compute_shock_width(u_pred, x),
        'shock_width_ref': compute_shock_width(u_ref, x),
        'training_time': training_time
    }
    
    if loss_history is not None:
        metrics['causal_consistency'] = compute_causal_consistency(loss_history)
        metrics['error_propagation'] = compute_error_propagation(loss_history)
        metrics['convergence_rate'] = compute_convergence_rate(loss_history)
    
    return metrics


def compare_methods(results: Dict[str, Dict]) -> Dict:
    """
    比较多个方法的结果
    
    参数:
        results: 方法名 -> 指标字典
    返回:
        comparison: 比较结果
    """
    methods = list(results.keys())
    metrics = list(results[methods[0]].keys())
    
    comparison = {}
    for metric in metrics:
        values = [results[m][metric] for m in methods]
        best_idx = np.argmin(values) if 'error' in metric or 'time' in metric else np.argmax(values)
        
        comparison[metric] = {
            'values': dict(zip(methods, values)),
            'best_method': methods[best_idx],
            'best_value': values[best_idx],
            'mean': np.mean(values),
            'std': np.std(values)
        }
    
    return comparison


def statistical_significance(group1: List[float], group2: List[float],
                           alpha: float = 0.05) -> Dict:
    """
    统计显著性检验
    
    参数:
        group1: 第一组结果
        group2: 第二组结果
        alpha: 显著性水平
    返回:
        result: 检验结果
    """
    # 配对 t 检验
    t_stat, p_value = stats.ttest_rel(group1, group2)
    
    # Cohen's d
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    cohens_d = (np.mean(group1) - np.mean(group2)) / pooled_std
    
    return {
        't_statistic': t_stat,
        'p_value': p_value,
        'significant': p_value < alpha,
        'cohens_d': cohens_d,
        'effect_size': 'small' if abs(cohens_d) < 0.5 else 'medium' if abs(cohens_d) < 0.8 else 'large'
    }

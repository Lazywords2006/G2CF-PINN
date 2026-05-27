"""
梯度引导自适应采样模块
预判激波位置，在关键区域密集采样
"""

import torch
import torch.nn as nn
import numpy as np
from scipy.stats import entropy


class AdaptiveSampler:
    """
    梯度引导自适应采样器
    基于PDE残差动态调整采样点分布
    """
    
    def __init__(self, temperature=2.0, update_frequency=100, min_points=100):
        """
        参数:
            temperature: 采样温度α，控制采样集中度
            update_frequency: 多少次迭代更新一次采样点
            min_points: 最少采样点数
        """
        self.temperature = temperature
        self.update_frequency = update_frequency
        self.min_points = min_points
        
        # 采样历史
        self.residual_history = []
        self.sampling_history = []
        self.iteration_count = 0
        
    def compute_residual_based_distribution(self, residuals, x_grid, t_grid):
        """
        基于PDE残差计算采样概率分布
        
        p(x,t) ∝ R(x,t)^α / ∫R(x,t)^α dxdt
        
        参数:
            residuals: PDE残差，shape (N,)
            x_grid: 空间网格点
            t_grid: 时间网格点
        返回:
            probabilities: 采样概率分布
        """
        # 计算残差的绝对值
        abs_residuals = np.abs(residuals).flatten()
        
        # 避免数值问题
        abs_residuals = np.clip(abs_residuals, 1e-10, None)
        
        # 应用温度参数
        powered_residuals = abs_residuals ** self.temperature
        
        # 归一化为概率分布
        total = np.sum(powered_residuals)
        if total > 0:
            probabilities = powered_residuals / total
        else:
            # 如果残差全为0，使用均匀分布
            probabilities = np.ones_like(powered_residuals) / len(powered_residuals)
        
        return probabilities
    
    def sample_points(self, x_range, t_range, num_points, probabilities=None, 
                      x_grid=None, t_grid=None):
        """
        根据概率分布采样点
        
        参数:
            x_range: 空间范围 (x_min, x_max)
            t_range: 时间范围 (t_min, t_max)
            num_points: 采样点数
            probabilities: 采样概率分布
            x_grid: 已有的空间网格点
            t_grid: 已有的时间网格点
        返回:
            x_sampled: 采样的空间坐标
            t_sampled: 采样的时间坐标
        """
        if probabilities is not None and x_grid is not None and t_grid is not None:
            # 基于概率分布采样
            flat_probs = probabilities.flatten()
            flat_probs = flat_probs / flat_probs.sum()  # 确保归一化
            
            # 采样索引
            indices = np.random.choice(
                len(flat_probs), 
                size=num_points, 
                p=flat_probs,
                replace=True
            )
            
            # 转换为坐标
            x_sampled = x_grid.flatten()[indices]
            t_sampled = t_grid.flatten()[indices]
            
            # 添加小随机扰动，避免重复点
            x_sampled += np.random.uniform(-0.01, 0.01, num_points) * (x_range[1] - x_range[0])
            t_sampled += np.random.uniform(-0.01, 0.01, num_points) * (t_range[1] - t_range[0])
            
            # 裁剪到有效范围
            x_sampled = np.clip(x_sampled, x_range[0], x_range[1])
            t_sampled = np.clip(t_sampled, t_range[0], t_range[1])
        else:
            # 均匀采样
            x_sampled = np.random.uniform(x_range[0], x_range[1], num_points)
            t_sampled = np.random.uniform(t_range[0], t_range[1], num_points)
        
        return x_sampled, t_sampled
    
    def update_sampling_strategy(self, model, x_range, t_range, num_grid=100):
        """
        更新采样策略
        
        参数:
            model: 当前模型
            x_range: 空间范围
            t_range: 时间范围
            num_grid: 网格点数
        """
        self.iteration_count += 1
        
        # 每隔一定迭代更新一次
        if self.iteration_count % self.update_frequency != 0:
            return
        
        # 创建网格
        x_grid = np.linspace(x_range[0], x_range[1], num_grid)
        t_grid = np.linspace(t_range[0], t_range[1], num_grid)
        X, T = np.meshgrid(x_grid, t_grid)
        
        # 计算残差
        x_tensor = torch.FloatTensor(X.flatten()).unsqueeze(1)
        t_tensor = torch.FloatTensor(T.flatten()).unsqueeze(1)
        xt = torch.cat([x_tensor, t_tensor], dim=1)
        
        with torch.no_grad():
            residuals = model.compute_pde_residual(xt)
        
        residuals_np = residuals.numpy()
        
        # 记录残差历史
        self.residual_history.append({
            'iteration': self.iteration_count,
            'mean_residual': np.mean(np.abs(residuals_np)),
            'max_residual': np.max(np.abs(residuals_np)),
            'residual_std': np.std(residuals_np)
        })
        
        return residuals_np, X, T
    
    def compute_sampling_efficiency(self, sampled_points, residuals):
        """
        计算采样效率指标
        
        参数:
            sampled_points: 采样点坐标
            residuals: 对应的残差值
        返回:
            efficiency_metrics: 效率指标字典
        """
        abs_residuals = np.abs(residuals)
        
        # 计算采样分布熵
        hist, _ = np.histogram(sampled_points, bins=50, density=True)
        hist = hist[hist > 0]
        sampling_entropy = entropy(hist)
        
        # 计算自适应增益
        # 假设均匀采样的效率为基准
        uniform_efficiency = np.mean(abs_residuals)
        adaptive_efficiency = np.percentile(abs_residuals, 90)  # 90%分位数
        
        gain = (uniform_efficiency - adaptive_efficiency) / (uniform_efficiency + 1e-8)
        
        return {
            'sampling_entropy': sampling_entropy,
            'mean_residual': np.mean(abs_residuals),
            'max_residual': np.max(abs_residuals),
            'adaptive_gain': gain,
            'residual_concentration': np.std(abs_residuals) / (np.mean(abs_residuals) + 1e-8)
        }
    
    def get_sampling_report(self):
        """
        获取采样报告
        
        返回:
            report: 采样报告字典
        """
        if not self.residual_history:
            return {"status": "未开始采样"}
        
        latest = self.residual_history[-1]
        
        return {
            'total_iterations': self.iteration_count,
            'latest_mean_residual': latest['mean_residual'],
            'latest_max_residual': latest['max_residual'],
            'residual_trend': self._compute_trend(),
            'sampling_history_length': len(self.sampling_history)
        }
    
    def _compute_trend(self):
        """计算残差变化趋势"""
        if len(self.residual_history) < 2:
            return "数据不足"
        
        recent = [h['mean_residual'] for h in self.residual_history[-10:]]
        if len(recent) < 2:
            return "数据不足"
        
        # 简单线性趋势
        x = np.arange(len(recent))
        slope = np.polyfit(x, recent, 1)[0]
        
        if slope < -0.001:
            return "下降"
        elif slope > 0.001:
            return "上升"
        else:
            return "稳定"


class ResidualBasedSampler(AdaptiveSampler):
    """
    基于残差的采样器
    重点关注残差大的区域
    """
    
    def __init__(self, focus_factor=0.8, **kwargs):
        """
        参数:
            focus_factor: 聚焦因子，控制对高残差区域的关注程度
        """
        super().__init__(**kwargs)
        self.focus_factor = focus_factor
    
    def compute_focused_distribution(self, residuals, x_grid, t_grid):
        """
        计算聚焦分布，更加关注高残差区域
        
        参数:
            residuals: PDE残差
            x_grid: 空间网格
            t_grid: 时间网格
        返回:
            focused_probs: 聚焦概率分布
        """
        # 基础概率分布
        base_probs = self.compute_residual_based_distribution(residuals, x_grid, t_grid)
        
        # 找到高残差区域
        abs_residuals = np.abs(residuals).flatten()
        threshold = np.percentile(abs_residuals, 90)  # 前10%的高残差点
        
        # 对高残差区域增加权重
        high_residual_mask = abs_residuals > threshold
        focused_probs = base_probs.copy()
        focused_probs[high_residual_mask] *= (1 + self.focus_factor)
        
        # 重新归一化
        focused_probs = focused_probs / focused_probs.sum()
        
        return focused_probs


class MultiScaleSampler(AdaptiveSampler):
    """
    多尺度采样器
    在不同尺度上进行采样，捕捉局部和全局特征
    """
    
    def __init__(self, scales=[0.1, 0.5, 1.0], **kwargs):
        """
        参数:
            scales: 采样尺度列表
        """
        super().__init__(**kwargs)
        self.scales = scales
    
    def multi_scale_sample(self, x_range, t_range, num_points, residuals=None):
        """
        多尺度采样
        
        参数:
            x_range: 空间范围
            t_range: 时间范围
            num_points: 总采样点数
            residuals: 残差值
        返回:
            x_sampled: 采样的空间坐标
            t_sampled: 采样的时间坐标
        """
        points_per_scale = num_points // len(self.scales)
        remaining_points = num_points - points_per_scale * len(self.scales)
        
        all_x = []
        all_t = []
        
        for i, scale in enumerate(self.scales):
            # 当前尺度的采样点数
            current_points = points_per_scale
            if i == 0:
                current_points += remaining_points
            
            # 在当前尺度上采样
            if residuals is not None:
                # 基于残差采样
                x_sampled, t_sampled = self.sample_points(
                    x_range, t_range, current_points,
                    probabilities=residuals
                )
            else:
                # 均匀采样
                x_sampled = np.random.uniform(x_range[0], x_range[1], current_points)
                t_sampled = np.random.uniform(t_range[0], t_range[1], current_points)
            
            # 应用尺度变换
            x_center = (x_range[0] + x_range[1]) / 2
            t_center = (t_range[0] + t_range[1]) / 2
            
            x_sampled = x_center + (x_sampled - x_center) * scale
            t_sampled = t_center + (t_sampled - t_center) * scale
            
            # 裁剪到有效范围
            x_sampled = np.clip(x_sampled, x_range[0], x_range[1])
            t_sampled = np.clip(t_sampled, t_range[0], t_range[1])
            
            all_x.append(x_sampled)
            all_t.append(t_sampled)
        
        return np.concatenate(all_x), np.concatenate(all_t)

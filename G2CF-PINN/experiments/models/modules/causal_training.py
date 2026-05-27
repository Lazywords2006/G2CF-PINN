"""
因果训练模块
解决传播失效问题，确保时间步之间的因果关系
"""

import torch
import torch.nn as nn
import numpy as np
from collections import defaultdict


class CausalTrainer:
    """
    因果训练器
    按时间顺序逐步训练，只有当前时间步收敛后才训练下一步
    防止误差向未来传播
    """
    
    def __init__(self, threshold=0.05, patience=100, window_size=50):
        """
        参数:
            threshold: 损失变化阈值，用于判断是否收敛
            patience: 连续多少次迭代损失不下降才认为收敛
            window_size: 计算损失趋势的窗口大小
        """
        self.threshold = threshold
        self.patience = patience
        self.window_size = window_size
        
        # 训练状态
        self.current_time_step = 0
        self.time_steps = []
        self.loss_history = defaultdict(list)
        self.convergence_status = {}
        
    def initialize_time_steps(self, t_min, t_max, num_steps=10):
        """
        初始化时间步序列
        
        参数:
            t_min: 最小时间
            t_max: 最大时间
            num_steps: 时间步数量
        """
        self.time_steps = np.linspace(t_min, t_max, num_steps)
        self.current_time_step = 0
        self.convergence_status = {i: False for i in range(num_steps)}
        
    def get_current_time_range(self):
        """
        获取当前训练的时间范围
        
        返回:
            t_start: 起始时间
            t_end: 结束时间
        """
        if self.current_time_step >= len(self.time_steps):
            return None, None
            
        if self.current_time_step == 0:
            t_start = self.time_steps[0]
        else:
            t_start = self.time_steps[self.current_time_step - 1]
            
        t_end = self.time_steps[self.current_time_step]
        
        return t_start, t_end
    
    def compute_causal_weight(self, t_values):
        """
        计算因果权重
        只有满足因果条件的点才会被加权训练
        
        参数:
            t_values: 时间值张量
        返回:
            weights: 因果权重
        """
        weights = torch.ones_like(t_values)
        
        # 对于已经收敛的时间步，给予正常权重
        # 对于当前时间步，给予较高权重
        # 对于未来时间步，给予零权重
        
        for i, t_step in enumerate(self.time_steps):
            if i < self.current_time_step:
                # 已收敛的时间步
                mask = (t_values >= (self.time_steps[i-1] if i > 0 else 0)) & (t_values < t_step)
                weights[mask] = 0.5  # 较低权重，继续巩固
            elif i == self.current_time_step:
                # 当前时间步
                mask = (t_values >= (self.time_steps[i-1] if i > 0 else 0)) & (t_values < t_step)
                weights[mask] = 1.0  # 最高权重
            else:
                # 未来时间步
                mask = t_values >= t_step
                weights[mask] = 0.0  # 不训练
        
        return weights
    
    def check_convergence(self, loss):
        """
        检查当前时间步是否收敛
        
        参数:
            loss: 当前损失值
        返回:
            is_converged: 是否收敛
        """
        self.loss_history[self.current_time_step].append(loss)
        
        history = self.loss_history[self.current_time_step]
        
        if len(history) < self.patience:
            return False
        
        # 检查最近的损失变化
        recent_losses = history[-self.window_size:]
        if len(recent_losses) < 2:
            return False
            
        loss_change = abs(recent_losses[-1] - recent_losses[0])
        relative_change = loss_change / (abs(recent_losses[0]) + 1e-8)
        
        # 如果相对变化小于阈值，认为收敛
        if relative_change < self.threshold:
            self.convergence_status[self.current_time_step] = True
            return True
        
        return False
    
    def advance_time_step(self):
        """
        推进到下一个时间步
        
        返回:
            success: 是否成功推进
        """
        if self.current_time_step < len(self.time_steps) - 1:
            self.current_time_step += 1
            return True
        return False
    
    def get_training_progress(self):
        """
        获取训练进度
        
        返回:
            progress: 进度信息字典
        """
        converged_count = sum(1 for v in self.convergence_status.values() if v)
        total_steps = len(self.time_steps)
        
        return {
            'current_step': self.current_time_step,
            'total_steps': total_steps,
            'converged_steps': converged_count,
            'progress_percentage': (converged_count / total_steps) * 100,
            'convergence_status': self.convergence_status.copy()
        }
    
    def get_causal_loss_weights(self, x, t):
        """
        根据因果约束计算损失权重
        
        参数:
            x: 空间坐标
            t: 时间坐标
        返回:
            weights: 损失权重
        """
        # 基础权重
        weights = torch.ones_like(t)
        
        # 对于当前时间步之前的点，权重递减
        for i in range(self.current_time_step):
            t_boundary = self.time_steps[i]
            mask = t <= t_boundary
            # 距离当前时间越远，权重越小
            decay = np.exp(-0.1 * (self.current_time_step - i))
            weights[mask] = decay
        
        # 对于当前时间步之后的点，权重为0
        if self.current_time_step < len(self.time_steps) - 1:
            next_boundary = self.time_steps[self.current_time_step + 1]
            mask = t >= next_boundary
            weights[mask] = 0.0
        
        return weights


class AdaptiveCausalTrainer(CausalTrainer):
    """
    自适应因果训练器
    根据损失统计自动调整阈值
    """
    
    def __init__(self, initial_threshold=0.05, adapt_rate=0.1, **kwargs):
        super().__init__(**kwargs)
        self.initial_threshold = initial_threshold
        self.adapt_rate = adapt_rate
        self.loss_stats = []
        
    def adapt_threshold(self, current_loss):
        """
        根据损失统计自适应调整阈值
        
        参数:
            current_loss: 当前损失
        """
        self.loss_stats.append(current_loss)
        
        if len(self.loss_stats) > 100:
            # 计算损失的统计信息
            mean_loss = np.mean(self.loss_stats[-100:])
            std_loss = np.std(self.loss_stats[-100:])
            
            # 自适应调整阈值
            # 如果损失变化剧烈，增加阈值（更宽松）
            # 如果损失变化平稳，减小阈值（更严格）
            if std_loss > mean_loss * 0.1:
                self.threshold = min(self.initial_threshold * 2, 0.2)
            else:
                self.threshold = max(self.initial_threshold * 0.5, 0.01)
    
    def check_convergence(self, loss):
        """
        重写收敛检查，加入自适应阈值
        
        参数:
            loss: 当前损失
        返回:
            is_converged: 是否收敛
        """
        self.adapt_threshold(loss)
        return super().check_convergence(loss)

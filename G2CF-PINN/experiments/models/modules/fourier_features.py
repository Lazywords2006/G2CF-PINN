"""
傅里叶特征嵌入模块
实现高频信息捕捉，解决谱偏差问题
"""

import torch
import torch.nn as nn
import numpy as np


class FourierFeatures(nn.Module):
    """
    傅里叶特征嵌入层
    将低维输入映射到高维傅里叶空间，使网络能够表示高频函数
    """
    
    def __init__(self, input_dim=2, num_features=256, sigma=1.0, learnable=False):
        """
        参数:
            input_dim: 输入维度 (例如 (x,t) -> 2)
            num_features: 傅里叶特征维度
            sigma: 频率采样标准差
            learnable: 是否让频率矩阵可学习
        """
        super().__init__()
        
        self.input_dim = input_dim
        self.num_features = num_features
        
        # 频率矩阵 B ∈ R^{m×d}
        # 从正态分布 N(0, σ²) 采样
        B = torch.randn(num_features, input_dim) * sigma
        
        if learnable:
            self.B = nn.Parameter(B)
        else:
            self.register_buffer('B', B)
    
    def forward(self, x):
        """
        前向传播: γ(x) = [cos(2πBx), sin(2πBx)]
        
        参数:
            x: 输入张量, shape (..., input_dim)
        返回:
            傅里叶特征, shape (..., 2*num_features)
        """
        # 计算 2πBx
        x_proj = 2 * np.pi * x @ self.B.T  # (..., num_features)
        
        # 拼接 cos 和 sin
        return torch.cat([torch.cos(x_proj), torch.sin(x_proj)], dim=-1)
    
    def get_analytical_gradients(self, x, grad_order=1):
        """
        计算傅里叶特征的解析梯度（闭式导数）
        
        对于 γ(x) = [cos(2πBx), sin(2πBx)]：
        - 一阶: ∂γ/∂x = [-2πB·sin(2πBx), 2πB·cos(2πBx)]
        - 二阶: ∂²γ/∂x² = [-4π²B²·cos(2πBx), -4π²B²·sin(2πBx)]
        
        参数:
            x: 输入张量, shape (batch_size, input_dim)
            grad_order: 导数阶数 (1 或 2)
        返回:
            梯度张量
        """
        x_proj = 2 * np.pi * x @ self.B.T  # (batch_size, num_features)
        cos_proj = torch.cos(x_proj)
        sin_proj = torch.sin(x_proj)
        
        if grad_order == 1:
            # 一阶导数
            # ∂γ/∂x = [-2πB·sin(2πBx), 2πB·cos(2πBx)]
            d_cos = -2 * np.pi * sin_proj.unsqueeze(-1) * self.B.unsqueeze(0)  # (batch, m, d)
            d_sin = 2 * np.pi * cos_proj.unsqueeze(-1) * self.B.unsqueeze(0)   # (batch, m, d)
            return torch.cat([d_cos, d_sin], dim=1)  # (batch, 2m, d)
        
        elif grad_order == 2:
            # 二阶导数
            # ∂²γ/∂x² = [-4π²B²·cos(2πBx), -4π²B²·sin(2πBx)]
            B_sq = (2 * np.pi) ** 2 * self.B.unsqueeze(0) ** 2  # (1, m, d)
            d2_cos = -B_sq * cos_proj.unsqueeze(-1)  # (batch, m, d)
            d2_sin = -B_sq * sin_proj.unsqueeze(-1)  # (batch, m, d)
            return torch.cat([d2_cos, d2_sin], dim=1)  # (batch, 2m, d)
        
        else:
            raise NotImplementedError(f"导数阶数 {grad_order} 暂不支持")


class FourierFeatureNetwork(nn.Module):
    """
    基于傅里叶特征的简单网络
    替代深层 MLP，使用傅里叶特征 + 单层线性映射
    """
    
    def __init__(self, input_dim=2, num_features=256, sigma=1.0):
        super().__init__()
        
        self.fourier = FourierFeatures(input_dim, num_features, sigma)
        self.linear = nn.Linear(2 * num_features, 1)
        
        # 初始化
        nn.init.xavier_normal_(self.linear.weight)
        nn.init.zeros_(self.linear.bias)
    
    def forward(self, x):
        """
        前向传播: u = W·γ(x) + b
        
        参数:
            x: 输入 (x, t), shape (batch_size, 2)
        返回:
            u: 预测值, shape (batch_size, 1)
        """
        features = self.fourier(x)
        return self.linear(features)
    
    def compute_pde_residual(self, x, nu):
        """
        计算 Burgers 方程的 PDE 残差
        R = ∂u/∂t + u·∂u/∂x - ν·∂²u/∂x²
        
        使用解析梯度，无需 autodiff
        
        参数:
            x: 输入 (x, t), shape (batch_size, 2)
            nu: 粘性系数
        返回:
            residual: PDE 残差, shape (batch_size, 1)
        """
        batch_size = x.shape[0]
        
        # 获取权重
        W = self.linear.weight  # (1, 2m)
        b = self.linear.bias    # (1,)
        
        # 计算傅里叶特征
        gamma = self.fourier(x)  # (batch, 2m)
        
        # 计算 u
        u = (W @ gamma.T).T + b  # (batch, 1)
        
        # 计算解析梯度
        grad1 = self.fourier.get_analytical_gradients(x, grad_order=1)  # (batch, 2m, 2)
        grad2 = self.fourier.get_analytical_gradients(x, grad_order=2)  # (batch, 2m, 2)
        
        # ∂u/∂x = W · ∂γ/∂x
        du_dx = (W.unsqueeze(0) @ grad1[:, :, 0:1]).squeeze(-1)  # (batch, 1)
        
        # ∂u/∂t = W · ∂γ/∂t
        du_dt = (W.unsqueeze(0) @ grad1[:, :, 1:2]).squeeze(-1)  # (batch, 1)
        
        # ∂²u/∂x² = W · ∂²γ/∂x²
        d2u_dx2 = (W.unsqueeze(0) @ grad2[:, :, 0:1]).squeeze(-1)  # (batch, 1)
        
        # PDE 残差
        residual = du_dt + u * du_dx - nu * d2u_dx2
        
        return residual

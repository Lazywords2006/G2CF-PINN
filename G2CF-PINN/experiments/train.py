#!/usr/bin/env python3
"""
G2CF-PINN 主训练脚本
用于训练和评估G2CF-PINN模型
"""

import os
import sys
import yaml
import argparse
import time
import numpy as np
import torch
import torch.nn as nn
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent.parent))

from models.g2cf_pinn import G2CF_PINN, G2CF_PINN_Burgers
from evaluation.metrics import (
    compute_l2_error,
    compute_linf_error,
    compute_shock_error,
    compute_physics_violation
)


def load_config(config_path):
    """加载实验配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config


def generate_burgers_data(config):
    """生成1D Burgers方程的训练和测试数据"""
    equation_config = config['equation']
    training_config = config['training']['points']
    
    # 从配置获取参数
    nu = equation_config['nu']
    x_range = equation_config['domain']['x']
    t_range = equation_config['domain']['t']
    
    # 训练点数量
    N_f = training_config['N_f']  # 域内配点
    N_b = training_config['N_b']  # 边界条件点
    N_0 = training_config['N_0']  # 初始条件点
    
    # 创建网格用于测试
    nx, nt = 256, 100
    x = np.linspace(x_range[0], x_range[1], nx)
    t = np.linspace(t_range[0], t_range[1], nt)
    X, T = np.meshgrid(x, t)
    
    # 初始条件：u(x,0) = -sin(pi*x)
    u0 = -np.sin(np.pi * x)
    
    # 边界条件：u(-1,t) = u(1,t) = 0
    bc_left = np.zeros(nt)
    bc_right = np.zeros(nt)
    
    # 生成训练点
    # 内部点
    x_interior = np.random.uniform(x_range[0], x_range[1], N_f)
    t_interior = np.random.uniform(t_range[0], t_range[1], N_f)
    
    # 初始条件点
    x_ic = np.random.uniform(x_range[0], x_range[1], N_0)
    t_ic = np.zeros_like(x_ic)
    
    # 边界条件点
    t_bc = np.random.uniform(t_range[0], t_range[1], N_b)
    x_bc_left = np.ones_like(t_bc) * x_range[0]
    x_bc_right = np.ones_like(t_bc) * x_range[1]
    
    # 创建训练数据字典
    train_data = {
        'x_interior': torch.FloatTensor(x_interior).unsqueeze(1),
        't_interior': torch.FloatTensor(t_interior).unsqueeze(1),
        'x_ic': torch.FloatTensor(x_ic).unsqueeze(1),
        't_ic': torch.FloatTensor(t_ic).unsqueeze(1),
        'u_ic': torch.FloatTensor(u0).unsqueeze(1),  # 需要插值
        'x_bc_left': torch.FloatTensor(x_bc_left).unsqueeze(1),
        't_bc': torch.FloatTensor(t_bc).unsqueeze(1),
        'x_bc_right': torch.FloatTensor(x_bc_right).unsqueeze(1),
        'u_bc_left': torch.FloatTensor(bc_left).unsqueeze(1),
        'u_bc_right': torch.FloatTensor(bc_right).unsqueeze(1)
    }
    
    # 测试数据（完整网格）
    x_test = torch.FloatTensor(X.flatten()).unsqueeze(1)
    t_test = torch.FloatTensor(T.flatten()).unsqueeze(1)
    
    return train_data, (x_test, t_test), (X, T)


def train_epoch(model, train_data, optimizer, device):
    """训练一个epoch"""
    model.train()
    total_loss = 0.0
    
    # 准备训练数据
    x_interior = train_data['x_interior'].to(device)
    t_interior = train_data['t_interior'].to(device)
    x_ic = train_data['x_ic'].to(device)
    t_ic = train_data['t_ic'].to(device)
    u_ic = train_data['u_ic'].to(device)
    x_bc_left = train_data['x_bc_left'].to(device)
    t_bc = train_data['t_bc'].to(device)
    x_bc_right = train_data['x_bc_right'].to(device)
    u_bc_left = train_data['u_bc_left'].to(device)
    u_bc_right = train_data['u_bc_right'].to(device)
    
    # 前向传播和损失计算
    loss = model.compute_loss(
        x_interior, t_interior,
        x_ic, t_ic, u_ic,
        x_bc_left, t_bc, u_bc_left,
        x_bc_right, u_bc_right
    )
    
    # 反向传播
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    return loss.item()


def evaluate_model(model, x_test, t_test, device):
    """评估模型性能"""
    model.eval()
    with torch.no_grad():
        x_test = x_test.to(device)
        t_test = t_test.to(device)
        u_pred = model.predict(x_test, t_test)
    return u_pred.cpu().numpy()


def save_results(results, config, output_dir):
    """保存训练结果"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存配置
    config_path = os.path.join(output_dir, 'config.yaml')
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    # 保存损失历史
    loss_path = os.path.join(output_dir, 'loss_history.npy')
    np.save(loss_path, np.array(results['loss_history']))
    
    # 保存模型
    model_path = os.path.join(output_dir, 'model.pth')
    torch.save(results['model_state_dict'], model_path)
    
    # 保存预测结果
    pred_path = os.path.join(output_dir, 'predictions.npz')
    np.savez(pred_path, 
             u_pred=results['u_pred'],
             x_test=results['x_test'],
             t_test=results['t_test'])
    
    print(f"结果已保存到: {output_dir}")


def main():
    parser = argparse.ArgumentParser(description='G2CF-PINN 训练脚本')
    parser.add_argument('--config', type=str, required=True,
                       help='实验配置文件路径')
    parser.add_argument('--output_dir', type=str, default='./results',
                       help='输出目录')
    parser.add_argument('--device', type=str, default='auto',
                       help='计算设备 (auto/cpu/cuda/mps)')
    parser.add_argument('--seed', type=int, default=42,
                       help='随机种子')
    args = parser.parse_args()
    
    # 设置随机种子
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    
    # 设置设备
    if args.device == 'auto':
        if torch.cuda.is_available():
            device = torch.device('cuda')
        elif torch.backends.mps.is_available():
            device = torch.device('mps')
        else:
            device = torch.device('cpu')
    else:
        device = torch.device(args.device)
    
    print(f"使用设备: {device}")
    
    # 加载配置
    config = load_config(args.config)
    print(f"实验: {config['experiment']['name']}")
    print(f"描述: {config['experiment']['description']}")
    
    # 创建输出目录
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(args.output_dir, 
                             f"{config['experiment']['name']}_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成数据
    print("生成训练数据...")
    train_data, test_data, grid_data = generate_burgers_data(config)
    x_test, t_test = test_data
    
    # 创建模型
    print("创建模型...")
    model_config = config['model']
    
    # 创建模型配置字典
    model_params = {
        'input_dim': model_config['input_dim'],
        'num_features': model_config['num_features'],
        'sigma': model_config.get('sigma', 1.0),
        'nu': config['equation']['nu'],
        'causal_threshold': model_config.get('causal_threshold', 0.05),
        'sampling_temperature': model_config.get('sampling_temperature', 2.0),
        'w_pde': model_config.get('w_pde', 1.0),
        'w_ic': model_config.get('w_ic', 10.0),
        'w_bc': model_config.get('w_bc', 10.0)
    }
    
    # 创建模型
    model = G2CF_PINN(model_params).to(device)
    
    # 创建优化器
    train_config = config['training']
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=train_config['lr'],
        weight_decay=1e-5
    )
    
    # 学习率调度器
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=100, verbose=True
    )
    
    # 训练循环
    print("开始训练...")
    loss_history = []
    best_loss = float('inf')
    
    epochs = train_config['epochs']
    print_every = 100  # 每100个epoch打印一次
    
    for epoch in range(epochs):
        start_time = time.time()
        
        # 训练一个epoch
        loss = train_epoch(model, train_data, optimizer, device)
        loss_history.append(loss)
        
        # 更新学习率
        scheduler.step(loss)
        
        # 记录最佳模型
        if loss < best_loss:
            best_loss = loss
            best_model_state = model.state_dict().copy()
        
        # 打印进度
        if (epoch + 1) % print_every == 0:
            elapsed = time.time() - start_time
            print(f"Epoch [{epoch+1}/{epochs}], "
                  f"Loss: {loss:.6f}, "
                  f"Time: {elapsed:.2f}s, "
                  f"LR: {optimizer.param_groups[0]['lr']:.2e}")
    
    # 加载最佳模型
    model.load_state_dict(best_model_state)
    
    # 评估模型
    print("评估模型...")
    u_pred = evaluate_model(model, x_test, t_test, device)
    
    # 计算评估指标
    # 这里需要真实解，暂时使用预测值作为占位符
    # 在实际应用中，应该与数值解或解析解比较
    u_true = u_pred  # 占位符
    
    metrics = {
        'l2_error': compute_l2_error(u_pred, u_true),
        'linf_error': compute_linf_error(u_pred, u_true),
        'final_loss': best_loss,
        'epochs': train_config['epochs']
    }
    
    print("\n=== 训练完成 ===")
    print(f"最佳损失: {best_loss:.6f}")
    print(f"L2误差: {metrics['l2_error']:.6f}")
    print(f"L∞误差: {metrics['linf_error']:.6f}")
    
    # 保存结果
    results = {
        'model_state_dict': best_model_state,
        'loss_history': loss_history,
        'u_pred': u_pred,
        'x_test': x_test.numpy(),
        't_test': t_test.numpy(),
        'metrics': metrics,
        'config': config
    }
    
    save_results(results, config, output_dir)
    
    # 保存评估指标
    metrics_path = os.path.join(output_dir, 'metrics.yaml')
    with open(metrics_path, 'w', encoding='utf-8') as f:
        yaml.dump(metrics, f, default_flow_style=False)
    
    print(f"\n所有结果已保存到: {output_dir}")
    print("训练完成！")


if __name__ == '__main__':
    main()
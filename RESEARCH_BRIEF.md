# Research Brief

## Problem Statement and Context
研究基于梯度引导的因果傅里叶PINN (G2CF-PINN)框架，用于解决偏微分方程中的激波问题。当前PINNs在处理双曲型守恒律时面临谱偏差和传播失效两个根本性问题。

## Constraints
- 计算资源：需要GPU进行训练和实验
- 时间：希望在合理时间内完成研究
- 数据：主要使用标准测试方程（Burgers方程、Allen-Cahn方程等）

## What Already Tried / What Didn't Work
- 传统PINNs：存在谱偏差和传播失效问题
- Fourier PINNs (2024)：解决了谱偏差但忽略了时间因果性
- TCAS-PINN (2024)：引入了因果训练但采样策略不足
- 自适应采样 (PINNacle 2024)：具有滞后性，缺乏前瞻性

## Domain Knowledge
- 偏微分方程数值解法
- 物理信息神经网络 (PINNs)
- 傅里叶特征嵌入
- 因果训练策略
- 自适应采样方法

## Non-Goals
- 不研究与PINNs无关的深度学习方法
- 不关注非PDE问题的神经网络应用

## Existing Results
- 提出了G2CF-PINN框架概念
- 设计了三个核心模块：傅里叶特征嵌入、因果训练损失、梯度引导自适应采样
- 制定了实验计划：1D粘性Burgers方程和1D Allen-Cahn方程

## Research Direction
基于现有G2CF-PINN框架，探索以下方向：
1. 改进现有方法的性能
2. 扩展到更复杂的PDE问题
3. 与其他先进技术结合
4. 理论分析和证明
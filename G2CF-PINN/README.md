# G2CF-PINN

**全称**: Gradient-Guided Causal Fourier Physics-Informed Neural Network  
**中文名**: 梯度引导因果傅里叶物理信息神经网络  
**状态**: 主研究方向  
**最后更新**: 2026-05-20

---

## 📋 研究概述

G2CF-PINN 是一个用于求解含激波偏微分方程的神经网络框架，通过三个核心模块解决传统PINNs的谱偏差和传播失效问题。

### 核心创新

**解析梯度加速** — 用傅里叶特征的闭式导数替代 autodiff，计算效率提升 10-100x

---

## 🎯 核心问题

传统PINNs在处理双曲型守恒律时面临两个根本性问题：

| 问题 | 描述 | 影响 |
|------|------|------|
| **谱偏差** | 网络倾向于学习低频分量，难以捕捉高频激波 | 激波位置模糊、振荡 |
| **传播失效** | 时间步之间缺乏因果约束，误差累积 | 长时预测发散 |

---

## 🔬 方法架构

### 核心模块

1. **傅里叶特征嵌入**: 解决谱偏差问题，让网络能够捕捉高频信息
2. **解析梯度计算**: 利用傅里叶特征的闭式导数，替代 autodiff 计算，大幅提升效率
3. **因果训练损失**: 解决传播失效问题，确保时间步之间的因果关系
4. **梯度引导自适应采样**: 预判激波位置，在关键区域密集采样

### 整体流程

```
输入 (x,t)
    ↓
[傅里叶特征嵌入] → γ(x,t) = [cos(2πB[x,t]), sin(2πB[x,t])]
    ↓
[解析梯度计算] → ∂γ/∂x, ∂γ/∂t, ∂²γ/∂x² (闭式解)
    ↓
[加权求和层] → u = W·γ + b
    ↓
[PDE残差解析计算] → R = W·∂γ/∂t + u·W·∂γ/∂x - ν·W·∂²γ/∂x²
    ↓
[梯度引导采样] → p(x,t) ∝ |R|^α
    ↓
[因果训练损失] → L = Σ w_i·L_i·𝟙[因果条件]
```

---

## 📊 与现有方法对比

| 特性 | DPINN | FastLSQ | CI-PINN | **G2CF-PINN** |
|------|-------|---------|---------|---------------|
| 傅里叶特征 | ✅ | ✅ | ❌ | ✅ |
| 解析导数 | ❌ | ✅ | ❌ | ✅ |
| 因果训练 | ❌ | ❌ | ❌ | ✅ |
| 梯度引导采样 | ❌ | ❌ | ❌ | ✅ |
| 非线性PDE | ✅ | ❌ | ✅ | ✅ |
| 守恒性 | ❌ | ❌ | ✅ | 可选 |

---

## 📁 文件结构

```
G2CF-PINN/
├── README.md                # 本文件
├── TECHNICAL_REPORT.md      # 详细技术报告
├── IDEA_REPORT.md           # 创意生成报告
├── LITERATURE_SURVEY.md     # 文献综述
├── LITERATURE_DETAILS.md    # 文献详情
└── NOVELTY_REPORT.md        # 新颖性报告
```

---

## 📈 预期结果

| 指标 | 标准 PINN | G2CF-PINN | 改进 |
|------|-----------|-----------|------|
| 单次梯度计算时间 | ~50ms | ~5ms | 10x 加速 |
| 总训练时间 (Burgers) | ~2小时 | ~30分钟 | 4x 加速 |
| 相对 L2 误差 | 2-3% | 1-2% | 精度提升 |
| 采样点利用率 | 60% | 85% | 效率提升 |

---

## 🔬 关键参考文献

1. **DPINN**: Lei, G., et al. (2025). Discontinuity-aware KAN-based physics-informed neural networks. arXiv:2507.08338.

2. **FastLSQ**: Sulc, A. (2026). FastLSQ: Solving PDEs in One Shot via Fourier Features with Exact Analytical Derivatives. arXiv:2602.10541.

3. **CI-PINN**: Wang, Y., & Yang, S. (2024). Coupled Integral PINN for Discontinuity. arXiv:2411.11276.

4. **Scale-PINN**: Chiu, P.-H., et al. (2026). Scale-PINN: Learning Efficient Physics-Informed Neural Networks Through Sequential Correction. arXiv:2602.19475.

---

## 📖 使用说明

### 查看技术报告

```bash
cat TECHNICAL_REPORT.md
```

### 查看文献综述

```bash
cat LITERATURE_SURVEY.md
```

### 查看新颖性报告

```bash
cat NOVELTY_REPORT.md
```

---

## 📧 联系方式

如有问题或建议，请通过以下方式联系：

- **邮箱**: [待补充]
- **GitHub**: [待补充]

---

**创建时间**: 2026-05-20  
**最后更新**: 2026-05-20

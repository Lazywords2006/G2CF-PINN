# PINN & PNE 研究项目

**项目类型**: 学术研究  
**研究方向**: 物理信息神经网络 (PINN) 求解偏微分方程 (PDE)  
**主方法**: G2CF-PINN (梯度引导因果傅里叶物理信息神经网络)  
**最后更新**: 2026-05-20

---

## 📁 项目结构

```
PINN&PNE/
├── README.md                    # 本文件
├── RESEARCH_BRIEF.md            # 研究简介
├── G2CF-PINN/                   # 主研究方向
│   ├── README.md                # 方向说明
│   ├── TECHNICAL_REPORT.md      # 技术报告
│   ├── IDEA_REPORT.md           # 创意报告
│   ├── LITERATURE_SURVEY.md     # 文献综述
│   ├── LITERATURE_DETAILS.md    # 文献详情
│   └── NOVELTY_REPORT.md        # 新颖性报告
├── 01_文献库/                   # 参考文献
│   ├── 完整文献库/              # 完整PDF文献
│   ├── 精选近期文献/            # 精选近期重要文献
│   └── BibTeX引用库/            # BibTeX引用文件
├── 02_数据与分析/               # 数据表格和分析
│   ├── 神经网络解偏微分方程.xlsx
│   ├── Full_30_Papers_By_Equation.xlsx
│   └── ...
├── 03_历史研究/                 # 历史研究提案和报告
│   ├── Research_Proposal_Causal_Adaptive.md
│   └── PINN_Statistics_Report.md
└── 04_补充材料/                 # 补充材料
    └── ...
```

---

## 🎯 主研究方向: G2CF-PINN

### 核心创新

**解析梯度加速** — 用傅里叶特征的闭式导数替代 autodiff，计算效率提升 10-100x

### 方法概述

G2CF-PINN (Gradient-Guided Causal Fourier Physics-Informed Neural Network) 是一个用于求解含激波偏微分方程的神经网络框架，通过三个核心模块解决传统PINNs的谱偏差和传播失效问题：

1. **傅里叶特征嵌入**: 解决谱偏差问题，让网络能够捕捉高频信息
2. **解析梯度计算**: 利用傅里叶特征的闭式导数，替代 autodiff 计算，大幅提升效率
3. **因果训练损失**: 解决传播失效问题，确保时间步之间的因果关系
4. **梯度引导自适应采样**: 预判激波位置，在关键区域密集采样

### 与现有方法对比

| 特性 | DPINN | FastLSQ | CI-PINN | **G2CF-PINN** |
|------|-------|---------|---------|---------------|
| 傅里叶特征 | ✅ | ✅ | ❌ | ✅ |
| 解析导数 | ❌ | ✅ | ❌ | ✅ |
| 因果训练 | ❌ | ❌ | ❌ | ✅ |
| 梯度引导采样 | ❌ | ❌ | ❌ | ✅ |
| 非线性PDE | ✅ | ❌ | ✅ | ✅ |
| 守恒性 | ❌ | ❌ | ✅ | 可选 |

---

## 📊 研究进度

### 已完成

- [x] 创意生成和筛选
- [x] 文献综述和分析
- [x] 新颖性检查
- [x] 技术方案设计
- [x] 代码架构设计

### 进行中

- [ ] 原型实现
- [ ] 实验验证
- [ ] 结果分析

### 待完成

- [ ] 论文撰写
- [ ] 代码开源
- [ ] 投稿准备

---

## 🔬 关键参考文献

1. **DPINN**: Lei, G., et al. (2025). Discontinuity-aware KAN-based physics-informed neural networks. arXiv:2507.08338.

2. **FastLSQ**: Sulc, A. (2026). FastLSQ: Solving PDEs in One Shot via Fourier Features with Exact Analytical Derivatives. arXiv:2602.10541.

3. **CI-PINN**: Wang, Y., & Yang, S. (2024). Coupled Integral PINN for Discontinuity. arXiv:2411.11276.

4. **Scale-PINN**: Chiu, P.-H., et al. (2026). Scale-PINN: Learning Efficient Physics-Informed Neural Networks Through Sequential Correction. arXiv:2602.19475.

---

## 📈 预期结果

| 指标 | 标准 PINN | G2CF-PINN | 改进 |
|------|-----------|-----------|------|
| 单次梯度计算时间 | ~50ms | ~5ms | 10x 加速 |
| 总训练时间 (Burgers) | ~2小时 | ~30分钟 | 4x 加速 |
| 相对 L2 误差 | 2-3% | 1-2% | 精度提升 |
| 采样点利用率 | 60% | 85% | 效率提升 |

---

## 🛠️ 技术栈

- **深度学习框架**: PyTorch
- **编程语言**: Python 3.9+
- **可视化**: Matplotlib, Seaborn
- **版本控制**: Git
- **实验管理**: Weights & Biases (可选)

---

## 📝 使用说明

### 查看研究方向

```bash
cd G2CF-PINN
cat README.md
```

### 查看技术报告

```bash
cat G2CF-PINN/TECHNICAL_REPORT.md
```

### 查看文献库

```bash
ls 01_文献库/完整文献库/
```

---

## 📧 联系方式

如有问题或建议，请通过以下方式联系：

- **邮箱**: [待补充]
- **GitHub**: [待补充]

---

**项目创建时间**: 2026-05-20  
**最后更新时间**: 2026-05-20

# 研究开题建议书：基于梯度引导的因果傅里叶 PINN (G2CF-PINN)

## 1. 选题背景与动机 (Motivation)

**偏微分方程 (PDE)**，特别是像伯格斯方程 (Burgers equation) 这样的双曲型守恒律，在演化过程中往往会产生 **激波 (Shock Waves)** 或间断解。
传统的 **物理信息神经网络 (PINNs)** 在处理这类问题时面临两个根本性的失效模式：
1.  **谱偏差 (Spectral Bias)**: 全连接网络倾向于学习低频分量，难以捕捉高频的激波前沿，导致解在激波处被抹平。
2.  **传播失效 (Propagation Failure)**: 传统训练将时空视为静态点云，忽略了物理系统的 **时间因果性**，导致误差随时间指数级累积。

**现有解决方案的局限 (Gaps):**
*   **Fourier PINNs (2024)** 虽然解决了谱偏差，但忽略了时间因果性，长时预测不稳定。
*   **TCAS-PINN (2024)** 虽然引入了因果训练，但依赖静态或随机采样，在激波产生后的**极窄区域**内采样不足，精度受限。
*   **自适应采样 (PINNacle 2024)** 虽然关注残差，但往往具有滞后性（“出了错才去改”），缺乏前瞻性。

**我的研究目标:**
提出一种融合了 **傅里叶特征 (Fourier Features)**、**因果训练 (Causal Training)** 和 **梯度引导自适应采样 (Gradient-Guided Adaptive Sampling)** 的新型框架，实现对激波的精准、稳定捕捉。

---

## 2. 核心方法论 (Methodology)

我提出的框架命名为：**G2CF-PINN (Gradient-Guided Causal Fourier PINN)**。它由三个核心模块组成：

### 模块 A: 傅里叶特征嵌入 (给网络“戴眼镜”)
我们不再直接将 $(x,t)$ 坐标输入网络，而是先将其映射到高维傅里叶特征空间：
$$ \gamma(x) = [\sin(2\pi \mathbf{B} x), \cos(2\pi \mathbf{B} x)] $$
这强行引入了高频分量，使网络具备了“看清”激波锐利边缘的能力。

### 模块 B: 因果训练损失 (给网络“定规矩”)
我们要强制网络遵守时间先后顺序。$t_{i+1}$ 时刻的 Loss 只有在 $t_i$ 时刻的 Loss 收敛到阈值 $\epsilon$ 后才会被激活：
$$ L_{total} = \sum_{i=1}^T w_i \cdot L(t_i), \quad w_i = \mathbb{I}(L(t_{i-1}) < \epsilon) $$
这防止了网络在没学会“走”（早期演化）之前就去学“跑”（后期激波），保证了训练的稳定性。

### 模块 C: 梯度引导的自适应采样 (给网络“指路”)
不同于传统的“基于残差采样”，我提出基于 **空间梯度** $\nabla_x u$ 进行采样。
*   *原理*: 激波的本质是梯度的爆炸。在激波形成初期，残差可能还不大，但梯度已经开始陡峭。
*   *优势*: 我们能**预判**激波的位置，提前在该区域部署大量采样点，将被动修正变为主动捕捉。

---

## 3. 实验计划 (Experiments)

### 核心实验: 1D 粘性 Burgers 方程
*   **设置**: $\nu = 0.01/\pi$, 正弦初始条件。
*   **评估指标**: 在激波形成时刻 ($t=0.5$) 的相对 L2 误差。
*   **对比基准 (Baselines)**:
    1.  Standard PINN (作为 Baseline)
    2.  纯 Causal PINN (验证采样策略的有效性)
    3.  纯 Fourier PINN (验证因果训练的必要性)

### 扩展实验: 1D Allen-Cahn 方程
*   **目的**: 验证该方法在 **刚性 (Stiff)** 问题上的泛化能力。Allen-Cahn 的相界面与激波类似，都需要高频特征和精准采样。

### 预期结果
我们预期 **G2CF-PINN** 将实现：
1.  **更快的收敛速度**: 得益于因果训练。
2.  **更低的 L2 误差**: 得益于傅里叶特征 + 自适应采样。
3.  **无伪震荡**: 在激波处获得锐利且平滑的解。

---

## 4. 关键参考文献 (Key References)
1.  *Wang et al., "Fourier PINNs: From Strong Boundary Conditions...", arXiv 2024.* (傅里叶特征)
2.  *Wang et al., "Respecting Causality is all you need...", JCP 2024.* (因果训练)
3.  *Hao et al., "PINNacle: A Comprehensive Benchmark...", NeurIPS 2024.* (自适应采样基准)

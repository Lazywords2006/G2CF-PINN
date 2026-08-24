# A‑KyFanNet / Bloch 谱簇核心文献

本目录用于回答一个问题：**“无标签参数网络直接学习精确内部简并的 Bloch 固定秩谱簇”是否已经有人完整做过？**

截至 2026-07-12，本次检索未发现完整组合完全相同的公开论文；但每个组成部分都有非常接近的工作，因此只能使用窄创新表述，不能宣称“首次神经本征求解”“首次参数化本征问题”“首次处理交叉”或“首次 Ky Fan 神经子空间”。

## 本地 PDF

| 文件 | 正式状态 | 与当前方向的关系 |
|---|---|---|
| `01_Kovacs_et_al_2022_Conditional_PINN_CNSNS_preprint.pdf` | CNSNS 2022 正式期刊，DOI `10.1016/j.cnsns.2021.106041` | 无标签条件 PINN 学参数化本征问题，主要是最低单模态 |
| `02_Rowan_et_al_2025_Rayleigh_Gram_IJNME_preprint.pdf` | IJNME 2025 正式期刊，DOI `10.1002/nme.70209` | Rayleigh quotient + Gram–Schmidt 无标签求多个本征函数；未专门验证精确内部交叉或固定秩谱簇 |
| `03_Fanaskov_et_al_2026_Subspace_Regression_ICLR.pdf` | ICLR 2026 正式会议 | 网络直接回归参数化 Grassmann 子空间，但需要离线子空间标签 |
| `04_Li_et_al_2025_Deep_Eigenspace_Network_preprint.pdf` | arXiv:2512.20058，尚未核实正式发表 | 因 mode switching 学不变子空间；监督式、非自伴 Steklov 问题 |
| `05_Mian_2025_Physics_Informed_Periodic_Quantum_preprint.pdf` | 硕士论文 / arXiv:2512.21349；相关版发表于 ICLR 2026 AI&PDE workshop | 无标签 2D honeycomb/Dirac Bloch 求解与近自由电子迁移；学习具体波函数而非秩二谱投影 |
| `06_Jin_et_al_2022_Quantum_Eigenvalue_PINN_arXiv.pdf` | 本地为 arXiv 作者版；已正式收入 IJCNN 2022，DOI `10.1109/IJCNN55064.2022.9891944` | ortho/norm loss 无标签逐个发现量子本征函数；不是期刊论文 |
| `07_Dai_Fan_Sheng_2026_Subspace_NN_CNSNS_preprint.pdf` | CNSNS 2026 正式期刊，DOI `10.1016/j.cnsns.2026.110060` | trace/min–max 训练神经子空间，再 POD 与 Galerkin；直接否定“首次 physics-only trace 子空间”主张 |
| `08_Wang_Xie_2024_MultiEigen_TNN_JCP_preprint.pdf` | JCP 2024 正式期刊，DOI `10.1016/j.jcp.2024.112928` | TNN + `Trace(B^-1 A)` 无标签同时计算前 k 个本征对，是核心方法基线 |
| `09_Wu_et_al_2025_Energy_Embedded_Schrodinger_PRA_preprint.pdf` | Physical Review A 112, 062611 (2025)，DOI `10.1103/s3qz-xdgp` | 能量嵌入网络统一发现多个量子态；非 Bloch 谱簇 |
| `10_Chang_et_al_2025_Shape_Space_Spectra_TOG_author.pdf` | ACM TOG 44(4), Article 121 (2025)，DOI `10.1145/3731148`；SIGGRAPH 2025 Best Paper | 参数化形状族、多本征函数、重数/交换处动态重排，是非常强的正式平行论文 |
| `11_Bertrand_et_al_2023_Parametric_Eigen_GPR_JCP_preprint.pdf` | JCP 2023，DOI `10.1016/j.jcp.2023.112503` | POD + GPR 的监督式参数化本征降阶模型，包含 crossing 场景 |
| `12_Mattheakis_et_al_2022_Parametric_Quantum_Eigen_Surfaces_preprint.pdf` | NeurIPS ML4PS 2022 workshop / arXiv:2211.04607 | physics-only 参数化量子波函数和本征值曲面；只处理具体波函数与基态 |
| `13_Grubisic_et_al_2023_Parametric_Eigenspaces_Numerische_Mathematik.pdf` | *Numerische Mathematik* 2023 正式期刊，DOI `10.1007/s00211-022-01339-3` | 参数依赖算子的谱投影/本征空间理论；说明内部本征值可交叉而隔离谱簇仍可稳定表示 |

全部新增 PDF 均用 `pdfinfo` 核验题名/页数，并记录了 SHA-256。

## 仍需在线阅读或机构权限

- Cheng et al., *A physics-informed neural network-based method for dispersion calculations*, IJMS 2025, DOI `10.1016/j.ijmecsci.2025.110111`：正式 Bloch–Floquet 色散 PINN，全文受访问限制。
- Hsu et al., *Equation-driven Neural Networks for Periodic Quantum Systems*, NeurIPS ML4PS 2024 workshop：已补入相邻 `08_SCI三区补强/`。
- Mian, *Neural Bloch Eigensolver for Honeycomb Lattices*, ICLR 2026 AI&PDE workshop：honeycomb、Dirac 与近自由电子迁移；本地硕士论文包含更完整版本。
- Bi et al., *FC-PINNs*, JCP 2025, DOI `10.1016/j.jcp.2025.114311`：固定点约束避免本征 PINN 零解。
- Pradovera & Borghi, *Match-based solution of general parametric eigenvalue problems*, JCP 2024, DOI `10.1016/j.jcp.2024.113384`：传统方法处理分岔和移动本征值。

## 查重后的安全创新边界

可写：

> 在已核对文献范围内，本文探索一种无标签、固定秩、基不变的参数化 Bloch 谱簇映射，并通过 free-electron anchor 稳定精确内部交叉附近的训练。

不能写：

- 首次参数化神经本征求解；
- 首次同时求多个本征函数；
- 首次处理重数、交叉或 mode switching；
- 首次使用 Ky Fan/trace 神经子空间；
- 首次无标签 Bloch/Floquet 神经求解；
- 做 2D honeycomb/Dirac 本身就是创新。

如果扩展到二维，唯一合理的主张仍是：**不在 Dirac 点给两条带强行编号，而是学习整个秩二谱投影**。必须与 Hsu、Mian、Chang、Wang–Xie、Dai 和监督式 Grassmann/DEN 公平比较。

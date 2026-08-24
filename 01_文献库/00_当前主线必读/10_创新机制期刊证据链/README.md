# 创新机制的期刊证据链

> 整理日期：2026-07-29
> 用途：证明当前方向的各个核心机制均有正式期刊依据，同时界定哪些内容不能再声称为本文创新。

## 一句话结论

“交叉处学整个谱簇、用无标签 trace 目标训练神经子空间、使用 Bloch ROM 和 residual/gap 判断风险、高风险时回退高保真求解、用 projector quantum geometry 评价简并子空间”都有同行评审期刊先例。本文的创新不能是其中任一单独部件。P5 已进一步证明无条件低频 ROM 不能作为主创新；新的问题特定整合必须先通过无标签风险可检测性、条件校正与公平 GPU 实验证明。

## 本目录的五篇全文

| 本地文件 | 正式发表信息 | 支撑的机制 | 全文来源 |
|---|---|---|---|
| [01_Pau_2007_Bloch_Reduced_Basis_PRE.pdf](./01_Pau_2007_Bloch_Reduced_Basis_PRE.pdf) | Pau, *Physical Review E* 76, 046704 (2007), DOI [10.1103/PhysRevE.76.046704](https://doi.org/10.1103/PhysRevE.76.046704) | Bloch 能带的 reduced basis、残差指标和 greedy \(k\)-point 选择 | LBNL 作者/机构公开版 |
| [02_Horger_et_al_2017_Multiple_Eigen_RB_M2AN.pdf](./02_Horger_et_al_2017_Multiple_Eigen_RB_M2AN.pdf) | Horger, Wohlmuth & Dickopf, *ESAIM: M2AN* 51, 443–465 (2017), DOI [10.1051/m2an/2016025](https://doi.org/10.1051/m2an/2016025) | 多重本征值、整个 eigenspace、residual/gap 后验指标 | NUMDAM 期刊公开 PDF |
| [03_Haasdonk_et_al_2023_Certified_RB_ML_ROM_SIAMJSC_arXiv.pdf](./03_Haasdonk_et_al_2023_Certified_RB_ML_ROM_SIAMJSC_arXiv.pdf) | Haasdonk et al., *SIAM Journal on Scientific Computing* 45 (2023), DOI [10.1137/22M1493318](https://doi.org/10.1137/22M1493318) | ML–ROM–FOM 分层路由、后验误差与在线更新 | arXiv 作者版 2204.13454 |
| [04_Mera_Mitscherling_2022_Degenerate_Quantum_Geometry_PRB_arXiv.pdf](./04_Mera_Mitscherling_2022_Degenerate_Quantum_Geometry_PRB_arXiv.pdf) | Mera & Mitscherling, *Physical Review B* 106, 165133 (2022), DOI [10.1103/PhysRevB.106.165133](https://doi.org/10.1103/PhysRevB.106.165133) | 简并能带的 Grassmann quantum metric | arXiv 作者版 2205.07900 |
| [05_Mitscherling_et_al_2025_Projector_Calculus_PRB_arXiv.pdf](./05_Mitscherling_et_al_2025_Projector_Calculus_PRB_arXiv.pdf) | Mitscherling, Avdoshkin & Moore, *Physical Review B* 112, 085104 (2025), DOI [10.1103/qscv-qxqt](https://doi.org/10.1103/qscv-qxqt) | 多态 Bloch 量子几何的 gauge-invariant projector calculus | arXiv 作者版 2412.03637 |

## 已在其他本地目录封存的三篇核心论文

- [Grubišić et al. 2023](../07_Bloch_Grassmann_%E6%9C%AC%E5%BE%81%E5%AD%90%E7%A9%BA%E9%97%B4/13_Grubisic_et_al_2023_Parametric_Eigenspaces_Numerische_Mathematik.pdf)：内部本征值可交叉，但外部隔离的整个谱簇/谱投影仍是合理对象。
- [Wang & Xie 2024](../07_Bloch_Grassmann_%E6%9C%AC%E5%BE%81%E5%AD%90%E7%A9%BA%E9%97%B4/08_Wang_Xie_2024_MultiEigen_TNN_JCP_preprint.pdf)：无真值标签的 trace/Ky Fan 神经 trial subspace 已在 *JCP* 发表。
- [Chang et al. 2025](../07_Bloch_Grassmann_%E6%9C%AC%E5%BE%81%E5%AD%90%E7%A9%BA%E9%97%B4/10_Chang_et_al_2025_Shape_Space_Spectra_TOG_author.pdf)：一组联合训练的无标签参数神经场（每模态一个 MLP）跨形状族做变分 PDE eigenanalysis，并处理 multiplicity/mode crossover；这是当前最重要的期刊级平行写作模板。

## 只提供官方页面、未保存付费 PDF 的论文

- Riffaud, *Journal of Computational Physics* 523, 113677 (2025), DOI [10.1016/j.jcp.2024.113677](https://doi.org/10.1016/j.jcp.2024.113677)：用误差指标判断 ROM 何时不可信，并切换到 FOM。这是“risk-triggered PWE fallback”的最直接结构先例。

## 完整分析

历史完整分析位于：`04_SCI三区投稿准备/90_历史材料/20260729_深度评估/12_创新机制正式期刊证据链.md`。当前实验与投稿口径请读：`04_SCI三区投稿准备/00_当前投稿判断_20260824.md`。

## 完整性信息

本目录的 PDF 已通过文件魔数检查。SHA-256 由同目录 `SHA256SUMS.txt` 记录，便于后续引用和复现审计。

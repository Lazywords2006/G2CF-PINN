# SCI 三区补强文献（2026-07-12核验）

本目录只收录当前稿件为冲击SCI三区新增的合法开放全文。PDF均已用`file`和`pdfinfo`检查；发表状态不能仅由文件名推断。

| 文件 | 正式状态 | 用途 |
|---|---|---|
| `01_Hsu_et_al_2024_Equation_Driven_Periodic_Quantum_ML4PS.pdf` | NeurIPS 2024 ML4PS workshop，非主会/期刊 | 最直接的无标签二维周期Schrödinger/Bloch应用基线 |
| `03_Dolz_Ebert_2024_Higher_Multiplicity_Eigenspaces_SIAM_JNA.pdf` | SIAM J. Numer. Anal. 62(1), 2024；DOI `10.1137/22M1529324` | 重数大于1时应评价eigenspace而非单个eigenvector的理论依据 |
| `04_Ryu_et_al_2024_Operator_SVD_ICML.pdf` | ICML 2024正式会议 | 自监督多模态/嵌套低秩基线候选 |
| `05_Wang_et_al_2025_STNet_NeurIPS.pdf` | NeurIPS 2025正式会议 | sequential deflation与spectral filtering近期基线候选 |
| `06_Jiang_et_al_2026_FieldTNN_Maxwell_JCP_preprint.pdf` | JCP 549 (2026) 114605的作者预印本；DOI `10.1016/j.jcp.2025.114605` | 后续Maxwell第二PDE扩展对照，不属于当前最低矩阵 |
| `07_Fefferman_Weinstein_2012_Honeycomb_Dirac_JAMS.pdf` | JAMS 25(4), 2012；DOI `10.1090/S0894-0347-2012-00745-0` | honeycomb势与Dirac点的基础理论 |
| `08_Lee_Thorp_et_al_2019_Dirac_Points_ARMA_preprint.pdf` | ARMA 2019对应作者预印本；DOI `10.1007/s00205-018-1315-4` | 强/局域honeycomb势的Dirac点理论 |

## 已核实但未保存全文

- Mian, *Neural Bloch Eigensolver for Honeycomb Lattices*, ICLR 2026 AI&PDE workshop：OpenReview下载端当前返回403；本地已有更完整的arXiv硕士论文`../07_Bloch_Grassmann_本征子空间/05_Mian_2025_Physics_Informed_Periodic_Quantum_preprint.pdf`，且官方MIT代码已封存。
- Cheng et al., *A physics-informed neural network-based method for dispersion calculations*, *International Journal of Mechanical Sciences* 291–292 (2025) 110111，DOI `10.1016/j.ijmecsci.2025.110111`：未找到合法开放作者稿，只保留出版社入口，不能用摘要页冒充PDF。
- Hares et al., *A stable physics-guided neural networks approach for electromagnetic problems*, JCP 548 (2026) 114568，DOI `10.1016/j.jcp.2025.114568`：当前未核实合法开放全文。

## 官方代码索引

见 `03_当前主线_BlockKyFanPINN/02_当前代码仓库/baselines/external/README.md`：其中记录 Mian Bloch solver、Fanaskov subreg 和 NeuralSVD 的官方地址、许可证与固定提交。第三方仓库副本和许可证不明确的 Wang–Xie 作者压缩包不再内嵌或分发。正式论文必须区分“作者官方代码”和“本文公式级适配实现”。

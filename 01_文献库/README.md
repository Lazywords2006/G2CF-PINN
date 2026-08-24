# 当前文献库索引

本目录保留 170 份 PDF；文件数不等于互不重复的论文数。当前主线应优先阅读
`00_当前主线必读/07`–`10`。编号 `01`–`05` 主要是已停止的 TSONN / Allen–Cahn
选题背景。

## 当前阅读顺序

1. `07_Bloch_Grassmann_本征子空间/`：Wang–Xie、Dai、Chang、Kovacs、Rowan、
   Fanaskov、Grubišić；
2. `10_创新机制期刊证据链/`：Bloch reduced basis、多重 eigenspace、certified
   RB-ML-ROM 和 projector geometry；
3. `08_SCI三区补强/`：二维 periodic quantum、Dirac、higher-multiplicity eigenspace；
4. `09_2026_增量审计/`：2026 年最新邻近工作；
5. `06_FalsifyPDE_基准与可信评估/`：弱基线、PINN/FEM 与可信评估。

## 初稿已经使用的核心来源

| 工作 | 状态 | 对本文的作用 |
|---|---|---|
| Wang & Xie, JCP 2024 | 正式期刊 | trace/Ky Fan 多本征对直接基线 |
| Dai et al., CNSNS 2026 | 正式期刊 | 最近邻 neural-subspace + Galerkin |
| Rowan et al., IJNME 2025 | 正式期刊 | Rayleigh quotient + Gram–Schmidt |
| Chang et al., ACM TOG 2025 | 正式期刊 | 参数化 eigenspace、重数与 mode switching |
| Grubišić et al., Numer. Math. 2023 | 正式期刊 | 外部隔离谱簇在内部交叉处仍良定 |
| Pau, PRE 2007 | 正式期刊 | Bloch band reduced basis |
| Horger et al., M2AN 2017 | 正式期刊 | 参数化多重本征空间与误差估计 |
| Fefferman & Weinstein, JAMS 2012 | 正式期刊 | honeycomb Dirac crossing 数学依据 |
| Fanaskov et al., ICLR 2026 | 正式顶会 | 监督式 Grassmann subspace regression |
| Hsu et al., NeurIPS workshop 2024 | Workshop | 二维周期量子神经 PDE 直接近邻 |

## 下一步文献工作

文献检索不再围绕普通 PINN + 简单 PDE 扩张。当前只补：

1. Dai/Wang–Xie 的实现细节与公平复现设置；
2. external gap、Davis–Kahan/Ritz projector error 与 a posteriori bound；
3. neural + numerical hybrid eigensolver 的成本摊销；
4. 新势族/晶格的期刊级对照。

## 完整性边界

- `BibTeX引用库/Final_Complete_Library.bib` 元数据不完整，不能直接投稿；
- 文件名中的 `preprint` 常表示本地作者版，不代表论文没有正式发表；
- 每个正式引用必须核验作者、题名、期刊/会议、年份、卷期页码和 DOI；
- arXiv-only 和 workshop 工作必须明确标注，不得冒充期刊证据。

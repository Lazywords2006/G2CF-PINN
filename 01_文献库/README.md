# 当前文献库索引

本目录保留 170 份 PDF；文件数不等于互不重复的论文数。当前主线优先阅读
`00_当前主线必读/06`–`10`，编号 `01`–`05` 只是早期 TSONN / Allen–Cahn 选题背景。

## 当前阅读顺序

1. `10_创新机制期刊证据链/`：Bloch reduced basis、多重 eigenspace、可靠回退和
   projector quantum geometry；
2. `07_Bloch_Grassmann_本征子空间/`：Wang–Xie、Dai、Chang、Kovacs、Mian 与参数化
   eigenspace；
3. `09_2026_增量审计/`：Boundary-aware NMR、NEO、Subspace Regression 等最新近邻；
4. `08_SCI三区补强/`：二维 periodic quantum、Dirac、Maxwell 与高重数 eigenspace；
5. `06_FalsifyPDE_基准与可信评估/`：PINNacle、PDENNEval、PINN vs FEM 与弱基线风险。

## 六篇最关键的期刊/正式工作

| 工作 | 正式状态 | 本项目中的作用 |
|---|---|---|
| Grubišić et al., *Numerische Mathematik* 2023 | 正式期刊 | 内部本征值可交叉，外部隔离的谱簇仍良定 |
| Wang & Xie, *JCP* 2024 | 正式期刊 | 无标签 trace/Ky Fan 神经子空间基线 |
| Chang et al., *ACM TOG* 2025 | 正式期刊 / SIGGRAPH | 参数化神经本征分析、重数和 mode switching 平行模板 |
| Pau, *Physical Review E* 2007 | 正式期刊 | Bloch reduced basis 与 residual 选点 |
| Horger et al., *M2AN* 2017 | 正式期刊 | 多重本征空间和 residual/gap 后验评估 |
| Riffaud et al., *JCP* 2025 | 正式期刊 | 风险触发高保真回退的相邻机制 |

## 创新边界

不能把 Ky Fan、trace、Grassmann、Bloch ROM、fallback、projector 或量子度量单独称作
首创。P5 已经进一步排除“无条件低频 ROM”作为本文核心创新。

当前只需要围绕三个问题补充文献：

1. 无标签模型失效与不确定性指标；
2. selective prediction、risk–coverage 与风险校准；
3. certified ROM/FOM 或 neural/numerical fallback。

新文献必须核验 DOI、正式发表状态和合法全文来源。文件名中的 `preprint` 只表示本地保存
的是作者版，不代表论文没有正式发表；arXiv-only 工作不得冒充期刊证据。

## 完整性

- 当前主线必读包：56 份 PDF；
- 整个文献库：170 份 PDF；
- `BibTeX引用库/Final_Complete_Library.bib` 元数据不完整，投稿前必须重新核对作者、题名、
  DOI、卷期和页码；
- `10_创新机制期刊证据链/SHA256SUMS.txt` 保存五篇核心全文的哈希。

# FalsifyPDE：基准与可信评估文献

本目录保存 2026-07-11 重新下载并用 `pdfinfo`、首页题名和 SHA-256 核验过的原文。
这里的主线不是再做一个更大的 PDE 排行榜，而是研究代理指标、退化解与论文主张之间的
`proxy–utility gap`。

| 文件 | 正式发表状态 | 本项目中的作用 |
|---|---|---|
| `01_Hao_et_al_2024_PINNacle_NeurIPS.pdf` | NeurIPS 2024 Datasets and Benchmarks Track | 20 余类 PDE、约 10 种 PINN 的大规模基准；界定 FalsifyPDE 不能重复做普通排行榜 |
| `02_Zhang_et_al_2024_PDENNEval_IJCAI.pdf` | IJCAI 2024 | 12 种神经 PDE 方法、19 个 PDE 的系统评价；作为另一直接平行基准 |
| `03_McGreivy_Hakim_2024_Weak_Baselines_NMI_preprint.pdf` | *Nature Machine Intelligence* 6, 1256–1269 (2024)，本地为对应 arXiv 全文 | 说明弱数值基线和选择性报告会产生过度乐观结论 |
| `04_Grossmann_et_al_2024_PINN_vs_FEM_IMAJAM_preprint.pdf` | *IMA Journal of Applied Mathematics* 89, 143–174 (2024)，本地为对应 arXiv 全文 | 强调同精度、同成本下与传统数值方法公平比较 |
| `05_Gie_et_al_2026_SL_PINN_JCAM_preprint.pdf` | *Journal of Computational and Applied Mathematics* 2026，DOI `10.1016/j.cam.2025.116918`；本地为作者预印本 | singular-layer PINN 正控制来源，不作为本文创新 |

## 已核验信息

- PINNacle：54 页，SHA-256 `775dd915e9df5d60890c005dd33eb0d334a2a404591d86282463d9f166c0d82a`；
- PDENNEval：9 页，SHA-256 `176a444edc3688bc3cf70651077734f8cf26b3855c25693249922bad42e3b9ba`；
- Weak baselines：47 页，SHA-256 `65ce0348174cfc893dd4d870e2d798450de2ad157e1ce150ac4dfdabf6f2c20a`；
- PINN vs FEM：27 页，SHA-256 `cb123e7936e5ae55bb63702d1cff30d69e940972450822afbea659ef28234a9a`；
- SL-PINN：41 页，SHA-256 `b4c1dca06abf4bd26539dccd9a2d0f37dd6f04bc386a38ca14fda91de56b0870`。

“对应期刊预印本”表示论文的期刊身份由 DOI/出版社页面核实，本地 PDF 是合法公开的作者版本；
没有把预印本文件本身误写成出版社排版版。

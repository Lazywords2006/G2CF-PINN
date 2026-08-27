# 神经网络求解二维 Bloch–Schrödinger PDE

当前唯一主线：使用无标签参数神经网络和 symmetry-consistent Rayleigh–Ritz，求解二维参数化
Bloch–Schrödinger 本征偏微分方程的最低 rank-2 谱投影。

## 先看这里

- [最新简明 HTML](00_项目总览/09_全部工作简版.html)
- [当前研究总档案](00_项目总览/00_当前研究总档案.md)
- [英文论文 DOCX](03_当前主线_BlockKyFanPINN/02_当前代码仓库/paper/v3_submission/SR-SC-NARR_manuscript_en.docx)
- [英文论文 PDF](03_当前主线_BlockKyFanPINN/02_当前代码仓库/paper/v3_submission/SR-SC-NARR_manuscript_en.pdf)
- [中文论文 DOCX](03_当前主线_BlockKyFanPINN/02_当前代码仓库/paper/v3_submission/SR-SC-NARR_manuscript_zh-CN.docx)
- [中文论文 PDF](03_当前主线_BlockKyFanPINN/02_当前代码仓库/paper/v3_submission/SR-SC-NARR_manuscript_zh-CN.pdf)

## 当前状态

- `V3_FORMAL_PROMOTION_GO`；
- 160点、2势族、5 splits、3 seeds、11方法、5,280行；
- SR-SC-NARR overall projector error `0.030929`；
- 相对 Fourier-25 改善28.76%，95%区间 `[28.08%,29.44%]`；
- 66篇核验文献，其中50篇正式期刊；
- 中英文 Markdown、DOCX、PDF、11张可复现图、表格和完整 evidence 已生成；
- GPU 已关闭，不再需要租用算力。

核心结论必须写成“对谱复杂 Gaussian 势的条件性神经增强；对 harmonic 安全回退 Fourier”。
SCI 四区已具备投稿准备基础；SCI 三区可以尝试，但建议增加固定阈值的 roughness 外部验证。

## 保留目录

- `00_项目总览/`：读者入口；
- `01_文献库/`：当前主线论文 PDF；
- `03_当前主线_BlockKyFanPINN/`：权威 Git 代码仓库快捷入口。

旧 P2/Q3 路线只保留在代码仓库中作为历史审计，禁止恢复为当前投稿稿件。

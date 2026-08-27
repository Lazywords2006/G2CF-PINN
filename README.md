# 神经网络求解二维 Bloch–Schrödinger PDE

本工作区只保留当前论文主线：使用无标签神经网络求解二维参数化
Bloch–Schrödinger 本征偏微分方程的最低 rank-2 谱簇。

## 先看这里

- [最新简版 HTML](00_项目总览/09_全部工作简版.html)：用最直白的语言说明方法、结果、创新和投稿判断；
- [当前研究总档案](00_项目总览/00_当前研究总档案.md)：唯一状态文档；
- [英文投稿 DOCX](03_当前主线_BlockKyFanPINN/02_当前代码仓库/paper/submission_nmpde/final/NMPDE_manuscript.docx)；
- [英文投稿预览 PDF](03_当前主线_BlockKyFanPINN/02_当前代码仓库/paper/submission_nmpde/final/NMPDE_manuscript.pdf)；
- [中文论文初稿](03_当前主线_BlockKyFanPINN/02_当前代码仓库/paper/p2_final/MANUSCRIPT.zh-CN.md)。

## 最终状态

- 方法：anchored generalized-trace SiLU MLP + 完整二阶六角 Fourier shell + Rayleigh–Ritz；
- 方程：二维周期参数化 Bloch–Schrödinger 本征 PDE；
- `P2_FROZEN_FINAL_GO`：640点、两个势族、3 seeds、10方法、19,200行；
- `Q3_SUPPLEMENT_GO`：160点、3方法、3 seeds、1,440行；
- P2 overall projector error `0.04532`，long-anchor `0.14719`；
- 独立 supplement 中 P2 `0.04728`，Wang–Xie 适配 `0.13114`；
- 英文稿、中文稿、期刊投稿 DOCX/PDF、cover letter、图表、理论和引用审计均已完成；
- 当前不需要继续租 GPU，frozen final 与 supplement 均保持关闭。

科研内容已具备合理投稿基础，但是否被录用仍取决于期刊审稿。投稿前只需作者填写姓名、
单位、邮箱、ORCID、CRediT 和资助信息，并用学校账号复核当年分区及预警名单。

## 保留目录

- `00_项目总览/`：唯一读者入口；
- `01_文献库/`：只保留与 Bloch 谱簇、神经本征求解和可信评估直接相关的论文；
- `03_当前主线_BlockKyFanPINN/`：权威代码仓库快捷入口。

旧路线快照、旧 HTML、过期投稿清单和无关文献副本已删除。实验原始证据、冻结基准、
checkpoint、CSV/JSON、哈希清单和复现脚本保存在权威代码仓库中。

# 神经网络求解二维 Bloch–Schrödinger PDE

本工作区当前只保留一条论文主线：使用无标签神经网络求解二维参数化
Bloch–Schrödinger 本征偏微分方程的最低 rank-2 谱簇。

## 先看这里

- [HTML 总览：研究结果、论文初稿与补实验](00_项目总览/03_研究进展与实验结果.html)
- [简版 HTML：总共做了什么](00_项目总览/09_全部工作简版.html)
- [当前研究总档案](00_项目总览/00_当前研究总档案.md)
- [中文论文初稿](03_当前主线_BlockKyFanPINN/02_当前代码仓库/paper/p2_final/MANUSCRIPT.zh-CN.md)
- [英文论文初稿](03_当前主线_BlockKyFanPINN/02_当前代码仓库/paper/p2_final/MANUSCRIPT.en.md)
- [核心数据与证据](03_当前主线_BlockKyFanPINN/02_当前代码仓库/paper/p2_final/CORE_RESULTS.zh-CN.md)

## 当前结论

- P2 full-shell frozen final：`GO`；
- SCI-Q3 independent supplement：`GO`；
- 640 点、两个势族、3 seeds、10 方法、19,200 行已经完整回传并审计；
- overall projector error：P2 `0.04532`，long-anchor `0.14719`；
- SCI 四区：具备合理投稿基础；
- SCI 三区：最近邻适配、external-gap/Ritz 理论和成本摊销均已补，当前重点是方法图和期刊定稿；
- frozen final 永久关闭，当前不需要继续租 GPU。

## 目录

- `00_项目总览/`：唯一面向读者的状态和 HTML；
- `01_文献库/`：本地 PDF、主线必读包和 BibTeX；
- `03_当前主线_BlockKyFanPINN/`：权威代码仓库快捷入口；
- `04_SCI三区投稿准备/`：投稿补强入口；
- `05_历史路线摘要/`：STOP 路线和负结果；
- `06_投稿筛查/`：风险期刊初筛提示。

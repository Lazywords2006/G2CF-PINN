# AI 研究工作区规则

唯一研究状态来源：`00_项目总览/00_当前研究总档案.md`。
权威代码：`03_当前主线_BlockKyFanPINN/02_当前代码仓库/`。
权威数值：代码仓库 `paper/p2_final/CORE_RESULTS.zh-CN.md`。

必须遵守：

- 当前最终方法为 P2 full-shell 基底不变神经增强 Rayleigh–Ritz；
- frozen final 状态为 `P2_FROZEN_FINAL_GO`，已经运行一次并永久关闭；
- 不重跑 final、不用 final 调参、不筛更好 checkpoint、不修改 final suite/reference；
- P5 low-ROM、P1 risk routing、P2 outer-shell 的 STOP 证据必须保留；
- MPS/CPU smoke 不是 CUDA 正式论文结果；
- `wang_xie_trace`、`dai_galerkin` 当前只是公式级适配，不得写成官方复现；
- 新 SCI 三区实验必须使用独立 supplement suite；
- 待运行、理论预期和配置文件不能写成实际结果；
- 不把 Rayleigh–Ritz、Galerkin、Fourier、Ky Fan 或 projector 称为本文发明。

验证命令：

```bash
cd 03_当前主线_BlockKyFanPINN/02_当前代码仓库
uv run --python 3.12 --with-requirements requirements.txt python -m pytest -q
```

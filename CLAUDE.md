# 当前研究工作区规则

更新日期：2026-08-24。

当前唯一论文主线是二维 Bloch–Schrödinger rank-2 神经谱簇求解。先读根目录
`README.md` 与 `00_项目总览/01_当前状态与下一步_20260824.md`，不要让历史 P3、P4
或 2026-07-29 材料覆盖 P5 独立审计结论。

## 权威来源顺序

1. `03_当前主线_BlockKyFanPINN/02_当前代码仓库/`（指向独立 `PINN-PDE` Git 仓库）；
2. 其中 `docs/CURRENT-STATUS.zh-CN.md`；
3. 其中 `docs/P5-INDEPENDENT-AUDIT.zh-CN.md`；
4. `00_项目总览/03_研究进展与实验结果.html`；
5. `04_SCI三区投稿准备/` 根层的当前文件。

## 当前事实

- P5 权威证据已回传并独立审计，36/36 run 完成，结论为 `P5_PROMOTION_STOP`；
- 低频 ROM 不能作为当前论文主创新；long-anchor 只是强计算预算基线；
- frozen final 未打开，STOP 状态下禁止运行 `evaluate_v2_final.py`；
- 2026-08-02 Apple M4 / MPS 12-run smoke 为 `SMOKE_PASS`，但 MPS 缺 float64 与原生复数
  QR，不能替代 CUDA/ROCm 正式实验；
- 初步风险探针中 residual 与谱隙阈值无效，Gram condition 只有弱信号；
- 下一步是独立开发集上的无标签风险可检测性与条件校正小测，不是重跑 P5。

## 默认不要读取或运行

- `05_历史路线摘要/BlockKyFan_旧阶段_20260729/` 中的旧工程；
- `04_SCI三区投稿准备/90_历史材料/` 中的旧提纲与初稿，除非追溯历史；
- `01_文献库/` 中未被点名的 PDF；
- frozen final、旧 V1 正式入口或完整矩阵。

## 当前验证入口

```bash
cd 03_当前主线_BlockKyFanPINN/02_当前代码仓库
uv run --python 3.12 --with-requirements requirements.txt python -m pytest -q
uv run --python 3.12 --with-requirements requirements.txt \
  python scripts/run_p5_executor.py --device mps --skip-cache --smoke-only
```

第二条只适用于 M4 工程烟测，会生成本地证据；它不是论文正式实验。正式结果仍以
CUDA/ROCm、冻结协议、原始证据和独立审计为准。

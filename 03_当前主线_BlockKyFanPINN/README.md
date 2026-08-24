# Block KyFan-PINN 当前主线

研究阶段、下一步和投稿缺口统一见：
[当前研究总档案](../00_项目总览/00_当前研究总档案.md)。

## 权威代码入口

- 本地：[02_当前代码仓库](02_当前代码仓库)；
- GitHub：[Lazywords2006/PINN-PDE](https://github.com/Lazywords2006/PINN-PDE)；
- 当前状态：[CURRENT-STATUS.zh-CN.md](02_当前代码仓库/docs/CURRENT-STATUS.zh-CN.md)；
- P5 独立审计：[P5-INDEPENDENT-AUDIT.zh-CN.md](02_当前代码仓库/docs/P5-INDEPENDENT-AUDIT.zh-CN.md)。

`02_当前代码仓库` 是指向独立 Git 仓库的相对快捷链接。它是唯一允许继续修改、测试和
运行的代码版本。2026-07-29 的旧工程副本已移至历史目录，只能通过 Git 或原始数据
追溯，不能继续实验。

## 研究对象

项目使用无标签神经网络求解二维参数化 Bloch–Schrödinger 本征 PDE，预测最低两个
本征态共同张成的 rank-2 谱簇。内部能带可以在 Dirac 点相交，评价对象是 projector 与
principal angle，而不是两列输出的固定顺序。

## 当前状态（2026-08-24）

- P4/P5 权威证据均已独立审计；
- P5 36/36 validation run 完成，结论 `P5_PROMOTION_STOP`；
- 低频 ROM 不能作为论文主创新；
- Apple M4 / MPS 12-run 工程烟测通过，但不能替代 CUDA/ROCm 正式结果；
- P0 独立 risk-development AUROC 0.869，状态 `RISK_DEVELOPMENT_GO`；
- frozen final 未打开；
- 下一步是 P1 条件校正器设计与公平小测。

## 安全验证

```bash
cd 02_当前代码仓库
uv run --python 3.12 --with-requirements requirements.txt python -m pytest -q
```

M4 工程烟测：

```bash
uv run --python 3.12 --with-requirements requirements.txt \
  python scripts/run_p5_executor.py --device mps --skip-cache --smoke-only
```

该 smoke 只检查链路、有限性、正交与 Gram 条件数。MPS 不支持项目正式复核所需的
float64 和原生复数 QR，因此不能把 smoke 时间或精度写入论文 CUDA 主结果。

## 禁止事项

- 不运行 `evaluate_v2_final.py`；
- 不修改 P5 门槛后重跑；
- 不从旧工程快照复制旧 P3/V1 入口回来；
- 不把 long-anchor 或更多训练步数称作创新；
- 不在 P1 条件校正小测 GO 前启动完整 10-seed 矩阵。

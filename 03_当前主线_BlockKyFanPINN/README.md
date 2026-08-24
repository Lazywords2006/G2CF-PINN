# 当前主线：P2 神经增强 Bloch 谱簇求解器

权威代码：[02_当前代码仓库](02_当前代码仓库)
GitHub：[Lazywords2006/PINN-PDE](https://github.com/Lazywords2006/PINN-PDE)

## 当前状态

- 最终方法：P2 full-shell basis-invariant neural-augmented Rayleigh–Ritz；
- frozen final：`P2_FROZEN_FINAL_GO`；
- independent supplement：`Q3_SUPPLEMENT_GO`；
- 640 点 × 10 方法 × 3 seeds = 19,200 行；
- 中英文论文初稿 v0.1 已生成；
- 当前任务：理论、FLOPs/成本摊销、方法图、引用和期刊定稿；
- frozen final 永久关闭。

## 阅读顺序

1. [当前研究总档案](../00_项目总览/00_当前研究总档案.md)
2. [中文论文初稿](02_当前代码仓库/paper/p2_final/MANUSCRIPT.zh-CN.md)
3. [英文论文初稿](02_当前代码仓库/paper/p2_final/MANUSCRIPT.en.md)
4. [核心数据](02_当前代码仓库/paper/p2_final/CORE_RESULTS.zh-CN.md)
5. [Q3 supplement 报告](02_当前代码仓库/paper/p2_final/Q3_SUPPLEMENT_REPORT.zh-CN.md)
6. [缺口与补实验](02_当前代码仓库/docs/KNOWN_GAPS.zh-CN.md)
7. [运行手册](02_当前代码仓库/docs/RUNBOOK.md)

## 安全验证

```bash
cd 02_当前代码仓库
uv run --python 3.12 --with-requirements requirements.txt python -m pytest -q
```

不要运行 `scripts/evaluate_p2_final.py`，也不要修改方法后重跑已关闭的 Q3 supplement。

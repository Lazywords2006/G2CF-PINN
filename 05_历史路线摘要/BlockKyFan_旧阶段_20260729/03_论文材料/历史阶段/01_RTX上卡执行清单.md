# RTX 4090 CUDA 执行记录

## 完成状态

2026-07-12 已在 AutoDL RTX 4090 24GB 完成：环境校准、17/17测试、CUDA smoke、三种子 pilot、正式基线、全部核心消融、anchor/配点/宽度敏感性、最终优化配置、全新种子44/55确认、效率审计、参考解收敛和绘图。

最终推荐配置：`configs/formal_optimized_cuda.json`，correct anchor scale `0.40`，Ky Fan trace-only，5000步，1024配点。合并5种子 projector sine error 为 `0.223719±0.001172`，比 ordered residual PINN 基线降低 `69.14%`。

## 关键工程结论

- residual 第二阶段对精度无可测收益，且提高训练时间和显存，因此最终方法删除该阶段；
- no-anchor 均值接近旧配置，但跨种子方差和外推误差明显变差，anchor 的主要作用是稳定性和 OOD；
- wrong/random anchor 显著失败，anchor 不是任意初始化都有效；
- 512→2048配点、宽度64→128几乎不改善，收益不是来自盲目扩大模型；
- 最终模型仅29,188参数，峰值显存约486MB。

## 结果与复现

- 详细报告：`02_RTX4090_CUDA旧V1实验报告.md`
- 原始数据：`../../02_实验工程/results/rtx4090_autodl_20260712/`
- 最终归档：`block_kyfan_results_final_with_figures.tgz`
- SHA-256：`22b82e13410daf5e6df2822afa50aaa719fff0c69635a98c0c818fea21905644`

## 下一轮上卡任务

当前核心实验已结束。下一轮仅在投稿前补：近期官方基线、第二势族/第二二维简并 PDE、谱隙扫描和批量查询摊销曲线。RTX 4090 足够，预计额外6–12 GPU小时。

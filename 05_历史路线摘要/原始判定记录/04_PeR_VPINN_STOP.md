# PeR-VPINN seed-0 gatecheck 终止记录

> 结论：**STOP**。本结论来自预正式的 seed-0 满 1500 步 gatecheck，不冒充 3-seed 正式结果。因为主方法已经输给最强机制基线且绝对误差失去求解器意义，不再浪费算力补跑其余 9 个运行。

## 1. 执行链

1. float64 参考验证：PASS；
2. CPU 单元/集成测试：20/20 PASS；
3. 四方法 MPS smoke：PASS；
4. 四方法 seed-0、300 步 precheck：全部无 NaN，但精度不足；
5. `rvpinn_h1 / supg_vpinn / per_rvpinn` seed-0、1500 步 gatecheck：完成；
6. 由于主方法未超过最强基线，阻断正式 12-run 矩阵。

## 2. 参考与数值完整性

`results/pilot_mps_v1/reference_validation.json` 记录：

- 制造解强残差最大值：`3.1086244689504383e-15`；
- 16×16 cell、8×8 Gauss 下弱残差最大值：`1.627780745819805e-10`；
- H1 Gram 最小特征值：`0.48764172335600914`；
- Pe Gram 最小特征值：`0.012517913832199551`；
- 积分域测度：`1.0000000000000004`；
- 边界误差：`0.0`。

因此本轮失败不能归因于制造解、弱式符号或 Gram 非正定。

## 3. 1500 步 seed-0 真实结果

| 方法 | global rel. L2 | layer rel. L2 | streamline-balanced | raw relative residual | estimator corr. | effectivity | time (s) | peak MPS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| RVPINN-H1 | 0.507511 | 0.899146 | 0.791047 | 1.418738 | 0.967521 | 0.001010 | 30.76 | 44,990,464 B |
| SUPG-VPINN proxy | **0.467484** | **0.871683** | **0.771906** | 1.423274 | 0.964165 | 0.001009 | 102.86 | 138,461,184 B |
| PeR-VPINN | 0.506593 | 0.898552 | 0.790614 | 1.418681 | **0.970236** | 0.006291 | 34.14 | 46,186,496 B |

原始产物：`02_实验工程/results/gatecheck_mps_v1/`。

## 4. 为什么必须停止

- PeR 相对 H1-RVPINN 只有约 `0.055%` 的 balanced-error 改善，远低于冻结的 25%；
- PeR 相对当前最强 SUPG 代理反而恶化约 `2.42%`；
- global/layer 误差分别约 `0.51/0.90`，距 `1e-2/3e-2` 绝对门槛超过一个数量级；
- 未缩放的相对 PDE 残差约 `1.42`，不能把当前输出解释为有用的 PDE 解；
- estimator 与真误差在 10 个 checkpoint 上相关系数很高，但 effectivity 远离 1，尚不是定量证书；
- 所有方法参数相同（16,897），因此失败不是由于 PeR 模型更小。

## 5. 可保留的学术信息

1. “loss--error 相关性”与“可用 effectivity”必须分开报告；
2. 局部 test norm 替换不会自动解决 trial-space 对薄层的表示偏置；
3. 该路线若要复活，必须是新的全局/最优 test-space 理论与试验空间重构，不能再只调 `tau`、步数或宽度。

本路线作为完整负结果保留，不再是当前主线。

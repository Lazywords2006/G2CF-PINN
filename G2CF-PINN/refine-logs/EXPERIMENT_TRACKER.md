# 实验跟踪器

| 运行ID | 里程碑 | 目的 | 系统/变体 | 分割 | 指标 | 优先级 | 状态 | 备注 |
|--------|--------|------|-----------|------|------|--------|------|------|
| R001 | M0 | 健全性检查-单点过拟合 | G2CF-PINN | 1D Burgers, 1点 | L2误差<1e-4 | MUST | TODO | 验证梯度正确性 |
| R002 | M0 | 健全性检查-小数据集 | G2CF-PINN | 1D Burgers, 100点 | L2误差<0.01 | MUST | TODO | 验证训练流程 |
| R003 | M0 | 健全性检查-边界条件 | G2CF-PINN | 1D Burgers, BC | BC误差<1e-4 | MUST | TODO | 验证边界处理 |
| R004 | M1 | 基线复现-标准PINN | 标准PINN | 1D Burgers | 与论文一致 | MUST | TODO | 参考实现 |
| R005 | M1 | 基线复现-SA-PINNs | SA-PINNs | 1D Burgers | 与论文一致 | MUST | TODO | 自适应权重 |
| R006 | M1 | 基线复现-RAD/RAR-D | RAD/RAR-D | 1D Burgers | 与论文一致 | MUST | TODO | 残差自适应采样 |
| R007 | M2 | 主方法-解析梯度效率 | G2CF-PINN | 1D Burgers | 时间加速>10x | MUST | TODO | Table 1 |
| R008 | M2 | 主方法-因果训练效果 | G2CF-PINN | 1D Burgers | 因果一致性>95% | MUST | TODO | Table 2 |
| R009 | M2 | 主方法-梯度引导采样 | G2CF-PINN | 1D Burgers | 采样效率>50% | MUST | TODO | Table 3 |
| R010 | M3 | 消融-无因果训练 | G2CF-PINN w/o 因果 | 1D Burgers | 性能下降显著 | MUST | TODO | Table 5 |
| R011 | M3 | 消融-无梯度引导 | G2CF-PINN w/o 梯度 | 1D Burgers | 性能下降显著 | MUST | TODO | Table 5 |
| R012 | M3 | 消融-无解析梯度 | G2CF-PINN w/o 解析 | 1D Burgers | 性能下降显著 | MUST | TODO | Table 5 |
| R013 | M3 | 决策-因果阈值固定vs自适应 | G2CF-PINN | 1D Burgers | 自适应更优 | MUST | TODO | 阈值策略 |
| R014 | M3 | 决策-温度参数α选择 | G2CF-PINN | 1D Burgers | 最优α值 | MUST | TODO | 采样参数 |
| R015 | M3 | 决策-傅里叶特征维度m | G2CF-PINN | 1D Burgers | 最优m值 | MUST | TODO | 网络参数 |
| R016 | M4 | SOTA对比-Burgers | G2CF-PINN vs 基线 | 1D Burgers | 最佳误差 | MUST | TODO | Table 4 |
| R017 | M4 | SOTA对比-Allen-Cahn | G2CF-PINN vs 基线 | 1D Allen-Cahn | 最佳误差 | MUST | TODO | Table 4 |
| R018 | M4 | SOTA对比-Euler | G2CF-PINN vs 基线 | 1D Euler | 最佳误差 | MUST | TODO | Table 4 |
| R019 | M4 | 敏感性-B矩阵随机性 | G2CF-PINN | 1D Burgers | 波动<10% | NICE | TODO | 附录Table A1 |
| R020 | M4 | 敏感性-特征维度m | G2CF-PINN | 1D Burgers | 稳定性 | NICE | TODO | 附录Table A1 |
| R021 | M4 | 敏感性-频率范围 | G2CF-PINN | 1D Burgers | 稳定性 | NICE | TODO | 附录Table A1 |
| R022 | M4 | 泛化性-2D热方程 | G2CF-PINN vs 基线 | 2D热方程 | 优于标准PINN | NICE | TODO | 附录Table A2 |
| R023 | M4 | 泛化性-2D Poisson | G2CF-PINN vs 基线 | 2D Poisson | 优于标准PINN | NICE | TODO | 附录Table A2 |
| R024 | M4 | 效率-不同批量大小 | G2CF-PINN | 1D Burgers | 线性加速 | NICE | TODO | 效率分析 |
| R025 | M4 | 效率-不同采样点数 | G2CF-PINN | 1D Burgers | 线性加速 | NICE | TODO | 效率分析 |
| R026 | M5 | 润色-生成图表 | G2CF-PINN | 1D Burgers | 图表质量 | NICE | TODO | Figure 3-7 |
| R027 | M5 | 润色-损失曲线可视化 | G2CF-PINN | 1D Burgers | 清晰度 | NICE | TODO | 训练过程 |
| R028 | M5 | 润色-采样分布可视化 | G2CF-PINN | 1D Burgers | 清晰度 | NICE | TODO | 采样策略 |
| R029 | M5 | 润色-激波位置对比图 | G2CF-PINN | 1D Burgers | 清晰度 | NICE | TODO | 预测质量 |
| R030 | M5 | 润色-计算时间对比图 | G2CF-PINN | 1D Burgers | 清晰度 | NICE | TODO | 效率优势 |

---

## 运行说明

- **MUST**: 必须运行，影响论文核心声明
- **NICE**: 可选运行，提升论文质量但非必须
- **TODO**: 待运行
- **RUNNING**: 运行中
- **DONE**: 已完成
- **FAIL**: 失败，需要调试

---

## 决策门

| 里程碑 | 决策条件 | 通过 | 失败 |
|--------|----------|------|------|
| M0 | 单点误差<1e-4 | 继续M1 | 调试梯度实现 |
| M1 | 基线误差与论文一致 | 继续M2 | 检查数据/代码 |
| M2 | 优于基线 | 继续M3 | 分析原因，调整超参 |
| M3 | 组件贡献明确 | 继续M4 | 简化框架或重新设计 |
| M4 | 在2+方程上SOTA | 论文可写 | 调整声明或增加实验 |
| M5 | 论文完整 | 提交 | 最后润色 |

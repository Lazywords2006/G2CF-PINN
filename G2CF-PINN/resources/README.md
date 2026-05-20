# G2CF-PINN 实验资源

**生成日期**: 2026-05-20

---

## 📁 目录结构

```
resources/
├── docs/
│   └── RESOURCE_REQUIREMENTS.md  # 算力需求分析
├── configs/
│   ├── default.yaml              # 默认配置
│   ├── module1_gradient_efficiency.yaml
│   ├── module2_causal_training.yaml
│   ├── module3_gradient_sampling.yaml
│   ├── module4_sota_comparison.yaml
│   ├── module5_ablation.yaml
│   ├── module6_frequency_sensitivity.yaml
│   └── module7_2d_generalization.yaml
├── scripts/
│   ├── train.py                  # 统一训练脚本
│   ├── run_experiments.sh        # 批量实验脚本
│   ├── submit_parallel.sh        # 多GPU并行提交
│   ├── submit_slurm.sh           # SLURM集群提交
│   ├── submit_autodl.sh          # AutoDL云GPU提交
│   └── collect_results.py        # 结果收集分析
├── requirements.txt              # Python依赖
└── README.md                     # 本文件
```

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 单次训练

```bash
# 使用默认配置训练
python scripts/train.py --config configs/default.yaml --seed 42

# 使用模块1配置训练
python scripts/train.py --config configs/module1_gradient_efficiency.yaml --seed 42 --method g2cf_pinn
```

### 3. 批量实验

```bash
# 运行单个模块
bash scripts/run_experiments.sh 1 0  # 模块1，GPU 0

# 运行主实验（模块1-5）
bash scripts/run_experiments.sh main 0

# 运行所有实验
bash scripts/run_experiments.sh all 0
```

### 4. 多GPU并行

```bash
# 4卡并行运行主实验
bash scripts/submit_parallel.sh main 4
```

### 5. 结果分析

```bash
python scripts/collect_results.py --input results/ --output report/
```

---

## ☁️ 云GPU部署

### AutoDL (推荐)

```bash
# 1. 上传代码到AutoDL
# 2. 登录实例
# 3. 运行实验
bash scripts/submit_autodl.sh main
```

### SLURM集群

```bash
# 提交任务
sbatch scripts/submit_slurm.sh main

# 查看任务状态
squeue -u $USER

# 查看日志
tail -f logs/slurm_*.out
```

### Vast.ai / RunPod

```bash
# 1. 租用GPU实例
# 2. SSH登录
# 3. 运行实验
bash scripts/run_experiments.sh main 0
```

---

## 📊 实验模块说明

| 模块 | 内容 | 实验数 | 预计时间 |
|------|------|--------|---------|
| 1 | 解析梯度效率 | 54组 | 9小时 |
| 2 | 因果训练效果 | 36组 | 12小时 |
| 3 | 梯度引导采样 | 108组 | 27小时 |
| 4 | SOTA对比 | 36组 | 27小时 |
| 5 | 消融研究 | 12组 | 6小时 |
| 6 | 频率敏感性(附录) | 45组 | 15小时 |
| 7 | 2D泛化性(附录) | 18组 | 18小时 |

**主文实验**: 模块1-5，共246组，约81小时
**含附录**: 模块1-7，共309组，约114小时

---

## 💰 成本估算

| 平台 | 主文实验 | 含附录 |
|------|---------|--------|
| RTX 4070 Ti | ~$12 | ~$17 |
| RTX 3090 | ~$16 | ~$23 |
| RTX 4090 | ~$28 | ~$40 |
| A100 40GB | ~$89 | ~$125 |

---

## 🔧 配置说明

### 继承机制

所有模块配置继承自 `default.yaml`，只需覆盖差异参数：

```yaml
inherit: default.yaml

experiment:
  name: my_experiment

# 只覆盖需要修改的参数
training:
  batch_size: 5000
```

### 参数覆盖

命令行参数优先级最高：

```bash
python train.py --config configs/default.yaml --seed 123
```

### 网格搜索

配置文件中的 `grid` 字段定义搜索空间：

```yaml
grid:
  fourier_features.m: [128, 256, 512]
  seed: [42, 43, 44]
```

---

## 📈 结果格式

每个实验输出JSON文件：

```json
{
  "seed": 42,
  "method": "g2cf_pinn",
  "training_time": 123.45,
  "relative_l2_error": 0.0123,
  "causal_consistency": 0.96,
  "shock_position_error": 0.005
}
```

---

## ❓ 常见问题

### Q: 内存不足(OOM)怎么办？

```bash
# 减小批量大小
python train.py --config configs/default.yaml
# 修改配置: training.batch_size: 500
```

### Q: 如何只运行部分实验？

```bash
# 只运行模块1-3
bash scripts/run_experiments.sh 1 0
bash scripts/run_experiments.sh 2 0
bash scripts/run_experiments.sh 3 0
```

### Q: 如何恢复中断的实验？

```bash
# 从检查点恢复
python train.py --config configs/default.yaml --resume results/checkpoint_epoch1000.pt
```

---

## 📞 技术支持

- 查看 `docs/RESOURCE_REQUIREMENTS.md` 了解详细算力需求
- 查看各配置文件了解参数含义
- 查看脚本注释了解使用方法

---

**祝实验顺利！** 🎉

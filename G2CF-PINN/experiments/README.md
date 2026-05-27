# G2CF-PINN 实验代码

**项目**: 梯度引导因果傅里叶物理信息神经网络  
**状态**: 代码准备完成，可接入服务器训练

---

## 📁 文件结构

```
experiments/
├── train.py                    # 主训练脚本
├── run_training.sh             # 训练启动脚本
├── requirements.txt            # Python依赖
├── configs/
│   └── burgers.yaml            # Burgers方程实验配置
├── models/
│   ├── __init__.py
│   ├── g2cf_pinn.py            # G2CF-PINN模型实现
│   └── modules/
│       ├── __init__.py
│       ├── fourier_features.py # 傅里叶特征模块
│       ├── causal_training.py  # 因果训练模块
│       └── adaptive_sampling.py # 自适应采样模块
└── evaluation/
    ├── __init__.py
    └── metrics.py              # 评估指标
```

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd G2CF-PINN/experiments

# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 本地测试（可选）

```bash
# 测试代码是否正常工作
python3 -c "
import sys
sys.path.append('..')
from models.g2cf_pinn import G2CF_PINN
import yaml

with open('configs/burgers.yaml', 'r') as f:
    config = yaml.safe_load(f)

model = G2CF_PINN({
    'input_dim': 2,
    'num_features': 256,
    'nu': 0.0318
})
print(f'✅ 模型创建成功，参数数量: {sum(p.numel() for p in model.parameters()):,}')
"
```

### 3. 开始训练

#### 方法一：使用启动脚本（推荐）

```bash
# 给脚本添加执行权限
chmod +x run_training.sh

# 运行训练（默认配置）
./run_training.sh

# 指定配置文件
./run_training.sh --config configs/burgers.yaml

# 指定设备和随机种子
./run_training.sh --device cuda --seed 42
```

#### 方法二：直接运行Python脚本

```bash
python3 train.py \
    --config configs/burgers.yaml \
    --output_dir results \
    --device auto \
    --seed 42
```

---

## ⚙️ 配置说明

### 实验配置文件 (configs/burgers.yaml)

```yaml
experiment:
  name: "E1_Burgers_Benchmark"
  description: "1D Burgers equation benchmark test"
  seed: 42

equation:
  type: "burgers_1d"
  nu: 0.0318  # 粘性系数
  domain:
    x: [-1, 1]
    t: [0, 1]
  ic: "u(x,0) = -sin(πx)"
  bc: "u(-1,t) = u(1,t) = 0"

training:
  points:
    N_f: 10000    # 域内配点
    N_b: 100      # 边界条件点
    N_0: 100      # 初始条件点
  optimizer: "adam"
  lr: 0.001
  epochs: 10000

model:
  name: "G2CF_PINN"
  input_dim: 2
  num_features: 256
  sigma: 1.0
  causal_threshold: 0.05
  sampling_temperature: 2.0
```

---

## 🖥️ 服务器部署

### 1. 上传代码到服务器

```bash
# 使用scp上传
scp -r experiments/ user@server:/path/to/project/

# 或使用rsync（推荐）
rsync -avz experiments/ user@server:/path/to/project/experiments/
```

### 2. 在服务器上安装依赖

```bash
# SSH登录服务器
ssh user@server

# 进入项目目录
cd /path/to/project/experiments

# 安装依赖
pip install -r requirements.txt

# 如果需要GPU支持，安装CUDA版本的PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 3. 使用Screen/Tmux后台运行

```bash
# 创建新的screen会话
screen -S g2cf_training

# 或使用tmux
tmux new -s g2cf_training

# 运行训练
./run_training.sh --device cuda

# 断开会话（训练继续运行）
# Screen: Ctrl+A, D
# tmux: Ctrl+B, D

# 重新连接会话
screen -r g2cf_training
# 或
tmux attach -t g2cf_training
```

### 4. 使用SLURM作业调度（HPC集群）

创建SLURM脚本 `train.slurm`:

```bash
#!/bin/bash
#SBATCH --job-name=g2cf_pinn
#SBATCH --output=logs/%j.out
#SBATCH --error=logs/%j.err
#SBATCH --gres=gpu:1
#SBATCH --mem=16G
#SBATCH --time=24:00:00

# 加载模块
module load python/3.9
module load cuda/11.8

# 激活虚拟环境
source venv/bin/activate

# 运行训练
python3 train.py \
    --config configs/burgers.yaml \
    --output_dir results \
    --device cuda \
    --seed $SLURM_ARRAY_TASK_ID
```

提交作业:

```bash
# 提交单个作业
sbatch train.slurm

# 提交数组作业（多个随机种子）
sbatch --array=42,123,456,789,1024 train.slurm

# 查看作业状态
squeue -u $USER

# 查看输出
tail -f logs/*.out
```

---

## 📊 输出结果

训练完成后，结果保存在 `results/` 目录：

```
results/
└── E1_Burgers_Benchmark_20260527_123456/
    ├── config.yaml           # 实验配置
    ├── model.pth             # 训练好的模型
    ├── loss_history.npy      # 损失历史
    ├── predictions.npz       # 预测结果
    └── metrics.yaml          # 评估指标
```

### 评估指标

- **L2误差**: 相对L2范数误差
- **L∞误差**: 最大绝对误差
- **最终损失**: 训练最终损失值
- **训练轮数**: 总训练epoch数

---

## 🔧 自定义实验

### 添加新的PDE问题

1. 在 `configs/` 目录创建新的配置文件
2. 在 `train.py` 中添加对应的数据生成函数
3. 在 `models/g2cf_pinn.py` 中添加对应的损失计算

### 修改模型参数

编辑配置文件中的 `model` 部分：

```yaml
model:
  num_features: 512          # 增加特征数量
  sigma: 2.0                 # 调整傅里叶特征尺度
  causal_threshold: 0.01     # 调整因果阈值
  sampling_temperature: 3.0  # 调整采样温度
```

### 调整训练参数

```yaml
training:
  points:
    N_f: 20000              # 增加配点数量
    N_b: 200                # 增加边界点数量
  lr: 0.0005                # 降低学习率
  epochs: 20000             # 增加训练轮数
```

---

## 📝 注意事项

1. **GPU内存**: 大规模训练需要足够的GPU内存，建议至少8GB
2. **随机种子**: 固定随机种子确保结果可复现
3. **数据生成**: 训练数据在运行时动态生成，无需预先准备
4. **检查点**: 建议定期保存检查点，防止训练中断丢失进度
5. **日志**: 使用 `tee` 命令同时输出到屏幕和文件

---

## 🐛 常见问题

### Q: 训练速度很慢怎么办？

A: 
- 确保使用GPU训练（`--device cuda`）
- 减少配点数量（`N_f`）
- 使用更小的模型（减少 `num_features`）

### Q: 损失不收敛怎么办？

A:
- 尝试调整学习率（`lr`）
- 增加训练轮数（`epochs`）
- 调整损失权重（`w_pde`, `w_ic`, `w_bc`）

### Q: 如何恢复中断的训练？

A: 目前代码不支持断点续训，建议：
- 定期保存检查点
- 使用SLURM的数组作业功能
- 实现自定义的检查点保存逻辑

---

## 📚 参考文献

- Raissi, M., Perdikaris, P., & Karniadakis, G. E. (2019). Physics-informed neural networks. Journal of Computational Physics.
- Wang, S., Teng, Y., & Perdikaris, P. (2021). Understanding and mitigating gradient flow pathologies in physics-informed neural networks.

---

**准备完成！现在可以接入服务器开始训练了。**
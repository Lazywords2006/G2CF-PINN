#!/bin/bash
#SBATCH --job-name=g2cf_pinn
#SBATCH --output=logs/%j.out
#SBATCH --error=logs/%j.err
#SBATCH --gres=gpu:1
#SBATCH --mem=16G
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=4

# 加载模块（根据服务器环境调整）
# module load python/3.9
# module load cuda/11.8

# 打印作业信息
echo "=========================================="
echo "G2CF-PINN 训练作业"
echo "作业ID: $SLURM_JOB_ID"
echo "节点: $SLURM_NODELIST"
echo "GPU: $CUDA_VISIBLE_DEVICES"
echo "开始时间: $(date)"
echo "=========================================="

# 激活虚拟环境（如果使用）
# source venv/bin/activate

# 设置环境变量
export PYTHONUNBUFFERED=1

# 创建日志目录
mkdir -p logs

# 运行训练
python3 train.py \
    --config configs/burgers.yaml \
    --output_dir results \
    --device cuda \
    --seed 42

# 检查训练结果
if [ $? -eq 0 ]; then
    echo "=========================================="
    echo "训练完成！"
    echo "结束时间: $(date)"
    echo "=========================================="
else
    echo "=========================================="
    echo "训练失败！"
    echo "结束时间: $(date)"
    echo "=========================================="
    exit 1
fi
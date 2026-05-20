#!/bin/bash
# SLURM集群提交脚本
# 用法: sbatch submit_slurm.sh [module]
# 示例: sbatch submit_slurm.sh main

#SBATCH --job-name=g2cf-pinn
#SBATCH --partition=gpu
#SBATCH --gres=gpu:4
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=48:00:00
#SBATCH --output=logs/slurm_%j.out
#SBATCH --error=logs/slurm_%j.err

# 加载模块（根据集群环境调整）
# module load python/3.9
# module load cuda/11.8
# module load pytorch/2.0

# 激活虚拟环境（根据环境调整）
# source activate g2cf-pinn

# 设置环境变量
export CUDA_VISIBLE_DEVICES=0,1,2,3
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# 创建日志目录
mkdir -p logs

# 运行实验
MODULE=${1:-"main"}

echo "=========================================="
echo "SLURM Job: $SLURM_JOB_ID"
echo "Module: $MODULE"
echo "GPUs: $CUDA_VISIBLE_DEVICES"
echo "=========================================="

if [ "$MODULE" == "main" ]; then
    # 并行运行主实验
    bash scripts/submit_parallel.sh main 4
elif [ "$MODULE" == "all" ]; then
    # 运行所有实验
    bash scripts/submit_parallel.sh all 4
else
    # 运行单个模块
    bash scripts/run_experiments.sh $MODULE 0
fi

echo ""
echo "=========================================="
echo "Job completed at: $(date)"
echo "=========================================="

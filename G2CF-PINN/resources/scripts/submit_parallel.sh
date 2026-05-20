#!/bin/bash
# 多GPU并行提交脚本
# 用法: bash submit_parallel.sh [module] [num_gpus]
# 示例: bash submit_parallel.sh main 4  (用4块GPU并行运行主实验)

set -e

MODULE=${1:-"main"}
NUM_GPUS=${2:-"4"}

echo "=========================================="
echo "Parallel Experiment Submission"
echo "Module: $MODULE"
echo "Number of GPUs: $NUM_GPUS"
echo "=========================================="

# ============================================================
# 按模块分配GPU
# ============================================================

if [ "$MODULE" == "main" ]; then
    echo "Running main modules (1-5) in parallel..."
    
    # 模块1-2: GPU 0
    bash run_experiments.sh 1 0 &
    bash run_experiments.sh 2 0 &
    
    # 模块3: GPU 1
    bash run_experiments.sh 3 1 &
    
    # 模块4: GPU 2
    bash run_experiments.sh 4 2 &
    
    # 模块5: GPU 3
    bash run_experiments.sh 5 3 &
    
elif [ "$MODULE" == "all" ]; then
    echo "Running all modules (1-7) in parallel..."
    
    # 模块1-2: GPU 0
    bash run_experiments.sh 1 0 &
    bash run_experiments.sh 2 0 &
    
    # 模块3: GPU 1
    bash run_experiments.sh 3 1 &
    
    # 模块4: GPU 2
    bash run_experiments.sh 4 2 &
    
    # 模块5: GPU 3
    bash run_experiments.sh 5 3 &
    
    # 附录模块: GPU 0-1 (等主实验完成后)
    wait
    echo "Main modules completed, starting appendix modules..."
    
    bash run_experiments.sh 6 0 &
    bash run_experiments.sh 7 1 &
    
else
    # 单模块并行
    echo "Running module $MODULE with $NUM_GPUS GPUs..."
    
    # 将种子分配到不同GPU
    seeds=(42 43 44)
    for i in "${!seeds[@]}"; do
        gpu_id=$((i % NUM_GPUS))
        echo "Seed ${seeds[$i]} -> GPU $gpu_id"
        # 这里需要修改run_experiments.sh支持单种子运行
        # 或者创建新的脚本
    done
fi

# 等待所有后台任务完成
wait

echo ""
echo "=========================================="
echo "All parallel experiments completed!"
echo "=========================================="

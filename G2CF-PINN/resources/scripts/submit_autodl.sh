#!/bin/bash
# AutoDL云GPU提交脚本
# 用法: bash submit_autodl.sh [module]
# 示例: bash submit_autodl.sh main

set -e

MODULE=${1:-"main"}

echo "=========================================="
echo "AutoDL Experiment Submission"
echo "Module: $MODULE"
echo "Start time: $(date)"
echo "=========================================="

# ============================================================
# 环境检查
# ============================================================
echo "Checking environment..."

# 检查GPU
if ! nvidia-smi &> /dev/null; then
    echo "Error: No GPU found!"
    exit 1
fi

GPU_INFO=$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader)
echo "GPU: $GPU_INFO"

# 检查Python环境
if ! command -v python &> /dev/null; then
    echo "Error: Python not found!"
    exit 1
fi

PYTHON_VERSION=$(python --version)
echo "Python: $PYTHON_VERSION"

# 检查PyTorch
if ! python -c "import torch; print(f'PyTorch {torch.__version__}, CUDA {torch.version.cuda}')" 2>/dev/null; then
    echo "Error: PyTorch not found!"
    exit 1
fi

# ============================================================
# 安装依赖（如果需要）
# ============================================================
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt -q
fi

# ============================================================
# 运行实验
# ============================================================
echo ""
echo "Starting experiments..."

# 创建输出目录
mkdir -p results logs

# 根据模块运行
case $MODULE in
    1|2|3|4|5|6|7)
        echo "Running module $MODULE..."
        bash scripts/run_experiments.sh $MODULE 0
        ;;
    main)
        echo "Running main modules (1-5)..."
        
        # 顺序运行（单GPU）
        for m in 1 2 3 4 5; do
            echo ""
            echo "=========================================="
            echo "Starting module $m..."
            echo "=========================================="
            bash scripts/run_experiments.sh $m 0
        done
        ;;
    all)
        echo "Running all modules (1-7)..."
        
        for m in 1 2 3 4 5 6 7; do
            echo ""
            echo "=========================================="
            echo "Starting module $m..."
            echo "=========================================="
            bash scripts/run_experiments.sh $m 0
        done
        ;;
    *)
        echo "Unknown module: $MODULE"
        echo "Usage: bash submit_autodl.sh [1-7|main|all]"
        exit 1
        ;;
esac

# ============================================================
# 完成
# ============================================================
echo ""
echo "=========================================="
echo "All experiments completed!"
echo "End time: $(date)"
echo ""
echo "Results summary:"
echo "- Results: results/"
echo "- Logs: logs/"
echo ""
echo "To download results:"
echo "  tar -czf results.tar.gz results/ logs/"
echo "=========================================="

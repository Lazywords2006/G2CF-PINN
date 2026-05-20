#!/bin/bash
# G2CF-PINN 实验批处理脚本
# 用法: bash run_experiments.sh [module] [gpu_id]
# 示例: bash run_experiments.sh 1 0  (在GPU 0上运行模块1)

set -e  # 遇到错误立即退出

# ============================================================
# 配置
# ============================================================
MODULE=${1:-"all"}  # 要运行的模块，默认运行所有
GPU_ID=${2:-"0"}    # GPU ID，默认0
CONFIG_DIR="configs"
OUTPUT_DIR="results"
LOG_DIR="logs"

# 创建目录
mkdir -p $OUTPUT_DIR $LOG_DIR

# 设置GPU
export CUDA_VISIBLE_DEVICES=$GPU_ID

# ============================================================
# 辅助函数
# ============================================================
run_experiment() {
    local config=$1
    local seed=$2
    local method=$3
    local output_subdir=$4
    
    echo "=========================================="
    echo "Running: $method (seed=$seed)"
    echo "Config: $config"
    echo "=========================================="
    
    python train.py \
        --config $config \
        --seed $seed \
        --method $method \
        --output $OUTPUT_DIR/$output_subdir \
        2>&1 | tee $LOG_DIR/${output_subdir}_seed${seed}.log
}

# ============================================================
# 模块1: 解析梯度效率验证
# ============================================================
run_module1() {
    echo "Running Module 1: Gradient Efficiency"
    
    for seed in 42 43 44; do
        # 标准PINN
        run_experiment $CONFIG_DIR/module1_gradient_efficiency.yaml $seed standard_pinn module1
        
        # FastLSQ
        run_experiment $CONFIG_DIR/module1_gradient_efficiency.yaml $seed fastlsq module1
        
        # G2CF-PINN
        run_experiment $CONFIG_DIR/module1_gradient_efficiency.yaml $seed g2cf_pinn module1
    done
}

# ============================================================
# 模块2: 因果训练效果验证
# ============================================================
run_module2() {
    echo "Running Module 2: Causal Training"
    
    for seed in 42 43 44; do
        # 标准PINN
        run_experiment $CONFIG_DIR/module2_causal_training.yaml $seed standard_pinn module2
        
        # SA-PINNs
        run_experiment $CONFIG_DIR/module2_causal_training.yaml $seed sa_pinns module2
        
        # TCAS-PINN
        run_experiment $CONFIG_DIR/module2_causal_training.yaml $seed tcas_pinn module2
        
        # G2CF-PINN
        run_experiment $CONFIG_DIR/module2_causal_training.yaml $seed g2cf_pinn module2
    done
}

# ============================================================
# 模块3: 梯度引导采样验证
# ============================================================
run_module3() {
    echo "Running Module 3: Gradient Sampling"
    
    for seed in 42 43 44; do
        # 均匀采样
        run_experiment $CONFIG_DIR/module3_gradient_sampling.yaml $seed uniform_sampling module3
        
        # RAD/RAR-D
        run_experiment $CONFIG_DIR/module3_gradient_sampling.yaml $seed rad_rar_d module3
        
        # RL-PINNs
        run_experiment $CONFIG_DIR/module3_gradient_sampling.yaml $seed rl_pinns module3
        
        # G2CF-PINN
        run_experiment $CONFIG_DIR/module3_gradient_sampling.yaml $seed g2cf_pinn module3
    done
}

# ============================================================
# 模块4: 端到端SOTA对比
# ============================================================
run_module4() {
    echo "Running Module 4: SOTA Comparison"
    
    for seed in 42 43 44; do
        # 标准PINN
        run_experiment $CONFIG_DIR/module4_sota_comparison.yaml $seed standard_pinn module4
        
        # DPINN
        run_experiment $CONFIG_DIR/module4_sota_comparison.yaml $seed dpinn module4
        
        # CI-PINN
        run_experiment $CONFIG_DIR/module4_sota_comparison.yaml $seed ci_pinn module4
        
        # Scale-PINN
        run_experiment $CONFIG_DIR/module4_sota_comparison.yaml $seed scale_pinn module4
        
        # G2CF-PINN
        run_experiment $CONFIG_DIR/module4_sota_comparison.yaml $seed g2cf_pinn module4
    done
}

# ============================================================
# 模块5: 消融研究
# ============================================================
run_module5() {
    echo "Running Module 5: Ablation Study"
    
    # 消融研究用固定种子
    seed=42
    
    # 完整版
    run_experiment $CONFIG_DIR/module5_ablation.yaml $seed g2cf_full module5
    
    # w/o 因果训练
    run_experiment $CONFIG_DIR/module5_ablation.yaml $seed g2cf_no_causal module5
    
    # w/o 梯度引导
    run_experiment $CONFIG_DIR/module5_ablation.yaml $seed g2cf_no_gradient module5
    
    # w/o 解析梯度
    run_experiment $CONFIG_DIR/module5_ablation.yaml $seed g2cf_autodiff module5
}

# ============================================================
# 模块6: 频率矩阵敏感性 (附录)
# ============================================================
run_module6() {
    echo "Running Module 6: Frequency Sensitivity (Appendix)"
    
    for seed in 42 43 44 45 46; do
        run_experiment $CONFIG_DIR/module6_frequency_sensitivity.yaml $seed g2cf_pinn module6
    done
}

# ============================================================
# 模块7: 2D方程泛化性 (附录)
# ============================================================
run_module7() {
    echo "Running Module 7: 2D Generalization (Appendix)"
    
    for seed in 42 43 44; do
        # 标准PINN
        run_experiment $CONFIG_DIR/module7_2d_generalization.yaml $seed standard_pinn module7
        
        # PhyGeoNet
        run_experiment $CONFIG_DIR/module7_2d_generalization.yaml $seed phygeonet module7
        
        # G2CF-PINN
        run_experiment $CONFIG_DIR/module7_2d_generalization.yaml $seed g2cf_pinn module7
    done
}

# ============================================================
# 主执行逻辑
# ============================================================
case $MODULE in
    1)
        run_module1
        ;;
    2)
        run_module2
        ;;
    3)
        run_module3
        ;;
    4)
        run_module4
        ;;
    5)
        run_module5
        ;;
    6)
        run_module6
        ;;
    7)
        run_module7
        ;;
    all)
        echo "Running all modules..."
        run_module1
        run_module2
        run_module3
        run_module4
        run_module5
        run_module6
        run_module7
        ;;
    main)
        echo "Running main modules only (1-5)..."
        run_module1
        run_module2
        run_module3
        run_module4
        run_module5
        ;;
    *)
        echo "Unknown module: $MODULE"
        echo "Usage: bash run_experiments.sh [1-7|all|main] [gpu_id]"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "All experiments completed!"
echo "Results saved to: $OUTPUT_DIR"
echo "Logs saved to: $LOG_DIR"
echo "=========================================="

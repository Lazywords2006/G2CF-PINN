#!/bin/bash
# G2CF-PINN 训练启动脚本
# 用于在服务器上启动训练任务

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Python环境
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD=python3
    elif command -v python &> /dev/null; then
        PYTHON_CMD=python
    else
        print_error "未找到Python，请先安装Python 3.8+"
        exit 1
    fi
    
    # 检查Python版本
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    print_info "Python版本: $PYTHON_VERSION"
}

# 检查并安装依赖
install_dependencies() {
    print_info "检查并安装依赖..."
    
    # 检查pip
    if ! $PYTHON_CMD -m pip --version &> /dev/null; then
        print_error "未找到pip，请先安装pip"
        exit 1
    fi
    
    # 安装依赖
    if [ -f "requirements.txt" ]; then
        print_info "从requirements.txt安装依赖..."
        $PYTHON_CMD -m pip install -r requirements.txt --quiet
    else
        print_warn "未找到requirements.txt，跳过依赖安装"
    fi
}

# 检查GPU可用性
check_gpu() {
    print_info "检查GPU可用性..."
    
    if $PYTHON_CMD -c "import torch; print('CUDA可用:', torch.cuda.is_available())" 2>/dev/null; then
        GPU_INFO=$($PYTHON_CMD -c "import torch; print('GPU数量:', torch.cuda.device_count()); print('当前GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else '无')" 2>/dev/null)
        print_info "$GPU_INFO"
    else
        print_warn "未检测到CUDA，将使用CPU训练"
    fi
}

# 创建必要的目录
create_directories() {
    print_info "创建必要的目录..."
    
    mkdir -p results
    mkdir -p logs
    mkdir -p checkpoints
    
    print_info "目录创建完成"
}

# 运行训练
run_training() {
    local config_file=$1
    local device=${2:-auto}
    local seed=${3:-42}
    
    if [ ! -f "$config_file" ]; then
        print_error "配置文件不存在: $config_file"
        exit 1
    fi
    
    print_info "开始训练..."
    print_info "配置文件: $config_file"
    print_info "设备: $device"
    print_info "随机种子: $seed"
    
    # 生成日志文件名
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    LOG_FILE="logs/training_${TIMESTAMP}.log"
    
    # 运行训练脚本
    $PYTHON_CMD experiments/train.py \
        --config "$config_file" \
        --output_dir results \
        --device "$device" \
        --seed "$seed" \
        2>&1 | tee "$LOG_FILE"
    
    # 检查训练结果
    if [ $? -eq 0 ]; then
        print_info "训练完成！"
        print_info "日志文件: $LOG_FILE"
        print_info "结果目录: results/"
    else
        print_error "训练失败，请查看日志: $LOG_FILE"
        exit 1
    fi
}

# 主函数
main() {
    echo "=========================================="
    echo "    G2CF-PINN 训练启动脚本"
    echo "=========================================="
    echo ""
    
    # 检查Python环境
    check_python
    
    # 安装依赖
    install_dependencies
    
    # 检查GPU
    check_gpu
    
    # 创建目录
    create_directories
    
    # 解析命令行参数
    CONFIG_FILE="experiments/configs/burgers.yaml"
    DEVICE="auto"
    SEED=42
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --config)
                CONFIG_FILE="$2"
                shift 2
                ;;
            --device)
                DEVICE="$2"
                shift 2
                ;;
            --seed)
                SEED="$2"
                shift 2
                ;;
            --help)
                echo "用法: $0 [选项]"
                echo ""
                echo "选项:"
                echo "  --config FILE    配置文件路径 (默认: experiments/configs/burgers.yaml)"
                echo "  --device DEVICE  计算设备 (auto/cpu/cuda/mps) (默认: auto)"
                echo "  --seed SEED      随机种子 (默认: 42)"
                echo "  --help           显示帮助信息"
                exit 0
                ;;
            *)
                print_error "未知参数: $1"
                exit 1
                ;;
        esac
    done
    
    # 运行训练
    run_training "$CONFIG_FILE" "$DEVICE" "$SEED"
}

# 执行主函数
main "$@"
#!/bin/bash
# G2CF-PINN 服务器部署脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 显示帮助
show_help() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  --server SERVER    服务器地址 (必需)"
    echo "  --user USER        用户名 (默认: 当前用户)"
    echo "  --path PATH        远程路径 (默认: ~/G2CF-PINN)"
    echo "  --port PORT        SSH端口 (默认: 22)"
    echo "  --help             显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 --server gpu.example.com"
    echo "  $0 --server gpu.example.com --user myuser --path /data/G2CF-PINN"
}

# 解析命令行参数
SERVER=""
USER=$(whoami)
REMOTE_PATH="~/G2CF-PINN"
PORT=22

while [[ $# -gt 0 ]]; do
    case $1 in
        --server)
            SERVER="$2"
            shift 2
            ;;
        --user)
            USER="$2"
            shift 2
            ;;
        --path)
            REMOTE_PATH="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            print_error "未知参数: $1"
            show_help
            exit 1
            ;;
    esac
done

# 检查必需参数
if [ -z "$SERVER" ]; then
    print_error "必须指定服务器地址"
    show_help
    exit 1
fi

print_info "开始部署 G2CF-PINN 到服务器"
print_info "服务器: $SERVER"
print_info "用户: $USER"
print_info "远程路径: $REMOTE_PATH"
print_info "SSH端口: $PORT"

# 测试SSH连接
print_info "测试SSH连接..."
if ! ssh -p $PORT -o ConnectTimeout=10 -o BatchMode=yes $USER@$SERVER "echo '连接成功'" 2>/dev/null; then
    print_error "无法连接到服务器，请检查SSH配置"
    exit 1
fi
print_info "SSH连接正常"

# 创建远程目录
print_info "创建远程目录..."
ssh -p $PORT $USER@$SERVER "mkdir -p $REMOTE_PATH/experiments"

# 上传代码
print_info "上传代码..."
rsync -avz -e "ssh -p $PORT" \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.git' \
    --exclude='results' \
    --exclude='logs' \
    --exclude='venv' \
    ./ $USER@$SERVER:$REMOTE_PATH/experiments/

print_info "代码上传完成"

# 在服务器上安装依赖
print_info "在服务器上安装依赖..."
ssh -p $PORT $USER@$SERVER "cd $REMOTE_PATH/experiments && pip install -r requirements.txt --user"

print_info "依赖安装完成"

# 创建启动脚本
print_info "创建启动脚本..."
ssh -p $PORT $USER@$SERVER "cd $REMOTE_PATH/experiments && chmod +x run_training.sh"

# 显示部署信息
echo ""
echo "=========================================="
echo "部署完成！"
echo "=========================================="
echo ""
echo "登录服务器:"
echo "  ssh -p $PORT $USER@$SERVER"
echo ""
echo "进入项目目录:"
echo "  cd $REMOTE_PATH/experiments"
echo ""
echo "开始训练:"
echo "  # 使用启动脚本"
echo "  ./run_training.sh --device cuda"
echo ""
echo "  # 或使用SLURM"
echo "  sbatch train.slurm"
echo ""
echo "  # 或直接运行Python"
echo "  python3 train.py --config configs/burgers.yaml --device cuda"
echo ""
echo "=========================================="
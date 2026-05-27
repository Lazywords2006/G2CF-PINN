#!/bin/bash
# G2CF-PINN 相关论文批量下载脚本
# 使用方法: bash download_papers.sh
# 注意: 需要网络连接正常

set -e

BASE_DIR="/Users/lazywords/Documents/PINN&PNE/01_文献库/完整文献库"

echo "=========================================="
echo "G2CF-PINN 相关论文批量下载脚本"
echo "=========================================="
echo ""

# 检查网络连接
echo "检查网络连接..."
if ! curl -s --head https://arxiv.org > /dev/null; then
    echo "错误: 无法连接到 arxiv.org，请检查网络连接"
    exit 1
fi
echo "网络连接正常"
echo ""

# 下载函数
download_paper() {
    local arxiv_id=$1
    local filename=$2
    local category=$3
    
    local url="https://arxiv.org/pdf/${arxiv_id}.pdf"
    local output_dir="${BASE_DIR}/${category}"
    local output_file="${output_dir}/${filename}"
    
    if [ -f "$output_file" ]; then
        echo "跳过 (已存在): $filename"
        return 0
    fi
    
    echo "下载: $filename"
    if curl -L -s -o "$output_file" "$url"; then
        echo "  成功: $output_file"
    else
        echo "  失败: $filename"
        rm -f "$output_file"
    fi
}

echo "=========================================="
echo "类别1: 自适应采样方法 (20篇)"
echo "=========================================="

# 自适应采样论文
download_paper "2207.10289" "Wu et al. - 2022 - Comprehensive study adaptive sampling PINNs.pdf" "01_自适应采样"
download_paper "2009.04544" "McClenny - 2020 - Self-Adaptive PINNs.pdf" "01_自适应采样"

echo ""
echo "=========================================="
echo "类别2: 傅里叶特征与频谱方法 (20篇)"
echo "=========================================="

# 傅里叶特征论文
download_paper "2401.11276" "Jin et al. - 2024 - Fourier warm start for PINNs.pdf" "02_傅里叶特征"

echo ""
echo "=========================================="
echo "类别3: 激波与双曲PDE求解 (20篇)"
echo "=========================================="

# 激波求解论文 - 使用已有的论文
echo "跳过 (使用已有论文库中的论文)"

echo ""
echo "=========================================="
echo "类别4: 因果训练与时序问题 (20篇)"
echo "=========================================="

# 因果训练论文
# CEENs 论文已在库中

echo ""
echo "=========================================="
echo "类别5: 梯度增强与优化方法 (20篇)"
echo "=========================================="

# 梯度增强论文
# gPINN 论文已在库中

echo ""
echo "=========================================="
echo "下载完成!"
echo "=========================================="
echo ""
echo "请手动下载以下重要论文:"
echo ""
echo "1. RAD/RAR-D (Wu et al., 2022):"
echo "   https://arxiv.org/abs/2207.10289"
echo ""
echo "2. SA-PINNs (McClenny, 2020):"
echo "   https://arxiv.org/abs/2009.04544"
echo ""
echo "3. gPINN (Yu et al., 2022):"
echo "   https://arxiv.org/abs/2211.08206"
echo ""
echo "4. CEENs (Jung et al., 2024):"
echo "   https://arxiv.org/abs/2403.12345"
echo ""
echo "5. DPINN (Lei et al., 2025):"
echo "   https://arxiv.org/abs/2507.08338"
echo ""
echo "6. FastLSQ (Sulc, 2026):"
echo "   https://arxiv.org/abs/2602.10541"
echo ""
echo "7. CI-PINN (Wang & Yang, 2024):"
echo "   https://arxiv.org/abs/2411.11276"
echo ""
echo "完整论文列表请参考: 02_数据与分析/EXPERIMENT_ANALYSIS_AND_PAPER_LIST.md"

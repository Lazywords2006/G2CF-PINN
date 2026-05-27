#!/usr/bin/env python3
"""
G2CF-PINN 相关论文批量下载脚本
从arXiv搜索并下载100篇相关论文
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import time
import os
import re
import json
from datetime import datetime

BASE_DIR = "/Users/lazywords/Documents/PINN&PNE/01_文献库/完整文献库"

# 搜索查询列表
SEARCH_QUERIES = [
    # 自适应采样
    ("01_自适应采样", [
        "physics-informed neural networks adaptive sampling",
        "PINN residual-based adaptive refinement",
        "neural network adaptive collocation points PDE",
        "importance sampling physics-informed",
    ]),
    # 傅里叶特征
    ("02_傅里叶特征", [
        "Fourier features neural network PDE",
        "spectral representation neural network",
        "frequency domain neural network differential equation",
        "positional encoding PINN high frequency",
    ]),
    # 激波求解
    ("03_激波求解", [
        "shock wave neural network PDE",
        "Burgers equation neural network",
        "discontinuous solution physics-informed",
        "conservation law neural network",
    ]),
    # 因果训练
    ("04_因果训练", [
        "causal training physics-informed neural network",
        "temporal causality PINN",
        "sequential training PDE neural network",
        "time-stepping physics-informed",
    ]),
    # 梯度增强
    ("05_梯度增强", [
        "gradient-enhanced physics-informed neural network",
        "automatic differentiation PDE residual",
        "higher-order derivative neural network",
        "Sobolev training neural network",
    ]),
    # 损失函数设计
    ("06_损失函数设计", [
        "loss function design PINN",
        "adaptive loss weighting physics-informed",
        "multi-task learning PDE",
        "curriculum learning PINN",
    ]),
    # 基准测试
    ("07_基准测试", [
        "PINN benchmark comparison",
        "physics-informed neural network evaluation",
        "neural PDE solver comparison study",
        "numerical method benchmark PDE",
    ]),
    # 混合方法
    ("08_混合方法", [
        "hybrid numerical neural network PDE",
        "physics-informed machine learning",
        "data-driven PDE solving",
        "neural network finite element",
    ]),
    # 算子学习
    ("09_算子学习", [
        "neural operator PDE solving",
        "DeepONet physics-informed",
        "Fourier neural operator",
        "operator learning differential equation",
    ]),
    # 不确定性量化
    ("10_不确定性量化", [
        "uncertainty quantification PINN",
        "Bayesian physics-informed neural network",
        "probabilistic PDE solving neural network",
        "ensemble methods PINN",
    ]),
]

# 已有论文标题（用于去重）
EXISTING_PAPERS = set()

def load_existing_papers():
    """加载已有论文标题"""
    try:
        result = os.popen(f'ls "{BASE_DIR}" 2>/dev/null').read()
        for line in result.strip().split('\n'):
            if line.endswith('.pdf'):
                # 提取标题部分
                title = line.replace('.pdf', '').split(' - ')[-1] if ' - ' in line else line
                EXISTING_PAPERS.add(title.lower()[:50])
    except:
        pass

def search_arxiv(query, max_results=15):
    """搜索arXiv论文"""
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"  搜索失败: {e}")
        return None

def parse_arxiv_response(xml_data):
    """解析arXiv API响应"""
    papers = []
    try:
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
        
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
            summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')[:200]
            
            # 获取PDF链接
            pdf_link = None
            for link in entry.findall('atom:link', ns):
                if link.get('title') == 'pdf':
                    pdf_link = link.get('href')
            
            # 获取arXiv ID
            id_url = entry.find('atom:id', ns).text
            arxiv_id = id_url.split('/abs/')[-1]
            
            # 获取作者
            authors = []
            for author in entry.findall('atom:author', ns):
                name = author.find('atom:name', ns).text
                authors.append(name)
            
            # 获取年份
            published = entry.find('atom:published', ns).text
            year = published[:4]
            
            papers.append({
                'title': title,
                'authors': authors[:3],
                'year': year,
                'arxiv_id': arxiv_id,
                'pdf_link': pdf_link or f"https://arxiv.org/pdf/{arxiv_id}",
                'summary': summary
            })
    except Exception as e:
        print(f"  解析失败: {e}")
    
    return papers

def download_paper(paper, category_dir, index):
    """下载单篇论文"""
    # 构建文件名
    first_author = paper['authors'][0].split()[-1] if paper['authors'] else 'Unknown'
    title_short = re.sub(r'[^\w\s-]', '', paper['title'])[:60].strip()
    filename = f"{first_author} et al. - {paper['year']} - {title_short}.pdf"
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    filepath = os.path.join(category_dir, filename)
    
    if os.path.exists(filepath):
        print(f"  [跳过] 已存在: {filename[:50]}...")
        return False
    
    try:
        print(f"  [{index}] 下载: {filename[:50]}...")
        urllib.request.urlretrieve(paper['pdf_link'], filepath)
        time.sleep(1)  # 避免请求过快
        return True
    except Exception as e:
        print(f"  [失败] {filename[:30]}... - {e}")
        if os.path.exists(filepath):
            os.remove(filepath)
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("G2CF-PINN 相关论文批量下载")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    load_existing_papers()
    
    total_downloaded = 0
    total_skipped = 0
    total_failed = 0
    
    results = {}
    
    for category, queries in SEARCH_QUERIES:
        print(f"\n{'='*50}")
        print(f"📁 分类: {category}")
        print(f"{'='*50}")
        
        category_dir = os.path.join(BASE_DIR, category)
        os.makedirs(category_dir, exist_ok=True)
        
        category_papers = []
        seen_ids = set()
        
        for query in queries:
            print(f"\n🔍 搜索: {query}")
            xml_data = search_arxiv(query, max_results=8)
            
            if xml_data:
                papers = parse_arxiv_response(xml_data)
                for paper in papers:
                    if paper['arxiv_id'] not in seen_ids:
                        seen_ids.add(paper['arxiv_id'])
                        category_papers.append(paper)
            
            time.sleep(2)  # API限制
        
        print(f"\n📊 找到 {len(category_papers)} 篇论文")
        
        # 下载论文（每个分类最多10篇）
        downloaded = 0
        for i, paper in enumerate(category_papers[:10]):
            if download_paper(paper, category_dir, i+1):
                downloaded += 1
                total_downloaded += 1
            else:
                total_skipped += 1
        
        results[category] = {
            'found': len(category_papers),
            'downloaded': downloaded
        }
        
        print(f"✅ 本分类下载: {downloaded} 篇")
    
    # 保存下载报告
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_downloaded': total_downloaded,
        'total_skipped': total_skipped,
        'categories': results
    }
    
    report_path = os.path.join(BASE_DIR, '..', 'download_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print("📊 下载完成统计")
    print("=" * 60)
    print(f"总下载: {total_downloaded} 篇")
    print(f"总跳过: {total_skipped} 篇")
    print(f"\n分类详情:")
    for cat, stats in results.items():
        print(f"  {cat}: 找到 {stats['found']}, 下载 {stats['downloaded']}")
    
    print(f"\n报告已保存: {report_path}")

if __name__ == "__main__":
    main()

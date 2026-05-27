#!/usr/bin/env python3
"""
论文下载重试脚本 - 定时重试直到下载完成
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
TARGET_PER_CATEGORY = 10  # 每个分类目标下载数量

# 所有分类及查询
ALL_QUERIES = {
    "01_自适应采样": [
        "physics-informed neural networks adaptive sampling",
        "PINN residual-based adaptive refinement",
    ],
    "02_傅里叶特征": [
        "Fourier features neural network PDE",
        "spectral representation neural network",
    ],
    "03_激波求解": [
        "shock wave neural network PDE",
        "Burgers equation neural network",
    ],
    "04_因果训练": [
        "causal training physics-informed neural network",
        "temporal causality PINN",
    ],
    "05_梯度增强": [
        "gradient-enhanced physics-informed neural network",
        "Sobolev training neural network",
    ],
    "06_损失函数设计": [
        "loss function design PINN",
        "adaptive loss weighting physics-informed",
    ],
    "07_混合方法": [
        "hybrid numerical neural network PDE",
        "physics-informed machine learning",
    ],
    "08_算子学习": [
        "neural operator PDE solving",
        "Fourier neural operator",
    ],
    "09_不确定性量化": [
        "uncertainty quantification PINN",
        "Bayesian physics-informed neural network",
    ],
    "10_高阶方法": [
        "high-order neural network PDE",
        "multi-scale physics-informed",
    ],
    "11_逆问题": [
        "inverse problem physics-informed neural network",
        "PDE discovery neural network",
    ],
}

def count_pdfs(category_dir):
    """统计目录中的PDF数量"""
    if not os.path.exists(category_dir):
        return 0
    return len([f for f in os.listdir(category_dir) if f.endswith('.pdf')])

def search_arxiv(query, max_results=10):
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
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
            
            pdf_link = None
            for link in entry.findall('atom:link', ns):
                if link.get('title') == 'pdf':
                    pdf_link = link.get('href')
            
            id_url = entry.find('atom:id', ns).text
            arxiv_id = id_url.split('/abs/')[-1]
            
            authors = []
            for author in entry.findall('atom:author', ns):
                name = author.find('atom:name', ns).text
                authors.append(name)
            
            published = entry.find('atom:published', ns).text
            year = published[:4]
            
            papers.append({
                'title': title,
                'authors': authors[:3],
                'year': year,
                'arxiv_id': arxiv_id,
                'pdf_link': pdf_link or f"https://arxiv.org/pdf/{arxiv_id}",
            })
    except Exception as e:
        print(f"  解析失败: {e}")
    
    return papers

def download_paper(paper, category_dir):
    """下载单篇论文"""
    first_author = paper['authors'][0].split()[-1] if paper['authors'] else 'Unknown'
    title_short = re.sub(r'[^\w\s-]', '', paper['title'])[:60].strip()
    filename = f"{first_author} et al. - {paper['year']} - {title_short}.pdf"
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    filepath = os.path.join(category_dir, filename)
    
    if os.path.exists(filepath):
        return False
    
    try:
        print(f"  下载: {filename[:50]}...")
        urllib.request.urlretrieve(paper['pdf_link'], filepath)
        time.sleep(2)  # 更长的延迟避免限流
        return True
    except Exception as e:
        print(f"  失败: {e}")
        if os.path.exists(filepath):
            os.remove(filepath)
        return False

def main():
    print("=" * 60)
    print("论文下载重试脚本")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 检查每个分类的下载进度
    categories_to_download = []
    
    for category in ALL_QUERIES:
        category_dir = os.path.join(BASE_DIR, category)
        current_count = count_pdfs(category_dir)
        
        if current_count < TARGET_PER_CATEGORY:
            categories_to_download.append((category, current_count))
            print(f"  {category}: {current_count}/{TARGET_PER_CATEGORY} 篇")
    
    if not categories_to_download:
        print("\n所有分类已达到目标数量！")
        return
    
    print(f"\n需要下载 {len(categories_to_download)} 个分类")
    
    total_downloaded = 0
    
    for category, current_count in categories_to_download:
        category_dir = os.path.join(BASE_DIR, category)
        os.makedirs(category_dir, exist_ok=True)
        
        needed = TARGET_PER_CATEGORY - current_count
        print(f"\n{'='*50}")
        print(f"📁 {category}: 需要再下载 {needed} 篇")
        print(f"{'='*50}")
        
        category_papers = []
        seen_ids = set()
        
        for query in ALL_QUERIES[category]:
            print(f"\n🔍 搜索: {query}")
            xml_data = search_arxiv(query, max_results=15)
            
            if xml_data:
                papers = parse_arxiv_response(xml_data)
                for paper in papers:
                    if paper['arxiv_id'] not in seen_ids:
                        seen_ids.add(paper['arxiv_id'])
                        category_papers.append(paper)
                print(f"  找到 {len(papers)} 篇")
            else:
                print("  搜索失败，等待30秒后重试...")
                time.sleep(30)
            
            time.sleep(5)  # 更长的API延迟
        
        # 下载论文
        downloaded = 0
        for paper in category_papers[:needed]:
            if download_paper(paper, category_dir):
                downloaded += 1
                total_downloaded += 1
                if downloaded >= needed:
                    break
        
        print(f"✅ 本分类下载: {downloaded} 篇")
    
    # 最终统计
    print("\n" + "=" * 60)
    print("📊 最终统计")
    print("=" * 60)
    
    grand_total = 0
    for category in ALL_QUERIES:
        category_dir = os.path.join(BASE_DIR, category)
        count = count_pdfs(category_dir)
        grand_total += count
        status = "✅" if count >= TARGET_PER_CATEGORY else "⚠️"
        print(f"  {status} {category}: {count} 篇")
    
    print(f"\n总计: {grand_total} 篇论文")
    print(f"本次新下载: {total_downloaded} 篇")

if __name__ == "__main__":
    main()

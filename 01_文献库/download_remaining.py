#!/usr/bin/env python3
"""
高效论文下载脚本 - 剩余分类下载
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

# 剩余需要下载的分类
SEARCH_QUERIES = [
    # 混合方法
    ("07_混合方法", [
        "hybrid numerical neural network PDE",
        "physics-informed machine learning",
        "data-driven PDE solving",
        "neural network finite element",
    ]),
    # 算子学习
    ("08_算子学习", [
        "neural operator PDE solving",
        "DeepONet physics-informed",
        "Fourier neural operator",
        "operator learning differential equation",
    ]),
    # 不确定性量化
    ("09_不确定性量化", [
        "uncertainty quantification PINN",
        "Bayesian physics-informed neural network",
        "probabilistic PDE solving neural network",
        "ensemble methods PINN",
    ]),
    # 补充：高阶方法
    ("10_高阶方法", [
        "high-order neural network PDE",
        "spectral method neural network",
        "hp-Adaptivity PINN",
        "multi-scale physics-informed",
    ]),
    # 补充：逆问题
    ("11_逆问题", [
        "inverse problem physics-informed neural network",
        "parameter identification PINN",
        "PDE discovery neural network",
        "system identification neural network",
    ]),
]

def search_arxiv(query, max_results=12):
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
            summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')[:200]
            
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
                'summary': summary
            })
    except Exception as e:
        print(f"  解析失败: {e}")
    
    return papers

def download_paper(paper, category_dir, index):
    """下载单篇论文"""
    first_author = paper['authors'][0].split()[-1] if paper['authors'] else 'Unknown'
    title_short = re.sub(r'[^\w\s-]', '', paper['title'])[:60].strip()
    filename = f"{first_author} et al. - {paper['year']} - {title_short}.pdf"
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    filepath = os.path.join(category_dir, filename)
    
    if os.path.exists(filepath):
        return False
    
    try:
        print(f"  [{index}] 下载: {filename[:50]}...")
        urllib.request.urlretrieve(paper['pdf_link'], filepath)
        time.sleep(1.5)
        return True
    except Exception as e:
        print(f"  [失败] {e}")
        if os.path.exists(filepath):
            os.remove(filepath)
        return False

def main():
    print("=" * 60)
    print("继续下载剩余分类论文")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    total_downloaded = 0
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
            xml_data = search_arxiv(query, max_results=10)
            
            if xml_data:
                papers = parse_arxiv_response(xml_data)
                for paper in papers:
                    if paper['arxiv_id'] not in seen_ids:
                        seen_ids.add(paper['arxiv_id'])
                        category_papers.append(paper)
            
            time.sleep(2)
        
        print(f"\n📊 找到 {len(category_papers)} 篇论文")
        
        downloaded = 0
        for i, paper in enumerate(category_papers[:10]):
            if download_paper(paper, category_dir, i+1):
                downloaded += 1
                total_downloaded += 1
        
        results[category] = {
            'found': len(category_papers),
            'downloaded': downloaded
        }
        
        print(f"✅ 本分类下载: {downloaded} 篇")
    
    # 统计所有分类
    print("\n" + "=" * 60)
    print("📊 所有分类统计")
    print("=" * 60)
    
    all_dirs = sorted([d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))])
    grand_total = 0
    for d in all_dirs:
        count = len([f for f in os.listdir(os.path.join(BASE_DIR, d)) if f.endswith('.pdf')])
        grand_total += count
        print(f"  {d}: {count} 篇")
    
    print(f"\n总计: {grand_total} 篇论文")
    print(f"本次新下载: {total_downloaded} 篇")

if __name__ == "__main__":
    main()

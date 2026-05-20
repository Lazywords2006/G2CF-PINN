#!/usr/bin/env python3
"""
实验结果收集与分析脚本
用法: python collect_results.py --input results/ --output report/
"""

import argparse
import json
import os
from pathlib import Path
from typing import Dict, List, Any
import numpy as np


def load_results(results_dir: str) -> List[Dict[str, Any]]:
    """加载所有实验结果"""
    results = []
    results_path = Path(results_dir)
    
    # 遍历所有JSON文件
    for json_file in results_path.rglob('*.json'):
        with open(json_file, 'r') as f:
            data = json.load(f)
            data['_file'] = str(json_file)
            results.append(data)
    
    print(f"Loaded {len(results)} result files")
    return results


def aggregate_by_method(results: List[Dict]) -> Dict[str, List[Dict]]:
    """按方法聚合结果"""
    aggregated = {}
    for r in results:
        method = r.get('method', 'unknown')
        if method not in aggregated:
            aggregated[method] = []
        aggregated[method].append(r)
    return aggregated


def compute_statistics(values: List[float]) -> Dict[str, float]:
    """计算统计量"""
    if not values:
        return {'mean': 0, 'std': 0, 'min': 0, 'max': 0, 'median': 0}
    
    return {
        'mean': np.mean(values),
        'std': np.std(values),
        'min': np.min(values),
        'max': np.max(values),
        'median': np.median(values)
    }


def generate_report(results: List[Dict], output_dir: str):
    """生成实验报告"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 按方法聚合
    by_method = aggregate_by_method(results)
    
    # 生成摘要
    summary = {
        'total_experiments': len(results),
        'methods': list(by_method.keys()),
        'experiments_per_method': {k: len(v) for k, v in by_method.items()}
    }
    
    # 计算各方法的统计量
    method_stats = {}
    for method, method_results in by_method.items():
        training_times = [r.get('training_time', 0) for r in method_results]
        errors = [r.get('relative_l2_error', 0) for r in method_results]
        
        method_stats[method] = {
            'training_time': compute_statistics(training_times),
            'relative_l2_error': compute_statistics(errors)
        }
    
    summary['method_statistics'] = method_stats
    
    # 保存报告
    report_file = output_path / 'experiment_report.json'
    with open(report_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nReport saved to: {report_file}")
    
    # 打印摘要
    print("\n" + "="*60)
    print("EXPERIMENT SUMMARY")
    print("="*60)
    print(f"Total experiments: {summary['total_experiments']}")
    print(f"Methods: {', '.join(summary['methods'])}")
    print("\nMethod Statistics:")
    for method, stats in method_stats.items():
        print(f"\n  {method}:")
        print(f"    Training time: {stats['training_time']['mean']:.2f}s ± {stats['training_time']['std']:.2f}s")
        print(f"    Relative L2 error: {stats['relative_l2_error']['mean']:.4f} ± {stats['relative_l2_error']['std']:.4f}")
    
    # 检查成功标准
    print("\n" + "="*60)
    print("SUCCESS CRITERIA CHECK")
    print("="*60)
    
    # 检查梯度加速（模块1）
    if 'standard_pinn' in method_stats and 'g2cf_pinn' in method_stats:
        std_time = method_stats['standard_pinn']['training_time']['mean']
        g2cf_time = method_stats['g2cf_pinn']['training_time']['mean']
        if g2cf_time > 0:
            speedup = std_time / g2cf_time
            print(f"\nGradient speedup: {speedup:.1f}x")
            if speedup >= 10:
                print("✓ PASSED: Speedup >= 10x")
            else:
                print("✗ FAILED: Speedup < 10x")
    
    # 检查因果一致性（模块2）
    for method in by_method:
        causal_values = [r.get('causal_consistency', 0) for r in by_method[method]]
        if causal_values:
            avg_causal = np.mean(causal_values)
            if avg_causal >= 0.95:
                print(f"\n{method}: Causal consistency = {avg_causal:.2%} ✓")
    
    return summary


def main():
    parser = argparse.ArgumentParser(description='Collect and analyze experiment results')
    parser.add_argument('--input', type=str, default='results', help='Input results directory')
    parser.add_argument('--output', type=str, default='report', help='Output report directory')
    args = parser.parse_args()
    
    # 加载结果
    results = load_results(args.input)
    
    if not results:
        print("No results found!")
        return
    
    # 生成报告
    generate_report(results, args.output)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
G2CF-PINN 统一训练脚本
用法: python train.py --config configs/default.yaml --seed 42
"""

import argparse
import yaml
import time
import torch
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional


def load_config(config_path: str, overrides: Optional[Dict] = None) -> Dict[str, Any]:
    """加载配置文件，支持继承和覆盖"""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # 处理继承
    if 'inherit' in config:
        parent_path = Path(config_path).parent / config['inherit']
        with open(parent_path, 'r') as f:
            parent_config = yaml.safe_load(f)
        # 合并配置（子配置优先）
        merged = {**parent_config, **config}
        del merged['inherit']
        config = merged
    
    # 应用覆盖参数
    if overrides:
        for key, value in overrides.items():
            if '.' in key:
                # 处理嵌套键，如 'model.type'
                keys = key.split('.')
                current = config
                for k in keys[:-1]:
                    if k not in current:
                        current[k] = {}
                    current = current[k]
                current[keys[-1]] = value
            else:
                config[key] = value
    
    return config


def set_seed(seed: int):
    """设置随机种子"""
    torch.manual_seed(seed)
    np.random.seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def get_device(device_str: str) -> torch.device:
    """获取计算设备"""
    if device_str == 'auto':
        if torch.cuda.is_available():
            return torch.device('cuda')
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            return torch.device('mps')
        else:
            return torch.device('cpu')
    return torch.device(device_str)


def build_model(config: Dict[str, Any]) -> torch.nn.Module:
    """根据配置构建模型"""
    model_type = config['model']['type']
    
    if model_type == 'standard_pinn':
        from models.standard_pinn import StandardPINN
        return StandardPINN(config)
    elif model_type == 'g2cf_pinn':
        from models.g2cf_pinn import G2CFPINN
        return G2CFPINN(config)
    elif model_type == 'fastlsq':
        from models.fastlsq import FastLSQ
        return FastLSQ(config)
    elif model_type == 'dpinn':
        from models.dpinn import DPINN
        return DPINN(config)
    elif model_type == 'ci_pinn':
        from models.ci_pinn import CIPINN
        return CIPINN(config)
    elif model_type == 'scale_pinn':
        from models.scale_pinn import ScalePINN
        return ScalePINN(config)
    else:
        raise ValueError(f"Unknown model type: {model_type}")


def build_equation(config: Dict[str, Any]):
    """根据配置构建方程"""
    eq_name = config['equation']['name']
    
    if eq_name == 'burgers':
        from equations.burgers import BurgersEquation
        return BurgersEquation(config)
    elif eq_name == 'allen_cahn':
        from equations.allen_cahn import AllenCahnEquation
        return AllenCahnEquation(config)
    elif eq_name == 'euler_sod':
        from equations.euler_sod import EulerSodEquation
        return EulerSodEquation(config)
    elif eq_name == 'heat_2d':
        from equations.heat_2d import Heat2DEquation
        return Heat2DEquation(config)
    elif eq_name == 'poisson_2d':
        from equations.poisson_2d import Poisson2DEquation
        return Poisson2DEquation(config)
    else:
        raise ValueError(f"Unknown equation: {eq_name}")


def train_single(config: Dict[str, Any], seed: int, method_name: str = 'g2cf_pinn'):
    """运行单次训练实验"""
    # 设置种子
    set_seed(seed)
    
    # 获取设备
    device = get_device(config['device'])
    print(f"Using device: {device}")
    
    # 构建模型和方程
    model = build_model(config).to(device)
    equation = build_equation(config)
    
    # 训练计时
    start_time = time.time()
    
    # TODO: 实现训练循环
    # 这里是框架，具体实现需要根据实际代码结构
    print(f"Training {method_name} with seed {seed}...")
    print(f"Model type: {config['model']['type']}")
    print(f"Batch size: {config['training']['batch_size']}")
    
    # 模拟训练（实际实现时替换）
    # trainer = Trainer(model, equation, config, device)
    # results = trainer.train()
    
    end_time = time.time()
    training_time = end_time - start_time
    
    print(f"Training completed in {training_time:.2f} seconds")
    
    return {
        'seed': seed,
        'method': method_name,
        'training_time': training_time,
        # 'results': results
    }


def run_grid_search(config: Dict[str, Any], grid_params: Dict[str, list]):
    """运行网格搜索实验"""
    import itertools
    
    # 生成参数组合
    param_names = list(grid_params.keys())
    param_values = list(grid_params.values())
    combinations = list(itertools.product(*param_values))
    
    print(f"Total experiments: {len(combinations)}")
    
    results = []
    for i, combo in enumerate(combinations):
        print(f"\n{'='*50}")
        print(f"Experiment {i+1}/{len(combinations)}")
        
        # 创建参数覆盖
        overrides = dict(zip(param_names, combo))
        print(f"Parameters: {overrides}")
        
        # 加载配置并应用覆盖
        exp_config = load_config(config.get('_config_path', 'configs/default.yaml'), overrides)
        
        # 运行训练
        seed = overrides.get('seed', 42)
        result = train_single(exp_config, seed)
        results.append(result)
    
    return results


def main():
    parser = argparse.ArgumentParser(description='G2CF-PINN Training')
    parser.add_argument('--config', type=str, required=True, help='Config file path')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--method', type=str, default='g2cf_pinn', help='Method name')
    parser.add_argument('--grid', action='store_true', help='Run grid search')
    parser.add_argument('--output', type=str, default='./results', help='Output directory')
    args = parser.parse_args()
    
    # 加载配置
    config = load_config(args.config)
    config['_config_path'] = args.config
    
    # 创建输出目录
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.grid:
        # 运行网格搜索
        grid_params = config.get('grid', {})
        results = run_grid_search(config, grid_params)
        
        # 保存结果
        import json
        with open(output_dir / 'grid_search_results.json', 'w') as f:
            json.dump(results, f, indent=2)
    else:
        # 运行单次训练
        result = train_single(config, args.seed, args.method)
        
        # 保存结果
        import json
        with open(output_dir / f'result_seed{args.seed}.json', 'w') as f:
            json.dump(result, f, indent=2)


if __name__ == '__main__':
    main()

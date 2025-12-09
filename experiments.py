"""
经济学实验示例
Economics Experiments Examples

展示如何使用系统进行不同的经济学实验
"""

import numpy as np
import config
from agents import Consumer, Producer
from market import Market
from utils.economics import create_agents
from utils.visualization import EconomicsVisualizer


def experiment_1_basic_equilibrium():
    """
    实验1: 基本的供需均衡
    
    展示市场如何通过价格机制达到均衡
    """
    print("\n" + "="*70)
    print("实验1: 基本的供需均衡")
    print("="*70)
    
    # 创建简化的市场 (较少主体，便于观察)
    consumer_params = {
        'income_mean': 1000,
        'income_std': 200,
        'income_min': 500,
        'alpha_mean': 100,
        'alpha_std': 10,
        'beta_mean': 0.5,
        'beta_std': 0.05
    }
    
    producer_params = {
        'fixed_cost_mean': 300,
        'fixed_cost_std': 50,
        'mc_a_mean': 10,
        'mc_a_std': 2,
        'mc_b_mean': 0.3,
        'mc_b_std': 0.05,
        'max_capacity_mean': 100,
        'max_capacity_std': 20
    }
    
    consumers, producers = create_agents(1000, 200, consumer_params, producer_params, 42)
    market = Market(consumers, producers, initial_price=50, price_adjustment_speed=0.1)
    
    # 运行50轮
    for i in range(50):
        market.run_round()
        if (i + 1) % 10 == 0:
            print(f"轮次 {i+1}: 价格 = {market.current_price:.2f}, "
                  f"需求 = {market.total_demand:.2f}, "
                  f"供给 = {market.total_supply:.2f}")
    
    print(f"\n最终均衡: 价格 = {market.current_price:.2f}, "
          f"交易量 = {market.quantity_history[-1]:.2f}")
    
    return market, consumers, producers


def experiment_2_demand_shift():
    """
    实验2: 需求曲线移动
    
    模拟收入增加导致的需求增加
    """
    print("\n" + "="*70)
    print("实验2: 需求曲线移动 - 收入增加的影响")
    print("="*70)
    
    consumer_params = {
        'income_mean': 800,  # 初始较低收入
        'income_std': 150,
        'income_min': 400,
        'alpha_mean': 100,
        'alpha_std': 10,
        'beta_mean': 0.5,
        'beta_std': 0.05
    }
    
    producer_params = {
        'fixed_cost_mean': 300,
        'fixed_cost_std': 50,
        'mc_a_mean': 10,
        'mc_a_std': 2,
        'mc_b_mean': 0.3,
        'mc_b_std': 0.05,
        'max_capacity_mean': 100,
        'max_capacity_std': 20
    }
    
    consumers, producers = create_agents(1000, 200, consumer_params, producer_params, 42)
    market = Market(consumers, producers, initial_price=50, price_adjustment_speed=0.1)
    
    # 第一阶段: 达到初始均衡
    print("\n阶段1: 初始均衡")
    for i in range(30):
        market.run_round()
    
    initial_price = market.current_price
    initial_quantity = market.quantity_history[-1]
    print(f"初始均衡: 价格 = {initial_price:.2f}, 数量 = {initial_quantity:.2f}")
    
    # 第二阶段: 收入增加 (模拟经济增长)
    print("\n阶段2: 收入增加50%")
    for consumer in consumers:
        consumer.income *= 1.5  # 收入增加50%
    
    # 重新达到均衡
    for i in range(30):
        market.run_round()
    
    new_price = market.current_price
    new_quantity = market.quantity_history[-1]
    print(f"新均衡: 价格 = {new_price:.2f}, 数量 = {new_quantity:.2f}")
    
    print(f"\n结果分析:")
    print(f"价格变化: {initial_price:.2f} → {new_price:.2f} ({(new_price/initial_price-1)*100:+.1f}%)")
    print(f"数量变化: {initial_quantity:.2f} → {new_quantity:.2f} ({(new_quantity/initial_quantity-1)*100:+.1f}%)")
    print(f"\n结论: 需求增加导致价格和数量同时上升 (需求曲线右移)")
    
    return market, consumers, producers


def experiment_3_supply_shift():
    """
    实验3: 供给曲线移动
    
    模拟技术进步降低生产成本
    """
    print("\n" + "="*70)
    print("实验3: 供给曲线移动 - 技术进步降低成本")
    print("="*70)
    
    consumer_params = {
        'income_mean': 1000,
        'income_std': 200,
        'income_min': 500,
        'alpha_mean': 100,
        'alpha_std': 10,
        'beta_mean': 0.5,
        'beta_std': 0.05
    }
    
    producer_params = {
        'fixed_cost_mean': 300,
        'fixed_cost_std': 50,
        'mc_a_mean': 15,  # 初始较高成本
        'mc_a_std': 2,
        'mc_b_mean': 0.4,
        'mc_b_std': 0.05,
        'max_capacity_mean': 100,
        'max_capacity_std': 20
    }
    
    consumers, producers = create_agents(1000, 200, consumer_params, producer_params, 42)
    market = Market(consumers, producers, initial_price=60, price_adjustment_speed=0.1)
    
    # 第一阶段: 初始均衡
    print("\n阶段1: 初始均衡 (技术进步前)")
    for i in range(30):
        market.run_round()
    
    initial_price = market.current_price
    initial_quantity = market.quantity_history[-1]
    print(f"初始均衡: 价格 = {initial_price:.2f}, 数量 = {initial_quantity:.2f}")
    
    # 第二阶段: 技术进步 - 降低边际成本
    print("\n阶段2: 技术进步 - 边际成本降低30%")
    for producer in producers:
        producer.mc_a *= 0.7  # 边际成本降低30%
        producer.mc_b *= 0.7
    
    # 重新达到均衡
    for i in range(30):
        market.run_round()
    
    new_price = market.current_price
    new_quantity = market.quantity_history[-1]
    print(f"新均衡: 价格 = {new_price:.2f}, 数量 = {new_quantity:.2f}")
    
    print(f"\n结果分析:")
    print(f"价格变化: {initial_price:.2f} → {new_price:.2f} ({(new_price/initial_price-1)*100:+.1f}%)")
    print(f"数量变化: {initial_quantity:.2f} → {new_quantity:.2f} ({(new_quantity/initial_quantity-1)*100:+.1f}%)")
    print(f"\n结论: 供给增加导致价格下降、数量上升 (供给曲线右移)")
    
    return market, consumers, producers


def experiment_4_price_elasticity():
    """
    实验4: 价格弹性比较
    
    比较必需品 (非弹性) 和奢侈品 (弹性) 的需求
    """
    print("\n" + "="*70)
    print("实验4: 价格弹性比较 - 必需品 vs 奢侈品")
    print("="*70)
    
    producer_params = {
        'fixed_cost_mean': 300,
        'fixed_cost_std': 50,
        'mc_a_mean': 10,
        'mc_a_std': 2,
        'mc_b_mean': 0.3,
        'mc_b_std': 0.05,
        'max_capacity_mean': 100,
        'max_capacity_std': 20
    }
    
    # 必需品: beta较小 (边际效用递减慢)
    print("\n场景A: 必需品 (如食物) - 需求非弹性")
    consumer_params_necessity = {
        'income_mean': 1000,
        'income_std': 200,
        'income_min': 500,
        'alpha_mean': 150,  # 高基本效用
        'alpha_std': 15,
        'beta_mean': 0.2,   # 低边际效用递减
        'beta_std': 0.02
    }
    
    consumers_n, producers_n = create_agents(1000, 200, consumer_params_necessity, producer_params, 42)
    
    # 测试不同价格下的需求
    prices_test = [30, 40, 50, 60, 70]
    demands_necessity = []
    
    for p in prices_test:
        total_demand = sum(c.calculate_demand(p) for c in consumers_n)
        demands_necessity.append(total_demand)
    
    print("价格 -> 需求量:")
    for p, d in zip(prices_test, demands_necessity):
        print(f"  {p:.0f} -> {d:.2f}")
    
    # 奢侈品: beta较大 (边际效用递减快)
    print("\n场景B: 奢侈品 (如珠宝) - 需求弹性")
    consumer_params_luxury = {
        'income_mean': 1000,
        'income_std': 200,
        'income_min': 500,
        'alpha_mean': 80,   # 较低基本效用
        'alpha_std': 10,
        'beta_mean': 1.0,   # 高边际效用递减
        'beta_std': 0.1
    }
    
    consumers_l, producers_l = create_agents(1000, 200, consumer_params_luxury, producer_params, 42)
    
    demands_luxury = []
    for p in prices_test:
        total_demand = sum(c.calculate_demand(p) for c in consumers_l)
        demands_luxury.append(total_demand)
    
    print("价格 -> 需求量:")
    for p, d in zip(prices_test, demands_luxury):
        print(f"  {p:.0f} -> {d:.2f}")
    
    # 计算弹性
    print("\n结果分析:")
    necessity_change = (demands_necessity[-1] - demands_necessity[0]) / demands_necessity[0]
    luxury_change = (demands_luxury[-1] - demands_luxury[0]) / demands_luxury[0]
    price_change = (prices_test[-1] - prices_test[0]) / prices_test[0]
    
    elasticity_n = necessity_change / price_change
    elasticity_l = luxury_change / price_change
    
    print(f"必需品弹性: {elasticity_n:.2f} (非弹性)")
    print(f"奢侈品弹性: {elasticity_l:.2f} (弹性)")
    print(f"\n结论: 必需品对价格变化不敏感，奢侈品对价格变化敏感")


def experiment_5_market_intervention():
    """
    实验5: 政府干预
    
    模拟价格上限 (如租金管制) 的影响
    """
    print("\n" + "="*70)
    print("实验5: 政府干预 - 价格上限的影响")
    print("="*70)
    
    consumer_params = {
        'income_mean': 1000,
        'income_std': 200,
        'income_min': 500,
        'alpha_mean': 100,
        'alpha_std': 10,
        'beta_mean': 0.5,
        'beta_std': 0.05
    }
    
    producer_params = {
        'fixed_cost_mean': 300,
        'fixed_cost_std': 50,
        'mc_a_mean': 10,
        'mc_a_std': 2,
        'mc_b_mean': 0.3,
        'mc_b_std': 0.05,
        'max_capacity_mean': 100,
        'max_capacity_std': 20
    }
    
    consumers, producers = create_agents(1000, 200, consumer_params, producer_params, 42)
    market = Market(consumers, producers, initial_price=50, price_adjustment_speed=0.1)
    
    # 自由市场均衡
    print("\n场景A: 自由市场")
    for i in range(40):
        market.run_round()
    
    free_market_price = market.current_price
    free_market_quantity = market.quantity_history[-1]
    free_market_demand = market.total_demand
    free_market_supply = market.total_supply
    
    print(f"自由市场均衡:")
    print(f"  价格: {free_market_price:.2f}")
    print(f"  交易量: {free_market_quantity:.2f}")
    print(f"  需求: {free_market_demand:.2f}")
    print(f"  供给: {free_market_supply:.2f}")
    
    # 价格上限
    print("\n场景B: 实施价格上限 (低于均衡价格)")
    price_ceiling = free_market_price * 0.8
    print(f"价格上限设定为: {price_ceiling:.2f}")
    
    # 在价格上限下的供需
    demand_at_ceiling = sum(c.calculate_demand(price_ceiling) for c in consumers)
    supply_at_ceiling = sum(p.calculate_supply(price_ceiling) for p in producers)
    
    print(f"\n价格上限下:")
    print(f"  需求量: {demand_at_ceiling:.2f}")
    print(f"  供给量: {supply_at_ceiling:.2f}")
    print(f"  短缺: {demand_at_ceiling - supply_at_ceiling:.2f}")
    
    print(f"\n结果分析:")
    print(f"价格上限导致:")
    print(f"  1. 供给减少: {free_market_supply:.2f} → {supply_at_ceiling:.2f} ({(supply_at_ceiling/free_market_supply-1)*100:.1f}%)")
    print(f"  2. 需求增加: {free_market_demand:.2f} → {demand_at_ceiling:.2f} ({(demand_at_ceiling/free_market_demand-1)*100:.1f}%)")
    print(f"  3. 出现短缺: {demand_at_ceiling - supply_at_ceiling:.2f}")
    print(f"\n结论: 价格上限虽然降低价格，但造成供给短缺和市场效率损失")


def run_all_experiments():
    """运行所有实验"""
    print("\n" + "="*70)
    print("           曼昆经济学原理 - 经济学实验系列")
    print("="*70)
    
    # 实验1: 基本均衡
    experiment_1_basic_equilibrium()
    
    # 实验2: 需求移动
    experiment_2_demand_shift()
    
    # 实验3: 供给移动
    experiment_3_supply_shift()
    
    # 实验4: 价格弹性
    experiment_4_price_elasticity()
    
    # 实验5: 政府干预
    experiment_5_market_intervention()
    
    print("\n" + "="*70)
    print("所有实验完成!")
    print("="*70 + "\n")


if __name__ == "__main__":
    run_all_experiments()

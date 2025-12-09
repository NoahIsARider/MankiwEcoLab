"""
经济学工具函数
Economics Utility Functions
"""

import numpy as np
from typing import List, Tuple
from agents import Consumer, Producer


def create_agents(num_consumers: int, num_producers: int, 
                 consumer_params: dict, producer_params: dict,
                 random_seed: int = None) -> Tuple[List[Consumer], List[Producer]]:
    """
    批量创建经济主体
    
    Args:
        num_consumers: 消费者数量
        num_producers: 生产者数量
        consumer_params: 消费者参数字典
        producer_params: 生产者参数字典
        random_seed: 随机种子
    
    Returns:
        (消费者列表, 生产者列表)
    """
    if random_seed is not None:
        np.random.seed(random_seed)
    
    # 创建消费者
    consumers = []
    for i in range(num_consumers):
        # 从正态分布中采样参数
        income = max(
            consumer_params['income_min'],
            np.random.normal(consumer_params['income_mean'], consumer_params['income_std'])
        )
        alpha = max(
            0.1,
            np.random.normal(consumer_params['alpha_mean'], consumer_params['alpha_std'])
        )
        beta = max(
            0.01,
            np.random.normal(consumer_params['beta_mean'], consumer_params['beta_std'])
        )
        
        consumer = Consumer(
            consumer_id=i,
            income=income,
            alpha=alpha,
            beta=beta
        )
        consumers.append(consumer)
    
    # 创建生产者
    producers = []
    for i in range(num_producers):
        # 从正态分布中采样参数
        fixed_cost = max(
            0,
            np.random.normal(producer_params['fixed_cost_mean'], producer_params['fixed_cost_std'])
        )
        mc_a = max(
            0.1,
            np.random.normal(producer_params['mc_a_mean'], producer_params['mc_a_std'])
        )
        mc_b = max(
            0.01,
            np.random.normal(producer_params['mc_b_mean'], producer_params['mc_b_std'])
        )
        max_capacity = max(
            1,
            np.random.normal(producer_params['max_capacity_mean'], producer_params['max_capacity_std'])
        )
        
        producer = Producer(
            producer_id=i,
            fixed_cost=fixed_cost,
            mc_a=mc_a,
            mc_b=mc_b,
            max_capacity=max_capacity
        )
        producers.append(producer)
    
    return consumers, producers


def calculate_gini_coefficient(values: List[float]) -> float:
    """
    计算基尼系数 (Gini Coefficient)
    
    衡量收入或财富分配的不平等程度
    0 = 完全平等, 1 = 完全不平等
    """
    values = np.array(sorted(values))
    n = len(values)
    
    if n == 0 or values.sum() == 0:
        return 0
    
    index = np.arange(1, n + 1)
    gini = (2 * np.sum(index * values)) / (n * values.sum()) - (n + 1) / n
    
    return gini


def calculate_lorenz_curve(values: List[float]) -> Tuple[np.ndarray, np.ndarray]:
    """
    计算洛伦兹曲线 (Lorenz Curve)
    
    用于可视化收入分配
    
    Returns:
        (累积人口比例, 累积收入比例)
    """
    values = np.array(sorted(values))
    n = len(values)
    
    if n == 0 or values.sum() == 0:
        return np.array([0, 1]), np.array([0, 1])
    
    # 累积比例
    cumsum = np.cumsum(values)
    cumsum = cumsum / cumsum[-1]  # 归一化
    
    # 人口比例
    population = np.arange(1, n + 1) / n
    
    # 添加原点
    population = np.insert(population, 0, 0)
    cumsum = np.insert(cumsum, 0, 0)
    
    return population, cumsum


def calculate_theil_index(values: List[float]) -> float:
    """
    计算泰尔指数 (Theil Index)
    
    另一种衡量不平等的指标
    """
    values = np.array(values)
    if len(values) == 0 or values.sum() == 0:
        return 0
    
    mean_value = values.mean()
    theil = np.mean(values / mean_value * np.log(values / mean_value + 1e-10))
    
    return theil


def calculate_market_concentration(quantities: List[float]) -> dict:
    """
    计算市场集中度指标
    
    Returns:
        包含CR4, CR8, HHI等指标的字典
    """
    quantities = np.array(sorted(quantities, reverse=True))
    total = quantities.sum()
    
    if total == 0:
        return {
            'CR4': 0,
            'CR8': 0,
            'HHI': 0
        }
    
    # 市场份额
    shares = quantities / total
    
    # CR4: 前4家企业的市场份额之和
    cr4 = shares[:4].sum() if len(shares) >= 4 else shares.sum()
    
    # CR8: 前8家企业的市场份额之和
    cr8 = shares[:8].sum() if len(shares) >= 8 else shares.sum()
    
    # HHI: 赫芬达尔-赫希曼指数
    hhi = np.sum(shares ** 2) * 10000
    
    return {
        'CR4': cr4,
        'CR8': cr8,
        'HHI': hhi
    }


def analyze_welfare_distribution(consumers: List[Consumer], producers: List[Producer]) -> dict:
    """
    分析福利分配
    
    Returns:
        包含各种福利指标的字典
    """
    # 消费者福利
    consumer_surpluses = [c.consumer_surplus for c in consumers]
    consumer_utilities = [c.utility for c in consumers]
    consumer_expenditures = [c.expenditure for c in consumers]
    
    # 生产者福利
    producer_surpluses = [p.producer_surplus for p in producers]
    producer_profits = [p.profit for p in producers]
    producer_revenues = [p.revenue for p in producers]
    
    # 总福利
    total_consumer_surplus = sum(consumer_surpluses)
    total_producer_surplus = sum(producer_surpluses)
    total_surplus = total_consumer_surplus + total_producer_surplus
    
    # 不平等指标
    consumer_gini = calculate_gini_coefficient(consumer_surpluses)
    producer_gini = calculate_gini_coefficient(producer_surpluses)
    
    return {
        'total_consumer_surplus': total_consumer_surplus,
        'total_producer_surplus': total_producer_surplus,
        'total_surplus': total_surplus,
        'avg_consumer_surplus': np.mean(consumer_surpluses),
        'avg_producer_surplus': np.mean(producer_surpluses),
        'avg_consumer_utility': np.mean(consumer_utilities),
        'avg_producer_profit': np.mean(producer_profits),
        'consumer_gini': consumer_gini,
        'producer_gini': producer_gini,
        'total_expenditure': sum(consumer_expenditures),
        'total_revenue': sum(producer_revenues)
    }


def calculate_price_elasticity_of_demand(prices: List[float], quantities: List[float]) -> float:
    """
    根据价格-数量数据计算需求价格弹性
    
    使用中点法: ε = (ΔQ/Q_avg) / (ΔP/P_avg)
    """
    if len(prices) < 2 or len(quantities) < 2:
        return 0
    
    prices = np.array(prices)
    quantities = np.array(quantities)
    
    # 计算变化率
    delta_q = np.diff(quantities)
    delta_p = np.diff(prices)
    
    # 中点
    q_avg = (quantities[:-1] + quantities[1:]) / 2
    p_avg = (prices[:-1] + prices[1:]) / 2
    
    # 避免除零
    mask = (p_avg != 0) & (q_avg != 0) & (delta_p != 0)
    
    if not np.any(mask):
        return 0
    
    # 弹性
    elasticities = (delta_q[mask] / q_avg[mask]) / (delta_p[mask] / p_avg[mask])
    
    return np.mean(elasticities)


def simulate_policy_intervention(market, intervention_type: str, **kwargs) -> dict:
    """
    模拟政策干预的影响
    
    Args:
        market: 市场对象
        intervention_type: 干预类型 ('price_ceiling', 'price_floor', 'tax', 'subsidy')
        **kwargs: 干预参数
    
    Returns:
        干预效果分析
    """
    original_price = market.current_price
    original_quantity = market.quantity_history[-1] if market.quantity_history else 0
    
    result = {
        'intervention_type': intervention_type,
        'original_price': original_price,
        'original_quantity': original_quantity
    }
    
    if intervention_type == 'price_ceiling':
        # 价格上限
        ceiling = kwargs.get('ceiling', original_price * 0.8)
        result['ceiling_price'] = ceiling
        result['binding'] = ceiling < original_price
        
        if result['binding']:
            # 短缺
            demand_at_ceiling = market.calculate_aggregate_demand(ceiling)
            supply_at_ceiling = market.calculate_aggregate_supply(ceiling)
            result['shortage'] = demand_at_ceiling - supply_at_ceiling
            result['new_quantity'] = supply_at_ceiling
    
    elif intervention_type == 'price_floor':
        # 价格下限
        floor = kwargs.get('floor', original_price * 1.2)
        result['floor_price'] = floor
        result['binding'] = floor > original_price
        
        if result['binding']:
            # 过剩
            demand_at_floor = market.calculate_aggregate_demand(floor)
            supply_at_floor = market.calculate_aggregate_supply(floor)
            result['surplus'] = supply_at_floor - demand_at_floor
            result['new_quantity'] = demand_at_floor
    
    elif intervention_type == 'tax':
        # 从量税
        tax = kwargs.get('tax', 5.0)
        result['tax_amount'] = tax
        # 税后价格会上升
        result['price_increase'] = tax  # 简化假设
        result['tax_revenue'] = tax * original_quantity
    
    elif intervention_type == 'subsidy':
        # 补贴
        subsidy = kwargs.get('subsidy', 5.0)
        result['subsidy_amount'] = subsidy
        # 补贴后价格会下降
        result['price_decrease'] = subsidy
        result['subsidy_cost'] = subsidy * original_quantity
    
    return result

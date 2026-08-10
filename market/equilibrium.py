"""
均衡计算模块 - Equilibrium Calculation
计算市场均衡和效率指标
"""

from typing import List, Tuple

import numpy as np

# 兼容 numpy 1.x (np.trapz) 与 numpy 2.x (np.trapezoid)
try:
    _trapz = np.trapezoid
except AttributeError:
    _trapz = np.trapz


def find_equilibrium(demand_func, supply_func, price_range: Tuple[float, float] = (0.1, 500)) -> Tuple[float, float]:
    """
    找到市场均衡点
    
    均衡条件: D(p*) = S(p*)
    
    Args:
        demand_func: 需求函数 D(p)
        supply_func: 供给函数 S(p)
        price_range: 价格搜索范围
    
    Returns:
        (均衡价格, 均衡数量)
    """
    # 使用网格搜索找到均衡点
    prices = np.linspace(price_range[0], price_range[1], 10000)
    demands = np.array([demand_func(p) for p in prices])
    supplies = np.array([supply_func(p) for p in prices])

    # 找到供需最接近的点
    excess_demand = np.abs(demands - supplies)
    equilibrium_idx = np.argmin(excess_demand)

    equilibrium_price = prices[equilibrium_idx]
    equilibrium_quantity = demands[equilibrium_idx]

    return equilibrium_price, equilibrium_quantity


def calculate_consumer_surplus_analytical(demand_func, equilibrium_price: float,
                                         equilibrium_quantity: float) -> float:
    """
    计算消费者剩余 (解析方法)
    
    CS = ∫[0 to Q*] D^(-1)(q) dq - P* × Q*
    
    其中 D^(-1)(q) 是反需求函数
    """
    # 使用数值积分
    quantities = np.linspace(0, equilibrium_quantity, 1000)

    # 需要反需求函数，这里使用近似
    # 通过求解 D(p) = q 得到 p = D^(-1)(q)
    inverse_demand = []
    for q in quantities:
        # 二分搜索找到对应的价格
        prices = np.linspace(0.1, 500, 1000)
        demands = np.array([demand_func(p) for p in prices])
        idx = np.argmin(np.abs(demands - q))
        inverse_demand.append(prices[idx])

    # 数值积分
    total_willingness = _trapz(inverse_demand, quantities)
    consumer_surplus = total_willingness - equilibrium_price * equilibrium_quantity

    return max(0, consumer_surplus)


def calculate_producer_surplus_analytical(supply_func, equilibrium_price: float,
                                         equilibrium_quantity: float) -> float:
    """
    计算生产者剩余 (解析方法)
    
    PS = P* × Q* - ∫[0 to Q*] S^(-1)(q) dq
    
    其中 S^(-1)(q) 是反供给函数 (边际成本)
    """
    # 使用数值积分
    quantities = np.linspace(0, equilibrium_quantity, 1000)

    # 需要反供给函数 (供给曲线即MC曲线)
    inverse_supply = []
    for q in quantities:
        prices = np.linspace(0.1, 500, 1000)
        supplies = np.array([supply_func(p) for p in prices])
        idx = np.argmin(np.abs(supplies - q))
        inverse_supply.append(prices[idx])

    # 数值积分
    total_cost = _trapz(inverse_supply, quantities)
    producer_surplus = equilibrium_price * equilibrium_quantity - total_cost

    return max(0, producer_surplus)


def calculate_deadweight_loss(demand_func, supply_func, actual_quantity: float,
                              equilibrium_quantity: float, actual_price: float) -> float:
    """
    计算无谓损失 (Deadweight Loss)
    
    当市场未达到均衡时产生的效率损失
    
    DWL = 0.5 × |Q* - Q| × |P_demand - P_supply|
    """
    if abs(actual_quantity - equilibrium_quantity) < 0.01:
        return 0

    # 在实际数量下，需求价格和供给价格
    # 通过反函数求得
    quantities = np.linspace(min(actual_quantity, equilibrium_quantity),
                            max(actual_quantity, equilibrium_quantity), 100)

    # 计算需求价格和供给价格
    demand_prices = []
    supply_prices = []

    for q in quantities:
        # 找到需求价格
        prices = np.linspace(0.1, 500, 1000)
        demands = np.array([demand_func(p) for p in prices])
        idx_d = np.argmin(np.abs(demands - q))
        demand_prices.append(prices[idx_d])

        # 找到供给价格
        supplies = np.array([supply_func(p) for p in prices])
        idx_s = np.argmin(np.abs(supplies - q))
        supply_prices.append(prices[idx_s])

    # 无谓损失是两条曲线之间的面积
    dwl = _trapz(np.array(demand_prices) - np.array(supply_prices), quantities)

    return abs(dwl)


def calculate_market_efficiency(consumer_surplus: float, producer_surplus: float,
                                deadweight_loss: float = 0) -> dict:
    """
    计算市场效率指标
    
    Returns:
        包含各种效率指标的字典
    """
    total_surplus = consumer_surplus + producer_surplus
    potential_surplus = total_surplus + deadweight_loss

    if potential_surplus > 0:
        efficiency = (total_surplus / potential_surplus) * 100
    else:
        efficiency = 0

    return {
        'consumer_surplus': consumer_surplus,
        'producer_surplus': producer_surplus,
        'total_surplus': total_surplus,
        'deadweight_loss': deadweight_loss,
        'efficiency_percentage': efficiency,
        'pareto_efficient': deadweight_loss < 0.01  # 几乎无无谓损失
    }


def calculate_elasticity(func, price: float, delta: float = 0.01) -> float:
    """
    计算价格弹性
    
    ε = (ΔQ/Q) / (ΔP/P) = (dQ/dP) × (P/Q)
    
    Args:
        func: 需求或供给函数
        price: 计算弹性的价格点
        delta: 价格变动的增量
    
    Returns:
        弹性系数
    """
    Q = func(price)
    if Q == 0 or price == 0:
        return 0

    # 数值导数
    Q_plus = func(price + delta)
    dQ_dP = (Q_plus - Q) / delta

    elasticity = (dQ_dP * price) / Q

    return elasticity


def classify_elasticity(elasticity: float) -> str:
    """
    分类弹性
    
    - |ε| > 1: 弹性 (elastic)
    - |ε| = 1: 单位弹性 (unit elastic)
    - |ε| < 1: 非弹性 (inelastic)
    """
    abs_e = abs(elasticity)

    if abs_e > 1.1:
        return "elastic"
    elif abs_e < 0.9:
        return "inelastic"
    else:
        return "unit elastic"


def analyze_market_structure(num_consumers: int, num_producers: int,
                            herfindahl_index: float = None) -> str:
    """
    分析市场结构
    
    Args:
        num_consumers: 消费者数量
        num_producers: 生产者数量
        herfindahl_index: 赫芬达尔指数 (可选)
    
    Returns:
        市场结构类型
    """
    if num_producers == 1:
        return "monopoly"
    elif num_producers <= 5:
        return "oligopoly"
    elif num_producers <= 20:
        return "monopolistic competition"
    else:
        return "perfect competition"


def calculate_herfindahl_hirschman_index(market_shares: List[float]) -> float:
    """
    计算赫芬达尔-赫希曼指数 (HHI)
    
    HHI = Σ (market_share_i)^2
    
    HHI越高，市场集中度越高
    - HHI < 1500: 竞争性市场
    - 1500 <= HHI < 2500: 中等集中
    - HHI >= 2500: 高度集中
    """
    hhi = sum(share ** 2 for share in market_shares)
    return hhi * 10000  # 转换为标准HHI (0-10000)

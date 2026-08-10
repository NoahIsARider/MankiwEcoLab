"""
市场类 - Market Class
实现市场机制和价格发现过程
"""

from typing import List

import numpy as np

from agents import Consumer, Producer


class Market:
    """
    市场类
    
    实现完全竞争市场的核心机制:
    1. 价格发现机制 (通过供需调整)
    2. 市场出清 (matching buyers and sellers)
    3. 均衡达成过程
    """

    def __init__(self, consumers: List[Consumer], producers: List[Producer],
                 initial_price: float, price_adjustment_speed: float = 0.1):
        """
        初始化市场
        
        Args:
            consumers: 消费者列表
            producers: 生产者列表
            initial_price: 初始价格
            price_adjustment_speed: 价格调整速度 (0-1)
        """
        self.consumers = consumers
        self.producers = producers
        self.current_price = initial_price
        self.price_adjustment_speed = price_adjustment_speed

        # 市场历史数据
        self.price_history = [initial_price]
        self.quantity_history = []
        self.total_demand_history = []
        self.total_supply_history = []
        self.consumer_surplus_history = []
        self.producer_surplus_history = []
        self.total_surplus_history = []

        # 当前市场状态
        self.total_demand = 0
        self.total_supply = 0
        self.equilibrium_reached = False
        self.transactions = []

    def calculate_aggregate_demand(self, price: float) -> float:
        """
        计算总需求: 所有消费者的需求量之和
        
        D(p) = Σ D_i(p)
        """
        total_demand = sum(consumer.calculate_demand(price) for consumer in self.consumers)
        return total_demand

    def calculate_aggregate_supply(self, price: float) -> float:
        """
        计算总供给: 所有生产者的供给量之和
        
        S(p) = Σ S_i(p)
        """
        total_supply = sum(producer.calculate_supply(price) for producer in self.producers)
        return total_supply

    def update_price(self):
        """
        根据供需关系更新价格
        
        价格调整规则 (tâtonnement process - 瓦尔拉斯均衡过程):
        - 如果需求 > 供给 => 价格上升
        - 如果供给 > 需求 => 价格下降
        
        调整幅度与供需缺口成正比
        """
        # 计算当前价格下的供需
        self.total_demand = self.calculate_aggregate_demand(self.current_price)
        self.total_supply = self.calculate_aggregate_supply(self.current_price)

        # 供需缺口
        excess_demand = self.total_demand - self.total_supply

        # 价格调整
        # Δp = α * (D - S) / (D + S) * p
        # 标准化的调整，避免价格变动过大
        if self.total_demand + self.total_supply > 0:
            price_change_rate = excess_demand / (self.total_demand + self.total_supply)
            price_change = self.price_adjustment_speed * price_change_rate * self.current_price

            # 更新价格
            new_price = self.current_price + price_change

            # 确保价格在合理范围内
            self.current_price = max(0.1, new_price)  # 价格不能为负或过小

        # 记录价格历史
        self.price_history.append(self.current_price)
        self.total_demand_history.append(self.total_demand)
        self.total_supply_history.append(self.total_supply)

    def clear_market(self):
        """
        市场出清: 撮合交易
        
        在当前价格下，按照以下规则进行交易:
        1. 实际交易量 = min(总需求, 总供给)
        2. 随机匹配消费者和生产者
        3. 执行交易
        """
        # 实际交易量
        quantity_traded = min(self.total_demand, self.total_supply)

        if quantity_traded <= 0:
            self.quantity_history.append(0)
            return

        # 为简化模拟，假设交易按比例分配
        # 实际中可以使用更复杂的匹配算法

        # 按需求比例分配给消费者
        if self.total_demand > 0:
            for consumer in self.consumers:
                consumer_share = consumer.quantity_demanded / self.total_demand
                allocated_quantity = consumer_share * quantity_traded
                consumer.consume(allocated_quantity, self.current_price)

        # 按供给比例分配给生产者
        if self.total_supply > 0:
            for producer in self.producers:
                producer_share = producer.quantity_supplied / self.total_supply
                allocated_quantity = producer_share * quantity_traded
                producer.produce(allocated_quantity, self.current_price)

        # 记录交易量
        self.quantity_history.append(quantity_traded)

        # 计算市场剩余
        total_consumer_surplus = sum(c.consumer_surplus for c in self.consumers)
        total_producer_surplus = sum(p.producer_surplus for p in self.producers)
        total_surplus = total_consumer_surplus + total_producer_surplus

        self.consumer_surplus_history.append(total_consumer_surplus)
        self.producer_surplus_history.append(total_producer_surplus)
        self.total_surplus_history.append(total_surplus)

    def check_equilibrium(self, threshold: float = 0.01) -> bool:
        """
        检查是否达到均衡
        
        均衡条件:
        1. 价格稳定 (价格变化小于阈值)
        2. 供需平衡 (|供给-需求| / (供给+需求) < 阈值)
        """
        # 检查价格是否稳定
        if len(self.price_history) < 5:
            return False

        recent_prices = self.price_history[-5:]
        price_variance = np.std(recent_prices) / np.mean(recent_prices)

        # 检查供需是否平衡
        if self.total_demand + self.total_supply > 0:
            supply_demand_gap = abs(self.total_supply - self.total_demand) / (self.total_supply + self.total_demand)
        else:
            supply_demand_gap = 1.0

        # 均衡条件
        price_stable = price_variance < threshold
        market_clear = supply_demand_gap < threshold

        self.equilibrium_reached = price_stable and market_clear
        return self.equilibrium_reached

    def run_round(self):
        """
        运行一轮市场交易
        
        步骤:
        1. 更新价格
        2. 市场出清
        3. 检查均衡
        """
        self.update_price()
        self.clear_market()
        return self.check_equilibrium()

    def get_demand_curve(self, price_range: np.ndarray) -> np.ndarray:
        """
        获取总需求曲线
        """
        return np.array([self.calculate_aggregate_demand(p) for p in price_range])

    def get_supply_curve(self, price_range: np.ndarray) -> np.ndarray:
        """
        获取总供给曲线
        """
        return np.array([self.calculate_aggregate_supply(p) for p in price_range])

    def get_market_stats(self):
        """
        获取市场统计信息
        """
        return {
            'current_price': self.current_price,
            'equilibrium_price': self.price_history[-1],
            'equilibrium_quantity': self.quantity_history[-1] if self.quantity_history else 0,
            'total_demand': self.total_demand,
            'total_supply': self.total_supply,
            'consumer_surplus': self.consumer_surplus_history[-1] if self.consumer_surplus_history else 0,
            'producer_surplus': self.producer_surplus_history[-1] if self.producer_surplus_history else 0,
            'total_surplus': self.total_surplus_history[-1] if self.total_surplus_history else 0,
            'equilibrium_reached': self.equilibrium_reached,
            'num_rounds': len(self.price_history) - 1
        }

    def __repr__(self):
        return (f"Market(consumers={len(self.consumers)}, producers={len(self.producers)}, "
                f"price={self.current_price:.2f}, equilibrium={self.equilibrium_reached})")

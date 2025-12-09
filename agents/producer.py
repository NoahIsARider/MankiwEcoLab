"""
生产者类 - Producer Class
基于曼昆经济学原理中的生产者理论
"""

import numpy as np


class Producer:
    """
    生产者类
    
    生产者具有成本函数和产能约束，基于利润最大化做出生产决策。
    
    总成本函数: TC(q) = FC + a * q + 0.5 * b * q^2
    - FC: 固定成本
    - a: 边际成本常数项
    - b: 边际成本斜率 (衡量规模报酬递减)
    
    边际成本: MC(q) = a + b * q
    """
    
    def __init__(self, producer_id, fixed_cost, mc_a, mc_b, max_capacity):
        """
        初始化生产者
        
        Args:
            producer_id: 生产者ID
            fixed_cost: 固定成本
            mc_a: 边际成本函数的常数项
            mc_b: 边际成本函数的斜率
            max_capacity: 最大产能
        """
        self.id = producer_id
        self.fixed_cost = max(fixed_cost, 0)
        self.mc_a = max(mc_a, 0)  # 边际成本不能为负
        self.mc_b = max(mc_b, 0)  # 边际成本斜率不能为负
        self.max_capacity = max(max_capacity, 1)
        
        # 生产状态
        self.quantity_supplied = 0  # 供给量
        self.quantity_produced = 0  # 实际生产量
        self.revenue = 0  # 收入
        self.cost = 0  # 总成本
        self.profit = 0  # 利润
        self.producer_surplus = 0  # 生产者剩余
    
    def total_cost(self, quantity):
        """
        总成本函数
        
        TC(q) = FC + a * q + 0.5 * b * q^2
        
        体现了:
        1. 固定成本 (与产量无关)
        2. 可变成本 (与产量相关)
        3. 规模报酬递减 (通过q^2项)
        """
        if quantity < 0:
            return np.inf
        if quantity > self.max_capacity:
            return np.inf  # 超出产能，成本无穷大
        
        return self.fixed_cost + self.mc_a * quantity + 0.5 * self.mc_b * quantity ** 2
    
    def marginal_cost(self, quantity):
        """
        边际成本: 多生产一单位的成本增量
        
        MC(q) = dTC/dq = a + b * q
        
        体现边际成本递增 (当b > 0时)
        """
        if quantity < 0 or quantity > self.max_capacity:
            return np.inf
        return self.mc_a + self.mc_b * quantity
    
    def average_cost(self, quantity):
        """
        平均成本
        
        AC(q) = TC(q) / q
        """
        if quantity <= 0:
            return np.inf
        return self.total_cost(quantity) / quantity
    
    def calculate_supply(self, price):
        """
        计算供给量: 基于利润最大化原则
        
        生产者最大化利润:
        max π(q) = p * q - TC(q)
        
        最优条件: dπ/dq = 0
        => p = MC(q)
        => p = a + b * q
        => q* = (p - a) / b
        
        在完全竞争市场中，价格等于边际成本
        """
        if price <= 0:
            return 0
        
        # 从MC(q) = p 求解q
        # p = a + b * q
        # q = (p - a) / b
        
        if self.mc_b > 0:
            optimal_quantity = (price - self.mc_a) / self.mc_b
        else:
            # 如果边际成本是常数
            if price >= self.mc_a:
                optimal_quantity = self.max_capacity
            else:
                optimal_quantity = 0
        
        # 确保不超过产能约束，且不为负
        optimal_quantity = max(0, min(optimal_quantity, self.max_capacity))
        
        # 检查是否覆盖固定成本（关闭决策）
        # 只有当价格至少覆盖平均可变成本时才生产
        if optimal_quantity > 0:
            avc = (self.mc_a * optimal_quantity + 0.5 * self.mc_b * optimal_quantity ** 2) / optimal_quantity
            if price < avc:
                optimal_quantity = 0
        
        self.quantity_supplied = optimal_quantity
        return optimal_quantity
    
    def calculate_minimum_price(self):
        """
        计算最低接受价格: 覆盖平均可变成本的最低价格
        """
        # 在完全竞争中，短期供给曲线是MC曲线在AVC以上的部分
        return self.mc_a
    
    def produce(self, quantity, price):
        """
        实际生产
        
        Args:
            quantity: 实际生产的数量
            price: 市场价格
        """
        self.quantity_produced = quantity
        self.revenue = price * quantity
        self.cost = self.total_cost(quantity)
        self.profit = self.revenue - self.cost
        
        # 计算生产者剩余 (producer surplus)
        # PS = 总收入 - 总可变成本
        # 或者: PS = 积分 (price - MC(q)) from 0 to quantity
        if quantity > 0:
            quantities = np.linspace(0, quantity, 100)
            mc_curve = np.array([self.marginal_cost(q) for q in quantities])
            total_variable_cost = np.trapz(mc_curve, quantities)  # 数值积分MC曲线
            self.producer_surplus = self.revenue - total_variable_cost
        else:
            self.producer_surplus = 0
    
    def get_supply_curve_point(self, price):
        """
        获取供给曲线上的一个点 (price, quantity)
        """
        return (price, self.calculate_supply(price))
    
    def __repr__(self):
        return (f"Producer(id={self.id}, FC={self.fixed_cost:.2f}, "
                f"MC=({self.mc_a:.2f} + {self.mc_b:.4f}*q), "
                f"capacity={self.max_capacity:.2f})")

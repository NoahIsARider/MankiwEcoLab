"""
消费者类 - Consumer Class
基于曼昆经济学原理中的消费者理论
"""

import numpy as np

# 兼容 numpy 1.x (np.trapz) 与 numpy 2.x (np.trapezoid)
try:
    _trapz = np.trapezoid
except AttributeError:
    _trapz = np.trapz


class Consumer:
    """
    消费者类
    
    消费者具有效用函数和预算约束，基于效用最大化做出消费决策。
    
    效用函数: U(q) = alpha * ln(q + 1) - beta * q^2
    - alpha: 衡量商品的基本效用价值
    - beta: 衡量边际效用递减的速度
    
    预算约束: p * q <= income
    """

    def __init__(self, consumer_id, income, alpha, beta):
        """
        初始化消费者
        
        Args:
            consumer_id: 消费者ID
            income: 收入
            alpha: 效用函数参数alpha (基本效用)
            beta: 效用函数参数beta (边际效用递减率)
        """
        self.id = consumer_id
        self.income = max(income, 0)  # 收入不能为负
        self.alpha = max(alpha, 0.1)  # alpha必须为正
        self.beta = max(beta, 0.01)  # beta必须为正

        # 消费状态
        self.quantity_demanded = 0  # 需求量
        self.quantity_consumed = 0  # 实际消费量
        self.utility = 0  # 实际获得的效用
        self.consumer_surplus = 0  # 消费者剩余
        self.expenditure = 0  # 支出

    def utility_function(self, quantity):
        """
        效用函数: 计算消费quantity单位商品的总效用
        
        U(q) = alpha * ln(q + 1) - beta * q^2
        
        这个函数体现了:
        1. 边际效用递减原理 (通过ln和-q^2项)
        2. 正效用 (在合理范围内)
        """
        if quantity < 0:
            return -np.inf
        return self.alpha * np.log(quantity + 1) - self.beta * quantity ** 2

    def marginal_utility(self, quantity):
        """
        边际效用: 计算在quantity水平下，多消费一单位的效用增量
        
        MU(q) = dU/dq = alpha / (q + 1) - 2 * beta * q
        """
        if quantity < 0:
            return 0
        return self.alpha / (quantity + 1) - 2 * self.beta * quantity

    def calculate_demand(self, price):
        """
        计算需求量: 基于效用最大化原则
        
        消费者在预算约束下最大化效用:
        max U(q) s.t. p * q <= income
        
        最优条件: MU(q) / p = λ (拉格朗日乘数)
        简化为: MU(q) = p (在边际上，效用等于价格)
        
        求解: alpha / (q + 1) - 2 * beta * q = p
        
        这是关于 q 的一元二次方程:
        2*beta*q^2 + (p + 2*beta)*q + (p - alpha) = 0
        
        解析求解后再应用预算约束，得到最优需求量。
        """
        if price <= 0:
            return 0

        # 解析求解 MU(q) = p 的二次方程
        # 2*beta*q^2 + (p + 2*beta)*q + (p - alpha) = 0
        a = 2 * self.beta
        b = price + 2 * self.beta
        c = price - self.alpha

        discriminant = b ** 2 - 4 * a * c

        if discriminant <= 0:
            # 无实数解 => 边际效用始终低于价格，不消费
            optimal_quantity = 0.0
        else:
            # 取正的根
            optimal_quantity = (-b + np.sqrt(discriminant)) / (2 * a)
            optimal_quantity = max(optimal_quantity, 0.0)

        # 应用预算约束: p * q <= income
        max_affordable = self.income / price
        optimal_quantity = min(optimal_quantity, max_affordable)

        self.quantity_demanded = optimal_quantity
        return optimal_quantity

    def calculate_willingness_to_pay(self, quantity):
        """
        计算支付意愿: 消费者愿意为quantity单位商品支付的最高价格
        
        WTP = MU(q) (边际效用即为支付意愿)
        """
        return self.marginal_utility(quantity)

    def consume(self, quantity, price):
        """
        实际消费
        
        Args:
            quantity: 实际购买的数量
            price: 实际支付的价格
        """
        self.quantity_consumed = quantity
        self.expenditure = price * quantity
        self.utility = self.utility_function(quantity)

        # 计算消费者剩余 (consumer surplus)
        # CS = 总支付意愿 - 实际支出
        # 近似计算: 积分 WTP(q) from 0 to quantity
        if quantity > 0:
            quantities = np.linspace(0, quantity, 100)
            wtp_curve = np.array([self.calculate_willingness_to_pay(q) for q in quantities])
            total_wtp = _trapz(wtp_curve, quantities)  # 数值积分
            self.consumer_surplus = total_wtp - self.expenditure
        else:
            self.consumer_surplus = 0

    def get_demand_curve_point(self, price):
        """
        获取需求曲线上的一个点 (price, quantity)
        """
        return (price, self.calculate_demand(price))

    def __repr__(self):
        return (f"Consumer(id={self.id}, income={self.income:.2f}, "
                f"alpha={self.alpha:.2f}, beta={self.beta:.4f})")

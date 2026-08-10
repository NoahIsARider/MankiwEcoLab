"""
索洛经济增长模型
Solow Growth Model

对应曼昆《经济学原理》宏观分册:
- 第25章 生产与增长 (Production and Growth)
- 第26章 储蓄、投资与金融体系
- 原理8: 一国的生活水平取决于它生产物品与服务的能力

核心概念:
- 生产函数: Y = F(K, L) = K^α * L^(1-α) (柯布-道格拉斯)
- 人均产出: y = f(k) = k^α
- 资本积累方程: Δk = s*f(k) - (δ + n)*k
- 稳态 (steady state): Δk = 0 => s*f(k*) = (δ+n)*k*
- 黄金律水平 (Golden Rule): 使人均消费最大的稳态资本存量
"""

from dataclasses import dataclass

import numpy as np


@dataclass
class SolowGrowthModel:
    """
    索洛增长模型 (人均形式)

    Attributes:
        alpha: 资本收入份额 (0 < α < 1)
        savings_rate: 储蓄率 s
        depreciation_rate: 折旧率 δ
        population_growth_rate: 人口增长率 n
        capital_per_worker0: 初始人均资本 k0
        productivity: 全要素生产率 A
    """
    alpha: float = 0.3
    savings_rate: float = 0.2
    depreciation_rate: float = 0.05
    population_growth_rate: float = 0.01
    capital_per_worker0: float = 1.0
    productivity: float = 1.0

    def __post_init__(self):
        if not 0 < self.alpha < 1:
            raise ValueError("alpha 必须介于 0 和 1 之间")
        if not 0 < self.savings_rate < 1:
            raise ValueError("储蓄率必须介于 0 和 1 之间")
        if self.depreciation_rate < 0 or self.population_growth_rate < 0:
            raise ValueError("折旧率与人口增长率不能为负")
        if self.capital_per_worker0 < 0:
            raise ValueError("初始人均资本不能为负")

    def output_per_worker(self, k: float) -> float:
        """人均产出: y = A * k^α"""
        if k < 0:
            raise ValueError("人均资本不能为负")
        return self.productivity * k ** self.alpha

    def investment_per_worker(self, k: float) -> float:
        """人均投资: i = s * f(k)"""
        return self.savings_rate * self.output_per_worker(k)

    def breakeven_investment(self, k: float) -> float:
        """
        持平投资 (break-even investment): (δ + n) * k

        使人均资本保持不变所需的投资量。
        """
        return (self.depreciation_rate + self.population_growth_rate) * k

    def capital_accumulation(self, k: float) -> float:
        """
        资本积累方程: Δk = s*f(k) - (δ + n)*k
        """
        return self.investment_per_worker(k) - self.breakeven_investment(k)

    def steady_state_k(self) -> float:
        """
        稳态人均资本: s*A*k^α = (δ+n)*k
        => k* = [s*A / (δ+n)]^(1/(1-α))
        """
        numerator = self.savings_rate * self.productivity
        denominator = self.depreciation_rate + self.population_growth_rate
        if denominator <= 0:
            raise ValueError("折旧率与人口增长率之和必须为正")
        return (numerator / denominator) ** (1 / (1 - self.alpha))

    def steady_state(self) -> dict:
        """稳态关键变量"""
        k_star = self.steady_state_k()
        y_star = self.output_per_worker(k_star)
        c_star = (1 - self.savings_rate) * y_star
        i_star = self.savings_rate * y_star
        return {
            'k': k_star,
            'y': y_star,
            'c': c_star,
            'i': i_star,
        }

    def golden_rule_k(self) -> float:
        """
        黄金律资本存量

        人均消费 c = f(k) - s*f(k) = (1-s)*f(k)，在稳态 c* = f(k*) - (δ+n)*k*
        最大化 c* => f'(k) = δ + n
        α*A*k^(α-1) = δ + n => k_gold = [α*A/(δ+n)]^(1/(1-α))
        """
        numerator = self.alpha * self.productivity
        denominator = self.depreciation_rate + self.population_growth_rate
        if denominator <= 0:
            raise ValueError("折旧率与人口增长率之和必须为正")
        return (numerator / denominator) ** (1 / (1 - self.alpha))

    def golden_rule_savings_rate(self) -> float:
        """
        黄金律储蓄率: s_gold = 使稳态消费最大化的储蓄率

        黄金律要求 s*f(k_gold) = (δ+n)*k_gold => s = (δ+n)*k_gold / f(k_gold)
        由于 f'(k_gold) = δ+n，可得 s_gold = α
        """
        return self.alpha

    def simulate(self, periods: int = 100) -> dict:
        """
        模拟经济从初始资本收敛到稳态的路径

        Args:
            periods: 模拟期数

        Returns:
            各期 k, y, c, i 序列
        """
        k = self.capital_per_worker0
        k_path, y_path, c_path, i_path = [], [], [], []

        for _ in range(periods):
            k_path.append(k)
            y = self.output_per_worker(k)
            i = self.investment_per_worker(k)
            c = y - i
            y_path.append(y)
            i_path.append(i)
            c_path.append(c)
            dk = self.capital_accumulation(k)
            k = max(k + dk, 0.0)

        return {
            'capital': np.array(k_path),
            'output': np.array(y_path),
            'investment': np.array(i_path),
            'consumption': np.array(c_path),
        }

    def convergence_speed(self, current_k: float = None) -> float:
        """
        收敛速度 (近似)

        索洛模型收敛速度约为 λ = (1-α)(δ+n)。
        距稳态越远，收敛越快。
        """
        return (1 - self.alpha) * (self.depreciation_rate + self.population_growth_rate)

    def analyze(self) -> dict:
        """生成模型分析"""
        steady = self.steady_state()
        k_gold = self.golden_rule_k()
        c_gold = self.output_per_worker(k_gold) - self.breakeven_investment(k_gold)
        return {
            'steady_state': steady,
            'golden_rule': {
                'k_gold': k_gold,
                'c_gold': c_gold,
                's_gold': self.golden_rule_savings_rate(),
            },
            'convergence_speed': self.convergence_speed(),
            'interpretation': (
                f"稳态人均资本 k* = {steady['k']:.2f}，稳态人均产出 y* = "
                f"{steady['y']:.2f}。黄金律资本存量 k_gold = {k_gold:.2f}。"
                f"{'经济储蓄率过高' if k_gold < steady['k'] else '经济储蓄率低于黄金律水平'}。"
            ),
        }

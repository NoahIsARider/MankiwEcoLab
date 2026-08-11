"""
消费者选择理论
Theory of Consumer Choice

对应曼昆《经济学原理》微观分册:
- 第21章 消费者选择理论 (The Theory of Consumer Choice)
- 原理3: 理性人考虑边际量 (Rational people think at the margin)

核心概念:
- 预算约束线 (Budget Constraint): Px * x + Py * y = I
- 无差异曲线 (Indifference Curve): U(x, y) = x^α * y^(1-α)  (柯布-道格拉斯)
- 边际替代率 (MRS) = MUx / MUy = [α/(1-α)] * (y/x)
- 最优选择: MRS = Px/Py (相切条件) 且满足预算约束
- 需求函数: x* = αI/Px, y* = (1-α)I/Py
"""

from dataclasses import dataclass

import numpy as np


@dataclass
class BudgetConstraint:
    """
    预算约束线

    消费者收入 I，商品 X 价格 Px，商品 Y 价格 Py。
    预算线方程: Px * x + Py * y = I

    Attributes:
        income: 消费者收入 I
        price_x: 商品 X 的价格 Px
        price_y: 商品 Y 的价格 Py
    """
    income: float
    price_x: float
    price_y: float

    def __post_init__(self):
        if self.income < 0:
            raise ValueError("收入不能为负")
        if self.price_x <= 0 or self.price_y <= 0:
            raise ValueError("商品价格必须为正数")

    @property
    def max_x(self) -> float:
        """全部收入用于购买 X 的最大数量 (X 轴截距)"""
        return self.income / self.price_x

    @property
    def max_y(self) -> float:
        """全部收入用于购买 Y 的最大数量 (Y 轴截距)"""
        return self.income / self.price_y

    @property
    def slope(self) -> float:
        """预算线斜率 = -Px/Py (市场价格比率)"""
        return -self.price_x / self.price_y

    def max_y_at(self, x: float) -> float:
        """在给定 X 消费量时能负担的最大 Y 消费量"""
        return (self.income - self.price_x * x) / self.price_y

    def affordable(self, x: float, y: float, tol: float = 1e-9) -> bool:
        """判断消费组合 (x, y) 是否在预算约束之内"""
        return self.price_x * x + self.price_y * y <= self.income + tol

    def on_budget_line(self, x: float, y: float, tol: float = 1e-9) -> bool:
        """判断消费组合是否恰好在预算线上"""
        return abs(self.price_x * x + self.price_y * y - self.income) <= tol

    def budget_line(self, num_points: int = 100) -> tuple:
        """
        生成预算线坐标点用于绘图

        Returns:
            (x_values, y_values)
        """
        x_values = np.linspace(0, self.max_x, num_points)
        y_values = np.array([self.max_y_at(x) for x in x_values])
        return x_values, y_values


@dataclass
class CobbDouglasUtility:
    """
    柯布-道格拉斯效用函数

    U(x, y) = x^α * y^(1-α)

    Attributes:
        alpha: 商品 X 的支出份额参数 (0 < α < 1)
    """
    alpha: float = 0.5

    def __post_init__(self):
        if not 0 < self.alpha < 1:
            raise ValueError("alpha 必须介于 0 和 1 之间")

    def utility(self, x: float, y: float) -> float:
        """总效用 U(x, y) = x^α * y^(1-α)"""
        if x < 0 or y < 0:
            return 0.0
        if x == 0 or y == 0:
            return 0.0
        return (x ** self.alpha) * (y ** (1 - self.alpha))

    def marginal_utility_x(self, x: float, y: float) -> float:
        """X 的边际效用 MUx = α * x^(α-1) * y^(1-α)"""
        if x <= 0 or y <= 0:
            return 0.0
        return self.alpha * (x ** (self.alpha - 1)) * (y ** (1 - self.alpha))

    def marginal_utility_y(self, x: float, y: float) -> float:
        """Y 的边际效用 MUy = (1-α) * x^α * y^(-α)"""
        if x <= 0 or y <= 0:
            return 0.0
        return (1 - self.alpha) * (x ** self.alpha) * (y ** (-self.alpha))

    def marginal_rate_of_substitution(self, x: float, y: float) -> float:
        """
        边际替代率 MRS = MUx / MUy = [α/(1-α)] * (y/x)

        表示愿意为多得到一单位 X 放弃的 Y 的数量。
        """
        if x <= 0 or y <= 0:
            return 0.0
        return (self.alpha / (1 - self.alpha)) * (y / x)

    def indifference_curve_y(self, x: float, target_utility: float) -> float:
        """
        在给定 X 下，达到 target_utility 所需的 Y

        y = [target_utility / x^α]^(1/(1-α))
        """
        if x <= 0:
            return np.inf
        return (target_utility / (x ** self.alpha)) ** (1.0 / (1.0 - self.alpha))

    def indifference_curve(self, target_utility: float,
                           x_max: float = 100, num_points: int = 200) -> tuple:
        """
        生成无差异曲线坐标点

        Returns:
            (x_values, y_values)
        """
        x_values = np.linspace(0.01, x_max, num_points)
        y_values = np.array([self.indifference_curve_y(x, target_utility)
                             for x in x_values])
        return x_values, y_values


class ConsumerChoice:
    """
    消费者最优选择

    消费者在预算约束下最大化效用:
    max U(x, y)  s.t.  Px*x + Py*y = I

    最优条件 (相切条件):
    MRS = Px/Py  =>  [α/(1-α)] * (y/x) = Px/Py

    解析需求函数:
    x* = α * I / Px
    y* = (1-α) * I / Py
    """

    def __init__(self, budget: BudgetConstraint,
                 utility: CobbDouglasUtility = None):
        """
        Args:
            budget: 预算约束
            utility: 效用函数 (默认 α=0.5 的柯布-道格拉斯)
        """
        self.budget = budget
        self.utility = utility if utility is not None else CobbDouglasUtility()

    @property
    def optimal_x(self) -> float:
        """最优 X 消费量: x* = αI/Px"""
        return self.utility.alpha * self.budget.income / self.budget.price_x

    @property
    def optimal_y(self) -> float:
        """最优 Y 消费量: y* = (1-α)I/Py"""
        return (1 - self.utility.alpha) * self.budget.income / self.budget.price_y

    def optimal_bundle(self) -> dict:
        """最优消费组合及其效用"""
        x_star = self.optimal_x
        y_star = self.optimal_y
        return {
            'x': x_star,
            'y': y_star,
            'utility': self.utility.utility(x_star, y_star),
            'expenditure': (self.budget.price_x * x_star
                            + self.budget.price_y * y_star),
        }

    def verify_tangency(self, tol: float = 1e-6) -> bool:
        """
        验证最优点的相切条件: MRS = Px/Py

        在最优组合处，无差异曲线的斜率 (=-MRS) 应等于预算线的斜率 (=-Px/Py)。
        """
        mrs = self.utility.marginal_rate_of_substitution(
            self.optimal_x, self.optimal_y)
        return abs(mrs - self.budget.price_x / self.budget.price_y) <= tol

    def verify_budget_satisfied(self, tol: float = 1e-6) -> bool:
        """验证最优点满足预算约束 Px*x + Py*y = I"""
        return abs(self.budget.price_x * self.optimal_x
                   + self.budget.price_y * self.optimal_y
                   - self.budget.income) <= tol

    def demand_curve(self, good: str = 'x', price_range: tuple = None,
                     num_points: int = 50) -> tuple:
        """
        生成需求曲线 (保持收入与另一商品价格不变)

        Args:
            good: 'x' 或 'y'
            price_range: 价格搜索范围 (min, max)

        Returns:
            (prices, quantities)
        """
        if good not in ('x', 'y'):
            raise ValueError("good 必须是 'x' 或 'y'")

        if price_range is None:
            price_range = (self.budget.price_x * 0.5, self.budget.price_x * 2.0)

        prices = np.linspace(price_range[0], price_range[1], num_points)

        if good == 'x':
            quantities = self.utility.alpha * self.budget.income / prices
        else:
            quantities = (1 - self.utility.alpha) * self.budget.income / prices

        return prices, quantities

    def engel_curve(self, good: str = 'x', income_range: tuple = None,
                    num_points: int = 50) -> tuple:
        """
        恩格尔曲线: 收入变化对最优消费量的影响

        Returns:
            (incomes, quantities)
        """
        if good not in ('x', 'y'):
            raise ValueError("good 必须是 'x' 或 'y'")

        if income_range is None:
            income_range = (self.budget.income * 0.5, self.budget.income * 2.0)

        incomes = np.linspace(income_range[0], income_range[1], num_points)

        if good == 'x':
            quantities = self.utility.alpha * incomes / self.budget.price_x
        else:
            quantities = (1 - self.utility.alpha) * incomes / self.budget.price_y

        return incomes, quantities

    def analyze(self) -> dict:
        """生成消费者选择完整分析"""
        bundle = self.optimal_bundle()
        mrs = self.utility.marginal_rate_of_substitution(bundle['x'], bundle['y'])
        price_ratio = self.budget.price_x / self.budget.price_y
        return {
            'budget': {
                'income': self.budget.income,
                'price_x': self.budget.price_x,
                'price_y': self.budget.price_y,
                'max_x': self.budget.max_x,
                'max_y': self.budget.max_y,
                'slope': self.budget.slope,
            },
            'utility_parameter_alpha': self.utility.alpha,
            'optimal_bundle': bundle,
            'mrs': mrs,
            'price_ratio': price_ratio,
            'tangency_condition': abs(mrs - price_ratio),
            'interpretation': (
                f"在预算 Px*{self.budget.price_x} + Py*{self.budget.price_y} = "
                f"收入 {self.budget.income} 下，最优消费组合为 "
                f"({bundle['x']:.2f}, {bundle['y']:.2f})，效用 {bundle['utility']:.2f}。"
                f"相切条件 MRS = Px/Py: {mrs:.3f} ≈ {price_ratio:.3f}。"
            ),
        }

"""
通货膨胀与物价水平
Inflation and Price Level

对应曼昆《经济学原理》宏观分册:
- 第24章 生活费用的衡量 (Measuring the Cost of Living)
- 第30章 货币增长与通货膨胀 (Money Growth and Inflation)
- 原理9: 当政府发行了过多货币时，物价上升

核心概念:
- 消费物价指数 CPI: 固定一篮子商品的价格变化
- 通货膨胀率: CPI 的百分比变化
- 货币数量论: M * V = P * Y
"""

from dataclasses import dataclass


@dataclass
class CPI:
    """
    消费物价指数 (Consumer Price Index)

    使用固定的一篮子商品 (base basket) 计算:
    CPI_t = (成本_篮子_t / 成本_篮子_基期) * 100

    Attributes:
        base_prices: 基期各商品价格
        base_quantities: 固定篮子中各商品数量
    """
    base_prices: list
    base_quantities: list

    def __post_init__(self):
        if len(self.base_prices) != len(self.base_quantities):
            raise ValueError("价格与数量列表长度必须一致")
        if len(self.base_prices) == 0:
            raise ValueError("商品列表不能为空")

    @property
    def base_cost(self) -> float:
        """基期篮子成本"""
        return sum(p * q for p, q in zip(self.base_prices, self.base_quantities))

    def compute(self, current_prices: list) -> float:
        """
        计算当前期 CPI

        Args:
            current_prices: 当前期各商品价格

        Returns:
            CPI 值 (基期为 100)
        """
        if len(current_prices) != len(self.base_prices):
            raise ValueError("当前价格列表长度与基期不一致")
        if self.base_cost == 0:
            raise ValueError("基期篮子成本不能为 0")
        current_cost = sum(p * q for p, q in zip(current_prices, self.base_quantities))
        return current_cost / self.base_cost * 100


def inflation_rate(previous_index: float, current_index: float) -> float:
    """
    计算通货膨胀率

    π = (CPI_t - CPI_{t-1}) / CPI_{t-1} * 100

    Args:
        previous_index: 上期价格指数
        current_index: 本期价格指数

    Returns:
        通货膨胀率 (百分比)
    """
    if previous_index <= 0:
        raise ValueError("上期价格指数必须为正数")
    return (current_index - previous_index) / previous_index * 100


def adjust_for_inflation(nominal_amount: float, base_index: float, current_index: float) -> float:
    """
    根据物价指数调整名义金额为实际金额

    实际金额 = 名义金额 * (基期指数 / 当前指数)
    """
    if current_index <= 0:
        raise ValueError("当前指数必须为正数")
    return nominal_amount * base_index / current_index


@dataclass
class QuantityTheory:
    """
    货币数量论 (Quantity Theory of Money)

    货币数量方程: M * V = P * Y
    - M: 货币供给量
    - V: 货币流通速度 (假设恒定)
    - P: 物价水平
    - Y: 实际产出

    该理论揭示: 货币供给增长 => 物价水平同比例上升 => 通货膨胀。
    对应曼昆十大原理 9: 当政府发行了过多货币时，物价上升。
    """
    money_supply: float = 1000.0
    velocity: float = 5.0
    real_output: float = 100.0

    def price_level(self) -> float:
        """由货币数量方程计算物价水平 P = M*V / Y"""
        if self.real_output == 0:
            raise ValueError("实际产出不能为 0")
        return self.money_supply * self.velocity / self.real_output

    def inflation_from_money_growth(self, money_growth_rate: float) -> float:
        """
        若货币流通速度 V 与产出 Y 不变，货币增长率即为通货膨胀率

        π = ΔM/M (当 V 和 Y 恒定时)
        """
        return money_growth_rate

    def required_money_supply(self, target_price: float) -> float:
        """为达到目标物价水平所需的货币供给量"""
        if self.velocity == 0:
            raise ValueError("货币流通速度不能为 0")
        return target_price * self.real_output / self.velocity

    def analyze(self) -> dict:
        """生成货币数量论分析"""
        price = self.price_level()
        return {
            'M': self.money_supply,
            'V': self.velocity,
            'P': price,
            'Y': self.real_output,
            'equation': f"M*V = {self.money_supply} * {self.velocity} = "
                        f"P*Y = {price:.2f} * {self.real_output}",
            'interpretation': (
                f"当前物价水平 P = {price:.2f}。若货币供给增加 X%，"
                f"在 V 和 Y 不变的情况下，物价水平将同比例上升 X%。"
            ),
        }

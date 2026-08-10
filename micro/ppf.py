"""
生产可能性边界与机会成本
Production Possibility Frontier and Opportunity Cost

对应曼昆《经济学原理》十大原理:
- 原理1: 人们面临权衡取舍 (People face trade-offs)
- 原理2: 某种东西的成本是为了得到它所放弃的东西 (Opportunity cost)
"""

from dataclasses import dataclass

import numpy as np


@dataclass
class OpportunityCost:
    """
    机会成本计算结果

    Attributes:
        good: 要生产的商品名称
        per_unit: 多生产一单位 good 所需放弃的其他商品数量
        tradeoff_rate: 两种商品的边际转换率 (MRT)
    """
    good: str
    per_unit: float
    tradeoff_rate: float


class ProductionPossibilityFrontier:
    """
    生产可能性边界 (PPF)

    表示在固定资源和技术条件下，一个经济体所能生产的两种商品
    最大数量的组合。PPF 上每一点都是有效率的产出组合。

    模型设定:
    - 经济体拥有固定的总资源 R
    - 生产一单位商品 X 需要 a 单位资源
    - 生产一单位商品 Y 需要 b 单位资源

    线性 PPF 方程:  a * X + b * Y = R
    """

    def __init__(self, resource: float, input_x: float, input_y: float,
                 good_x: str = "Good X", good_y: str = "Good Y"):
        """
        初始化 PPF

        Args:
            resource: 经济体的总资源量
            input_x: 生产一单位 X 所需的资源量
            input_y: 生产一单位 Y 所需的资源量
            good_x: X 商品名称
            good_y: Y 商品名称
        """
        if resource <= 0 or input_x <= 0 or input_y <= 0:
            raise ValueError("resource 与两种投入系数必须为正数")
        self.resource = resource
        self.input_x = input_x
        self.input_y = input_y
        self.good_x = good_x
        self.good_y = good_y

    @property
    def max_x(self) -> float:
        """全部资源用于生产 X 时的最大产量 (X 轴截距)"""
        return self.resource / self.input_x

    @property
    def max_y(self) -> float:
        """全部资源用于生产 Y 时的最大产量 (Y 轴截距)"""
        return self.resource / self.input_y

    def max_output_x(self, y: float) -> float:
        """在给定 Y 产量下，X 的最大可能产量"""
        return (self.resource - self.input_y * y) / self.input_x

    def max_output_y(self, x: float) -> float:
        """在给定 X 产量下，Y 的最大可能产量"""
        return (self.resource - self.input_x * x) / self.input_y

    def opportunity_cost_x(self) -> float:
        """
        多生产一单位 X 的机会成本

        为多生产一单位 X，需要把 input_x 单位资源从 Y 生产转移到 X 生产，
        这将放弃 input_x / input_y 单位 Y。
        """
        return self.input_x / self.input_y

    def opportunity_cost_y(self) -> float:
        """多生产一单位 Y 的机会成本"""
        return self.input_y / self.input_x

    def is_efficient(self, x: float, y: float, tol: float = 1e-6) -> bool:
        """
        判断产出组合 (x, y) 是否位于 PPF 上 (是否有效率)

        PPF 上的点满足 a*x + b*y = R
        """
        return abs(self.input_x * x + self.input_y * y - self.resource) <= tol

    def is_attainable(self, x: float, y: float) -> bool:
        """判断产出组合是否可行 (在 PPF 上或 PPF 之内)"""
        return self.input_x * x + self.input_y * y <= self.resource + 1e-9

    def get_ppf_points(self, num_points: int = 100) -> tuple:
        """
        生成 PPF 上的一系列点用于绘图

        Returns:
            (x_values, y_values)
        """
        x_values = np.linspace(0, self.max_x, num_points)
        y_values = np.array([self.max_output_y(x) for x in x_values])
        return x_values, y_values

    def marginal_rate_of_transformation(self) -> float:
        """
        边际转换率 MRT = |dY/dX| = a / b

        线性 PPF 的 MRT 恒定，等于 X 的机会成本。
        """
        return self.opportunity_cost_x()

    def __repr__(self):
        return (f"PPF(resource={self.resource}, "
                f"a={self.input_x} resources/unit {self.good_x}, "
                f"b={self.input_y} resources/unit {self.good_y})")


def analyze_opportunity_cost(ppf: ProductionPossibilityFrontier) -> dict:
    """
    分析 PPF 的机会成本信息

    Returns:
        包含机会成本分析的字典
    """
    oc_x = ppf.opportunity_cost_x()
    oc_y = ppf.opportunity_cost_y()

    return {
        "max_x": ppf.max_x,
        "max_y": ppf.max_y,
        "opportunity_cost_x": oc_x,
        "opportunity_cost_y": oc_y,
        "interpretation": (
            f"多生产 1 单位 {ppf.good_x} 必须放弃 {oc_x:.2f} 单位 {ppf.good_y}；"
            f"反之，多生产 1 单位 {ppf.good_y} 必须放弃 {oc_y:.2f} 单位 {ppf.good_x}。"
        ),
        "tradeoff_direction": f"{ppf.good_y} / {ppf.good_x}",
    }

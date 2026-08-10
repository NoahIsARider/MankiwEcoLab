"""
菲利普斯曲线
Phillips Curve

对应曼昆《经济学原理》宏观分册:
- 第35章 通货膨胀与失业的短期权衡
- 原理10: 社会面临通货膨胀与失业之间的短期权衡取舍

核心概念:
- 短期菲利普斯曲线: 通货膨胀与失业负相关 (负斜率)
- 预期因素: π = π^e - β*(u - u_n)
- 自然失业率 u_n: 当实际失业率 = 自然失业率时，通胀等于预期通胀
- 长期菲利普斯曲线: 垂直 (失业率回到自然率，无通胀-失业权衡)
"""

from dataclasses import dataclass

import numpy as np


@dataclass
class PhillipsCurve:
    """
    菲利普斯曲线模型

    方程: π = π^e - β*(u - u_n)

    Attributes:
        expected_inflation: 预期通货膨胀率 π^e
        beta: 失业率对通胀的影响系数 (β > 0)
        natural_unemployment_rate: 自然失业率 u_n
    """
    expected_inflation: float = 3.0
    beta: float = 0.5
    natural_unemployment_rate: float = 5.0

    def __post_init__(self):
        if self.beta <= 0:
            raise ValueError("beta 必须为正数")
        if self.natural_unemployment_rate < 0:
            raise ValueError("自然失业率不能为负")

    def inflation_at(self, unemployment_rate: float) -> float:
        """
        给定失业率下的通货膨胀率

        π = π^e - β*(u - u_n)
        """
        return (self.expected_inflation
                - self.beta * (unemployment_rate - self.natural_unemployment_rate))

    def unemployment_at(self, inflation: float) -> float:
        """
        给定通货膨胀率下的失业率 (短期)

        u = u_n - (π - π^e) / β
        """
        return (self.natural_unemployment_rate
                - (inflation - self.expected_inflation) / self.beta)

    def tradeoff_ratio(self) -> float:
        """
        权衡比率: 为降低 1 个百分点通货膨胀需要付出多少失业率上升

        Δu = -Δπ / β
        """
        return 1.0 / self.beta

    def sacrifice_ratio(self, beta: float = None) -> float:
        """
        牺牲率: 每降低 1% 通胀所失去的实际产出百分比

        奥肯定律近似: 失业率每上升 1%，产出损失约 2%。
        牺牲率 ≈ 2 * Δu / Δπ
        """
        b = beta if beta is not None else self.beta
        return 2.0 / b

    def curve_points(self, u_min: float = 1.0, u_max: float = 12.0,
                     num_points: int = 100) -> tuple:
        """
        生成短期菲利普斯曲线上的点

        Returns:
            (unemployment_values, inflation_values)
        """
        u_values = np.linspace(u_min, u_max, num_points)
        pi_values = np.array([self.inflation_at(u) for u in u_values])
        return u_values, pi_values

    def analyze(self) -> dict:
        """生成菲利普斯曲线分析"""
        return {
            'expected_inflation': self.expected_inflation,
            'natural_unemployment_rate': self.natural_unemployment_rate,
            'beta': self.beta,
            'tradeoff_ratio': self.tradeoff_ratio(),
            'sacrifice_ratio': self.sacrifice_ratio(),
            'interpretation': (
                f"当失业率高于自然失业率 {self.natural_unemployment_rate:.1f}% 时，"
                f"通胀低于预期 {self.expected_inflation:.1f}%；"
                f"降低 1 个百分点通胀需付出失业率上升 "
                f"{self.tradeoff_ratio():.1f} 个百分点的代价。"
            ),
        }

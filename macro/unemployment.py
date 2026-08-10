"""
失业与劳动力市场
Unemployment and the Labor Market

对应曼昆《经济学原理》宏观分册:
- 第28章 失业 (Unemployment)

核心概念:
- 失业率 = 失业人数 / 劳动力 * 100
- 劳动力参与率 = 劳动力 / 成年人口 * 100
- 自然失业率 = 摩擦性失业率 + 结构性失业率
- 周期性失业 = 实际失业率 - 自然失业率
"""

from dataclasses import dataclass


@dataclass
class LaborMarketStats:
    """
    劳动力市场统计

    Attributes:
        adult_population: 成年人口
        employed: 就业人数
        unemployed: 失业人数
        not_in_labor_force: 非劳动力人口 (不在劳动力队伍中)
    """
    adult_population: float
    employed: float
    unemployed: float
    not_in_labor_force: float = 0.0

    def __post_init__(self):
        if self.adult_population <= 0:
            raise ValueError("成年人口必须为正数")
        if self.not_in_labor_force == 0:
            # 自动补全: 非劳动力 = 成年人口 - 劳动力
            self.not_in_labor_force = max(
                0.0, self.adult_population - self.employed - self.unemployed)
        elif abs(self.adult_population - self.employed - self.unemployed
                 - self.not_in_labor_force) > 1e-6:
            raise ValueError("成年人口应等于就业+失业+非劳动力人口")

    @property
    def labor_force(self) -> float:
        """劳动力 = 就业 + 失业"""
        return self.employed + self.unemployed

    def labor_force_participation_rate(self) -> float:
        """劳动力参与率 = 劳动力 / 成年人口 * 100"""
        return self.labor_force / self.adult_population * 100

    def unemployment_rate(self) -> float:
        """失业率 = 失业 / 劳动力 * 100"""
        if self.labor_force == 0:
            return 0.0
        return self.unemployed / self.labor_force * 100

    def employment_population_ratio(self) -> float:
        """就业人口比 = 就业 / 成年人口 * 100"""
        return self.employed / self.adult_population * 100

    def analyze(self) -> dict:
        """生成劳动力市场分析"""
        return {
            'labor_force': self.labor_force,
            'labor_force_participation_rate': self.labor_force_participation_rate(),
            'unemployment_rate': self.unemployment_rate(),
            'employment_population_ratio': self.employment_population_ratio(),
            'not_in_labor_force': self.not_in_labor_force,
        }


def unemployment_decomposition(actual_unemployment_rate: float,
                              frictional_rate: float,
                              structural_rate: float) -> dict:
    """
    失业类型分解

    Args:
        actual_unemployment_rate: 实际失业率 (%)
        frictional_rate: 摩擦性失业率 (%)
        structural_rate: 结构性失业率 (%)

    Returns:
        自然失业率、周期性失业及解释
    """
    natural_rate = frictional_rate + structural_rate
    cyclical_rate = actual_unemployment_rate - natural_rate

    return {
        'natural_unemployment_rate': natural_rate,
        'frictional_unemployment_rate': frictional_rate,
        'structural_unemployment_rate': structural_rate,
        'cyclical_unemployment_rate': cyclical_rate,
        'interpretation': (
            f"自然失业率 = 摩擦性 ({frictional_rate:.1f}%) + 结构性 "
            f"({structural_rate:.1f}%) = {natural_rate:.1f}%。"
            f"实际失业率 {actual_unemployment_rate:.1f}% 中，"
            f"周期性失业为 {cyclical_rate:+.1f}%。"
        ),
    }

"""
GDP 核算
GDP Accounting

对应曼昆《经济学原理》宏观分册:
- 第23章 一国收入的衡量 (Measuring a Nation's Income)
- 原理8: 一国的生活水平取决于它生产物品与服务的能力

核心概念:
- 支出法: GDP = C + I + G + NX
- 名义 GDP vs 实际 GDP
- GDP 平减指数 = 名义GDP / 实际GDP * 100
- 经济增长率
"""

from dataclasses import dataclass

import numpy as np


@dataclass
class GDPAccounts:
    """
    国民收入账户

    Attributes:
        consumption: 消费 C
        investment: 投资 I
        government_spending: 政府购买 G
        net_exports: 净出口 NX (可正可负)
    """
    consumption: float
    investment: float
    government_spending: float
    net_exports: float = 0.0

    @property
    def gdp(self) -> float:
        """支出法 GDP: Y = C + I + G + NX"""
        return (self.consumption + self.investment +
                self.government_spending + self.net_exports)

    def components_share(self) -> dict:
        """各支出组成部分占 GDP 的比重"""
        g = self.gdp
        if g == 0:
            return {k: 0.0 for k in ['C', 'I', 'G', 'NX']}
        return {
            'C': self.consumption / g,
            'I': self.investment / g,
            'G': self.government_spending / g,
            'NX': self.net_exports / g,
        }

    def analyze(self) -> dict:
        """生成国民账户分析"""
        shares = self.components_share()
        return {
            'GDP': self.gdp,
            'components': {
                'consumption_C': self.consumption,
                'investment_I': self.investment,
                'government_G': self.government_spending,
                'net_exports_NX': self.net_exports,
            },
            'shares': shares,
            'interpretation': (
                f"GDP = {self.gdp:.2f}，其中消费占 {shares['C']*100:.1f}%，"
                f"投资占 {shares['I']*100:.1f}%，"
                f"政府购买占 {shares['G']*100:.1f}%，"
                f"净出口占 {shares['NX']*100:.1f}%。"
            ),
        }


def calculate_real_gdp(nominal_gdp: list, price_level: list) -> np.ndarray:
    """
    计算实际 GDP

    实际 GDP = 名义 GDP / 价格水平 * 基期价格

    Args:
        nominal_gdp: 各期名义 GDP 列表
        price_level: 各期价格水平列表 (与名义 GDP 对应)

    Returns:
        各期实际 GDP 数组
    """
    nominal = np.array(nominal_gdp, dtype=float)
    price = np.array(price_level, dtype=float)
    if np.any(price <= 0):
        raise ValueError("价格水平必须为正数")
    base_price = price[0]
    return nominal / price * base_price


class GDPDeflator:
    """
    GDP 平减指数

    衡量相对于基期经济中所有商品与服务的总体价格水平。
    GDP 平减指数 = (名义 GDP / 实际 GDP) * 100
    """

    def __init__(self, nominal_gdp: list, real_gdp: list):
        if len(nominal_gdp) != len(real_gdp):
            raise ValueError("名义 GDP 与实际 GDP 长度必须一致")
        self.nominal_gdp = np.array(nominal_gdp, dtype=float)
        self.real_gdp = np.array(real_gdp, dtype=float)
        if np.any(self.real_gdp <= 0):
            raise ValueError("实际 GDP 必须为正数")

    def values(self) -> np.ndarray:
        """各期 GDP 平减指数"""
        return self.nominal_gdp / self.real_gdp * 100

    def inflation_rate(self) -> np.ndarray:
        """
        由 GDP 平减指数计算的通货膨胀率

        π_t = (GDPdef_t - GDPdef_{t-1}) / GDPdef_{t-1} * 100
        """
        v = self.values()
        if len(v) < 2:
            return np.array([])
        return (np.diff(v) / v[:-1]) * 100


def gdp_growth_rate(gdp_series: list) -> np.ndarray:
    """
    计算 GDP 增长率

    g_t = (Y_t - Y_{t-1}) / Y_{t-1} * 100

    Args:
        gdp_series: GDP 时间序列

    Returns:
        各期增长率 (首期无值)
    """
    series = np.array(gdp_series, dtype=float)
    if len(series) < 2:
        return np.array([])
    if np.any(series[:-1] == 0):
        raise ValueError("GDP 序列不能包含 0")
    return (np.diff(series) / series[:-1]) * 100

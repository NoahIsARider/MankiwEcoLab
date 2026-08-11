"""
宏观经济学模块
Macroeconomics Module

覆盖曼昆《经济学原理·宏观分册》的核心概念:
- GDP 核算 (GDP Accounting)
- 通货膨胀与 CPI (Inflation and CPI)
- 失业 (Unemployment)
- 经济增长与索洛模型 (Solow Growth Model)
- 货币与银行体系 (Money and Banking)
- 总需求-总供给模型 (AD-AS Model)
- 菲利普斯曲线 (Phillips Curve)
- 可贷资金市场 (Market for Loanable Funds)
- IS-LM 模型 (IS-LM Model)
"""

from .ad_as import ADASModel
from .gdp import GDPAccounts, GDPDeflator, calculate_real_gdp, gdp_growth_rate
from .inflation import CPI, QuantityTheory, adjust_for_inflation, inflation_rate
from .islm import ISLMModel
from .loanable_funds import LoanableFundsModel
from .money import MoneyCreationModel
from .phillips import PhillipsCurve
from .solow import SolowGrowthModel
from .unemployment import LaborMarketStats, unemployment_decomposition

__all__ = [
    'GDPAccounts',
    'GDPDeflator',
    'calculate_real_gdp',
    'gdp_growth_rate',
    'CPI',
    'inflation_rate',
    'adjust_for_inflation',
    'QuantityTheory',
    'LaborMarketStats',
    'unemployment_decomposition',
    'SolowGrowthModel',
    'MoneyCreationModel',
    'ADASModel',
    'PhillipsCurve',
    'LoanableFundsModel',
    'ISLMModel',
]

"""
微观经济学模块
Microeconomics Module

覆盖曼昆《经济学原理·微观分册》的核心概念:
- 生产可能性边界与机会成本 (PPF and Opportunity Cost)
- 比较优势与贸易 (Comparative Advantage and Trade)
- 外部性与公共政策 (Externalities)
- 市场结构 (Market Structure)
"""

from .externality import ExternalityModel
from .market_structure import MarketStructureAnalyzer
from .ppf import OpportunityCost, ProductionPossibilityFrontier
from .trade import TradeModel

__all__ = [
    'ProductionPossibilityFrontier',
    'OpportunityCost',
    'TradeModel',
    'ExternalityModel',
    'MarketStructureAnalyzer',
]

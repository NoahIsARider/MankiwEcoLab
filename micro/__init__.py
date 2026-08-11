"""
微观经济学模块
Microeconomics Module

覆盖曼昆《经济学原理·微观分册》的核心概念:
- 生产可能性边界与机会成本 (PPF and Opportunity Cost)
- 比较优势与贸易 (Comparative Advantage and Trade)
- 外部性与公共政策 (Externalities)
- 市场结构 (Market Structure)
- 消费者选择理论 (Theory of Consumer Choice)
- 博弈论与寡头竞争 (Game Theory and Oligopoly)
"""

from .consumer_choice import BudgetConstraint, CobbDouglasUtility, ConsumerChoice
from .externality import ExternalityModel
from .game_theory import CournotGame, NormalFormGame, matching_pennies, prisoners_dilemma
from .market_structure import MarketStructureAnalyzer
from .ppf import OpportunityCost, ProductionPossibilityFrontier
from .trade import TradeModel

__all__ = [
    'ProductionPossibilityFrontier',
    'OpportunityCost',
    'TradeModel',
    'ExternalityModel',
    'MarketStructureAnalyzer',
    'BudgetConstraint',
    'CobbDouglasUtility',
    'ConsumerChoice',
    'NormalFormGame',
    'CournotGame',
    'prisoners_dilemma',
    'matching_pennies',
]

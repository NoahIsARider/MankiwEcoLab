"""
市场结构分析
Market Structure Analysis

对应曼昆《经济学原理》:
- 第14章 竞争市场 (Competitive Markets)
- 第15章 垄断 (Monopoly)
- 第16章 垄断竞争 (Monopolistic Competition)
- 第17章 寡头 (Oligopoly)

核心概念:
- 完全竞争: 价格接受者，P = MC，长期零经济利润
- 垄断: 价格制定者，MR = MC，P > MC，产生无谓损失
- 寡头: 少数企业，策略互动 (古诺模型)
- HHI 赫芬达尔指数: 市场集中度衡量
"""

from dataclasses import dataclass


@dataclass
class MarketStructureAnalyzer:
    """
    市场结构分析器 (线性市场需求 + 成本结构)

    市场需求曲线: P = a - b * Q
    企业成本函数: TC(q) = FC + c * q (常数边际成本)

    通过企业数量区分市场结构:
    - 1 家企业   => 垄断
    - 2-5 家企业 => 寡头 (古诺竞争)
    - 大量企业   => 完全竞争
    """

    market_demand_intercept: float = 100.0
    market_demand_slope: float = 1.0
    firm_mc: float = 20.0
    firm_fixed_cost: float = 0.0
    num_firms: int = 1

    def __post_init__(self):
        if self.market_demand_slope <= 0:
            raise ValueError("市场需求曲线斜率必须为正")
        if self.num_firms < 1:
            raise ValueError("企业数量必须至少为 1")

    def structure_type(self) -> str:
        """根据企业数量判断市场结构"""
        if self.num_firms == 1:
            return "垄断 (Monopoly)"
        elif self.num_firms <= 5:
            return "寡头 (Oligopoly)"
        elif self.num_firms <= 20:
            return "垄断竞争 (Monopolistic Competition)"
        else:
            return "完全竞争 (Perfect Competition)"

    def competitive_equilibrium(self) -> dict:
        """
        完全竞争均衡: P = MC

        P = MC => a - b*Q = MC => Q = (a - MC) / b
        """
        q = (self.market_demand_intercept - self.firm_mc) / self.market_demand_slope
        q = max(0.0, q)
        p = self.market_demand_intercept - self.market_demand_slope * q
        return {'quantity': q, 'price': p}

    def monopoly_equilibrium(self) -> dict:
        """
        垄断均衡: MR = MC

        总收益 TR = P*Q = (a - b*Q)*Q = a*Q - b*Q^2
        边际收益 MR = a - 2b*Q
        MR = MC => a - 2b*Q = MC => Q = (a - MC) / (2b)
        """
        q = (self.market_demand_intercept - self.firm_mc) / (2 * self.market_demand_slope)
        q = max(0.0, q)
        p = self.market_demand_intercept - self.market_demand_slope * q
        return {'quantity': q, 'price': p}

    def cournot_equilibrium(self) -> dict:
        """
        古诺寡头均衡 (同质企业)

        企业 i 的反应函数: q_i = (a - MC) / (2b) - q_j / 2
        对称均衡: q_i = (a - MC) / (b * (n + 1))
        """
        n = self.num_firms
        a = self.market_demand_intercept
        b = self.market_demand_slope
        mc = self.firm_mc

        q_total = n * (a - mc) / (b * (n + 1))
        q_total = max(0.0, q_total)
        p = a - b * q_total
        return {'quantity': q_total, 'price': p}

    def equilibrium(self) -> dict:
        """根据企业数量选择对应的市场均衡"""
        if self.num_firms == 1:
            return self.monopoly_equilibrium()
        elif self.num_firms <= 20:
            return self.cournot_equilibrium()
        else:
            return self.competitive_equilibrium()

    def herfindahl_index(self, market_shares: list = None) -> float:
        """
        赫芬达尔-赫希曼指数 (HHI)

        HHI = Σ s_i^2 * 10000, 其中 s_i 是第 i 家企业的市场份额

        Args:
            market_shares: 各企业市场份额 (小数或百分数均可)

        Returns:
            0-10000 的 HHI 值
        """
        if market_shares is None:
            # 均匀分布假设
            shares = [1.0 / self.num_firms] * self.num_firms
        else:
            total = sum(market_shares)
            shares = [s / total for s in market_shares]
        return sum(s ** 2 for s in shares) * 10000

    def hhi_interpretation(self, hhi: float) -> str:
        """解释 HHI 值对应的市场集中度"""
        if hhi < 1500:
            return "竞争性市场 (competitive)"
        elif hhi <= 2500:
            return "中等集中市场 (moderately concentrated)"
        else:
            return "高度集中市场 (highly concentrated)"

    def deadweight_loss(self) -> float:
        """
        垄断造成的无谓损失

        DWL = 0.5 * (P_m - MC) * (Q_c - Q_m)
        """
        comp = self.competitive_equilibrium()
        mono = self.monopoly_equilibrium()
        return 0.5 * (mono['price'] - self.firm_mc) * (comp['quantity'] - mono['quantity'])

    def analyze(self) -> dict:
        """生成市场结构完整分析"""
        comp = self.competitive_equilibrium()
        if self.num_firms <= 20:
            actual = self.equilibrium()
        else:
            actual = comp
        hhi = self.herfindahl_index()

        return {
            'structure': self.structure_type(),
            'num_firms': self.num_firms,
            'equilibrium': actual,
            'competitive_benchmark': comp,
            'price_markup': actual['price'] - comp['price'],
            'quantity_shortfall': comp['quantity'] - actual['quantity'],
            'deadweight_loss': self.deadweight_loss(),
            'HHI': hhi,
            'HHI_interpretation': self.hhi_interpretation(hhi),
        }

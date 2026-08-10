"""
外部性与市场失灵
Externalities and Market Failure

对应曼昆《经济学原理》:
- 第10章 外部性 (Externalities)
- 原理7: 政府有时可以改善市场结果

核心概念:
- 负外部性 (Negative Externality): 如污染，边际社会成本 > 边际私人成本
- 正外部性 (Positive Externality): 如教育，边际社会收益 > 边际私人收益
- 庇古税 (Pigouvian Tax): 使私人成本等于社会成本的矫正税
- 无谓损失 (Deadweight Loss): 外部性导致的市场效率损失
"""

from dataclasses import dataclass


@dataclass
class ExternalityModel:
    """
    外部性模型 (线性供需框架)

    线性需求:   P_d = a_d - b_d * Q
    线性供给:   P_s = a_s + b_s * Q

    负外部性时，社会边际成本曲线 = 私人供给曲线 + 外部成本，位于其上方；
    正外部性时，社会边际收益曲线 = 私人需求曲线 + 外部收益，位于其上方。

    Attributes:
        demand_intercept: 需求曲线截距 a_d
        demand_slope: 需求曲线斜率绝对值 b_d
        supply_intercept: 供给曲线截距 a_s
        supply_slope: 供给曲线斜率 b_s
        externality_value: 外部成本 (正) 或外部收益 (负) 的绝对值大小
    """

    demand_intercept: float = 100.0
    demand_slope: float = 2.0
    supply_intercept: float = 10.0
    supply_slope: float = 1.0
    externality_value: float = 10.0

    def __post_init__(self):
        if self.demand_slope <= 0 or self.supply_slope <= 0:
            raise ValueError("曲线斜率必须为正")
        if self.demand_intercept <= self.supply_intercept:
            raise ValueError("需求曲线截距必须大于供给曲线截距，否则无均衡")

    def private_equilibrium(self) -> dict:
        """
        私人市场均衡 (不考虑外部性)

        均衡条件: P_d = P_s
        即 a_d - b_d*Q = a_s + b_s*Q
        => Q* = (a_d - a_s) / (b_d + b_s)
        """
        q_star = (self.demand_intercept - self.supply_intercept) / \
                 (self.demand_slope + self.supply_slope)
        p_star = self.demand_intercept - self.demand_slope * q_star
        return {'quantity': q_star, 'price': p_star}

    def social_optimum(self) -> dict:
        """
        社会最优均衡

        负外部性 (外部成本 > 0): 社会供给曲线 = 私人供给 + 外部成本
        正外部性 (外部收益 > 0, 记为负): 社会需求曲线 = 私人需求 + 外部收益

        返回社会最优产量。
        """
        if self.externality_value >= 0:
            # 负外部性: 社会边际成本 = 私人MC + 外部成本
            effective_intercept = self.supply_intercept + self.externality_value
            q_social = (self.demand_intercept - effective_intercept) / \
                       (self.demand_slope + self.supply_slope)
        else:
            # 正外部性: 社会边际收益 = 私人MB + 外部收益
            effective_intercept = self.demand_intercept + abs(self.externality_value)
            q_social = (effective_intercept - self.supply_intercept) / \
                       (self.demand_slope + self.supply_slope)
        q_social = max(0.0, q_social)
        return {'quantity': q_social}

    def is_negative(self) -> bool:
        """判断是否为负外部性"""
        return self.externality_value >= 0

    def deadweight_loss(self) -> float:
        """
        计算市场无谓损失 (DWL)

        负外部性下，市场均衡产量 Q_private 高于社会最优 Q_social，
        额外产量 Q_private - Q_social 的社会成本高于社会收益，
        三角形面积为 0.5 * (Q_private - Q_social) * |外部性价值|。
        """
        q_private = self.private_equilibrium()['quantity']
        q_social = self.social_optimum()['quantity']
        gap = abs(q_private - q_social)
        return 0.5 * gap * abs(self.externality_value)

    def pigouvian_tax(self) -> float:
        """
        最优庇古税 = 外部性价值

        通过征收等于外部成本的税收，使私人成本等于社会成本，
        从而让私人市场均衡等于社会最优。
        """
        return abs(self.externality_value)

    def analyze(self) -> dict:
        """生成完整分析报告"""
        private = self.private_equilibrium()
        social = self.social_optimum()
        q_private = private['quantity']
        q_social = social['quantity']

        externality_type = "负外部性" if self.is_negative() else "正外部性"
        overproduction = q_private > q_social

        return {
            'externality_type': externality_type,
            'private_quantity': q_private,
            'private_price': private['price'],
            'social_quantity': q_social,
            'production_gap': abs(q_private - q_social),
            'overproduction': overproduction,
            'deadweight_loss': self.deadweight_loss(),
            'pigouvian_tax': self.pigouvian_tax(),
            'interpretation': (
                f"市场产量 ({q_private:.2f}) "
                f"{'大于' if overproduction else '小于'} 社会最优产量 ({q_social:.2f})，"
                f"造成无谓损失 {self.deadweight_loss():.2f}。"
                f"征收庇古税 {self.pigouvian_tax():.2f} 可矫正外部性。"
            ),
        }

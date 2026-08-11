"""
可贷资金市场
The Market for Loanable Funds

对应曼昆《经济学原理》宏观分册:
- 第26章 储蓄、投资与金融体系 (Saving, Investment, and the Financial System)

核心概念:
- 可贷资金供给: 国民储蓄 S(r) = S0 + S1 * r (利率上升，储蓄增加)
- 可贷资金需求: 投资需求 I(r) = I0 - I1 * r (利率上升，投资减少)
- 均衡利率: S(r*) = I(r*) (+ 政府借款)
- 财政政策影响: 政府借款增加 -> 需求右移 -> 利率上升 -> 挤出私人投资
"""

from dataclasses import dataclass


@dataclass
class LoanableFundsModel:
    """
    可贷资金市场模型 (线性)

    供给 (储蓄):  S(r) = savings_autonomous + savings_sensitivity * r
    需求 (投资):  I(r) = investment_autonomous - investment_sensitivity * r
    均衡条件:     S(r*) = I(r*) + government_borrowing

    Attributes:
        savings_autonomous: 自主储蓄 S0
        savings_sensitivity: 储蓄对利率的敏感度 S1
        investment_autonomous: 自主投资 I0
        investment_sensitivity: 投资对利率的敏感度 I1
        government_borrowing: 政府借款 G (通过发行债券融资的赤字)
    """
    savings_autonomous: float = 800.0
    savings_sensitivity: float = 200.0
    investment_autonomous: float = 1200.0
    investment_sensitivity: float = 400.0
    government_borrowing: float = 0.0

    def __post_init__(self):
        if self.savings_sensitivity <= 0 or self.investment_sensitivity <= 0:
            raise ValueError("利率敏感度必须为正数")
        if self.investment_autonomous < 0:
            raise ValueError("自主投资不能为负")
        if self.government_borrowing < 0:
            raise ValueError("政府借款不能为负")

    def savings(self, rate: float) -> float:
        """可贷资金供给 (储蓄): S(r) = S0 + S1*r"""
        return self.savings_autonomous + self.savings_sensitivity * rate

    def investment(self, rate: float) -> float:
        """可贷资金需求 (投资): I(r) = I0 - I1*r"""
        return max(0.0, self.investment_autonomous
                   - self.investment_sensitivity * rate)

    def excess_demand(self, rate: float) -> float:
        """超额需求: ED(r) = I(r) + G - S(r)"""
        return (self.investment(rate) + self.government_borrowing
                - self.savings(rate))

    def equilibrium_rate(self) -> float:
        """
        均衡利率

        求解 S(r) = I(r) + G:
        S0 + S1*r = I0 - I1*r + G
        r* = (I0 + G - S0) / (S1 + I1)
        """
        numerator = (self.investment_autonomous + self.government_borrowing
                     - self.savings_autonomous)
        denominator = self.savings_sensitivity + self.investment_sensitivity
        if denominator <= 0:
            raise ValueError("敏感度之和必须为正数")
        return max(0.0, numerator / denominator)

    def equilibrium(self) -> dict:
        """均衡结果: 利率、储蓄、投资"""
        rate = self.equilibrium_rate()
        savings = self.savings(rate)
        investment = self.investment(rate)
        return {
            'interest_rate': rate,
            'savings': savings,
            'investment': investment,
            'government_borrowing': self.government_borrowing,
        }

    def with_fiscal_policy(self, additional_borrowing: float) -> dict:
        """
        扩张性财政政策 (政府借款增加)

        政府为赤字融资发行债券，增加可贷资金需求:
        需求右移 -> 均衡利率上升 -> 私人投资被挤出 (挤出效应)

        Returns:
            政策前后对比
        """
        if additional_borrowing < 0:
            raise ValueError("政府借款增加量不能为负")

        before = self.equilibrium()
        new_model = LoanableFundsModel(
            savings_autonomous=self.savings_autonomous,
            savings_sensitivity=self.savings_sensitivity,
            investment_autonomous=self.investment_autonomous,
            investment_sensitivity=self.investment_sensitivity,
            government_borrowing=self.government_borrowing
            + additional_borrowing,
        )
        after = new_model.equilibrium()

        return {
            'additional_borrowing': additional_borrowing,
            'before': before,
            'after': after,
            'interest_rate_change': after['interest_rate'] - before['interest_rate'],
            'investment_change': after['investment'] - before['investment'],
            'crowding_out': before['investment'] - after['investment'],
            'interpretation': (
                f"政府借款增加 {additional_borrowing:.0f} 使可贷资金需求右移，"
                f"均衡利率从 {before['interest_rate']:.2f}% 升至 "
                f"{after['interest_rate']:.2f}%，私人投资从 {before['investment']:.2f} "
                f"降至 {after['investment']:.2f} (挤出 {before['investment'] - after['investment']:.2f})。"
            ),
        }

    def with_tax_incentive(self, savings_increase: float) -> dict:
        """
        鼓励储蓄的税收激励

        税收优惠使储蓄供给右移: 均衡利率下降，投资增加。
        """
        if savings_increase < 0:
            raise ValueError("储蓄增加量不能为负")

        before = self.equilibrium()
        new_model = LoanableFundsModel(
            savings_autonomous=self.savings_autonomous + savings_increase,
            savings_sensitivity=self.savings_sensitivity,
            investment_autonomous=self.investment_autonomous,
            investment_sensitivity=self.investment_sensitivity,
            government_borrowing=self.government_borrowing,
        )
        after = new_model.equilibrium()

        return {
            'savings_increase': savings_increase,
            'before': before,
            'after': after,
            'interest_rate_change': after['interest_rate'] - before['interest_rate'],
            'investment_change': after['investment'] - before['investment'],
            'interpretation': (
                f"税收激励使储蓄增加 {savings_increase:.0f}，供给右移，"
                f"均衡利率从 {before['interest_rate']:.2f}% 降至 "
                f"{after['interest_rate']:.2f}%，投资从 {before['investment']:.2f} "
                f"增至 {after['investment']:.2f}。"
            ),
        }

    def analyze(self) -> dict:
        """生成可贷资金市场完整分析"""
        eq = self.equilibrium()
        return {
            'equilibrium': eq,
            'savings_function': (f"S(r) = {self.savings_autonomous:.0f} + "
                                 f"{self.savings_sensitivity:.0f}·r"),
            'investment_function': (f"I(r) = {self.investment_autonomous:.0f} - "
                                    f"{self.investment_sensitivity:.0f}·r"),
            'government_borrowing': self.government_borrowing,
            'interpretation': (
                f"可贷资金市场均衡利率为 {eq['interest_rate']*100:.1f}%。"
                f"储蓄 (资金供给) {eq['savings']:.1f} = "
                f"投资 ({eq['investment']:.1f}) + 政府借款 "
                f"({self.government_borrowing:.1f})。"
            ),
        }

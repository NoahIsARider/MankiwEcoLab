"""
IS-LM 模型
The IS-LM Model

对应曼昆《经济学原理》宏观分册:
- 第33章 总需求与总供给 (Aggregate Demand and Aggregate Supply) - IS-LM 是 AD 曲线的推导基础
- 第34章 货币与财政政策对总需求的影响

核心概念:
- IS 曲线: 商品市场均衡, Y 与 r 负相关
  Y = C + I + G
  C = a + b*(Y - T), T = t*Y
  I = d - e*r
- LM 曲线: 货币市场均衡, Y 与 r 正相关
  M/P = k*Y - h*r
- IS-LM 交点决定短期均衡 (Y*, r*)
- 财政政策使 IS 移动, 货币政策使 LM 移动
"""

from dataclasses import dataclass


@dataclass
class ISLMModel:
    """
    IS-LM 模型 (线性)

    Attributes:
        consumption_autonomous: 自主消费 a
        marginal_propensity_to_consume: 边际消费倾向 b (0<b<1)
        tax_rate: 税率 t (0<=t<1)
        investment_autonomous: 自主投资 d
        investment_sensitivity: 投资对利率敏感度 e
        government_spending: 政府购买 G
        real_money_supply: 实际货币供给 M/P
        money_demand_income: 货币需求的收入敏感度 k
        money_demand_interest: 货币需求的利率敏感度 h
    """
    consumption_autonomous: float = 100.0
    marginal_propensity_to_consume: float = 0.8
    tax_rate: float = 0.25
    investment_autonomous: float = 200.0
    investment_sensitivity: float = 1000.0
    government_spending: float = 300.0
    real_money_supply: float = 500.0
    money_demand_income: float = 0.5
    money_demand_interest: float = 200.0

    def __post_init__(self):
        if not 0 < self.marginal_propensity_to_consume < 1:
            raise ValueError("边际消费倾向必须介于 0 和 1 之间")
        if not 0 <= self.tax_rate < 1:
            raise ValueError("税率必须介于 0 和 1 之间")
        if self.investment_sensitivity <= 0:
            raise ValueError("投资对利率的敏感度必须为正数")
        if self.real_money_supply <= 0:
            raise ValueError("实际货币供给必须为正数")
        if self.money_demand_income <= 0:
            raise ValueError("货币需求收入敏感度必须为正数")
        if self.money_demand_interest <= 0:
            raise ValueError("货币需求利率敏感度必须为正数")

    @property
    def _multiplier_denominator(self) -> float:
        """1 - b*(1-t): 支出乘数分母"""
        return 1.0 - self.marginal_propensity_to_consume * (1 - self.tax_rate)

    @property
    def is_intercept(self) -> float:
        """IS 曲线截距 A = (a + d + G) / (1 - b(1-t))"""
        numerator = (self.consumption_autonomous
                     + self.investment_autonomous
                     + self.government_spending)
        return numerator / self._multiplier_denominator

    @property
    def is_slope_abs(self) -> float:
        """IS 曲线斜率绝对值 B = e / (1 - b(1-t))"""
        return self.investment_sensitivity / self._multiplier_denominator

    def is_curve(self, rate: float) -> float:
        """IS 曲线: Y = A - B*r"""
        return self.is_intercept - self.is_slope_abs * rate

    def lm_curve(self, rate: float) -> float:
        """LM 曲线: Y = (M/P)/k + (h/k)*r"""
        return (self.real_money_supply / self.money_demand_income
                + (self.money_demand_interest / self.money_demand_income) * rate)

    def equilibrium(self) -> dict:
        """
        短期 IS-LM 均衡

        联立: Y = A - B*r  且  Y = (M/P)/k + (h/k)*r
        r* = (A - (M/P)/k) / (B + h/k)
        """
        numerator = self.is_intercept - self.real_money_supply / self.money_demand_income
        denominator = self.is_slope_abs + self.money_demand_interest / self.money_demand_income
        if denominator <= 0:
            raise ValueError("IS 与 LM 曲线平行，无均衡")
        rate = max(0.0, numerator / denominator)
        output = self.is_curve(rate)
        return {'output': output, 'interest_rate': rate}

    def verify_on_curves(self, tol: float = 1e-6) -> bool:
        """
        验证均衡点同时位于 IS 与 LM 曲线上
        """
        eq = self.equilibrium()
        return (abs(self.is_curve(eq['interest_rate']) - eq['output']) <= tol
                and abs(self.lm_curve(eq['interest_rate']) - eq['output']) <= tol)

    def fiscal_policy(self, spending_change: float = 50.0) -> dict:
        """
        扩张性财政政策 (政府购买增加)

        使 IS 右移 -> 均衡产出上升, 利率上升 (挤出效应)
        """
        new_model = ISLMModel(
            consumption_autonomous=self.consumption_autonomous,
            marginal_propensity_to_consume=self.marginal_propensity_to_consume,
            tax_rate=self.tax_rate,
            investment_autonomous=self.investment_autonomous,
            investment_sensitivity=self.investment_sensitivity,
            government_spending=self.government_spending + spending_change,
            real_money_supply=self.real_money_supply,
            money_demand_income=self.money_demand_income,
            money_demand_interest=self.money_demand_interest,
        )
        before = self.equilibrium()
        after = new_model.equilibrium()
        return {
            'spending_change': spending_change,
            'before': before,
            'after': after,
            'output_change': after['output'] - before['output'],
            'interest_rate_change': after['interest_rate'] - before['interest_rate'],
            'interpretation': (
                f"政府购买增加 {spending_change:.0f} 使 IS 右移，"
                f"均衡产出从 {before['output']:.2f} 升至 {after['output']:.2f}，"
                f"利率从 {before['interest_rate']*100:.2f}% 升至 "
                f"{after['interest_rate']*100:.2f}% (部分挤出私人投资)。"
            ),
        }

    def monetary_policy(self, money_supply_change: float = 100.0) -> dict:
        """
        扩张性货币政策 (货币供给增加)

        使 LM 右移 -> 均衡产出上升, 利率下降
        """
        new_model = ISLMModel(
            consumption_autonomous=self.consumption_autonomous,
            marginal_propensity_to_consume=self.marginal_propensity_to_consume,
            tax_rate=self.tax_rate,
            investment_autonomous=self.investment_autonomous,
            investment_sensitivity=self.investment_sensitivity,
            government_spending=self.government_spending,
            real_money_supply=self.real_money_supply + money_supply_change,
            money_demand_income=self.money_demand_income,
            money_demand_interest=self.money_demand_interest,
        )
        before = self.equilibrium()
        after = new_model.equilibrium()
        return {
            'money_supply_change': money_supply_change,
            'before': before,
            'after': after,
            'output_change': after['output'] - before['output'],
            'interest_rate_change': after['interest_rate'] - before['interest_rate'],
            'interpretation': (
                f"货币供给增加 {money_supply_change:.0f} 使 LM 右移，"
                f"均衡产出从 {before['output']:.2f} 升至 {after['output']:.2f}，"
                f"利率从 {before['interest_rate']*100:.2f}% 降至 "
                f"{after['interest_rate']*100:.2f}% (刺激投资)。"
            ),
        }

    def analyze(self) -> dict:
        """生成 IS-LM 模型完整分析"""
        eq = self.equilibrium()
        return {
            'equilibrium': eq,
            'is_curve': {
                'intercept': self.is_intercept,
                'slope_abs': self.is_slope_abs,
                'equation': f"Y = {self.is_intercept:.2f} - {self.is_slope_abs:.2f}·r",
            },
            'lm_curve': {
                'equation': (f"Y = {self.real_money_supply / self.money_demand_income:.2f} "
                             f"+ {(self.money_demand_interest / self.money_demand_income):.2f}·r"),
            },
            'spending_multiplier': 1.0 / self._multiplier_denominator,
            'interpretation': (
                f"IS-LM 短期均衡: 产出 Y* = {eq['output']:.2f}, "
                f"利率 r* = {eq['interest_rate']*100:.2f}%。"
                f"IS 与 LM 同时出清商品与货币市场。"
            ),
        }

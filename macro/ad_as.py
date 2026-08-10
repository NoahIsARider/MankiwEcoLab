"""
总需求-总供给模型
Aggregate Demand - Aggregate Supply Model

对应曼昆《经济学原理》宏观分册:
- 第33章 总需求与总供给 (Aggregate Demand and Aggregate Supply)

核心概念:
- 总需求曲线 AD: 物价水平与总需求量反向关系 (财富效应、利率效应、汇率效应)
- 短期总供给曲线 SRAS: 工资黏性假设下，短期向上倾斜
- 长期总供给曲线 LRAS: 在潜在产出处垂直
- 经济波动: 需求冲击使短期偏离均衡，长期自动回归潜在产出
"""

from dataclasses import dataclass


@dataclass
class ADASModel:
    """
    总需求-总供给模型 (线性近似)

    AD 曲线:  Y = a - b * P
    SRAS 曲线: Y = c + d * P  (向上倾斜)
    LRAS:     Y = Y_potential (垂直，在潜在产出处)

    Attributes:
        potential_output: 潜在产出 Y*
        ad_intercept: AD 曲线截距 a
        ad_slope: AD 曲线斜率绝对值 b
        sras_intercept: SRAS 曲线截距 c
        sras_slope: SRAS 曲线斜率 d
    """
    potential_output: float = 100.0
    ad_intercept: float = 150.0
    ad_slope: float = 0.5
    sras_intercept: float = 50.0
    sras_slope: float = 0.4

    def __post_init__(self):
        if self.ad_slope <= 0 or self.sras_slope <= 0:
            raise ValueError("曲线斜率必须为正")
        if self.potential_output <= 0:
            raise ValueError("潜在产出必须为正数")

    def ad_price(self, output: float) -> float:
        """AD 曲线上的价格水平: P = (a - Y) / b"""
        return (self.ad_intercept - output) / self.ad_slope

    def sras_price(self, output: float) -> float:
        """SRAS 曲线上的价格水平: P = (Y - c) / d"""
        return (output - self.sras_intercept) / self.sras_slope

    def lras_price(self) -> float:
        """长期均衡价格水平: 在潜在产出处 AD 与 LRAS 相交"""
        return self.ad_price(self.potential_output)

    def short_run_equilibrium(self) -> dict:
        """
        短期均衡: AD 与 SRAS 相交

        求解 a - b*P = c + d*P
        => P = (a - c) / (b + d)
        """
        price = (self.ad_intercept - self.sras_intercept) / \
                (self.ad_slope + self.sras_slope)
        output = self.ad_intercept - self.ad_slope * price
        return {'price': price, 'output': output}

    def long_run_equilibrium(self) -> dict:
        """
        长期均衡: AD 与 LRAS 相交 (产出 = 潜在产出)
        """
        price = self.lras_price()
        return {'price': price, 'output': self.potential_output}

    def output_gap(self) -> float:
        """
        产出缺口 (实际产出与潜在产出之差)

        正缺口 = 经济过热; 负缺口 = 经济衰退
        """
        sr = self.short_run_equilibrium()
        return sr['output'] - self.potential_output

    def demand_shock(self, shift: float = 10.0) -> dict:
        """
        正向需求冲击 (如扩张性财政政策、乐观预期)

        使 AD 曲线右移 shift 单位:
        Y = (a + shift) - b * P

        短期: 产出上升至新的均衡; 长期: 产出回归潜在产出。
        """
        new_ad_intercept = self.ad_intercept + shift
        price = (new_ad_intercept - self.sras_intercept) / \
                (self.ad_slope + self.sras_slope)
        short_output = new_ad_intercept - self.ad_slope * price
        long_price = (new_ad_intercept - self.potential_output) / self.ad_slope

        return {
            'short_run': {'price': price, 'output': short_output},
            'long_run': {'price': long_price, 'output': self.potential_output},
            'interpretation': (
                f"需求冲击使短期产出上升至 {short_output:.2f}，"
                f"物价上升至 {price:.2f}；长期产出回归潜在产出 "
                f"{self.potential_output:.2f}，物价继续上升至 {long_price:.2f}。"
            ),
        }

    def supply_shock(self, shift: float = 10.0) -> dict:
        """
        负向供给冲击 (如油价上涨、工资上升)

        使 SRAS 曲线左移/上移，在同等产出下价格更高:
        Y = c - shift + d * P

        短期: 产出下降、物价上升 (滞胀); 长期: SRAS 恢复。
        """
        new_sras_intercept = self.sras_intercept - shift
        price = (self.ad_intercept - new_sras_intercept) / \
                (self.ad_slope + self.sras_slope)
        short_output = self.ad_intercept - self.ad_slope * price

        return {
            'short_run': {'price': price, 'output': short_output},
            'long_run': {'price': self.lras_price(), 'output': self.potential_output},
            'interpretation': (
                f"负向供给冲击使短期产出下降至 {short_output:.2f}，"
                f"物价上升至 {price:.2f} (滞胀)；长期产出回归潜在产出。"
            ),
        }

    def analyze(self) -> dict:
        """生成模型分析"""
        sr = self.short_run_equilibrium()
        lr = self.long_run_equilibrium()
        gap = self.output_gap()
        return {
            'short_run': sr,
            'long_run': lr,
            'output_gap': gap,
            'potential_output': self.potential_output,
            'recession': gap < 0,
            'interpretation': (
                f"短期均衡产出 {sr['output']:.2f}，物价 {sr['price']:.2f}；"
                f"长期均衡产出 {lr['output']:.2f}，物价 {lr['price']:.2f}。"
                f"产出缺口 {gap:+.2f}，经济处于"
                f"{'衰退' if gap < 0 else '扩张'}状态。"
            ),
        }

"""
比较优势与贸易
Comparative Advantage and Trade

对应曼昆《经济学原理》十大原理:
- 原理5: 贸易能使每个人状况更好 (Trade can make everyone better off)
- 原理1/2: 机会成本与权衡取舍

核心概念:
- 绝对优势 (Absolute Advantage): 用更少资源生产同量商品的能力
- 比较优势 (Comparative Advantage): 以更低机会成本生产商品的能力
- 贸易收益 (Gains from Trade): 专业化分工后双方都能获益
"""

from dataclasses import dataclass


@dataclass
class ProducerProfile:
    """
    一个生产者 (国家或个人) 的生产能力档案

    Attributes:
        name: 生产者名称
        output_x_per_hour: 每小时生产 X 的数量
        output_y_per_hour: 每小时生产 Y 的数量
        hours_available: 可用生产时间
    """
    name: str
    output_x_per_hour: float
    output_y_per_hour: float
    hours_available: float = 40.0

    def __post_init__(self):
        if self.output_x_per_hour <= 0 or self.output_y_per_hour <= 0:
            raise ValueError("每小时产出必须为正数")
        if self.hours_available <= 0:
            raise ValueError("可用时间必须为正数")

    @property
    def opportunity_cost_x(self) -> float:
        """
        多生产一单位 X 的机会成本 (以 Y 计)

        生产 1 单位 X 需要 1/output_x_per_hour 小时，
        这些时间原本可生产 output_y_per_hour / output_x_per_hour 单位 Y。
        """
        return self.output_y_per_hour / self.output_x_per_hour

    @property
    def opportunity_cost_y(self) -> float:
        """多生产一单位 Y 的机会成本 (以 X 计)"""
        return self.output_x_per_hour / self.output_y_per_hour

    def autarky_bundle(self, fraction_x: float = 0.5):
        """
        自给自足下的产出组合 (无贸易)

        Args:
            fraction_x: 投入生产 X 的时间比例 (0-1)

        Returns:
            (x_units, y_units)
        """
        if not 0 <= fraction_x <= 1:
            raise ValueError("fraction_x 必须在 0 到 1 之间")
        hours_x = self.hours_available * fraction_x
        hours_y = self.hours_available * (1 - fraction_x)
        return (hours_x * self.output_x_per_hour,
                hours_y * self.output_y_per_hour)


class TradeModel:
    """
    双边贸易模型

    分析两个生产者之间的比较优势与贸易收益:
    1. 计算双方各自的比较优势
    2. 设计专业化分工方案
    3. 量化贸易收益
    """

    def __init__(self, producer_a: ProducerProfile, producer_b: ProducerProfile):
        self.producer_a = producer_a
        self.producer_b = producer_b

    def _comparative_advantage_x(self):
        """谁在 X 上具有比较优势 (X 机会成本更低者)"""
        if self.producer_a.opportunity_cost_x < self.producer_b.opportunity_cost_x:
            return self.producer_a.name
        elif self.producer_b.opportunity_cost_x < self.producer_a.opportunity_cost_x:
            return self.producer_b.name
        return None

    def _comparative_advantage_y(self):
        """谁在 Y 上具有比较优势"""
        if self.producer_a.opportunity_cost_y < self.producer_b.opportunity_cost_y:
            return self.producer_a.name
        elif self.producer_b.opportunity_cost_y < self.producer_a.opportunity_cost_y:
            return self.producer_b.name
        return None

    def absolute_advantage(self) -> dict:
        """分析双方的绝对优势"""
        result = {}
        result['X'] = max(
            (self.producer_a, self.producer_b),
            key=lambda p: p.output_x_per_hour
        ).name
        result['Y'] = max(
            (self.producer_a, self.producer_b),
            key=lambda p: p.output_y_per_hour
        ).name
        return result

    def comparative_advantage(self) -> dict:
        """分析双方的比较优势"""
        return {
            'X': self._comparative_advantage_x(),
            'Y': self._comparative_advantage_y(),
        }

    def specialization_plan(self) -> dict:
        """
        专业化分工方案

        比较优势生产者集中生产各自优势商品，无优势方的时间按需分配。
        返回各自应投入生产 X 的时间比例。
        """
        adv_x = self._comparative_advantage_x()
        adv_y = self._comparative_advantage_y()

        plan = {
            'A_fraction_x': 0.0,
            'B_fraction_x': 0.0,
            'logic': ''
        }

        if adv_x == self.producer_a.name:
            plan['A_fraction_x'] = 1.0
            if adv_y == self.producer_b.name:
                plan['B_fraction_x'] = 0.0
            else:
                plan['B_fraction_x'] = 0.5
        else:
            plan['B_fraction_x'] = 1.0
            if adv_y == self.producer_a.name:
                plan['A_fraction_x'] = 0.0
            else:
                plan['A_fraction_x'] = 0.5

        plan['logic'] = (
            f"{adv_x} 在 X 上具有比较优势，{adv_y} 在 Y 上具有比较优势；"
            f"专业化生产各自优势商品后再进行交换。"
        )
        return plan

    def total_production(self, specialization: bool = True) -> dict:
        """
        计算总产量

        Args:
            specialization: True 使用专业化分工，False 使用自给自足

        Returns:
            两种商品的总产量
        """
        if specialization:
            plan = self.specialization_plan()
            fa = plan['A_fraction_x']
            fb = plan['B_fraction_x']
        else:
            fa = fb = 0.5

        ax, ay = self.producer_a.autarky_bundle(fa)
        bx, by = self.producer_b.autarky_bundle(fb)

        return {'X': ax + bx, 'Y': ay + by}

    def gains_from_trade(self) -> dict:
        """
        计算贸易收益

        比较自给自足与专业化分工的总产量差异。
        """
        autarky = self.total_production(specialization=False)
        specialized = self.total_production(specialization=True)

        gains_x = specialized['X'] - autarky['X']
        gains_y = specialized['Y'] - autarky['Y']

        return {
            'autarky_X': autarky['X'],
            'autarky_Y': autarky['Y'],
            'specialized_X': specialized['X'],
            'specialized_Y': specialized['Y'],
            'gain_X': gains_x,
            'gain_Y': gains_y,
            'total_gain_X_percent': (gains_x / autarky['X'] * 100) if autarky['X'] else 0,
            'total_gain_Y_percent': (gains_y / autarky['Y'] * 100) if autarky['Y'] else 0,
            'trade_benefits_both': gains_x >= 0 and gains_y >= 0,
        }

    def analyze(self) -> dict:
        """生成完整的贸易分析报告"""
        report = {
            'absolute_advantage': self.absolute_advantage(),
            'comparative_advantage': self.comparative_advantage(),
            'specialization_plan': self.specialization_plan(),
            'gains': self.gains_from_trade(),
        }
        return report

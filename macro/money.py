"""
货币与银行体系
Money and the Banking System

对应曼昆《经济学原理》宏观分册:
- 第29章 货币制度 (The Monetary System)

核心概念:
- 货币职能: 交换媒介、计价单位、价值储藏
- 存款准备金制度
- 货币乘数 = 1 / 准备金率
- 货币创造过程: 银行体系将 1 元存款放大为 1/准备金率 元的货币供给
"""

from dataclasses import dataclass


@dataclass
class MoneyCreationModel:
    """
    货币创造模型

    央行发行基础货币 (高能货币)，商业银行体系通过贷款将货币放大。

    Attributes:
        reserve_ratio: 法定存款准备金率 (0-1)
        initial_deposit: 初始存款 (基础货币)
        currency_deposit_ratio: 现金持有率 (0-1), 0 表示所有货币留在银行体系
    """
    reserve_ratio: float = 0.10
    initial_deposit: float = 1000.0
    currency_deposit_ratio: float = 0.0

    def __post_init__(self):
        if not 0 < self.reserve_ratio < 1:
            raise ValueError("准备金率必须介于 0 和 1 之间")
        if self.initial_deposit <= 0:
            raise ValueError("初始存款必须为正数")
        if not 0 <= self.currency_deposit_ratio < 1:
            raise ValueError("现金持有率必须介于 0 和 1 之间")

    @property
    def deposit_multiplier(self) -> float:
        """简单存款乘数 = 1 / 准备金率"""
        return 1.0 / self.reserve_ratio

    @property
    def money_multiplier(self) -> float:
        """
        广义货币乘数 (考虑现金持有)

        m = 1 / (准备金率 + 现金持有率)
        当现金持有率为 0 时，等于存款乘数。
        """
        return 1.0 / (self.reserve_ratio + self.currency_deposit_ratio)

    @property
    def total_money_supply(self) -> float:
        """货币总供给 = 基础货币 * 货币乘数"""
        return self.initial_deposit * self.money_multiplier

    @property
    def total_loans(self) -> float:
        """
        银行体系创造的贷款总量

        贷款 = 总存款 - 准备金 = 初始存款 * (1 - 准备金率) / (准备金率 + 现金率)
        """
        return self.initial_deposit * (1 - self.reserve_ratio) / \
               (self.reserve_ratio + self.currency_deposit_ratio)

    def deposit_creation_rounds(self, max_rounds: int = 12) -> list:
        """
        逐轮展示货币创造过程

        每一轮: 存款 -> 保留准备金 -> 贷出剩余
        贷出的钱再次成为下一轮存款。

        Returns:
            每轮 (存款, 准备金, 贷款) 列表
        """
        rounds = []
        deposit = self.initial_deposit
        total_deposits = 0.0
        for _ in range(max_rounds):
            if deposit < 1e-9:
                break
            reserves = deposit * self.reserve_ratio
            loans = deposit * (1 - self.reserve_ratio)
            # 考虑现金持有: 部分贷款以现金形式流出银行体系
            cash_out = loans * self.currency_deposit_ratio
            next_deposit = loans - cash_out
            rounds.append({
                'round': len(rounds) + 1,
                'deposit': deposit,
                'reserves': reserves,
                'loans': loans,
            })
            total_deposits += deposit
            deposit = next_deposit
        return rounds

    def analyze(self) -> dict:
        """生成货币创造分析"""
        return {
            'reserve_ratio': self.reserve_ratio,
            'initial_deposit': self.initial_deposit,
            'deposit_multiplier': self.deposit_multiplier,
            'money_multiplier': self.money_multiplier,
            'total_money_supply': self.total_money_supply,
            'total_loans': self.total_loans,
            'interpretation': (
                f"准备金率 {self.reserve_ratio*100:.0f}% 下，存款乘数为 "
                f"{self.deposit_multiplier:.2f}。初始存款 {self.initial_deposit:.0f} 元"
                f"最终可创造约 {self.total_money_supply:.0f} 元的货币供给。"
            ),
        }

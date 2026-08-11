"""
博弈论与寡头竞争
Game Theory and Oligopoly Competition

对应曼昆《经济学原理》微观分册:
- 第17章 寡头 (Oligopoly) - 博弈论与纳什均衡
- 原理5: 贸易能使每个人状况更好 (通过合作实现共赢)
- 原理7: 政府有时可以改善市场结果 (防止串谋)

核心概念:
- 占优策略 (Dominant Strategy): 无论对手如何选择都最优的策略
- 纳什均衡 (Nash Equilibrium): 每个参与者在他人策略不变时都没有动机偏离
- 囚徒困境 (Prisoner's Dilemma): 个人理性导致集体非理性
- 混合策略均衡 (Mixed Strategy Equilibrium): 随机化选择策略
- 古诺博弈 (Cournot Game): 寡头产量竞争
"""


import numpy as np


class NormalFormGame:
    """
    两人两策略 (2x2) 标准式博弈

    参与者 A 的策略: 1, 2；参与者 B 的策略: 1, 2
    payoff_a[i][j]: A 在 (A_i, B_j) 下的收益
    payoff_b[i][j]: B 在 (A_i, B_j) 下的收益

    Attributes:
        payoff_a: A 的收益矩阵 (2x2)
        payoff_b: B 的收益矩阵 (2x2)
    """

    def __init__(self, payoff_a: np.ndarray, payoff_b: np.ndarray,
                 strategies_a: tuple = None, strategies_b: tuple = None):
        self.payoff_a = np.asarray(payoff_a, dtype=float)
        self.payoff_b = np.asarray(payoff_b, dtype=float)
        if self.payoff_a.shape != (2, 2) or self.payoff_b.shape != (2, 2):
            raise ValueError("收益矩阵必须是 2x2")

        self.strategies_a = strategies_a or ('A1', 'A2')
        self.strategies_b = strategies_b or ('B1', 'B2')
        if (len(self.strategies_a) != 2 or len(self.strategies_b) != 2):
            raise ValueError("策略名称必须恰好 2 个")

    def payoff(self, strategy_a: int, strategy_b: int) -> dict:
        """
        给定策略组合的收益

        Args:
            strategy_a: A 的策略索引 (0 或 1)
            strategy_b: B 的策略索引 (0 或 1)

        Returns:
            {'A': ..., 'B': ...}
        """
        return {
            'A': float(self.payoff_a[strategy_a][strategy_b]),
            'B': float(self.payoff_b[strategy_a][strategy_b]),
        }

    def _best_responses(self, player: str) -> list:
        """计算某个参与者在对手每个策略下的最优反应集合"""
        if player == 'A':
            best = []
            for j in range(2):
                col = self.payoff_a[:, j]
                best.append([i for i in range(2)
                             if col[i] >= col.max() - 1e-9])
            return best
        else:
            best = []
            for i in range(2):
                row = self.payoff_b[i, :]
                best.append([j for j in range(2)
                             if row[j] >= row.max() - 1e-9])
            return best

    def dominant_strategies(self) -> dict:
        """
        占优策略分析

        Returns:
            {'A': 索引或 None, 'B': 索引或 None, 'explanation': ...}
        """
        result = {'A': None, 'B': None}
        a1_better = (self.payoff_a[0, 0] > self.payoff_a[1, 0] and
                     self.payoff_a[0, 1] > self.payoff_a[1, 1])
        a2_better = (self.payoff_a[1, 0] > self.payoff_a[0, 0] and
                     self.payoff_a[1, 1] > self.payoff_a[0, 1])
        if a1_better:
            result['A'] = 0
        elif a2_better:
            result['A'] = 1

        b1_better = (self.payoff_b[0, 0] > self.payoff_b[0, 1] and
                     self.payoff_b[1, 0] > self.payoff_b[1, 1])
        b2_better = (self.payoff_b[0, 1] > self.payoff_b[0, 0] and
                     self.payoff_b[1, 1] > self.payoff_b[1, 0])
        if b1_better:
            result['B'] = 0
        elif b2_better:
            result['B'] = 1

        return result

    def has_dominant_strategy_equilibrium(self) -> bool:
        """是否存在占优策略均衡"""
        dom = self.dominant_strategies()
        return dom['A'] is not None and dom['B'] is not None

    def pure_nash_equilibria(self) -> list:
        """
        纯策略纳什均衡

        策略组合 (i, j) 是纳什均衡当且仅当:
        - i 是 A 对 B_j 的最优反应
        - j 是 B 对 A_i 的最优反应

        Returns:
            均衡列表，每项 {'A': 索引, 'B': 索引, 'payoff': {...}}
        """
        best_a = self._best_responses('A')
        best_b = self._best_responses('B')

        equilibria = []
        for i in range(2):
            for j in range(2):
                if i in best_a[j] and j in best_b[i]:
                    equilibria.append({
                        'A': i,
                        'B': j,
                        'A_strategy': self.strategies_a[i],
                        'B_strategy': self.strategies_b[j],
                        'payoff': self.payoff(i, j),
                    })
        return equilibria

    def mixed_strategy_equilibrium(self) -> dict:
        """
        混合策略纳什均衡 (2x2 博弈)

        A 以概率 p 选择策略 1；B 以概率 q 选择策略 1。
        通过无差异条件求解:
        p = (B22 - B21) / (B11 - B12 + B22 - B21)
        q = (A22 - A12) / (A11 - A21 + A22 - A12)

        Returns:
            {'p': ..., 'q': ..., 'valid': bool, 'payoff_A': ..., 'payoff_B': ...}
        """
        a = self.payoff_a
        b = self.payoff_b

        denom_p = b[0, 0] - b[0, 1] + b[1, 1] - b[1, 0]
        denom_q = a[0, 0] - a[1, 0] + a[1, 1] - a[0, 1]

        if abs(denom_p) < 1e-12 or abs(denom_q) < 1e-12:
            return {'p': None, 'q': None, 'valid': False,
                    'payoff_A': None, 'payoff_B': None,
                    'reason': '退化博弈，无内部混合策略均衡'}

        p = (b[1, 1] - b[1, 0]) / denom_p
        q = (a[1, 1] - a[0, 1]) / denom_q

        valid = 0 <= p <= 1 and 0 <= q <= 1

        # 在混合均衡处双方收益
        payoff_a = q * (p * a[0, 0] + (1 - p) * a[1, 0]) \
            + (1 - q) * (p * a[0, 1] + (1 - p) * a[1, 1])
        payoff_b = p * (q * b[0, 0] + (1 - q) * b[0, 1]) \
            + (1 - p) * (q * b[1, 0] + (1 - q) * b[1, 1])

        return {'p': float(p), 'q': float(q), 'valid': bool(valid),
                'payoff_A': float(payoff_a), 'payoff_B': float(payoff_b)}

    def pareto_optimal(self) -> list:
        """
        帕累托最优策略组合

        一个策略组合是帕累托最优的，如果不存在其他组合使双方都不变差
        且至少一方变好。
        """
        outcomes = [(i, j, float(self.payoff_a[i, j]), float(self.payoff_b[i, j]))
                    for i in range(2) for j in range(2)]

        optimal = []
        for i, j, pa, pb in outcomes:
            dominated = False
            for i2, j2, pa2, pb2 in outcomes:
                if (i2, j2) == (i, j):
                    continue
                if pa2 >= pa and pb2 >= pb and (pa2 > pa or pb2 > pb):
                    dominated = True
                    break
            if not dominated:
                optimal.append({
                    'A': i, 'B': j,
                    'A_strategy': self.strategies_a[i],
                    'B_strategy': self.strategies_b[j],
                    'payoff': {'A': pa, 'B': pb},
                })
        return optimal

    def analyze(self) -> dict:
        """生成完整博弈分析"""
        dom = self.dominant_strategies()
        nash = self.pure_nash_equilibria()
        mixed = self.mixed_strategy_equilibrium()
        pareto = self.pareto_optimal()

        return {
            'payoff_matrix': {
                'A': self.payoff_a.tolist(),
                'B': self.payoff_b.tolist(),
            },
            'dominant_strategies': dom,
            'dominant_strategy_equilibrium': self.has_dominant_strategy_equilibrium(),
            'pure_nash_equilibria': nash,
            'mixed_strategy_equilibrium': mixed,
            'pareto_optimal': pareto,
            'num_nash_equilibria': len(nash),
        }


def prisoners_dilemma() -> NormalFormGame:
    """
    经典囚徒困境

    策略: 沉默 (0) 或 招供 (1)
    A 的收益矩阵 (years in prison, 负值表示越少越好):
    - 双方沉默: (-1, -1)
    - A 招供 B 沉默: (0, -5)
    - A 沉默 B 招供: (-5, 0)
    - 双方招供: (-3, -3)

    Returns:
        NormalFormGame 实例
    """
    payoff_a = np.array([[-1.0, -5.0],
                         [0.0, -3.0]])
    payoff_b = np.array([[-1.0, 0.0],
                         [-5.0, -3.0]])
    return NormalFormGame(payoff_a, payoff_b,
                          strategies_a=('Silent', 'Confess'),
                          strategies_b=('Silent', 'Confess'))


def matching_pennies() -> NormalFormGame:
    """
    抛硬币配对 (零和博弈)

    A 赢: +1；B 赢: -1。
    只有混合策略均衡。
    """
    payoff_a = np.array([[1.0, -1.0],
                         [-1.0, 1.0]])
    payoff_b = np.array([[-1.0, 1.0],
                         [1.0, -1.0]])
    return NormalFormGame(payoff_a, payoff_b,
                          strategies_a=('Heads', 'Tails'),
                          strategies_b=('Heads', 'Tails'))


class CournotGame:
    """
    古诺寡头产量竞争博弈

    市场需求: P = a - b * Q, Q = Σ q_i
    每家企业成本: C(q) = c * q

    企业 i 的最优反应函数:
    q_i = (a - c - b * Σ_{j≠i} q_j) / (2b)

    对称纳什均衡:
    q* = (a - c) / (b * (n + 1))
    """

    def __init__(self, num_firms: int = 2, demand_intercept: float = 100.0,
                 demand_slope: float = 1.0, marginal_cost: float = 20.0):
        if num_firms < 1:
            raise ValueError("企业数量必须至少为 1")
        if demand_intercept <= 0 or demand_slope <= 0:
            raise ValueError("需求参数必须为正数")
        if marginal_cost < 0:
            raise ValueError("边际成本不能为负")

        self.num_firms = num_firms
        self.demand_intercept = demand_intercept
        self.demand_slope = demand_slope
        self.marginal_cost = marginal_cost

    def best_response(self, others_total: float) -> float:
        """
        最优反应函数: q_i = (a - c - b*Q_{-i}) / (2b)
        """
        return max(0.0, (self.demand_intercept - self.marginal_cost
                         - self.demand_slope * others_total)
                   / (2 * self.demand_slope))

    def nash_equilibrium(self) -> dict:
        """
        对称纳什均衡

        q* = (a - c) / (b * (n + 1))
        """
        n = self.num_firms
        a = self.demand_intercept
        b = self.demand_slope
        c = self.marginal_cost

        q_star = max(0.0, (a - c) / (b * (n + 1)))
        q_total = n * q_star
        price = max(0.0, a - b * q_total)

        profit = (price - c) * q_star

        return {
            'num_firms': n,
            'per_firm_output': q_star,
            'total_output': q_total,
            'price': price,
            'per_firm_profit': profit,
            'total_profit': n * profit,
        }

    def collusion_output(self) -> dict:
        """
        串谋 (卡特尔) 结果: 相当于垄断

        Q_m = (a - c) / (2b)
        """
        a = self.demand_intercept
        b = self.demand_slope
        c = self.marginal_cost

        q_total = max(0.0, (a - c) / (2 * b))
        price = max(0.0, a - b * q_total)
        total_profit = (price - c) * q_total

        return {
            'total_output': q_total,
            'price': price,
            'total_profit': total_profit,
            'per_firm_profit': total_profit / self.num_firms,
        }

    def competitive_output(self) -> dict:
        """完全竞争结果: P = MC"""
        a = self.demand_intercept
        b = self.demand_slope
        c = self.marginal_cost

        q_total = max(0.0, (a - c) / b)
        return {
            'total_output': q_total,
            'price': c,
            'total_profit': 0.0,
        }

    def analyze(self) -> dict:
        """生成古诺博弈分析"""
        nash = self.nash_equilibrium()
        collusion = self.collusion_output()
        competitive = self.competitive_output()
        return {
            'nash_equilibrium': nash,
            'collusion': collusion,
            'competitive': competitive,
            'interpretation': (
                f"{self.num_firms} 家企业进行古诺竞争，纳什均衡价格 "
                f"{nash['price']:.2f}，总产量 {nash['total_output']:.2f}。"
                f"串谋价格 {collusion['price']:.2f} 更高、产量更低；"
                f"完全竞争价格 {competitive['price']:.2f} 最低。"
            ),
        }

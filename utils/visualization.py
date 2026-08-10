"""
可视化工具
Visualization utilities for economic simulations
"""

import os
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np


class EconomicsVisualizer:
    """
    经济学模拟可视化类
    
    提供各种图表绘制功能:
    - 供需曲线
    - 价格收敛过程
    - 市场剩余
    - 福利分配
    """

    def __init__(self, output_dir: str = 'output', figure_size: Tuple[int, int] = (15, 10),
                 dpi: int = 100, style: str = 'seaborn-v0_8-darkgrid'):
        """
        初始化可视化工具
        
        Args:
            output_dir: 输出目录
            figure_size: 图表大小
            dpi: 分辨率
            style: 绘图风格
        """
        self.output_dir = output_dir
        self.figure_size = figure_size
        self.dpi = dpi

        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)

        # 设置绘图风格
        try:
            if 'seaborn' in style:
                plt.style.use('ggplot')  # 使用替代风格
            else:
                plt.style.use(style)
        except Exception:
            plt.style.use('default')
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False

    def plot_supply_demand_curves(self, market, price_range: np.ndarray = None,
                                  save: bool = True, show: bool = True):
        """
        绘制供需曲线和均衡点
        """
        print("  - 绘制供需曲线...")
        if price_range is None:
            # 减少价格点数量以提高速度
            price_range = np.linspace(1, 200, 50)

        # 计算供需曲线
        print("    计算需求曲线...")
        demand_curve = market.get_demand_curve(price_range)
        print("    计算供给曲线...")
        supply_curve = market.get_supply_curve(price_range)

        # 当前价格和数量
        current_price = market.current_price
        current_quantity = market.quantity_history[-1] if market.quantity_history else 0

        # 绘图
        fig, ax = plt.subplots(figsize=(10, 8), dpi=self.dpi)

        # 供需曲线
        ax.plot(demand_curve, price_range, 'b-', linewidth=2, label='需求曲线 (Demand)')
        ax.plot(supply_curve, price_range, 'r-', linewidth=2, label='供给曲线 (Supply)')

        # 均衡点
        ax.plot(current_quantity, current_price, 'go', markersize=12,
               label=f'均衡点 (P*={current_price:.2f}, Q*={current_quantity:.2f})', zorder=5)

        # 均衡线
        ax.axhline(y=current_price, color='g', linestyle='--', alpha=0.5)
        ax.axvline(x=current_quantity, color='g', linestyle='--', alpha=0.5)

        # 标注
        ax.set_xlabel('数量 (Quantity)', fontsize=12)
        ax.set_ylabel('价格 (Price)', fontsize=12)
        ax.set_title('供需曲线和市场均衡 (Supply-Demand Curves and Market Equilibrium)', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save:
            plt.savefig(os.path.join(self.output_dir, 'supply_demand_curves.png'),
                       dpi=self.dpi, bbox_inches='tight')

        if show:
            plt.show()
        else:
            plt.close()

    def plot_price_convergence(self, market, save: bool = True, show: bool = True):
        """
        绘制价格收敛过程
        """
        print("  - 绘制价格收敛图...")
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), dpi=self.dpi)

        rounds = range(len(market.price_history))

        # 价格变化
        ax1.plot(rounds, market.price_history, 'b-', linewidth=2, label='市场价格')
        ax1.axhline(y=market.current_price, color='r', linestyle='--',
                   label=f'均衡价格 = {market.current_price:.2f}')
        ax1.set_xlabel('交易轮次 (Round)', fontsize=12)
        ax1.set_ylabel('价格 (Price)', fontsize=12)
        ax1.set_title('价格收敛过程 (Price Convergence Process)', fontsize=14, fontweight='bold')
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)

        # 供需变化
        if market.total_demand_history and market.total_supply_history:
            rounds_sd = range(len(market.total_demand_history))
            ax2.plot(rounds_sd, market.total_demand_history, 'b-', linewidth=2, label='总需求')
            ax2.plot(rounds_sd, market.total_supply_history, 'r-', linewidth=2, label='总供给')
            ax2.set_xlabel('交易轮次 (Round)', fontsize=12)
            ax2.set_ylabel('数量 (Quantity)', fontsize=12)
            ax2.set_title('供需数量变化 (Supply-Demand Quantity Changes)', fontsize=14, fontweight='bold')
            ax2.legend(fontsize=10)
            ax2.grid(True, alpha=0.3)

        plt.tight_layout()

        if save:
            plt.savefig(os.path.join(self.output_dir, 'price_convergence.png'),
                       dpi=self.dpi, bbox_inches='tight')

        if show:
            plt.show()
        else:
            plt.close()

    def plot_surplus(self, market, save: bool = True, show: bool = True):
        """
        绘制市场剩余变化
        """
        print("  - 绘制市场剩余图...")
        if not market.consumer_surplus_history or not market.producer_surplus_history:
            return

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), dpi=self.dpi)

        rounds = range(len(market.consumer_surplus_history))

        # 消费者剩余和生产者剩余
        ax1.plot(rounds, market.consumer_surplus_history, 'b-', linewidth=2, label='消费者剩余')
        ax1.plot(rounds, market.producer_surplus_history, 'r-', linewidth=2, label='生产者剩余')
        ax1.plot(rounds, market.total_surplus_history, 'g-', linewidth=2, label='总剩余')
        ax1.set_xlabel('交易轮次 (Round)', fontsize=12)
        ax1.set_ylabel('剩余 (Surplus)', fontsize=12)
        ax1.set_title('市场剩余变化 (Market Surplus Changes)', fontsize=14, fontweight='bold')
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)

        # 剩余比例 (饼图)
        final_cs = market.consumer_surplus_history[-1]
        final_ps = market.producer_surplus_history[-1]

        if final_cs + final_ps > 0:
            ax2.pie([final_cs, final_ps],
                   labels=['消费者剩余', '生产者剩余'],
                   autopct='%1.1f%%',
                   colors=['#3498db', '#e74c3c'],
                   startangle=90)
            ax2.set_title(f'最终剩余分配 (Final Surplus Distribution)\n'
                         f'消费者剩余: {final_cs:.2f}, 生产者剩余: {final_ps:.2f}',
                         fontsize=14, fontweight='bold')

        plt.tight_layout()

        if save:
            plt.savefig(os.path.join(self.output_dir, 'surplus_analysis.png'),
                       dpi=self.dpi, bbox_inches='tight')

        if show:
            plt.show()
        else:
            plt.close()

    def plot_transaction_volume(self, market, save: bool = True, show: bool = True):
        """
        绘制交易量变化
        """
        print("  - 绘制交易量图...")
        if not market.quantity_history:
            return

        fig, ax = plt.subplots(figsize=(10, 6), dpi=self.dpi)

        rounds = range(len(market.quantity_history))
        ax.plot(rounds, market.quantity_history, 'g-', linewidth=2, marker='o', markersize=4)
        ax.fill_between(rounds, market.quantity_history, alpha=0.3, color='green')

        ax.set_xlabel('交易轮次 (Round)', fontsize=12)
        ax.set_ylabel('交易量 (Transaction Volume)', fontsize=12)
        ax.set_title('市场交易量变化 (Market Transaction Volume)', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)

        # 添加统计信息
        avg_volume = np.mean(market.quantity_history)
        ax.axhline(y=avg_volume, color='r', linestyle='--', alpha=0.5,
                  label=f'平均交易量 = {avg_volume:.2f}')
        ax.legend(fontsize=10)

        plt.tight_layout()

        if save:
            plt.savefig(os.path.join(self.output_dir, 'transaction_volume.png'),
                       dpi=self.dpi, bbox_inches='tight')

        if show:
            plt.show()
        else:
            plt.close()

    def plot_agent_distributions(self, consumers: List, producers: List,
                                save: bool = True, show: bool = True):
        """
        绘制经济主体的参数分布
        """
        print("  - 绘制经济主体分布图...")
        fig, axes = plt.subplots(2, 3, figsize=self.figure_size, dpi=self.dpi)

        # 消费者收入分布
        incomes = [c.income for c in consumers]
        axes[0, 0].hist(incomes, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
        axes[0, 0].set_xlabel('收入 (Income)')
        axes[0, 0].set_ylabel('频数 (Frequency)')
        axes[0, 0].set_title('消费者收入分布')
        axes[0, 0].grid(True, alpha=0.3)

        # 消费者效用参数alpha分布
        alphas = [c.alpha for c in consumers]
        axes[0, 1].hist(alphas, bins=50, color='lightgreen', edgecolor='black', alpha=0.7)
        axes[0, 1].set_xlabel('效用参数 α')
        axes[0, 1].set_ylabel('频数')
        axes[0, 1].set_title('消费者效用参数分布')
        axes[0, 1].grid(True, alpha=0.3)

        # 消费者需求量分布
        demands = [c.quantity_demanded for c in consumers if c.quantity_demanded > 0]
        if demands:
            axes[0, 2].hist(demands, bins=50, color='salmon', edgecolor='black', alpha=0.7)
            axes[0, 2].set_xlabel('需求量 (Demand)')
            axes[0, 2].set_ylabel('频数')
            axes[0, 2].set_title('消费者需求量分布')
            axes[0, 2].grid(True, alpha=0.3)

        # 生产者固定成本分布
        fixed_costs = [p.fixed_cost for p in producers]
        axes[1, 0].hist(fixed_costs, bins=50, color='gold', edgecolor='black', alpha=0.7)
        axes[1, 0].set_xlabel('固定成本 (Fixed Cost)')
        axes[1, 0].set_ylabel('频数')
        axes[1, 0].set_title('生产者固定成本分布')
        axes[1, 0].grid(True, alpha=0.3)

        # 生产者边际成本参数分布
        mc_as = [p.mc_a for p in producers]
        axes[1, 1].hist(mc_as, bins=50, color='orchid', edgecolor='black', alpha=0.7)
        axes[1, 1].set_xlabel('边际成本参数 a')
        axes[1, 1].set_ylabel('频数')
        axes[1, 1].set_title('生产者边际成本分布')
        axes[1, 1].grid(True, alpha=0.3)

        # 生产者供给量分布
        supplies = [p.quantity_supplied for p in producers if p.quantity_supplied > 0]
        if supplies:
            axes[1, 2].hist(supplies, bins=50, color='lightcoral', edgecolor='black', alpha=0.7)
            axes[1, 2].set_xlabel('供给量 (Supply)')
            axes[1, 2].set_ylabel('频数')
            axes[1, 2].set_title('生产者供给量分布')
            axes[1, 2].grid(True, alpha=0.3)

        plt.suptitle('经济主体参数分布 (Agent Parameter Distributions)',
                    fontsize=16, fontweight='bold', y=0.995)
        plt.tight_layout()

        if save:
            plt.savefig(os.path.join(self.output_dir, 'agent_distributions.png'),
                       dpi=self.dpi, bbox_inches='tight')

        if show:
            plt.show()
        else:
            plt.close()

    def plot_welfare_analysis(self, consumers: List, producers: List,
                            save: bool = True, show: bool = True):
        """
        绘制福利分析
        """
        print("  - 绘制福利分析图...")
        fig, axes = plt.subplots(2, 2, figsize=(14, 12), dpi=self.dpi)

        # 消费者剩余分布
        cs_values = [c.consumer_surplus for c in consumers if c.consumer_surplus > 0]
        if cs_values:
            axes[0, 0].hist(cs_values, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
            axes[0, 0].set_xlabel('消费者剩余')
            axes[0, 0].set_ylabel('频数')
            axes[0, 0].set_title(f'消费者剩余分布\n平均: {np.mean(cs_values):.2f}')
            axes[0, 0].grid(True, alpha=0.3)

        # 生产者剩余分布
        ps_values = [p.producer_surplus for p in producers if p.producer_surplus > 0]
        if ps_values:
            axes[0, 1].hist(ps_values, bins=50, color='lightcoral', edgecolor='black', alpha=0.7)
            axes[0, 1].set_xlabel('生产者剩余')
            axes[0, 1].set_ylabel('频数')
            axes[0, 1].set_title(f'生产者剩余分布\n平均: {np.mean(ps_values):.2f}')
            axes[0, 1].grid(True, alpha=0.3)

        # 消费者效用分布
        utilities = [c.utility for c in consumers if c.utility > 0]
        if utilities:
            axes[1, 0].hist(utilities, bins=50, color='lightgreen', edgecolor='black', alpha=0.7)
            axes[1, 0].set_xlabel('效用')
            axes[1, 0].set_ylabel('频数')
            axes[1, 0].set_title(f'消费者效用分布\n平均: {np.mean(utilities):.2f}')
            axes[1, 0].grid(True, alpha=0.3)

        # 生产者利润分布
        profits = [p.profit for p in producers]
        if profits:
            axes[1, 1].hist(profits, bins=50, color='gold', edgecolor='black', alpha=0.7)
            axes[1, 1].set_xlabel('利润')
            axes[1, 1].set_ylabel('频数')
            axes[1, 1].set_title(f'生产者利润分布\n平均: {np.mean(profits):.2f}')
            axes[1, 1].axvline(x=0, color='r', linestyle='--', linewidth=2, label='盈亏平衡点')
            axes[1, 1].legend()
            axes[1, 1].grid(True, alpha=0.3)

        plt.suptitle('福利分析 (Welfare Analysis)', fontsize=16, fontweight='bold', y=0.995)
        plt.tight_layout()

        if save:
            plt.savefig(os.path.join(self.output_dir, 'welfare_analysis.png'),
                       dpi=self.dpi, bbox_inches='tight')

        if show:
            plt.show()
        else:
            plt.close()

    def generate_report(self, market, consumers: List, producers: List):
        """
        生成完整的可视化报告
        """
        print("正在生成可视化报告...")

        self.plot_supply_demand_curves(market, show=False)
        print("✓ 供需曲线图已生成")

        self.plot_price_convergence(market, show=False)
        print("✓ 价格收敛图已生成")

        self.plot_surplus(market, show=False)
        print("✓ 市场剩余图已生成")

        self.plot_transaction_volume(market, show=False)
        print("✓ 交易量图已生成")

        self.plot_agent_distributions(consumers, producers, show=False)
        print("✓ 经济主体分布图已生成")

        self.plot_welfare_analysis(consumers, producers, show=False)
        print("✓ 福利分析图已生成")

        print(f"\n所有图表已保存到目录: {self.output_dir}")


class MacroVisualizer:
    """
    宏观经济学模型可视化类

    提供宏观经济学模型的图表绘制:
    - 索洛增长模型收敛路径
    - AD-AS 模型均衡
    - 菲利普斯曲线
    - 货币创造过程
    """

    def __init__(self, output_dir: str = 'output', dpi: int = 100, style: str = 'seaborn-v0_8-darkgrid'):
        """
        初始化宏观可视化工具

        Args:
            output_dir: 输出目录
            dpi: 分辨率
            style: 绘图风格
        """
        self.output_dir = output_dir
        self.dpi = dpi

        os.makedirs(output_dir, exist_ok=True)

        try:
            if 'seaborn' in style:
                plt.style.use('ggplot')
            else:
                plt.style.use(style)
        except Exception:
            plt.style.use('default')
        plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False

    def plot_solow(self, solow, save: bool = True):
        """
        绘制索洛模型收敛路径与黄金律
        """
        print("  - 绘制索洛增长模型图...")
        path = solow.simulate(periods=120)

        fig, axes = plt.subplots(1, 3, figsize=(18, 5), dpi=self.dpi)

        # 人均资本收敛
        axes[0].plot(path['capital'], color='#3498db', linewidth=2)
        axes[0].axhline(y=solow.steady_state_k(), color='r', linestyle='--',
                        label=f"稳态 k* = {solow.steady_state_k():.2f}")
        axes[0].set_xlabel('时间 (期数)')
        axes[0].set_ylabel('人均资本 k')
        axes[0].set_title('资本积累与收敛 (Capital Accumulation)')
        axes[0].legend(fontsize=10)
        axes[0].grid(True, alpha=0.3)

        # 人均产出与消费
        axes[1].plot(path['output'], label='人均产出 y', color='#2ecc71', linewidth=2)
        axes[1].plot(path['consumption'], label='人均消费 c', color='#e67e22', linewidth=2)
        axes[1].plot(path['investment'], label='人均投资 i', color='#9b59b6', linewidth=2)
        axes[1].set_xlabel('时间 (期数)')
        axes[1].set_ylabel('人均水平')
        axes[1].set_title('产出、消费与投资路径')
        axes[1].legend(fontsize=10)
        axes[1].grid(True, alpha=0.3)

        # 稳态与黄金律对比
        k_values = np.linspace(0.01, solow.steady_state_k() * 2.2, 200)
        y_values = np.array([solow.output_per_worker(k) for k in k_values])
        inv_values = np.array([solow.investment_per_worker(k) for k in k_values])
        break_even = np.array([solow.breakeven_investment(k) for k in k_values])

        axes[2].plot(k_values, y_values, label='y = f(k)', color='#2ecc71', linewidth=2)
        axes[2].plot(k_values, inv_values, label='s·f(k)', color='#9b59b6', linewidth=2)
        axes[2].plot(k_values, break_even, label='(δ+n)·k', color='#e74c3c', linewidth=2)
        axes[2].axvline(x=solow.steady_state_k(), color='r', linestyle='--',
                        label=f'k* = {solow.steady_state_k():.2f}')
        axes[2].axvline(x=solow.golden_rule_k(), color='b', linestyle='--',
                        label=f'k_gold = {solow.golden_rule_k():.2f}')
        axes[2].set_xlabel('人均资本 k')
        axes[2].set_ylabel('人均水平')
        axes[2].set_title('稳态与黄金律 (Steady State vs Golden Rule)')
        axes[2].legend(fontsize=9)
        axes[2].grid(True, alpha=0.3)

        plt.tight_layout()
        if save:
            plt.savefig(os.path.join(self.output_dir, 'solow_growth.png'),
                        dpi=self.dpi, bbox_inches='tight')
        plt.close()

    def plot_ad_as(self, adas, save: bool = True):
        """
        绘制 AD-AS 模型
        """
        print("  - 绘制 AD-AS 模型图...")
        output_range = np.linspace(adas.potential_output * 0.7,
                                   adas.ad_intercept / adas.ad_slope * 0.95, 100)

        # AD 与 SRAS 曲线
        ad_prices = np.array([adas.ad_price(y) for y in output_range])
        sras_prices = np.array([adas.sras_price(y) for y in output_range])

        sr = adas.short_run_equilibrium()
        lr = adas.long_run_equilibrium()

        fig, ax = plt.subplots(figsize=(10, 8), dpi=self.dpi)

        ax.plot(output_range, ad_prices, label='总需求 AD', color='#3498db', linewidth=2.5)
        ax.plot(output_range, sras_prices, label='短期总供给 SRAS', color='#e74c3c', linewidth=2.5)
        ax.axvline(x=adas.potential_output, color='#2ecc71', linestyle='--',
                   label=f'长期总供给 LRAS (Y*={adas.potential_output:.0f})', linewidth=2)

        ax.plot(sr['output'], sr['price'], 'o', color='#f39c12', markersize=10,
                label=f'短期均衡 ({sr["output"]:.0f}, {sr["price"]:.0f})')
        ax.plot(lr['output'], lr['price'], 'D', color='#8e44ad', markersize=10,
                label=f'长期均衡 ({lr["output"]:.0f}, {lr["price"]:.0f})')

        ax.set_xlabel('产出 Y')
        ax.set_ylabel('物价水平 P')
        ax.set_title('总需求-总供给模型 (AD-AS Model)')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        if save:
            plt.savefig(os.path.join(self.output_dir, 'ad_as_model.png'),
                        dpi=self.dpi, bbox_inches='tight')
        plt.close()

    def plot_phillips(self, phillips, save: bool = True):
        """
        绘制菲利普斯曲线
        """
        print("  - 绘制菲利普斯曲线图...")
        u_values, pi_values = phillips.curve_points()

        fig, ax = plt.subplots(figsize=(10, 7), dpi=self.dpi)

        ax.plot(u_values, pi_values, color='#3498db', linewidth=2.5,
                label='短期菲利普斯曲线')
        ax.axvline(x=phillips.natural_unemployment_rate, color='#e74c3c', linestyle='--',
                   label=f'自然失业率 u_n = {phillips.natural_unemployment_rate:.0f}%')
        ax.axhline(y=phillips.expected_inflation, color='#2ecc71', linestyle=':',
                   label=f'预期通胀 π^e = {phillips.expected_inflation:.0f}%')

        ax.set_xlabel('失业率 u (%)')
        ax.set_ylabel('通货膨胀率 π (%)')
        ax.set_title('菲利普斯曲线 (Phillips Curve)')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        if save:
            plt.savefig(os.path.join(self.output_dir, 'phillips_curve.png'),
                        dpi=self.dpi, bbox_inches='tight')
        plt.close()

    def plot_money_creation(self, money, save: bool = True):
        """
        绘制货币创造过程
        """
        print("  - 绘制货币创造过程图...")
        rounds = money.deposit_creation_rounds(max_rounds=15)
        if not rounds:
            return

        round_nums = [r['round'] for r in rounds]
        deposits = [r['deposit'] for r in rounds]
        cumulative = np.cumsum(deposits)

        fig, ax = plt.subplots(figsize=(10, 6), dpi=self.dpi)
        ax.bar(round_nums, deposits, color='#3498db', alpha=0.8, label='各轮新增存款')
        ax.plot(round_nums, cumulative, 'ro-', linewidth=2, label='累计存款 (货币供给)')
        ax.axhline(y=money.total_money_supply, color='#e67e22', linestyle='--',
                   label=f'理论货币供给 {money.total_money_supply:.0f}')

        ax.set_xlabel('轮次')
        ax.set_ylabel('金额')
        ax.set_title(f'货币创造过程 (准备金率 {money.reserve_ratio*100:.0f}%, '
                     f'乘数 {money.money_multiplier:.2f})')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        if save:
            plt.savefig(os.path.join(self.output_dir, 'money_creation.png'),
                        dpi=self.dpi, bbox_inches='tight')
        plt.close()

    def generate_macro_report(self, solow=None, adas=None, phillips=None, money=None):
        """
        生成宏观经济学可视化报告
        """
        print("正在生成宏观经济学图表...")
        if solow is not None:
            self.plot_solow(solow)
            print("✓ 索洛增长模型图已生成")
        if adas is not None:
            self.plot_ad_as(adas)
            print("✓ AD-AS 模型图已生成")
        if phillips is not None:
            self.plot_phillips(phillips)
            print("✓ 菲利普斯曲线图已生成")
        if money is not None:
            self.plot_money_creation(money)
            print("✓ 货币创造过程图已生成")
        print(f"\n所有宏观图表已保存到目录: {self.output_dir}")

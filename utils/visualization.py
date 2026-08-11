"""
可视化工具
Visualization utilities for economic simulations

English labels are used by default so that charts render correctly on any
system without requiring CJK fonts.
"""

import os
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np


class EconomicsVisualizer:
    """
    经济学模拟可视化类
    Economics simulation visualizer

    Provides chart functions:
    - Supply/demand curves and market equilibrium
    - Price convergence process
    - Market surplus and welfare distribution
    - Agent parameter distributions
    - Consumer choice (budget line + indifference curves)
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

        os.makedirs(output_dir, exist_ok=True)

        try:
            if 'seaborn' in style:
                plt.style.use('ggplot')
            else:
                plt.style.use(style)
        except Exception:
            plt.style.use('default')
        plt.rcParams['axes.unicode_minus'] = False

    def plot_supply_demand_curves(self, market, price_range: np.ndarray = None,
                                  save: bool = True, show: bool = True):
        """
        绘制供需曲线和均衡点
        Plot supply/demand curves and the equilibrium point.
        """
        print("  - Plotting supply/demand curves...")
        if price_range is None:
            price_range = np.linspace(1, 200, 50)

        demand_curve = market.get_demand_curve(price_range)
        supply_curve = market.get_supply_curve(price_range)

        current_price = market.current_price
        current_quantity = market.quantity_history[-1] if market.quantity_history else 0

        fig, ax = plt.subplots(figsize=(10, 8), dpi=self.dpi)

        ax.plot(demand_curve, price_range, 'b-', linewidth=2, label='Demand')
        ax.plot(supply_curve, price_range, 'r-', linewidth=2, label='Supply')

        ax.plot(current_quantity, current_price, 'go', markersize=12,
                label=f'Equilibrium (P*={current_price:.2f}, Q*={current_quantity:.2f})',
                zorder=5)

        ax.axhline(y=current_price, color='g', linestyle='--', alpha=0.5)
        ax.axvline(x=current_quantity, color='g', linestyle='--', alpha=0.5)

        ax.set_xlabel('Quantity', fontsize=12)
        ax.set_ylabel('Price', fontsize=12)
        ax.set_title('Supply-Demand Curves and Market Equilibrium', fontsize=14, fontweight='bold')
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
        Plot the price convergence process.
        """
        print("  - Plotting price convergence...")
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), dpi=self.dpi)

        rounds = range(len(market.price_history))

        ax1.plot(rounds, market.price_history, 'b-', linewidth=2, label='Market price')
        ax1.axhline(y=market.current_price, color='r', linestyle='--',
                    label=f'Equilibrium price = {market.current_price:.2f}')
        ax1.set_xlabel('Trading round', fontsize=12)
        ax1.set_ylabel('Price', fontsize=12)
        ax1.set_title('Price Convergence Process', fontsize=14, fontweight='bold')
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)

        if market.total_demand_history and market.total_supply_history:
            rounds_sd = range(len(market.total_demand_history))
            ax2.plot(rounds_sd, market.total_demand_history, 'b-', linewidth=2, label='Total demand')
            ax2.plot(rounds_sd, market.total_supply_history, 'r-', linewidth=2, label='Total supply')
            ax2.set_xlabel('Trading round', fontsize=12)
            ax2.set_ylabel('Quantity', fontsize=12)
            ax2.set_title('Supply-Demand Quantity Changes', fontsize=14, fontweight='bold')
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
        Plot market surplus changes.
        """
        print("  - Plotting market surplus...")
        if not market.consumer_surplus_history or not market.producer_surplus_history:
            return

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), dpi=self.dpi)

        rounds = range(len(market.consumer_surplus_history))

        ax1.plot(rounds, market.consumer_surplus_history, 'b-', linewidth=2,
                 label='Consumer surplus')
        ax1.plot(rounds, market.producer_surplus_history, 'r-', linewidth=2,
                 label='Producer surplus')
        ax1.plot(rounds, market.total_surplus_history, 'g-', linewidth=2,
                 label='Total surplus')
        ax1.set_xlabel('Trading round', fontsize=12)
        ax1.set_ylabel('Surplus', fontsize=12)
        ax1.set_title('Market Surplus Changes', fontsize=14, fontweight='bold')
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)

        final_cs = market.consumer_surplus_history[-1]
        final_ps = market.producer_surplus_history[-1]

        if final_cs + final_ps > 0:
            ax2.pie([final_cs, final_ps],
                    labels=['Consumer surplus', 'Producer surplus'],
                    autopct='%1.1f%%',
                    colors=['#3498db', '#e74c3c'],
                    startangle=90)
            ax2.set_title(f'Final Surplus Distribution\n'
                          f'Consumer surplus: {final_cs:.2f}, Producer surplus: {final_ps:.2f}',
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
        Plot transaction volume over time.
        """
        print("  - Plotting transaction volume...")
        if not market.quantity_history:
            return

        fig, ax = plt.subplots(figsize=(10, 6), dpi=self.dpi)

        rounds = range(len(market.quantity_history))
        ax.plot(rounds, market.quantity_history, 'g-', linewidth=2, marker='o', markersize=4)
        ax.fill_between(rounds, market.quantity_history, alpha=0.3, color='green')

        ax.set_xlabel('Trading round', fontsize=12)
        ax.set_ylabel('Transaction volume', fontsize=12)
        ax.set_title('Market Transaction Volume', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)

        avg_volume = np.mean(market.quantity_history)
        ax.axhline(y=avg_volume, color='r', linestyle='--', alpha=0.5,
                   label=f'Average volume = {avg_volume:.2f}')
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
        Plot agent parameter distributions.
        """
        print("  - Plotting agent distributions...")
        fig, axes = plt.subplots(2, 3, figsize=self.figure_size, dpi=self.dpi)

        incomes = [c.income for c in consumers]
        axes[0, 0].hist(incomes, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
        axes[0, 0].set_xlabel('Income')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].set_title('Consumer Income Distribution')
        axes[0, 0].grid(True, alpha=0.3)

        alphas = [c.alpha for c in consumers]
        axes[0, 1].hist(alphas, bins=50, color='lightgreen', edgecolor='black', alpha=0.7)
        axes[0, 1].set_xlabel('Utility parameter alpha')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].set_title('Consumer Utility Parameter Distribution')
        axes[0, 1].grid(True, alpha=0.3)

        demands = [c.quantity_demanded for c in consumers if c.quantity_demanded > 0]
        if demands:
            axes[0, 2].hist(demands, bins=50, color='salmon', edgecolor='black', alpha=0.7)
            axes[0, 2].set_xlabel('Demand')
            axes[0, 2].set_ylabel('Frequency')
            axes[0, 2].set_title('Consumer Demand Distribution')
            axes[0, 2].grid(True, alpha=0.3)

        fixed_costs = [p.fixed_cost for p in producers]
        axes[1, 0].hist(fixed_costs, bins=50, color='gold', edgecolor='black', alpha=0.7)
        axes[1, 0].set_xlabel('Fixed cost')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].set_title('Producer Fixed Cost Distribution')
        axes[1, 0].grid(True, alpha=0.3)

        mc_as = [p.mc_a for p in producers]
        axes[1, 1].hist(mc_as, bins=50, color='orchid', edgecolor='black', alpha=0.7)
        axes[1, 1].set_xlabel('Marginal cost parameter a')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].set_title('Producer Marginal Cost Distribution')
        axes[1, 1].grid(True, alpha=0.3)

        supplies = [p.quantity_supplied for p in producers if p.quantity_supplied > 0]
        if supplies:
            axes[1, 2].hist(supplies, bins=50, color='lightcoral', edgecolor='black', alpha=0.7)
            axes[1, 2].set_xlabel('Supply')
            axes[1, 2].set_ylabel('Frequency')
            axes[1, 2].set_title('Producer Supply Distribution')
            axes[1, 2].grid(True, alpha=0.3)

        plt.suptitle('Agent Parameter Distributions', fontsize=16, fontweight='bold', y=0.995)
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
        Plot welfare analysis.
        """
        print("  - Plotting welfare analysis...")
        fig, axes = plt.subplots(2, 2, figsize=(14, 12), dpi=self.dpi)

        cs_values = [c.consumer_surplus for c in consumers if c.consumer_surplus > 0]
        if cs_values:
            axes[0, 0].hist(cs_values, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
            axes[0, 0].set_xlabel('Consumer surplus')
            axes[0, 0].set_ylabel('Frequency')
            axes[0, 0].set_title(f'Consumer Surplus Distribution\nMean: {np.mean(cs_values):.2f}')
            axes[0, 0].grid(True, alpha=0.3)

        ps_values = [p.producer_surplus for p in producers if p.producer_surplus > 0]
        if ps_values:
            axes[0, 1].hist(ps_values, bins=50, color='lightcoral', edgecolor='black', alpha=0.7)
            axes[0, 1].set_xlabel('Producer surplus')
            axes[0, 1].set_ylabel('Frequency')
            axes[0, 1].set_title(f'Producer Surplus Distribution\nMean: {np.mean(ps_values):.2f}')
            axes[0, 1].grid(True, alpha=0.3)

        utilities = [c.utility for c in consumers if c.utility > 0]
        if utilities:
            axes[1, 0].hist(utilities, bins=50, color='lightgreen', edgecolor='black', alpha=0.7)
            axes[1, 0].set_xlabel('Utility')
            axes[1, 0].set_ylabel('Frequency')
            axes[1, 0].set_title(f'Consumer Utility Distribution\nMean: {np.mean(utilities):.2f}')
            axes[1, 0].grid(True, alpha=0.3)

        profits = [p.profit for p in producers]
        if profits:
            axes[1, 1].hist(profits, bins=50, color='gold', edgecolor='black', alpha=0.7)
            axes[1, 1].set_xlabel('Profit')
            axes[1, 1].set_ylabel('Frequency')
            axes[1, 1].set_title(f'Producer Profit Distribution\nMean: {np.mean(profits):.2f}')
            axes[1, 1].axvline(x=0, color='r', linestyle='--', linewidth=2,
                               label='Break-even')
            axes[1, 1].legend()
            axes[1, 1].grid(True, alpha=0.3)

        plt.suptitle('Welfare Analysis', fontsize=16, fontweight='bold', y=0.995)
        plt.tight_layout()

        if save:
            plt.savefig(os.path.join(self.output_dir, 'welfare_analysis.png'),
                        dpi=self.dpi, bbox_inches='tight')

        if show:
            plt.show()
        else:
            plt.close()

    def plot_consumer_choice(self, choice, save: bool = True, show: bool = True):
        """
        绘制消费者选择: 预算线与无差异曲线
        Plot consumer choice: budget line and indifference curves.
        """
        print("  - Plotting consumer choice...")
        budget = choice.budget
        utility = choice.utility

        fig, ax = plt.subplots(figsize=(10, 8), dpi=self.dpi)

        x_vals, y_vals = budget.budget_line(200)
        ax.plot(x_vals, y_vals, 'b-', linewidth=2.5, label='Budget line')

        opt = choice.optimal_bundle()
        x_star, y_star = opt['x'], opt['y']

        for mult in (0.6, 1.0, 1.4):
            target = utility.utility(x_star, y_star) * mult
            ix, iy = utility.indifference_curve(target, x_max=budget.max_x * 1.2, num_points=200)
            ax.plot(ix, iy, linestyle='--', alpha=0.6,
                    label=f'U = {target:.2f}')

        ax.plot(x_star, y_star, 'ro', markersize=12, zorder=5,
                label=f'Optimal bundle ({x_star:.2f}, {y_star:.2f})')

        ax.set_xlabel('Good X quantity')
        ax.set_ylabel('Good Y quantity')
        ax.set_title('Consumer Choice: Budget Line and Indifference Curves',
                     fontsize=14, fontweight='bold')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, budget.max_x * 1.1)
        ax.set_ylim(0, budget.max_y * 1.1)

        plt.tight_layout()

        if save:
            plt.savefig(os.path.join(self.output_dir, 'consumer_choice.png'),
                        dpi=self.dpi, bbox_inches='tight')

        if show:
            plt.show()
        else:
            plt.close()

    def generate_report(self, market, consumers: List, producers: List):
        """
        生成完整的可视化报告
        Generate the complete visualization report.
        """
        print("Generating visualization report...")

        self.plot_supply_demand_curves(market, show=False)
        print("OK supply/demand curves generated")

        self.plot_price_convergence(market, show=False)
        print("OK price convergence generated")

        self.plot_surplus(market, show=False)
        print("OK market surplus generated")

        self.plot_transaction_volume(market, show=False)
        print("OK transaction volume generated")

        self.plot_agent_distributions(consumers, producers, show=False)
        print("OK agent distributions generated")

        self.plot_welfare_analysis(consumers, producers, show=False)
        print("OK welfare analysis generated")

        print(f"\nAll charts saved to directory: {self.output_dir}")


class MacroVisualizer:
    """
    宏观经济学模型可视化类
    Macroeconomics model visualizer

    Provides:
    - Solow growth model convergence path
    - AD-AS model equilibrium
    - Phillips curve
    - Money creation process
    - Loanable funds market
    - IS-LM model
    """

    def __init__(self, output_dir: str = 'output', dpi: int = 100, style: str = 'seaborn-v0_8-darkgrid'):
        """
        初始化宏观可视化工具
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
        plt.rcParams['axes.unicode_minus'] = False

    def plot_solow(self, solow, save: bool = True):
        """
        绘制索洛模型收敛路径与黄金律
        Plot the Solow model convergence path and golden rule.
        """
        print("  - Plotting Solow growth model...")
        path = solow.simulate(periods=120)

        fig, axes = plt.subplots(1, 3, figsize=(18, 5), dpi=self.dpi)

        axes[0].plot(path['capital'], color='#3498db', linewidth=2)
        axes[0].axhline(y=solow.steady_state_k(), color='r', linestyle='--',
                        label=f"Steady state k* = {solow.steady_state_k():.2f}")
        axes[0].set_xlabel('Time (period)')
        axes[0].set_ylabel('Capital per worker k')
        axes[0].set_title('Capital Accumulation and Convergence')
        axes[0].legend(fontsize=10)
        axes[0].grid(True, alpha=0.3)

        axes[1].plot(path['output'], label='Output per worker y', color='#2ecc71', linewidth=2)
        axes[1].plot(path['consumption'], label='Consumption per worker c', color='#e67e22', linewidth=2)
        axes[1].plot(path['investment'], label='Investment per worker i', color='#9b59b6', linewidth=2)
        axes[1].set_xlabel('Time (period)')
        axes[1].set_ylabel('Per worker level')
        axes[1].set_title('Output, Consumption and Investment Paths')
        axes[1].legend(fontsize=10)
        axes[1].grid(True, alpha=0.3)

        k_values = np.linspace(0.01, solow.steady_state_k() * 2.2, 200)
        y_values = np.array([solow.output_per_worker(k) for k in k_values])
        inv_values = np.array([solow.investment_per_worker(k) for k in k_values])
        break_even = np.array([solow.breakeven_investment(k) for k in k_values])

        axes[2].plot(k_values, y_values, label='y = f(k)', color='#2ecc71', linewidth=2)
        axes[2].plot(k_values, inv_values, label='s·f(k)', color='#9b59b6', linewidth=2)
        axes[2].plot(k_values, break_even, label='(delta+n)·k', color='#e74c3c', linewidth=2)
        axes[2].axvline(x=solow.steady_state_k(), color='r', linestyle='--',
                        label=f'k* = {solow.steady_state_k():.2f}')
        axes[2].axvline(x=solow.golden_rule_k(), color='b', linestyle='--',
                        label=f'k_gold = {solow.golden_rule_k():.2f}')
        axes[2].set_xlabel('Capital per worker k')
        axes[2].set_ylabel('Per worker level')
        axes[2].set_title('Steady State vs Golden Rule')
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
        Plot the AD-AS model.
        """
        print("  - Plotting AD-AS model...")
        output_range = np.linspace(adas.potential_output * 0.7,
                                   adas.ad_intercept / adas.ad_slope * 0.95, 100)

        ad_prices = np.array([adas.ad_price(y) for y in output_range])
        sras_prices = np.array([adas.sras_price(y) for y in output_range])

        sr = adas.short_run_equilibrium()
        lr = adas.long_run_equilibrium()

        fig, ax = plt.subplots(figsize=(10, 8), dpi=self.dpi)

        ax.plot(output_range, ad_prices, label='Aggregate demand AD', color='#3498db', linewidth=2.5)
        ax.plot(output_range, sras_prices, label='Short-run AS SRAS', color='#e74c3c', linewidth=2.5)
        ax.axvline(x=adas.potential_output, color='#2ecc71', linestyle='--',
                   label=f'Long-run AS LRAS (Y*={adas.potential_output:.0f})', linewidth=2)

        ax.plot(sr['output'], sr['price'], 'o', color='#f39c12', markersize=10,
                label=f'Short-run equilibrium ({sr["output"]:.0f}, {sr["price"]:.0f})')
        ax.plot(lr['output'], lr['price'], 'D', color='#8e44ad', markersize=10,
                label=f'Long-run equilibrium ({lr["output"]:.0f}, {lr["price"]:.0f})')

        ax.set_xlabel('Output Y')
        ax.set_ylabel('Price level P')
        ax.set_title('Aggregate Demand - Aggregate Supply Model')
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
        Plot the Phillips curve.
        """
        print("  - Plotting Phillips curve...")
        u_values, pi_values = phillips.curve_points()

        fig, ax = plt.subplots(figsize=(10, 7), dpi=self.dpi)

        ax.plot(u_values, pi_values, color='#3498db', linewidth=2.5,
                label='Short-run Phillips curve')
        ax.axvline(x=phillips.natural_unemployment_rate, color='#e74c3c', linestyle='--',
                   label=f'Natural unemployment u_n = {phillips.natural_unemployment_rate:.0f}%')
        ax.axhline(y=phillips.expected_inflation, color='#2ecc71', linestyle=':',
                   label=f'Expected inflation pi^e = {phillips.expected_inflation:.0f}%')

        ax.set_xlabel('Unemployment rate u (%)')
        ax.set_ylabel('Inflation rate pi (%)')
        ax.set_title('Phillips Curve')
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
        Plot the money creation process.
        """
        print("  - Plotting money creation process...")
        rounds = money.deposit_creation_rounds(max_rounds=15)
        if not rounds:
            return

        round_nums = [r['round'] for r in rounds]
        deposits = [r['deposit'] for r in rounds]
        cumulative = np.cumsum(deposits)

        fig, ax = plt.subplots(figsize=(10, 6), dpi=self.dpi)
        ax.bar(round_nums, deposits, color='#3498db', alpha=0.8, label='New deposits per round')
        ax.plot(round_nums, cumulative, 'ro-', linewidth=2, label='Cumulative deposits (money supply)')
        ax.axhline(y=money.total_money_supply, color='#e67e22', linestyle='--',
                   label=f'Theoretical money supply {money.total_money_supply:.0f}')

        ax.set_xlabel('Round')
        ax.set_ylabel('Amount')
        ax.set_title(f'Money Creation Process (Reserve ratio {money.reserve_ratio*100:.0f}%, '
                     f'Multiplier {money.money_multiplier:.2f})')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        if save:
            plt.savefig(os.path.join(self.output_dir, 'money_creation.png'),
                        dpi=self.dpi, bbox_inches='tight')
        plt.close()

    def plot_loanable_funds(self, model, save: bool = True):
        """
        绘制可贷资金市场
        Plot the market for loanable funds.
        """
        print("  - Plotting loanable funds market...")
        rate_range = np.linspace(0, 0.10, 100)
        savings = np.array([model.savings(r) for r in rate_range])
        investment = np.array([model.investment(r) for r in rate_range])

        eq = model.equilibrium()

        fig, ax = plt.subplots(figsize=(10, 7), dpi=self.dpi)

        ax.plot(savings, rate_range * 100, color='#3498db', linewidth=2.5,
                label='Loanable funds supply (savings)')
        ax.plot(investment, rate_range * 100, color='#e74c3c', linewidth=2.5,
                label='Loanable funds demand (investment)')

        ax.plot(eq['savings'], eq['interest_rate'] * 100, 'go', markersize=12, zorder=5,
                label=f"Equilibrium r* = {eq['interest_rate']*100:.2f}%")
        ax.axhline(y=eq['interest_rate'] * 100, color='g', linestyle='--', alpha=0.5)

        ax.set_xlabel('Quantity of loanable funds')
        ax.set_ylabel('Interest rate (%)')
        ax.set_title('Market for Loanable Funds')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        if save:
            plt.savefig(os.path.join(self.output_dir, 'loanable_funds.png'),
                        dpi=self.dpi, bbox_inches='tight')
        plt.close()

    def plot_islm(self, model, save: bool = True):
        """
        绘制 IS-LM 模型
        Plot the IS-LM model.
        """
        print("  - Plotting IS-LM model...")
        rate_range = np.linspace(0, 0.25, 100)
        is_y = np.array([model.is_curve(r) for r in rate_range])
        lm_y = np.array([model.lm_curve(r) for r in rate_range])

        eq = model.equilibrium()

        fig, ax = plt.subplots(figsize=(10, 7), dpi=self.dpi)

        ax.plot(is_y, rate_range * 100, color='#3498db', linewidth=2.5,
                label='IS curve (goods market)')
        ax.plot(lm_y, rate_range * 100, color='#e74c3c', linewidth=2.5,
                label='LM curve (money market)')

        ax.plot(eq['output'], eq['interest_rate'] * 100, 'go', markersize=12, zorder=5,
                label=f"Equilibrium (Y*={eq['output']:.0f}, r*={eq['interest_rate']*100:.2f}%)")

        ax.set_xlabel('Output Y')
        ax.set_ylabel('Interest rate (%)')
        ax.set_title('IS-LM Model')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        if save:
            plt.savefig(os.path.join(self.output_dir, 'islm_model.png'),
                        dpi=self.dpi, bbox_inches='tight')
        plt.close()

    def generate_macro_report(self, solow=None, adas=None, phillips=None, money=None,
                              loanable_funds=None, islm=None):
        """
        生成宏观经济学可视化报告
        Generate the macroeconomics visualization report.
        """
        print("Generating macroeconomics charts...")
        if solow is not None:
            self.plot_solow(solow)
            print("OK Solow growth model generated")
        if adas is not None:
            self.plot_ad_as(adas)
            print("OK AD-AS model generated")
        if phillips is not None:
            self.plot_phillips(phillips)
            print("OK Phillips curve generated")
        if money is not None:
            self.plot_money_creation(money)
            print("OK money creation generated")
        if loanable_funds is not None:
            self.plot_loanable_funds(loanable_funds)
            print("OK loanable funds generated")
        if islm is not None:
            self.plot_islm(islm)
            print("OK IS-LM model generated")
        print(f"\nAll macro charts saved to directory: {self.output_dir}")

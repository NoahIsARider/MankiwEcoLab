"""
可视化工具
Visualization utilities for economic simulations
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
import os


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
        # 设置绘图风格
        try:
            if 'seaborn' in style:
                plt.style.use('ggplot')  # 使用替代风格
            else:
                plt.style.use(style)
        except:
            plt.style.use('default')
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
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
        final_volume = market.quantity_history[-1]
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
        """
        绘制经济主体的参数分布
        """
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

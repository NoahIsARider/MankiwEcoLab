"""
经济学原理模拟系统 - 主程序
Economics Principles Simulation - Main Program

基于曼昆《经济学原理》的经济系统模拟
"""

import numpy as np
import pandas as pd
import logging
from datetime import datetime
import config
from agents import Consumer, Producer
from market import Market
from utils.economics import create_agents, analyze_welfare_distribution, calculate_price_elasticity_of_demand
from utils.visualization import EconomicsVisualizer


# 配置日志
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def print_banner():
    """打印程序横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║          经济学原理模拟系统                                  ║
    ║    Economics Principles Simulation System                   ║
    ║                                                              ║
    ║    基于曼昆《经济学原理》的经济系统模拟                      ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def initialize_simulation():
    """初始化模拟"""
    logger.info("=" * 70)
    logger.info("开始初始化经济系统模拟")
    logger.info("=" * 70)
    
    # 设置随机种子
    if config.RANDOM_SEED is not None:
        np.random.seed(config.RANDOM_SEED)
        logger.info(f"随机种子: {config.RANDOM_SEED}")
    
    # 创建消费者参数字典
    consumer_params = {
        'income_mean': config.CONSUMER_INCOME_MEAN,
        'income_std': config.CONSUMER_INCOME_STD,
        'income_min': config.CONSUMER_INCOME_MIN,
        'alpha_mean': config.CONSUMER_ALPHA_MEAN,
        'alpha_std': config.CONSUMER_ALPHA_STD,
        'beta_mean': config.CONSUMER_BETA_MEAN,
        'beta_std': config.CONSUMER_BETA_STD
    }
    
    # 创建生产者参数字典
    producer_params = {
        'fixed_cost_mean': config.PRODUCER_FIXED_COST_MEAN,
        'fixed_cost_std': config.PRODUCER_FIXED_COST_STD,
        'mc_a_mean': config.PRODUCER_MC_A_MEAN,
        'mc_a_std': config.PRODUCER_MC_A_STD,
        'mc_b_mean': config.PRODUCER_MC_B_MEAN,
        'mc_b_std': config.PRODUCER_MC_B_STD,
        'max_capacity_mean': config.PRODUCER_MAX_CAPACITY_MEAN,
        'max_capacity_std': config.PRODUCER_MAX_CAPACITY_STD
    }
    
    # 创建经济主体
    logger.info(f"创建 {config.NUM_CONSUMERS} 个消费者...")
    logger.info(f"创建 {config.NUM_PRODUCERS} 个生产者...")
    
    consumers, producers = create_agents(
        config.NUM_CONSUMERS,
        config.NUM_PRODUCERS,
        consumer_params,
        producer_params,
        config.RANDOM_SEED
    )
    
    logger.info(f"✓ 成功创建 {len(consumers)} 个消费者")
    logger.info(f"✓ 成功创建 {len(producers)} 个生产者")
    
    # 创建市场
    logger.info(f"初始化市场，初始价格: {config.INITIAL_PRICE}")
    market = Market(
        consumers=consumers,
        producers=producers,
        initial_price=config.INITIAL_PRICE,
        price_adjustment_speed=config.PRICE_ADJUSTMENT_SPEED
    )
    
    logger.info("✓ 市场初始化完成")
    logger.info("=" * 70)
    
    return market, consumers, producers


def run_simulation(market, consumers, producers):
    """运行模拟"""
    logger.info("\n" + "=" * 70)
    logger.info("开始市场模拟")
    logger.info("=" * 70)
    
    logger.info(f"模拟轮次: {config.NUM_ROUNDS}")
    logger.info(f"收敛阈值: {config.CONVERGENCE_THRESHOLD}")
    logger.info(f"价格调整速度: {config.PRICE_ADJUSTMENT_SPEED}")
    logger.info("-" * 70)
    
    # 运行模拟
    for round_num in range(config.NUM_ROUNDS):
        # 运行一轮
        equilibrium_reached = market.run_round()
        
        # 定期输出日志
        if (round_num + 1) % config.LOG_INTERVAL == 0 or round_num == 0:
            logger.info(
                f"轮次 {round_num + 1:3d} | "
                f"价格: {market.current_price:7.2f} | "
                f"需求: {market.total_demand:8.2f} | "
                f"供给: {market.total_supply:8.2f} | "
                f"交易量: {market.quantity_history[-1] if market.quantity_history else 0:8.2f} | "
                f"缺口: {abs(market.total_demand - market.total_supply):7.2f}"
            )
        
        # 检查是否达到均衡
        if equilibrium_reached:
            logger.info("-" * 70)
            logger.info(f"✓ 市场在第 {round_num + 1} 轮达到均衡!")
            break
    
    logger.info("=" * 70)
    logger.info("模拟完成")
    logger.info("=" * 70 + "\n")


def analyze_results(market, consumers, producers):
    """分析结果"""
    logger.info("\n" + "=" * 70)
    logger.info("市场分析结果")
    logger.info("=" * 70)
    
    # 获取市场统计信息
    stats = market.get_market_stats()
    
    # 市场均衡信息
    logger.info("\n【市场均衡】")
    logger.info(f"  均衡价格: {stats['equilibrium_price']:.2f}")
    logger.info(f"  均衡数量: {stats['equilibrium_quantity']:.2f}")
    logger.info(f"  总需求: {stats['total_demand']:.2f}")
    logger.info(f"  总供给: {stats['total_supply']:.2f}")
    logger.info(f"  是否达到均衡: {'是' if stats['equilibrium_reached'] else '否'}")
    logger.info(f"  模拟轮次: {stats['num_rounds']}")
    
    # 市场剩余
    logger.info("\n【市场剩余】")
    logger.info(f"  消费者剩余: {stats['consumer_surplus']:.2f}")
    logger.info(f"  生产者剩余: {stats['producer_surplus']:.2f}")
    logger.info(f"  总剩余 (社会福利): {stats['total_surplus']:.2f}")
    
    # 福利分析
    welfare = analyze_welfare_distribution(consumers, producers)
    logger.info("\n【福利分析】")
    logger.info(f"  平均消费者剩余: {welfare['avg_consumer_surplus']:.2f}")
    logger.info(f"  平均生产者剩余: {welfare['avg_producer_surplus']:.2f}")
    logger.info(f"  平均消费者效用: {welfare['avg_consumer_utility']:.2f}")
    logger.info(f"  平均生产者利润: {welfare['avg_producer_profit']:.2f}")
    logger.info(f"  消费者基尼系数: {welfare['consumer_gini']:.4f}")
    logger.info(f"  生产者基尼系数: {welfare['producer_gini']:.4f}")
    
    # 市场效率
    logger.info("\n【市场效率】")
    logger.info(f"  总支出: {welfare['total_expenditure']:.2f}")
    logger.info(f"  总收入: {welfare['total_revenue']:.2f}")
    
    # 价格弹性
    if len(market.price_history) >= 2 and len(market.quantity_history) >= 2:
        elasticity = calculate_price_elasticity_of_demand(
            market.price_history[-20:],
            market.quantity_history[-20:]
        )
        logger.info(f"  需求价格弹性: {elasticity:.4f}")
        
        if abs(elasticity) > 1:
            elasticity_type = "弹性需求"
        elif abs(elasticity) < 1:
            elasticity_type = "非弹性需求"
        else:
            elasticity_type = "单位弹性需求"
        logger.info(f"  需求类型: {elasticity_type}")
    
    # 市场参与度
    active_consumers = sum(1 for c in consumers if c.quantity_consumed > 0)
    active_producers = sum(1 for p in producers if p.quantity_produced > 0)
    
    logger.info("\n【市场参与度】")
    logger.info(f"  活跃消费者: {active_consumers} ({active_consumers/len(consumers)*100:.1f}%)")
    logger.info(f"  活跃生产者: {active_producers} ({active_producers/len(producers)*100:.1f}%)")
    
    logger.info("=" * 70 + "\n")
    
    return stats, welfare


def save_results(market, consumers, producers, stats, welfare):
    """保存结果到文件"""
    if not config.SAVE_RESULTS:
        return
    
    logger.info("正在保存结果...")
    
    import os
    import csv
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    
    # 保存市场数据
    with open(f"{config.OUTPUT_DIR}/market_data.csv", 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['Round', 'Price', 'Total_Demand', 'Total_Supply', 'Quantity', 
                        'Consumer_Surplus', 'Producer_Surplus', 'Total_Surplus'])
        
        for i in range(len(market.price_history)):
            writer.writerow([
                i,
                market.price_history[i],
                0 if i == 0 else market.total_demand_history[i-1],
                0 if i == 0 else market.total_supply_history[i-1],
                0 if i == 0 else market.quantity_history[i-1],
                0 if i == 0 else market.consumer_surplus_history[i-1],
                0 if i == 0 else market.producer_surplus_history[i-1],
                0 if i == 0 else market.total_surplus_history[i-1]
            ])
    logger.info(f"✓ 市场数据已保存到 {config.OUTPUT_DIR}/market_data.csv")
    
    # 保存消费者数据
    with open(f"{config.OUTPUT_DIR}/consumer_data.csv", 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Income', 'Alpha', 'Beta', 'Demand', 'Consumption', 
                        'Expenditure', 'Utility', 'Consumer_Surplus'])
        
        for c in consumers:
            writer.writerow([
                c.id, c.income, c.alpha, c.beta, c.quantity_demanded,
                c.quantity_consumed, c.expenditure, c.utility, c.consumer_surplus
            ])
    logger.info(f"✓ 消费者数据已保存到 {config.OUTPUT_DIR}/consumer_data.csv")
    
    # 保存生产者数据
    with open(f"{config.OUTPUT_DIR}/producer_data.csv", 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Fixed_Cost', 'MC_a', 'MC_b', 'Max_Capacity', 'Supply', 
                        'Production', 'Revenue', 'Cost', 'Profit', 'Producer_Surplus'])
        
        for p in producers:
            writer.writerow([
                p.id, p.fixed_cost, p.mc_a, p.mc_b, p.max_capacity,
                p.quantity_supplied, p.quantity_produced, p.revenue,
                p.cost, p.profit, p.producer_surplus
            ])
    logger.info(f"✓ 生产者数据已保存到 {config.OUTPUT_DIR}/producer_data.csv")
    
    # 保存统计摘要
    with open(f"{config.OUTPUT_DIR}/summary.csv", 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['Parameter', 'Value'])
        writer.writerow(['Equilibrium_Price', stats['equilibrium_price']])
        writer.writerow(['Equilibrium_Quantity', stats['equilibrium_quantity']])
        writer.writerow(['Consumer_Surplus', stats['consumer_surplus']])
        writer.writerow(['Producer_Surplus', stats['producer_surplus']])
        writer.writerow(['Total_Surplus', stats['total_surplus']])
        writer.writerow(['Consumer_Gini', welfare['consumer_gini']])
        writer.writerow(['Producer_Gini', welfare['producer_gini']])
        writer.writerow(['Num_Rounds', stats['num_rounds']])
        writer.writerow(['Equilibrium_Reached', 1 if stats['equilibrium_reached'] else 0])
    logger.info(f"✓ 统计摘要已保存到 {config.OUTPUT_DIR}/summary.csv")
    logger.info("")


def main():
    """主函数"""
    # 打印横幅
    print_banner()
    
    # 记录开始时间
    start_time = datetime.now()
    logger.info(f"模拟开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 1. 初始化
        market, consumers, producers = initialize_simulation()
        
        # 2. 运行模拟
        run_simulation(market, consumers, producers)
        
        # 3. 分析结果
        stats, welfare = analyze_results(market, consumers, producers)
        
        # 4. 保存结果
        save_results(market, consumers, producers, stats, welfare)
        
        # 5. 生成可视化
        if config.SAVE_PLOTS:
            logger.info("正在生成可视化图表...")
            visualizer = EconomicsVisualizer(
                output_dir=config.OUTPUT_DIR,
                figure_size=config.FIGURE_SIZE,
                dpi=config.DPI,
                style=config.PLOT_STYLE
            )
            visualizer.generate_report(market, consumers, producers)
            logger.info("")
        
        # 记录结束时间
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        logger.info("=" * 70)
        logger.info("模拟成功完成!")
        logger.info(f"结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"总耗时: {duration:.2f} 秒")
        logger.info("=" * 70)
        
        # 打印结论
        print("\n" + "=" * 70)
        print("【模拟结论】")
        print("=" * 70)
        print("\n本模拟展示了曼昆经济学原理中的核心概念:")
        print("\n1. 供需法则:")
        print(f"   市场通过价格机制自动调节，经过 {stats['num_rounds']} 轮交易")
        print(f"   达到均衡价格 {stats['equilibrium_price']:.2f}，均衡数量 {stats['equilibrium_quantity']:.2f}")
        
        print("\n2. 看不见的手:")
        print("   成千上万的个体基于自身利益最大化独立决策，")
        print("   最终市场自发达到均衡，实现资源有效配置。")
        
        print("\n3. 市场效率:")
        print(f"   总社会福利 (消费者剩余 + 生产者剩余) = {stats['total_surplus']:.2f}")
        print("   在完全竞争市场中，均衡状态即为帕累托最优。")
        
        print("\n4. 边际分析:")
        print("   消费者根据边际效用递减规律做出消费决策,")
        print("   生产者根据边际成本递增规律做出生产决策。")
        
        print("\n" + "=" * 70 + "\n")
        
    except Exception as e:
        logger.error(f"模拟过程中发生错误: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()

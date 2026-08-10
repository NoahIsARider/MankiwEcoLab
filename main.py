"""
经济学原理模拟系统 - 主程序
Economics Principles Simulation - Main Program

基于曼昆《经济学原理》的经济系统模拟与学习工具。

用法:
    python main.py                  # 运行完整微观市场模拟
    python main.py --macro          # 运行宏观经济学模型演示
    python main.py --demo           # 运行十大原理演示
"""

import argparse
import logging
from datetime import datetime

import numpy as np

import config
from agents import Consumer
from market import Market
from utils.economics import (
    analyze_welfare_distribution,
    calculate_price_elasticity_of_demand,
    create_agents,
)
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
    ║    Micro & Macro Economics Learning Lab                     ║
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

    import csv
    import os
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


def run_full_simulation():
    """运行完整的微观市场模拟"""
    # 记录开始时间
    start_time = datetime.now()
    logger.info(f"模拟开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

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


def run_macro_demo():
    """
    运行宏观经济学模型演示

    展示 GDP、通胀、失业、索洛增长、货币创造、AD-AS、菲利普斯曲线等宏观概念。
    """
    from macro import (
        CPI,
        ADASModel,
        GDPAccounts,
        GDPDeflator,
        LaborMarketStats,
        MoneyCreationModel,
        PhillipsCurve,
        QuantityTheory,
        SolowGrowthModel,
        calculate_real_gdp,
        inflation_rate,
        unemployment_decomposition,
    )
    from utils.visualization import MacroVisualizer

    print("\n" + "=" * 70)
    print("宏观经济学模型演示")
    print("=" * 70)

    results = {}

    # 1. GDP 核算
    print("\n【1. GDP 核算 - 原理8: 一国的生活水平取决于生产物品与服务的能力】")
    gdp = GDPAccounts(consumption=6000, investment=1500,
                      government_spending=2000, net_exports=-500)
    analysis = gdp.analyze()
    print(f"  GDP = {analysis['GDP']:.2f}")
    print(f"  支出构成: {analysis['interpretation']}")
    results['gdp'] = analysis

    # 名义/实际 GDP 与平减指数
    nominal = [1000, 1100, 1210, 1331]
    price = [100, 105, 110, 115]
    real = calculate_real_gdp(nominal, price)
    deflator = GDPDeflator(nominal, real)
    print(f"\n  名义GDP: {nominal}")
    print(f"  实际GDP: {[round(r, 2) for r in real]}")
    print(f"  GDP平减指数: {[round(d, 2) for d in deflator.values()]}")

    # 2. CPI 与通胀
    print("\n【2. 通货膨胀 - 原理9: 当政府发行了过多货币时，物价上升】")
    cpi = CPI(base_prices=[10, 20, 30], base_quantities=[4, 3, 2])
    current = [12, 22, 31]
    cpi_value = cpi.compute(current)
    print(f"  CPI = {cpi_value:.2f} (基期 100)")
    print(f"  通货膨胀率 = {inflation_rate(100, cpi_value):.2f}%")
    qt = QuantityTheory(money_supply=1000, velocity=5, real_output=100)
    print(f"  货币数量论: {qt.analyze()['equation']}")
    print("  若货币供给增长 10%，通胀约上升 10%")
    results['inflation'] = {'cpi': cpi_value, 'inflation_rate': inflation_rate(100, cpi_value)}

    # 3. 失业
    print("\n【3. 失业分析】")
    labor = LaborMarketStats(adult_population=10000, employed=9000, unemployed=500)
    l_analysis = labor.analyze()
    print(f"  劳动力: {l_analysis['labor_force']:.0f}")
    print(f"  失业率: {l_analysis['unemployment_rate']:.2f}%")
    print(f"  劳动力参与率: {l_analysis['labor_force_participation_rate']:.2f}%")
    decomp = unemployment_decomposition(actual_unemployment_rate=5.5,
                                        frictional_rate=2.0, structural_rate=2.5)
    print(f"  失业分解: {decomp['interpretation']}")
    results['unemployment'] = l_analysis

    # 4. 索洛增长模型
    print("\n【4. 索洛增长模型】")
    solow = SolowGrowthModel(alpha=0.3, savings_rate=0.2,
                             depreciation_rate=0.05, population_growth_rate=0.01)
    s_analysis = solow.analyze()
    print(f"  稳态人均资本: {s_analysis['steady_state']['k']:.2f}")
    print(f"  稳态人均产出: {s_analysis['steady_state']['y']:.2f}")
    print(f"  黄金律资本存量: {s_analysis['golden_rule']['k_gold']:.2f}")
    print(f"  黄金律储蓄率: {s_analysis['golden_rule']['s_gold']:.2f}")
    print(f"  收敛速度: {s_analysis['convergence_speed']:.4f}")
    results['solow'] = s_analysis

    # 5. 货币创造
    print("\n【5. 货币创造 - 银行体系】")
    money = MoneyCreationModel(reserve_ratio=0.10, initial_deposit=1000)
    m_analysis = money.analyze()
    print(f"  准备金率 10% => 货币乘数 {m_analysis['money_multiplier']:.2f}")
    print(f"  初始存款 1000 元 => 货币供给 {m_analysis['total_money_supply']:.2f} 元")
    print(f"  {m_analysis['interpretation']}")
    results['money'] = m_analysis

    # 6. AD-AS 模型
    print("\n【6. 总需求-总供给模型】")
    adas = ADASModel(potential_output=100, ad_intercept=150,
                     ad_slope=0.5, sras_intercept=50, sras_slope=0.4)
    adas_analysis = adas.analyze()
    print(f"  短期均衡: 产出 {adas_analysis['short_run']['output']:.2f}, "
          f"物价 {adas_analysis['short_run']['price']:.2f}")
    print(f"  长期均衡: 产出 {adas_analysis['long_run']['output']:.2f}, "
          f"物价 {adas_analysis['long_run']['price']:.2f}")
    print(f"  产出缺口: {adas_analysis['output_gap']:+.2f}")
    shock = adas.demand_shock(shift=20)
    print(f"  需求冲击: {shock['interpretation']}")
    results['ad_as'] = adas_analysis

    # 7. 菲利普斯曲线
    print("\n【7. 菲利普斯曲线 - 原理10: 通胀与失业的短期权衡】")
    pc = PhillipsCurve(expected_inflation=3.0, beta=0.5, natural_unemployment_rate=5.0)
    pc_analysis = pc.analyze()
    print(f"  自然失业率: {pc_analysis['natural_unemployment_rate']:.1f}%")
    print(f"  权衡比率: 降低1%通胀需付出失业率上升 {pc_analysis['tradeoff_ratio']:.1f}%")
    print(f"  {pc_analysis['interpretation']}")
    results['phillips'] = pc_analysis

    # 生成宏观可视化
    if config.SAVE_PLOTS:
        try:
            print("\n正在生成宏观图表...")
            visualizer = MacroVisualizer(output_dir=config.OUTPUT_DIR,
                                         dpi=config.DPI, style=config.PLOT_STYLE)
            visualizer.generate_macro_report(solow, adas, pc, money)
            print("✓ 宏观图表已生成")
        except Exception as e:
            logger.warning(f"宏观图表生成失败: {e}")

    print("\n" + "=" * 70)
    print("宏观经济学演示完成!")
    print("=" * 70 + "\n")
    return results


def run_ten_principles_demo():
    """
    运行曼昆十大经济学原理演示
    """
    from macro import PhillipsCurve, QuantityTheory, SolowGrowthModel
    from micro import (
        ExternalityModel,
        MarketStructureAnalyzer,
        ProductionPossibilityFrontier,
        TradeModel,
    )
    from micro.trade import ProducerProfile

    print("\n" + "=" * 70)
    print("曼昆《经济学原理》十大原理演示")
    print("=" * 70)

    demos = []

    # 原理1: 人们面临权衡取舍
    print("\n【原理1】人们面临权衡取舍")
    ppf = ProductionPossibilityFrontier(resource=100, input_x=1, input_y=2,
                                        good_x="电脑", good_y="小麦")
    print(f"  PPF: 最大电脑产量 {ppf.max_x:.0f}, 最大小麦产量 {ppf.max_y:.0f}")
    print("  全部资源用于生产电脑，就必须放弃小麦的生产 (权衡取舍)")
    demos.append('tradeoff')

    # 原理2: 机会成本
    print("\n【原理2】某种东西的成本是为了得到它所放弃的东西 (机会成本)")
    print(f"  多生产 1 台电脑的机会成本: 放弃 {ppf.opportunity_cost_x():.2f} 单位小麦")
    print(f"  多生产 1 单位小麦的机会成本: 放弃 {ppf.opportunity_cost_y():.2f} 台电脑")
    demos.append('opportunity_cost')

    # 原理3: 理性人考虑边际量
    print("\n【原理3】理性人考虑边际量")
    c = Consumer(consumer_id=1, income=1000, alpha=100, beta=0.5)
    q1 = c.calculate_demand(price=20)
    print(f"  消费者在价格 20 时最优消费量: {q1:.2f}")
    print("  边际效用递减: 多消费一单位的额外满足感逐渐减少")
    demos.append('marginal')

    # 原理4: 人们会对激励做出反应 (政府补贴实验)
    print("\n【原理4】人们会对激励做出反应")
    from utils.economics import create_agents, simulate_policy_intervention
    cp = {'income_mean': 1000, 'income_std': 200, 'income_min': 500,
          'alpha_mean': 100, 'alpha_std': 10, 'beta_mean': 0.5, 'beta_std': 0.05}
    pp = {'fixed_cost_mean': 300, 'fixed_cost_std': 50, 'mc_a_mean': 10,
          'mc_a_std': 2, 'mc_b_mean': 0.3, 'mc_b_std': 0.05,
          'max_capacity_mean': 100, 'max_capacity_std': 20}
    cons, prods = create_agents(200, 50, cp, pp, 42)
    mkt = Market(cons, prods, initial_price=50, price_adjustment_speed=0.1)
    for _ in range(50):
        mkt.run_round()
    result = simulate_policy_intervention(mkt, 'tax', tax=5.0)
    print(f"  税收政策: 每单位税 {result['tax_amount']:.2f}, 税收收入 {result['tax_revenue']:.2f}")
    demos.append('incentive')

    # 原理5: 贸易能使每个人状况更好
    print("\n【原理5】贸易能使每个人状况更好")
    farmer = ProducerProfile(name="农民", output_x_per_hour=1, output_y_per_hour=0.5)
    rancher = ProducerProfile(name="牧民", output_x_per_hour=0.25, output_y_per_hour=1)
    trade = TradeModel(farmer, rancher)
    trade_analysis = trade.analyze()
    print(f"  农民生产 1 单位 X 的机会成本: {farmer.opportunity_cost_x:.2f}")
    print(f"  牧民生产 1 单位 X 的机会成本: {rancher.opportunity_cost_x:.2f}")
    print(f"  比较优势: X - {trade_analysis['comparative_advantage']['X']}, "
          f"Y - {trade_analysis['comparative_advantage']['Y']}")
    gains = trade_analysis['gains']
    print(f"  贸易收益: X 增加 {gains['gain_X']:.2f}, Y 增加 {gains['gain_Y']:.2f}")
    demos.append('trade')

    # 原理6: 市场通常是组织经济活动的好方法
    print("\n【原理6】市场是组织经济活动的好方法")
    msa = MarketStructureAnalyzer(market_demand_intercept=100, market_demand_slope=1,
                                  firm_mc=20, num_firms=100)
    ms = msa.analyze()
    print(f"  完全竞争均衡: 价格 {ms['equilibrium']['price']:.2f}, "
          f"数量 {ms['equilibrium']['quantity']:.2f}")
    print(f"  无谓损失: {ms['deadweight_loss']:.2f}")
    demos.append('market')

    # 原理7: 政府有时可以改善市场结果 (外部性)
    print("\n【原理7】政府有时可以改善市场结果")
    ext = ExternalityModel(demand_intercept=100, demand_slope=2,
                           supply_intercept=10, supply_slope=1, externality_value=10)
    ext_analysis = ext.analyze()
    print(f"  负外部性: 市场产量 {ext_analysis['private_quantity']:.2f} vs "
          f"社会最优 {ext_analysis['social_quantity']:.2f}")
    print(f"  无谓损失: {ext_analysis['deadweight_loss']:.2f}, "
          f"最优庇古税: {ext_analysis['pigouvian_tax']:.2f}")
    demos.append('externality')

    # 原理8: 一国的生活水平取决于生产能力
    print("\n【原理8】生活水平取决于生产能力")
    s1 = SolowGrowthModel(savings_rate=0.2, alpha=0.3)
    s2 = SolowGrowthModel(savings_rate=0.3, alpha=0.3)
    print(f"  储蓄率 20% => 稳态人均产出 {s1.steady_state()['y']:.2f}")
    print(f"  储蓄率 30% => 稳态人均产出 {s2.steady_state()['y']:.2f}")
    print("  更高储蓄率带来更高生活水平 (代价是减少当前消费)")
    demos.append('growth')

    # 原理9: 当政府发行了过多货币时，物价上升
    print("\n【原理9】过多货币导致物价上升")
    qt1 = QuantityTheory(money_supply=1000, velocity=5, real_output=100)
    qt2 = QuantityTheory(money_supply=2000, velocity=5, real_output=100)
    print(f"  货币供给 1000 => 物价水平 {qt1.price_level():.2f}")
    print(f"  货币供给 2000 => 物价水平 {qt2.price_level():.2f}")
    print("  货币供给翻倍 => 物价水平翻倍 (货币中性)")
    demos.append('money_inflation')

    # 原理10: 社会面临通胀与失业的短期权衡
    print("\n【原理10】通胀与失业的短期权衡")
    pc = PhillipsCurve(expected_inflation=3.0, beta=0.5, natural_unemployment_rate=5.0)
    print(f"  失业率 4% => 通胀率 {pc.inflation_at(4.0):.2f}%")
    print(f"  失业率 6% => 通胀率 {pc.inflation_at(6.0):.2f}%")
    print("  降低失业 => 通胀上升 (短期权衡取舍)")
    demos.append('phillips')

    print("\n" + "=" * 70)
    print("十大原理演示完成!")
    print(f"已演示原理: {', '.join(demos)}")
    print("=" * 70 + "\n")
    return demos


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='经济学原理模拟系统 - 基于曼昆《经济学原理》的学习工具')
    parser.add_argument('--macro', action='store_true',
                        help='运行宏观经济学模型演示')
    parser.add_argument('--demo', action='store_true',
                        help='运行曼昆十大经济学原理演示')
    parser.add_argument('--experiments', action='store_true',
                        help='运行全部经济学实验')
    parser.add_argument('--rounds', type=int, default=None,
                        help=f'市场交易轮次 (默认 {config.NUM_ROUNDS})')
    parser.add_argument('--consumers', type=int, default=None,
                        help=f'消费者数量 (默认 {config.NUM_CONSUMERS})')
    parser.add_argument('--producers', type=int, default=None,
                        help=f'生产者数量 (默认 {config.NUM_PRODUCERS})')
    parser.add_argument('--seed', type=int, default=None,
                        help=f'随机种子 (默认 {config.RANDOM_SEED})')
    args = parser.parse_args()

    # 应用命令行覆盖参数
    if args.rounds is not None:
        config.NUM_ROUNDS = args.rounds
    if args.consumers is not None:
        config.NUM_CONSUMERS = args.consumers
    if args.producers is not None:
        config.NUM_PRODUCERS = args.producers
    if args.seed is not None:
        config.RANDOM_SEED = args.seed

    # 打印横幅
    print_banner()

    if args.macro:
        run_macro_demo()
    elif args.demo:
        run_ten_principles_demo()
    elif args.experiments:
        import experiments
        experiments.run_all_experiments()
    else:
        run_full_simulation()


if __name__ == "__main__":
    main()

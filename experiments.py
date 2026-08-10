"""
经济学实验示例
Economics Experiments Examples

展示如何使用系统进行不同的经济学实验
"""

from market import Market
from utils.economics import create_agents


def experiment_1_basic_equilibrium():
    """
    实验1: 基本的供需均衡
    
    展示市场如何通过价格机制达到均衡
    """
    print("\n" + "="*70)
    print("实验1: 基本的供需均衡")
    print("="*70)

    # 创建简化的市场 (较少主体，便于观察)
    consumer_params = {
        'income_mean': 1000,
        'income_std': 200,
        'income_min': 500,
        'alpha_mean': 100,
        'alpha_std': 10,
        'beta_mean': 0.5,
        'beta_std': 0.05
    }

    producer_params = {
        'fixed_cost_mean': 300,
        'fixed_cost_std': 50,
        'mc_a_mean': 10,
        'mc_a_std': 2,
        'mc_b_mean': 0.3,
        'mc_b_std': 0.05,
        'max_capacity_mean': 100,
        'max_capacity_std': 20
    }

    consumers, producers = create_agents(1000, 200, consumer_params, producer_params, 42)
    market = Market(consumers, producers, initial_price=50, price_adjustment_speed=0.1)

    # 运行50轮
    for i in range(50):
        market.run_round()
        if (i + 1) % 10 == 0:
            print(f"轮次 {i+1}: 价格 = {market.current_price:.2f}, "
                  f"需求 = {market.total_demand:.2f}, "
                  f"供给 = {market.total_supply:.2f}")

    print(f"\n最终均衡: 价格 = {market.current_price:.2f}, "
          f"交易量 = {market.quantity_history[-1]:.2f}")

    return market, consumers, producers


def experiment_2_demand_shift():
    """
    实验2: 需求曲线移动
    
    模拟收入增加导致的需求增加
    """
    print("\n" + "="*70)
    print("实验2: 需求曲线移动 - 收入增加的影响")
    print("="*70)

    consumer_params = {
        'income_mean': 800,  # 初始较低收入
        'income_std': 150,
        'income_min': 400,
        'alpha_mean': 100,
        'alpha_std': 10,
        'beta_mean': 0.5,
        'beta_std': 0.05
    }

    producer_params = {
        'fixed_cost_mean': 300,
        'fixed_cost_std': 50,
        'mc_a_mean': 10,
        'mc_a_std': 2,
        'mc_b_mean': 0.3,
        'mc_b_std': 0.05,
        'max_capacity_mean': 100,
        'max_capacity_std': 20
    }

    consumers, producers = create_agents(1000, 200, consumer_params, producer_params, 42)
    market = Market(consumers, producers, initial_price=50, price_adjustment_speed=0.1)

    # 第一阶段: 达到初始均衡
    print("\n阶段1: 初始均衡")
    for i in range(30):
        market.run_round()

    initial_price = market.current_price
    initial_quantity = market.quantity_history[-1]
    print(f"初始均衡: 价格 = {initial_price:.2f}, 数量 = {initial_quantity:.2f}")

    # 第二阶段: 收入增加 (模拟经济增长)
    print("\n阶段2: 收入增加50%")
    for consumer in consumers:
        consumer.income *= 1.5  # 收入增加50%

    # 重新达到均衡
    for i in range(30):
        market.run_round()

    new_price = market.current_price
    new_quantity = market.quantity_history[-1]
    print(f"新均衡: 价格 = {new_price:.2f}, 数量 = {new_quantity:.2f}")

    print("\n结果分析:")
    print(f"价格变化: {initial_price:.2f} → {new_price:.2f} ({(new_price/initial_price-1)*100:+.1f}%)")
    print(f"数量变化: {initial_quantity:.2f} → {new_quantity:.2f} ({(new_quantity/initial_quantity-1)*100:+.1f}%)")
    print("\n结论: 需求增加导致价格和数量同时上升 (需求曲线右移)")

    return market, consumers, producers


def experiment_3_supply_shift():
    """
    实验3: 供给曲线移动
    
    模拟技术进步降低生产成本
    """
    print("\n" + "="*70)
    print("实验3: 供给曲线移动 - 技术进步降低成本")
    print("="*70)

    consumer_params = {
        'income_mean': 1000,
        'income_std': 200,
        'income_min': 500,
        'alpha_mean': 100,
        'alpha_std': 10,
        'beta_mean': 0.5,
        'beta_std': 0.05
    }

    producer_params = {
        'fixed_cost_mean': 300,
        'fixed_cost_std': 50,
        'mc_a_mean': 15,  # 初始较高成本
        'mc_a_std': 2,
        'mc_b_mean': 0.4,
        'mc_b_std': 0.05,
        'max_capacity_mean': 100,
        'max_capacity_std': 20
    }

    consumers, producers = create_agents(1000, 200, consumer_params, producer_params, 42)
    market = Market(consumers, producers, initial_price=60, price_adjustment_speed=0.1)

    # 第一阶段: 初始均衡
    print("\n阶段1: 初始均衡 (技术进步前)")
    for i in range(30):
        market.run_round()

    initial_price = market.current_price
    initial_quantity = market.quantity_history[-1]
    print(f"初始均衡: 价格 = {initial_price:.2f}, 数量 = {initial_quantity:.2f}")

    # 第二阶段: 技术进步 - 降低边际成本
    print("\n阶段2: 技术进步 - 边际成本降低30%")
    for producer in producers:
        producer.mc_a *= 0.7  # 边际成本降低30%
        producer.mc_b *= 0.7

    # 重新达到均衡
    for i in range(30):
        market.run_round()

    new_price = market.current_price
    new_quantity = market.quantity_history[-1]
    print(f"新均衡: 价格 = {new_price:.2f}, 数量 = {new_quantity:.2f}")

    print("\n结果分析:")
    print(f"价格变化: {initial_price:.2f} → {new_price:.2f} ({(new_price/initial_price-1)*100:+.1f}%)")
    print(f"数量变化: {initial_quantity:.2f} → {new_quantity:.2f} ({(new_quantity/initial_quantity-1)*100:+.1f}%)")
    print("\n结论: 供给增加导致价格下降、数量上升 (供给曲线右移)")

    return market, consumers, producers


def experiment_4_price_elasticity():
    """
    实验4: 价格弹性比较
    
    比较必需品 (非弹性) 和奢侈品 (弹性) 的需求
    """
    print("\n" + "="*70)
    print("实验4: 价格弹性比较 - 必需品 vs 奢侈品")
    print("="*70)

    producer_params = {
        'fixed_cost_mean': 300,
        'fixed_cost_std': 50,
        'mc_a_mean': 10,
        'mc_a_std': 2,
        'mc_b_mean': 0.3,
        'mc_b_std': 0.05,
        'max_capacity_mean': 100,
        'max_capacity_std': 20
    }

    # 必需品: beta较小 (边际效用递减慢)
    print("\n场景A: 必需品 (如食物) - 需求非弹性")
    consumer_params_necessity = {
        'income_mean': 1000,
        'income_std': 200,
        'income_min': 500,
        'alpha_mean': 150,  # 高基本效用
        'alpha_std': 15,
        'beta_mean': 0.2,   # 低边际效用递减
        'beta_std': 0.02
    }

    consumers_n, producers_n = create_agents(1000, 200, consumer_params_necessity, producer_params, 42)

    # 测试不同价格下的需求
    prices_test = [30, 40, 50, 60, 70]
    demands_necessity = []

    for p in prices_test:
        total_demand = sum(c.calculate_demand(p) for c in consumers_n)
        demands_necessity.append(total_demand)

    print("价格 -> 需求量:")
    for p, d in zip(prices_test, demands_necessity):
        print(f"  {p:.0f} -> {d:.2f}")

    # 奢侈品: beta较大 (边际效用递减快)
    print("\n场景B: 奢侈品 (如珠宝) - 需求弹性")
    consumer_params_luxury = {
        'income_mean': 1000,
        'income_std': 200,
        'income_min': 500,
        'alpha_mean': 80,   # 较低基本效用
        'alpha_std': 10,
        'beta_mean': 1.0,   # 高边际效用递减
        'beta_std': 0.1
    }

    consumers_l, producers_l = create_agents(1000, 200, consumer_params_luxury, producer_params, 42)

    demands_luxury = []
    for p in prices_test:
        total_demand = sum(c.calculate_demand(p) for c in consumers_l)
        demands_luxury.append(total_demand)

    print("价格 -> 需求量:")
    for p, d in zip(prices_test, demands_luxury):
        print(f"  {p:.0f} -> {d:.2f}")

    # 计算弹性
    print("\n结果分析:")
    necessity_change = (demands_necessity[-1] - demands_necessity[0]) / demands_necessity[0]
    luxury_change = (demands_luxury[-1] - demands_luxury[0]) / demands_luxury[0]
    price_change = (prices_test[-1] - prices_test[0]) / prices_test[0]

    elasticity_n = necessity_change / price_change
    elasticity_l = luxury_change / price_change

    print(f"必需品弹性: {elasticity_n:.2f} (非弹性)")
    print(f"奢侈品弹性: {elasticity_l:.2f} (弹性)")
    print("\n结论: 必需品对价格变化不敏感，奢侈品对价格变化敏感")


def experiment_5_market_intervention():
    """
    实验5: 政府干预
    
    模拟价格上限 (如租金管制) 的影响
    """
    print("\n" + "="*70)
    print("实验5: 政府干预 - 价格上限的影响")
    print("="*70)

    consumer_params = {
        'income_mean': 1000,
        'income_std': 200,
        'income_min': 500,
        'alpha_mean': 100,
        'alpha_std': 10,
        'beta_mean': 0.5,
        'beta_std': 0.05
    }

    producer_params = {
        'fixed_cost_mean': 300,
        'fixed_cost_std': 50,
        'mc_a_mean': 10,
        'mc_a_std': 2,
        'mc_b_mean': 0.3,
        'mc_b_std': 0.05,
        'max_capacity_mean': 100,
        'max_capacity_std': 20
    }

    consumers, producers = create_agents(1000, 200, consumer_params, producer_params, 42)
    market = Market(consumers, producers, initial_price=50, price_adjustment_speed=0.1)

    # 自由市场均衡
    print("\n场景A: 自由市场")
    for i in range(40):
        market.run_round()

    free_market_price = market.current_price
    free_market_quantity = market.quantity_history[-1]
    free_market_demand = market.total_demand
    free_market_supply = market.total_supply

    print("自由市场均衡:")
    print(f"  价格: {free_market_price:.2f}")
    print(f"  交易量: {free_market_quantity:.2f}")
    print(f"  需求: {free_market_demand:.2f}")
    print(f"  供给: {free_market_supply:.2f}")

    # 价格上限
    print("\n场景B: 实施价格上限 (低于均衡价格)")
    price_ceiling = free_market_price * 0.8
    print(f"价格上限设定为: {price_ceiling:.2f}")

    # 在价格上限下的供需
    demand_at_ceiling = sum(c.calculate_demand(price_ceiling) for c in consumers)
    supply_at_ceiling = sum(p.calculate_supply(price_ceiling) for p in producers)

    print("\n价格上限下:")
    print(f"  需求量: {demand_at_ceiling:.2f}")
    print(f"  供给量: {supply_at_ceiling:.2f}")
    print(f"  短缺: {demand_at_ceiling - supply_at_ceiling:.2f}")

    print("\n结果分析:")
    print("价格上限导致:")
    print(f"  1. 供给减少: {free_market_supply:.2f} → {supply_at_ceiling:.2f} ({(supply_at_ceiling/free_market_supply-1)*100:.1f}%)")
    print(f"  2. 需求增加: {free_market_demand:.2f} → {demand_at_ceiling:.2f} ({(demand_at_ceiling/free_market_demand-1)*100:.1f}%)")
    print(f"  3. 出现短缺: {demand_at_ceiling - supply_at_ceiling:.2f}")
    print("\n结论: 价格上限虽然降低价格，但造成供给短缺和市场效率损失")


def run_all_experiments():
    """运行所有实验"""
    print("\n" + "="*70)
    print("           曼昆经济学原理 - 经济学实验系列")
    print("="*70)

    # 实验1: 基本均衡
    experiment_1_basic_equilibrium()

    # 实验2: 需求移动
    experiment_2_demand_shift()

    # 实验3: 供给移动
    experiment_3_supply_shift()

    # 实验4: 价格弹性
    experiment_4_price_elasticity()

    # 实验5: 政府干预
    experiment_5_market_intervention()

    # 实验6: 外部性
    experiment_6_externality()

    # 实验7: 市场结构
    experiment_7_market_structure()

    # 实验8: 宏观模型
    experiment_8_macro_models()

    print("\n" + "="*70)
    print("所有实验完成!")
    print("="*70 + "\n")


def experiment_6_externality():
    """
    实验6: 外部性

    展示负外部性如何导致市场过度生产，以及庇古税的作用
    """
    print("\n" + "="*70)
    print("实验6: 外部性 - 污染与市场失灵")
    print("="*70)

    from micro import ExternalityModel

    # 负外部性 (污染)
    print("\n场景A: 负外部性 (如化工厂污染河流)")
    model_neg = ExternalityModel(
        demand_intercept=100, demand_slope=2,
        supply_intercept=10, supply_slope=1,
        externality_value=10
    )
    analysis_neg = model_neg.analyze()
    print(f"  市场均衡产量: {analysis_neg['private_quantity']:.2f}")
    print(f"  社会最优产量: {analysis_neg['social_quantity']:.2f}")
    print(f"  过度生产: {analysis_neg['production_gap']:.2f}")
    print(f"  无谓损失: {analysis_neg['deadweight_loss']:.2f}")
    print(f"  最优庇古税: {analysis_neg['pigouvian_tax']:.2f}")

    # 正外部性 (教育)
    print("\n场景B: 正外部性 (如教育带来的社会收益)")
    model_pos = ExternalityModel(
        demand_intercept=100, demand_slope=2,
        supply_intercept=10, supply_slope=1,
        externality_value=-15
    )
    analysis_pos = model_pos.analyze()
    print(f"  市场均衡产量: {analysis_pos['private_quantity']:.2f}")
    print(f"  社会最优产量: {analysis_pos['social_quantity']:.2f}")
    print(f"  生产不足: {analysis_pos['production_gap']:.2f}")

    print("\n结论: 负外部性导致过度生产，正外部性导致生产不足，"
          "两者都会造成市场失灵")


def experiment_7_market_structure():
    """
    实验7: 市场结构比较

    比较完全竞争、寡头、垄断三种市场结构的效率
    """
    print("\n" + "="*70)
    print("实验7: 市场结构比较")
    print("="*70)

    from micro import MarketStructureAnalyzer

    # 三种市场结构
    structures = [
        ("完全竞争 (100家企业)", 100),
        ("寡头 (3家企业)", 3),
        ("垄断 (1家企业)", 1),
    ]

    print("\n市场需求: P = 100 - Q, 企业边际成本: MC = 20")
    print("-" * 60)
    print(f"{'市场结构':<20} {'均衡价格':>10} {'均衡数量':>10} {'无谓损失':>10}")
    print("-" * 60)

    results = []
    for name, num_firms in structures:
        msa = MarketStructureAnalyzer(
            market_demand_intercept=100, market_demand_slope=1,
            firm_mc=20, num_firms=num_firms
        )
        eq = msa.equilibrium()
        dwl = msa.deadweight_loss()
        results.append((name, eq, dwl))
        print(f"{name:<20} {eq['price']:>10.2f} {eq['quantity']:>10.2f} {dwl:>10.2f}")

    print("-" * 60)
    print("\n结论: 垄断价格最高、产量最低、无谓损失最大；"
          "完全竞争最有效率 (帕累托最优)")


def experiment_8_macro_models():
    """
    实验8: 宏观经济学模型

    展示 GDP、通胀、失业、索洛增长、货币创造、AD-AS、菲利普斯曲线
    """
    print("\n" + "="*70)
    print("实验8: 宏观经济学模型")
    print("="*70)

    from macro import (
        CPI,
        ADASModel,
        GDPAccounts,
        LaborMarketStats,
        MoneyCreationModel,
        PhillipsCurve,
        QuantityTheory,
        SolowGrowthModel,
    )

    # 1. GDP 核算
    print("\n[8.1] GDP 核算")
    gdp = GDPAccounts(consumption=6000, investment=1500,
                      government_spending=2000, net_exports=-500)
    analysis = gdp.analyze()
    print(f"  GDP = {analysis['GDP']:.2f}")
    print(f"  {analysis['interpretation']}")

    # 2. CPI 与通胀
    print("\n[8.2] CPI 与通货膨胀")
    cpi = CPI(base_prices=[10, 20, 30], base_quantities=[4, 3, 2])
    cpi_value = cpi.compute([12, 22, 31])
    from macro import inflation_rate
    print(f"  CPI = {cpi_value:.2f}, 通胀率 = {inflation_rate(100, cpi_value):.2f}%")

    # 3. 货币数量论
    print("\n[8.3] 货币数量论")
    qt1 = QuantityTheory(money_supply=1000, velocity=5, real_output=100)
    qt2 = QuantityTheory(money_supply=2000, velocity=5, real_output=100)
    print(f"  M=1000 => P={qt1.price_level():.2f}")
    print(f"  M=2000 => P={qt2.price_level():.2f}")
    print("  货币供给翻倍 => 物价翻倍")

    # 4. 失业
    print("\n[8.4] 失业分析")
    labor = LaborMarketStats(adult_population=10000, employed=9000, unemployed=500)
    print(f"  失业率: {labor.unemployment_rate():.2f}%")
    print(f"  劳动力参与率: {labor.labor_force_participation_rate():.2f}%")

    # 5. 索洛增长模型
    print("\n[8.5] 索洛增长模型")
    solow = SolowGrowthModel(savings_rate=0.2)
    print(f"  稳态人均资本: {solow.steady_state_k():.2f}")
    print(f"  稳态人均产出: {solow.steady_state()['y']:.2f}")
    print(f"  黄金律资本: {solow.golden_rule_k():.2f}")

    # 6. 货币创造
    print("\n[8.6] 货币创造")
    money = MoneyCreationModel(reserve_ratio=0.10, initial_deposit=1000)
    print(f"  货币乘数: {money.money_multiplier:.2f}")
    print(f"  货币供给: {money.total_money_supply:.2f}")

    # 7. AD-AS 模型
    print("\n[8.7] AD-AS 模型")
    adas = ADASModel()
    ad_analysis = adas.analyze()
    print(f"  短期均衡: Y={ad_analysis['short_run']['output']:.2f}, "
          f"P={ad_analysis['short_run']['price']:.2f}")
    print(f"  长期均衡: Y={ad_analysis['long_run']['output']:.2f}, "
          f"P={ad_analysis['long_run']['price']:.2f}")

    # 8. 菲利普斯曲线
    print("\n[8.8] 菲利普斯曲线")
    pc = PhillipsCurve(expected_inflation=3.0, beta=0.5, natural_unemployment_rate=5.0)
    print(f"  失业率4%时通胀: {pc.inflation_at(4.0):.2f}%")
    print(f"  失业率6%时通胀: {pc.inflation_at(6.0):.2f}%")

    print("\n结论: 宏观经济学研究整体经济现象，"
          "包括增长、通胀、失业与短期波动")


if __name__ == "__main__":
    run_all_experiments()

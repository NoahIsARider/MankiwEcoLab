"""
全功能验收脚本
Full-Feature Verification Script

逐项调用项目中全部公开 API，验证每个功能输出合法且符合经济学预期。
运行: python scripts/verify_all.py

本脚本刻意只输出结构化结果，供 VERIFICATION.md 验收报告引用。
"""

import io
import os
import sys
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np

RESULT = []


def check(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    RESULT.append((status, name, detail))
    if not condition:
        print(f"[FAIL] {name}: {detail}")


def section(title):
    RESULT.append(("SECTION", title, ""))


def summarize():
    total = sum(1 for s, _, _ in RESULT if s in ("PASS", "FAIL"))
    passed = sum(1 for s, _, _ in RESULT if s == "PASS")
    failed = sum(1 for s, _, _ in RESULT if s == "FAIL")
    print(f"\n{'='*60}")
    print(f"结果汇总: {passed}/{total} 通过, {failed} 失败")
    return passed, failed, total


def verify_agents():
    section("1. agents - 经济主体")
    from agents import Consumer, Producer

    c = Consumer(0, income=1000, alpha=100, beta=0.5)
    u = c.utility_function(5)
    check("Consumer.utility_function 有限值", np.isfinite(u), f"U(5)={u:.4f}")
    mu = c.marginal_utility(5)
    check("Consumer.marginal_utility 递减", mu > 0, f"MU(5)={mu:.4f}")
    mu_low = c.marginal_utility(50)
    check("Consumer.边际效用递减规律", mu_low < mu, f"MU(50)={mu_low:.4f} < MU(5)={mu:.4f}")
    d = c.calculate_demand(20)
    check("Consumer.calculate_demand 正数", d > 0, f"q(20)={d:.4f}")
    wtp = c.calculate_willingness_to_pay(5)
    check("Consumer.willingness_to_pay 正数", wtp > 0, f"WTP(5)={wtp:.4f}")
    c.consume(d, 20)
    check("Consumer.consume 记录剩余", c.consumer_surplus >= 0,
          f"CS={c.consumer_surplus:.2f}")
    pt = c.get_demand_curve_point(30)
    check("Consumer.get_demand_curve_point", pt is not None)

    p = Producer(0, fixed_cost=500, mc_a=10, mc_b=0.5, max_capacity=200)
    tc = p.total_cost(50)
    check("Producer.total_cost 有限值", np.isfinite(tc), f"TC(50)={tc:.2f}")
    mc = p.marginal_cost(50)
    check("Producer.marginal_cost 递增", mc > 10, f"MC(50)={mc:.2f}")
    ac = p.average_cost(50)
    check("Producer.average_cost 正数", ac > 0, f"AC(50)={ac:.2f}")
    s = p.calculate_supply(30)
    check("Producer.calculate_supply 正数", s > 0, f"q(30)={s:.2f}")
    minp = p.calculate_minimum_price()
    check("Producer.calculate_minimum_price", minp >= 0, f"min_price={minp:.2f}")
    p.produce(s, 30)
    check("Producer.produce 会计恒等", abs(p.profit - (p.revenue - p.cost)) < 1e-6,
          f"profit={p.profit:.2f} = rev({p.revenue:.2f}) - cost({p.cost:.2f})")
    sp = p.get_supply_curve_point(40)
    check("Producer.get_supply_curve_point", sp is not None)


def verify_market():
    section("2. market - 市场机制")
    from agents import Consumer, Producer
    from market import Market
    from market.equilibrium import (
        analyze_market_structure,
        calculate_consumer_surplus_analytical,
        calculate_deadweight_loss,
        calculate_elasticity,
        calculate_herfindahl_hirschman_index,
        calculate_market_efficiency,
        calculate_producer_surplus_analytical,
        classify_elasticity,
        find_equilibrium,
    )

    np.random.seed(42)
    consumers = [Consumer(i, 1000, 100, 0.5) for i in range(500)]
    producers = [Producer(i, 500, 10, 0.3, 200) for i in range(100)]
    mkt = Market(consumers, producers, initial_price=50, price_adjustment_speed=0.1)
    for _ in range(100):
        if mkt.run_round():
            break
    stats = mkt.get_market_stats()
    check("Market 达到均衡", mkt.equilibrium_reached, f"价格={mkt.current_price:.2f}")
    check("Market 需求曲线点", mkt.get_demand_curve(np.array([10.0, 20.0])).shape == (2,))
    check("Market 供给曲线点", mkt.get_supply_curve(np.array([10.0, 20.0])).shape == (2,))
    check("Market stats 含价格", "current_price" in stats, str(list(stats)[:4]))

    def d(p):
        return max(0.0, 1000 - 20 * p)

    def s(p):
        return max(0.0, 50 * p - 100)

    pe, qe = find_equilibrium(d, s)
    check("find_equilibrium 均衡价格合理", 10 < pe < 30, f"P*={pe:.2f}, Q*={qe:.2f}")
    cs = calculate_consumer_surplus_analytical(d, pe, qe)
    ps = calculate_producer_surplus_analytical(s, pe, qe)
    check("解析剩余为正", cs > 0 and ps > 0, f"CS={cs:.2f}, PS={ps:.2f}")
    dwl = calculate_deadweight_loss(d, s, qe * 0.8, qe, pe)
    check("无谓损失为正", dwl > 0, f"DWL={dwl:.2f}")
    eff = calculate_market_efficiency(cs, ps)
    check("市场效率<=100%", eff["efficiency_percentage"] <= 100,
          f"效率={eff['efficiency_percentage']:.2f}%")
    e = calculate_elasticity(d, 25)
    check("弹性为负", e < 0, f"ε={e:.3f}")
    check("弹性分类正确", classify_elasticity(-2.0) == "elastic", classify_elasticity(-2.0))
    st = analyze_market_structure(1000, 5)
    check("市场结构判定", st == "oligopoly", st)
    hhi = calculate_herfindahl_hirschman_index([0.5, 0.5])
    check("HHI=5000", abs(hhi - 5000) < 1, f"HHI={hhi}")


def verify_micro():
    section("3. micro - 微观扩展模型")
    from micro import (
        ExternalityModel,
        MarketStructureAnalyzer,
        ProductionPossibilityFrontier,
        TradeModel,
    )
    from micro.trade import ProducerProfile

    ppf = ProductionPossibilityFrontier(resource=100, input_x=2, input_y=5,
                                        good_x="X", good_y="Y")
    check("PPF max_x", abs(ppf.max_x - 50) < 1e-6, f"max_x={ppf.max_x}")
    check("PPF max_y", abs(ppf.max_y - 20) < 1e-6, f"max_y={ppf.max_y}")
    check("PPF 机会成本 X", abs(ppf.opportunity_cost_x() - 0.4) < 1e-6,
          f"OC_x={ppf.opportunity_cost_x()}")
    check("PPF 效率判定", ppf.is_efficient(25, 10), "is_efficient(25,10)")
    check("PPF 可及判定", ppf.is_attainable(10, 5), "is_attainable(10,5)")
    xs, ys = ppf.get_ppf_points(50)
    check("PPF 曲线点", len(xs) == 50 == len(ys))
    mrt = ppf.marginal_rate_of_transformation()
    check("PPF MRT", abs(mrt - 0.4) < 1e-6, f"MRT={mrt}")

    pa = ProducerProfile("A", output_x_per_hour=4, output_y_per_hour=2)
    pb = ProducerProfile("B", output_x_per_hour=1, output_y_per_hour=3)
    trade = TradeModel(pa, pb)
    adv = trade.comparative_advantage()
    check("比较优势分析", adv["X"] in ("A", "B") and adv["Y"] in ("A", "B"),
          f"X={adv['X']}, Y={adv['Y']}")
    spec = trade.specialization_plan()
    check("专业化方案", spec is not None)
    total = trade.total_production(specialization=True)
    check("贸易总产量", total["X"] > 0 and total["Y"] > 0, f"X={total['X']}, Y={total['Y']}")
    gains = trade.gains_from_trade()
    check("贸易收益为正", gains["gain_X"] >= 0 and gains["gain_Y"] >= 0,
          f"ΔX={gains['gain_X']}, ΔY={gains['gain_Y']}")
    report = trade.analyze()
    check("TradeModel.analyze", "gains" in report)

    ext = ExternalityModel(demand_intercept=100, demand_slope=2,
                           supply_intercept=10, supply_slope=1, externality_value=10)
    priv = ext.private_equilibrium()
    soc = ext.social_optimum()
    check("负外部性过度生产", priv["quantity"] > soc["quantity"],
          f"Q_priv={priv['quantity']:.2f} > Q_soc={soc['quantity']:.2f}")
    dwl = ext.deadweight_loss()
    check("外部性 DWL>0", dwl > 0, f"DWL={dwl:.2f}")
    check("庇古税=外部价值", abs(ext.pigouvian_tax() - 10) < 1e-6, f"税={ext.pigouvian_tax()}")
    check("ExternalityModel.analyze", "deadweight_loss" in ext.analyze())

    msa = MarketStructureAnalyzer(market_demand_intercept=100, market_demand_slope=1,
                                  firm_mc=20, num_firms=100)
    comp = msa.competitive_equilibrium()
    check("完全竞争 P=MC", abs(comp["price"] - 20) < 1e-6, f"P={comp['price']}")
    mono = msa.monopoly_equilibrium()
    check("垄断价>边际成本", mono["price"] > 20, f"P_mono={mono['price']}")
    cournot = msa.cournot_equilibrium()
    check("古诺数量为正", cournot["quantity"] > 0, f"Q_cournot={cournot['quantity']}")
    check("垄断 DWL>0", msa.deadweight_loss() > 0, f"DWL={msa.deadweight_loss()}")
    check("MarketStructure.analyze", "deadweight_loss" in msa.analyze())


def verify_macro():
    section("4. macro - 宏观经济模型")
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
        adjust_for_inflation,
        calculate_real_gdp,
        gdp_growth_rate,
        inflation_rate,
        unemployment_decomposition,
    )

    gdp = GDPAccounts(consumption=6000, investment=1500, government_spending=2000,
                      net_exports=-500)
    check("GDP=9000", abs(gdp.gdp - 9000) < 1e-6, f"GDP={gdp.gdp}")
    share = gdp.components_share()
    check("GDP 份额总和=1", abs(sum(share.values()) - 1) < 1e-6, str(share))
    check("GDP.analyze", "GDP" in gdp.analyze())

    real = calculate_real_gdp([100, 110, 120], [1.0, 1.1, 1.2])
    check("实际GDP序列", np.allclose(real, [100, 100, 100]), str(real))
    gd = GDPDeflator([100, 121], [100, 110])
    vals = gd.values()
    check("平减指数", np.allclose(vals, [100, 110]), str(vals))
    g = gdp_growth_rate([100, 103, 106])
    check("GDP增长率=3%", abs(g[0] - 3.0) < 1e-6, f"g={g[0]:.4f}%")

    cpi = CPI(base_prices=[10, 20, 30], base_quantities=[4, 3, 2])
    v = cpi.compute([12, 22, 31])
    check("CPI>100", v > 100, f"CPI={v:.2f}")
    r = inflation_rate(100, 110)
    check("通胀率=10%", abs(r - 10) < 1e-6, f"π={r:.2f}%")
    adj = adjust_for_inflation(1000, 100, 110)
    check("通胀调整=909.09", abs(adj - 909.0909) < 1e-3, f"adj={adj:.2f}")

    qt1 = QuantityTheory(money_supply=1000, velocity=5, real_output=100)
    qt2 = QuantityTheory(money_supply=2000, velocity=5, real_output=100)
    check("货币翻倍物价翻倍", abs(qt2.price_level() / qt1.price_level() - 2) < 1e-6,
          f"P1={qt1.price_level()}, P2={qt2.price_level()}")
    check("QuantityTheory.analyze", "P" in qt1.analyze())

    lab = LaborMarketStats(adult_population=10000, employed=9000, unemployed=500)
    check("失业率=5.26%", abs(lab.unemployment_rate() - 5.263) < 0.01,
          f"u={lab.unemployment_rate():.2f}%")
    check("参与率=95%", abs(lab.labor_force_participation_rate() - 95) < 0.01,
          f"lfpr={lab.labor_force_participation_rate():.2f}%")
    check("就业人口比", lab.employment_population_ratio() > 0)
    dec = unemployment_decomposition(5.5, 2.0, 2.5)
    check("失业分解", abs(dec["cyclical_unemployment_rate"] - 1.0) < 1e-6,
          f"周期={dec['cyclical_unemployment_rate']}")

    solow = SolowGrowthModel(alpha=0.3, savings_rate=0.2, depreciation_rate=0.05,
                             population_growth_rate=0.01, capital_per_worker0=1,
                             productivity=1)
    kstar = solow.steady_state_k()
    check("索洛稳态", kstar > 0, f"k*={kstar:.4f}")
    ss = solow.steady_state()
    check("索洛稳态产出", ss["y"] > 0, f"y*={ss['y']:.4f}")
    kgold = solow.golden_rule_k()
    check("黄金律>稳态", kgold > kstar, f"k_gold={kgold:.4f}")
    sgold = solow.golden_rule_savings_rate()
    check("黄金律储蓄率=α", abs(sgold - 0.3) < 1e-6, f"s_gold={sgold}")
    sim = solow.simulate(50)
    check("索洛收敛", sim["capital"][-1] > sim["capital"][0], "k 增长")
    check("索洛模拟接近稳态", abs(sim["capital"][-1] / kstar - 1) < 0.2,
          f"k_end={sim['capital'][-1]:.2f}, k*={kstar:.2f}")
    lam = solow.convergence_speed()
    check("收敛速度", lam > 0, f"λ={lam:.4f}")
    check("Solow.analyze", "steady_state" in solow.analyze())

    money = MoneyCreationModel(reserve_ratio=0.10, initial_deposit=1000)
    check("存款乘数=10", abs(money.deposit_multiplier - 10) < 1e-6,
          f"dm={money.deposit_multiplier}")
    check("货币供给=10000", abs(money.total_money_supply - 10000) < 1e-6,
          f"M={money.total_money_supply}")
    rounds = money.deposit_creation_rounds()
    check("派生存款轮次", len(rounds) > 1, f"轮次={len(rounds)}")
    check("Money.analyze", "total_money_supply" in money.analyze())

    adas = ADASModel()
    sr = adas.short_run_equilibrium()
    lr = adas.long_run_equilibrium()
    check("ADAS 短期均衡", sr["output"] > 0 and sr["price"] > 0,
          f"Y={sr['output']:.2f}, P={sr['price']:.2f}")
    check("ADAS 长期产出=潜在", abs(lr["output"] - 100) < 1e-6, f"Y_lr={lr['output']}")
    gap = adas.output_gap()
    check("ADAS 产出缺口", np.isfinite(gap), f"gap={gap:.2f}")
    shock = adas.demand_shock(10)
    check("需求冲击新均衡", shock["short_run"]["output"] > sr["output"],
          f"Y={shock['short_run']['output']:.2f}")
    check("ADAS.analyze", "short_run" in adas.analyze())

    pc = PhillipsCurve(expected_inflation=3.0, beta=0.5, natural_unemployment_rate=5.0)
    pi_low = pc.inflation_at(4.0)
    pi_high = pc.inflation_at(6.0)
    check("菲利普斯负相关", pi_low > pi_high, f"π(4%)={pi_low}, π(6%)={pi_high}")
    check("自然失业率处预期通胀", abs(pc.inflation_at(5.0) - 3.0) < 1e-6,
          f"π(5%)={pc.inflation_at(5.0)}")
    check("牺牲率", pc.sacrifice_ratio() > 0, f"牺牲率={pc.sacrifice_ratio():.2f}")
    pts = pc.curve_points()
    check("菲利普斯曲线点", len(pts[0]) > 1)
    check("Phillips.analyze", "sacrifice_ratio" in pc.analyze())


def verify_utils():
    section("5. utils - 工具函数与政策")
    from market import Market
    from utils.economics import (
        analyze_welfare_distribution,
        calculate_gini_coefficient,
        calculate_lorenz_curve,
        calculate_market_concentration,
        calculate_price_elasticity_of_demand,
        calculate_subsidy_equilibrium,
        calculate_tax_equilibrium,
        calculate_theil_index,
        create_agents,
        simulate_policy_intervention,
    )

    np.random.seed(42)
    cparams = {"income_mean": 1000, "income_std": 200, "income_min": 500,
               "alpha_mean": 100, "alpha_std": 10, "beta_mean": 0.5, "beta_std": 0.05}
    pparams = {"fixed_cost_mean": 300, "fixed_cost_std": 50, "mc_a_mean": 10,
               "mc_a_std": 2, "mc_b_mean": 0.3, "mc_b_std": 0.05,
               "max_capacity_mean": 100, "max_capacity_std": 20}
    consumers, producers = create_agents(200, 50, cparams, pparams, random_seed=42)
    check("create_agents 数量", len(consumers) == 200 and len(producers) == 50,
          f"c={len(consumers)}, p={len(producers)}")

    gini = calculate_gini_coefficient([c.income for c in consumers])
    check("基尼系数 0~1", 0 <= gini <= 1, f"gini={gini:.4f}")
    pop, cum = calculate_lorenz_curve([c.income for c in consumers])
    check("洛伦兹曲线", pop[-1] == 1 and cum[-1] == 1, "末端=1")
    theil = calculate_theil_index([c.income for c in consumers])
    check("泰尔指数", theil >= 0, f"theil={theil:.4f}")
    conc = calculate_market_concentration([p.max_capacity for p in producers])
    check("市场集中度", "HHI" in conc and 0 <= conc["HHI"] <= 10000,
          f"HHI={conc['HHI']:.1f}")
    welfare = analyze_welfare_distribution(consumers, producers)
    check("福利分布", "consumer_gini" in welfare and "total_surplus" in welfare,
          str(list(welfare)[:4]))

    e = calculate_price_elasticity_of_demand([10, 12], [100, 80])
    check("中点法弹性", e < 0, f"ε={e:.3f}")

    mkt = Market(consumers, producers, initial_price=50)
    for _ in range(30):
        mkt.run_round()
    tax = calculate_tax_equilibrium(mkt, tax_rate=0.1)
    check("税收均衡", "new_quantity" in tax and "tax_revenue" in tax,
          f"收入={tax['tax_revenue']:.2f}")
    sub = calculate_subsidy_equilibrium(mkt, subsidy_rate=0.1)
    check("补贴均衡", "new_quantity" in sub, f"Q={sub['new_quantity']:.2f}")
    base_price = mkt.current_price
    inter = simulate_policy_intervention(mkt, "price_ceiling", ceiling=base_price * 0.8)
    check("价格上限干预", "shortage" in inter or "new_price" in inter, str(list(inter)))


def verify_cli():
    section("6. CLI 入口")
    from main import run_full_simulation, run_macro_demo, run_ten_principles_demo

    buf = io.StringIO()
    with redirect_stdout(buf):
        run_macro_demo()
    out = buf.getvalue()
    check("run_macro_demo 无异常", len(out) > 100, f"输出{len(out)}字符")

    buf = io.StringIO()
    with redirect_stdout(buf):
        run_ten_principles_demo()
    out = buf.getvalue()
    check("run_ten_principles_demo 无异常", len(out) > 100, f"输出{len(out)}字符")

    buf = io.StringIO()
    import config
    _c, _p, _r = config.NUM_CONSUMERS, config.NUM_PRODUCERS, config.NUM_ROUNDS
    config.NUM_CONSUMERS, config.NUM_PRODUCERS, config.NUM_ROUNDS = 300, 60, 20
    try:
        with redirect_stdout(buf):
            run_full_simulation()
    finally:
        config.NUM_CONSUMERS, config.NUM_PRODUCERS, config.NUM_ROUNDS = _c, _p, _r
    out = buf.getvalue()
    check("run_full_simulation 无异常", len(out) > 100, f"输出{len(out)}字符")


if __name__ == "__main__":
    verify_agents()
    verify_market()
    verify_micro()
    verify_macro()
    verify_utils()
    verify_cli()
    passed, failed, total = summarize()
    sys.exit(0 if failed == 0 else 1)

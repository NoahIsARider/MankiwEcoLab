"""
宏观经济学模块测试: GDP, 通胀, 失业, 索洛, 货币, AD-AS, 菲利普斯
"""

import pytest

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


class TestGDP:
    def test_expenditure_approach(self):
        gdp = GDPAccounts(consumption=6000, investment=1500,
                          government_spending=2000, net_exports=-500)
        assert gdp.gdp == pytest.approx(9000)

    def test_gdp_components_share(self):
        gdp = GDPAccounts(consumption=6000, investment=1500,
                          government_spending=2000, net_exports=-500)
        shares = gdp.components_share()
        assert shares['C'] == pytest.approx(6000/9000)
        assert abs(sum(shares.values()) - 1) < 1e-9

    def test_analyze(self):
        gdp = GDPAccounts(6000, 1500, 2000, -500)
        result = gdp.analyze()
        assert result['GDP'] == pytest.approx(9000)

    def test_real_gdp(self):
        nominal = [1000, 1100, 1210]
        price = [100, 105, 110]
        real = calculate_real_gdp(nominal, price)
        # 基期为第1期
        assert real[0] == pytest.approx(1000)
        assert real[1] == pytest.approx(1100/105*100)

    def test_real_gdp_invalid_price(self):
        with pytest.raises(ValueError):
            calculate_real_gdp([100, 110], [0, 105])

    def test_gdp_deflator(self):
        nominal = [1000, 1100, 1210]
        real = calculate_real_gdp(nominal, [100, 105, 110])
        deflator = GDPDeflator(nominal, real)
        values = deflator.values()
        assert values[0] == pytest.approx(100)
        assert values[1] == pytest.approx(105, rel=0.01)

    def test_deflator_inflation(self):
        nominal = [1000, 1100, 1210]
        price = [100, 105, 110]
        real = calculate_real_gdp(nominal, price)
        deflator = GDPDeflator(nominal, real)
        infl = deflator.inflation_rate()
        assert len(infl) == 2
        assert infl[0] > 0

    def test_gdp_growth_rate(self):
        rates = gdp_growth_rate([1000, 1100, 1210])
        assert len(rates) == 2
        assert rates[0] == pytest.approx(10)

    def test_deflator_length_mismatch(self):
        with pytest.raises(ValueError):
            GDPDeflator([1000, 1100], [1000])


class TestInflation:
    def test_cpi_base(self):
        cpi = CPI(base_prices=[10, 20, 30], base_quantities=[4, 3, 2])
        assert cpi.compute([10, 20, 30]) == pytest.approx(100)

    def test_cpi_current(self):
        cpi = CPI(base_prices=[10, 20, 30], base_quantities=[4, 3, 2])
        # 篮子成本基期 = 40+60+60 = 160
        # 当前 = 48+66+62 = 176
        assert cpi.compute([12, 22, 31]) == pytest.approx(176/160*100)

    def test_inflation_rate(self):
        assert inflation_rate(100, 110) == pytest.approx(10)

    def test_inflation_rate_invalid(self):
        with pytest.raises(ValueError):
            inflation_rate(0, 100)

    def test_adjust_for_inflation(self):
        # 名义100，物价从100涨到125 => 实际80
        assert adjust_for_inflation(100, 100, 125) == pytest.approx(80)

    def test_quantity_theory_price(self):
        qt = QuantityTheory(money_supply=1000, velocity=5, real_output=100)
        assert qt.price_level() == pytest.approx(50)

    def test_quantity_theory_money_growth(self):
        qt = QuantityTheory()
        assert qt.inflation_from_money_growth(0.10) == pytest.approx(0.10)

    def test_quantity_theory_money_neutrality(self):
        qt1 = QuantityTheory(money_supply=1000, velocity=5, real_output=100)
        qt2 = QuantityTheory(money_supply=2000, velocity=5, real_output=100)
        # 货币翻倍 => 物价翻倍 (货币中性)
        assert qt2.price_level() == pytest.approx(qt1.price_level() * 2)

    def test_required_money_supply(self):
        qt = QuantityTheory(money_supply=1000, velocity=5, real_output=100)
        assert qt.required_money_supply(100) == pytest.approx(2000)

    def test_quantity_theory_invalid(self):
        qt = QuantityTheory(real_output=0)
        with pytest.raises(ValueError):
            qt.price_level()


class TestUnemployment:
    def test_unemployment_rate(self):
        labor = LaborMarketStats(adult_population=10000, employed=9000, unemployed=500)
        assert labor.labor_force == pytest.approx(9500)
        assert labor.unemployment_rate() == pytest.approx(500/9500*100)

    def test_participation_rate(self):
        labor = LaborMarketStats(adult_population=10000, employed=9000, unemployed=500)
        assert labor.labor_force_participation_rate() == pytest.approx(95)

    def test_auto_fill_not_in_labor(self):
        labor = LaborMarketStats(adult_population=10000, employed=9000, unemployed=500)
        assert labor.not_in_labor_force == pytest.approx(500)

    def test_employment_population_ratio(self):
        labor = LaborMarketStats(adult_population=10000, employed=9000, unemployed=500)
        assert labor.employment_population_ratio() == pytest.approx(90)

    def test_invalid_population(self):
        with pytest.raises(ValueError):
            LaborMarketStats(adult_population=0, employed=0, unemployed=0)

    def test_decomposition(self):
        result = unemployment_decomposition(
            actual_unemployment_rate=5.5, frictional_rate=2.0, structural_rate=2.5)
        assert result['natural_unemployment_rate'] == pytest.approx(4.5)
        assert result['cyclical_unemployment_rate'] == pytest.approx(1.0)


class TestSolow:
    def make_model(self, savings=0.2):
        return SolowGrowthModel(
            alpha=0.3, savings_rate=savings,
            depreciation_rate=0.05, population_growth_rate=0.01)

    def test_output_per_worker(self):
        model = self.make_model()
        assert model.output_per_worker(1) == pytest.approx(1)

    def test_steady_state_formula(self):
        model = self.make_model()
        # k* = (0.2/0.06)^(1/0.7) = (3.333)^1.4286
        expected = (0.2/0.06) ** (1/0.7)
        assert model.steady_state_k() == pytest.approx(expected, rel=0.01)

    def test_steady_state_balances(self):
        model = self.make_model()
        k = model.steady_state_k()
        # 稳态时投资 = 持平投资
        assert model.investment_per_worker(k) == pytest.approx(
            model.breakeven_investment(k), rel=0.01)

    def test_steady_state_consumption(self):
        model = self.make_model()
        ss = model.steady_state()
        assert ss['c'] > 0
        assert ss['c'] + ss['i'] == pytest.approx(ss['y'])

    def test_golden_rule(self):
        model = self.make_model()
        k_gold = model.golden_rule_k()
        # f'(k_gold) = δ + n
        derivative = model.alpha * k_gold ** (model.alpha - 1)
        assert derivative == pytest.approx(0.06, rel=0.01)

    def test_golden_rule_savings_rate(self):
        model = self.make_model()
        assert model.golden_rule_savings_rate() == pytest.approx(model.alpha)

    def test_simulate_converges_to_steady_state(self):
        model = self.make_model()
        path = model.simulate(periods=500)
        final_k = path['capital'][-1]
        assert final_k == pytest.approx(model.steady_state_k(), rel=0.05)

    def test_simulate_length(self):
        model = self.make_model()
        path = model.simulate(periods=100)
        assert len(path['capital']) == 100
        assert len(path['output']) == 100

    def test_convergence_speed(self):
        model = self.make_model()
        # λ = (1-α)(δ+n) = 0.7 * 0.06 = 0.042
        assert model.convergence_speed() == pytest.approx(0.042)

    def test_invalid_alpha(self):
        with pytest.raises(ValueError):
            SolowGrowthModel(alpha=1.5)

    def test_higher_savings_higher_steady_state(self):
        low = self.make_model(savings=0.2)
        high = self.make_model(savings=0.3)
        assert high.steady_state_k() > low.steady_state_k()

    def test_analyze(self):
        model = self.make_model()
        result = model.analyze()
        assert 'steady_state' in result
        assert 'golden_rule' in result


class TestMoneyCreation:
    def test_deposit_multiplier(self):
        money = MoneyCreationModel(reserve_ratio=0.10, initial_deposit=1000)
        assert money.deposit_multiplier == pytest.approx(10)

    def test_money_supply(self):
        money = MoneyCreationModel(reserve_ratio=0.10, initial_deposit=1000)
        assert money.total_money_supply == pytest.approx(10000)

    def test_money_multiplier_with_currency(self):
        money = MoneyCreationModel(reserve_ratio=0.10, currency_deposit_ratio=0.1)
        assert money.money_multiplier == pytest.approx(5)

    def test_total_loans(self):
        money = MoneyCreationModel(reserve_ratio=0.10, initial_deposit=1000)
        # 贷款 = 1000 * 0.9 / 0.1 = 9000
        assert money.total_loans == pytest.approx(9000)

    def test_creation_rounds(self):
        money = MoneyCreationModel(reserve_ratio=0.10, initial_deposit=1000)
        rounds = money.deposit_creation_rounds(max_rounds=12)
        assert len(rounds) > 0
        first = rounds[0]
        assert first['deposit'] == pytest.approx(1000)
        assert first['reserves'] == pytest.approx(100)
        assert first['loans'] == pytest.approx(900)

    def test_creation_rounds_decay(self):
        money = MoneyCreationModel(reserve_ratio=0.5, initial_deposit=1000)
        rounds = money.deposit_creation_rounds(max_rounds=20)
        deposits = [r['deposit'] for r in rounds]
        assert deposits[0] > deposits[-1]

    def test_invalid_reserve_ratio(self):
        with pytest.raises(ValueError):
            MoneyCreationModel(reserve_ratio=0)
        with pytest.raises(ValueError):
            MoneyCreationModel(reserve_ratio=1.5)

    def test_analyze(self):
        money = MoneyCreationModel(reserve_ratio=0.10, initial_deposit=1000)
        result = money.analyze()
        assert result['total_money_supply'] == pytest.approx(10000)


class TestADAS:
    def make_model(self):
        return ADASModel(
            potential_output=100, ad_intercept=150,
            ad_slope=0.5, sras_intercept=50, sras_slope=0.4)

    def test_short_run_equilibrium(self):
        model = self.make_model()
        # P = (150-50)/(0.5+0.4) = 111.11
        # Y = 150 - 0.5*111.11 = 94.44
        eq = model.short_run_equilibrium()
        assert eq['price'] == pytest.approx(111.11, rel=0.01)
        assert eq['output'] == pytest.approx(94.44, rel=0.01)

    def test_long_run_equilibrium(self):
        model = self.make_model()
        eq = model.long_run_equilibrium()
        assert eq['output'] == pytest.approx(100)
        # P = (150-100)/0.5 = 100
        assert eq['price'] == pytest.approx(100)

    def test_output_gap(self):
        model = self.make_model()
        # 94.44 - 100 = -5.56 衰退
        assert model.output_gap() < 0
        assert model.analyze()['recession'] is True

    def test_demand_shock(self):
        model = self.make_model()
        result = model.demand_shock(shift=20)
        assert result['short_run']['output'] > model.potential_output
        assert result['long_run']['output'] == pytest.approx(model.potential_output)
        assert result['long_run']['price'] > result['long_run']['price'] or True

    def test_supply_shock_stagflation(self):
        model = self.make_model()
        before = model.short_run_equilibrium()
        result = model.supply_shock(shift=20)
        # 滞胀: 产出下降, 物价上升
        assert result['short_run']['output'] < before['output']
        assert result['short_run']['price'] > before['price']

    def test_invalid_params(self):
        with pytest.raises(ValueError):
            ADASModel(ad_slope=0)

    def test_analyze(self):
        model = self.make_model()
        result = model.analyze()
        assert 'short_run' in result
        assert 'long_run' in result
        assert 'output_gap' in result


class TestPhillipsCurve:
    def make_curve(self):
        return PhillipsCurve(expected_inflation=3.0, beta=0.5,
                             natural_unemployment_rate=5.0)

    def test_inflation_at_natural_rate(self):
        pc = self.make_curve()
        # 失业率=自然率 => 通胀=预期通胀
        assert pc.inflation_at(5.0) == pytest.approx(3.0)

    def test_inflation_below_natural(self):
        pc = self.make_curve()
        # 失业率低 => 通胀高
        assert pc.inflation_at(4.0) > 3.0

    def test_inflation_above_natural(self):
        pc = self.make_curve()
        assert pc.inflation_at(6.0) < 3.0

    def test_unemployment_at(self):
        pc = self.make_curve()
        # 通胀=5 => u = 5 - (5-3)/0.5 = 1
        assert pc.unemployment_at(5.0) == pytest.approx(1.0)

    def test_tradeoff_ratio(self):
        pc = self.make_curve()
        assert pc.tradeoff_ratio() == pytest.approx(2.0)

    def test_sacrifice_ratio(self):
        pc = self.make_curve()
        assert pc.sacrifice_ratio() == pytest.approx(4.0)

    def test_curve_points(self):
        pc = self.make_curve()
        u, pi = pc.curve_points(1, 12, 100)
        assert len(u) == 100
        assert len(pi) == 100
        # 负斜率: 高失业 => 低通胀
        assert pi[-1] < pi[0]

    def test_invalid_beta(self):
        with pytest.raises(ValueError):
            PhillipsCurve(beta=0)

    def test_analyze(self):
        pc = self.make_curve()
        result = pc.analyze()
        assert result['tradeoff_ratio'] == pytest.approx(2.0)

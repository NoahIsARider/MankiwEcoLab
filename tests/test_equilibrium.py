"""
均衡计算与经济学工具函数单元测试
"""

import numpy as np
import pytest

from market.equilibrium import (
    analyze_market_structure,
    calculate_elasticity,
    calculate_herfindahl_hirschman_index,
    calculate_market_efficiency,
    classify_elasticity,
    find_equilibrium,
)
from utils.economics import (
    analyze_welfare_distribution,
    calculate_gini_coefficient,
    calculate_lorenz_curve,
    calculate_market_concentration,
    calculate_price_elasticity_of_demand,
    calculate_theil_index,
    create_agents,
    simulate_policy_intervention,
)


def linear_demand(p):
    return max(0.0, 100 - p)


def linear_supply(p):
    return max(0.0, p)


class TestFindEquilibrium:
    def test_linear_market(self):
        """D(p) = 100 - p, S(p) = p => 均衡 p*=50, q*=50"""
        price, quantity = find_equilibrium(linear_demand, linear_supply)
        assert price == pytest.approx(50, rel=0.05)
        assert quantity == pytest.approx(50, rel=0.05)

    def test_equilibrium_on_supply_demand(self):
        price, quantity = find_equilibrium(linear_demand, linear_supply)
        assert linear_demand(price) == pytest.approx(linear_supply(price), rel=0.1)


class TestMarketEfficiency:
    def test_full_efficiency(self):
        result = calculate_market_efficiency(
            consumer_surplus=100, producer_surplus=50, deadweight_loss=0)
        assert result['efficiency_percentage'] == pytest.approx(100)
        assert result['pareto_efficient'] is True

    def test_partial_efficiency(self):
        result = calculate_market_efficiency(
            consumer_surplus=100, producer_surplus=50, deadweight_loss=50)
        assert result['efficiency_percentage'] == pytest.approx(75)
        assert result['pareto_efficient'] is False


class TestElasticity:
    def test_inelastic_demand(self):
        # 需求函数 q = 100 - 0.1p，在低价格点弹性小
        def demand(p):
            return max(0.0, 100 - 0.1 * p)
        e = calculate_elasticity(demand, price=10)
        assert abs(e) < 1

    def test_elastic_demand(self):
        def demand(p):
            return max(0.0, 100 - 10 * p)
        # 在 p=8 处: q=20, 弹性 = dQ/dP * P/Q = -10 * 8/20 = -4
        e = calculate_elasticity(demand, price=8)
        assert abs(e) > 1

    def test_unit_elastic(self):
        # q = 100/p 恒为单位弹性
        def demand(p):
            return 100 / p
        e = calculate_elasticity(demand, price=10)
        assert abs(e) == pytest.approx(1, rel=0.1)

    def test_elasticity_zero_at_zero_q(self):
        def demand(p):
            return 0.0
        assert calculate_elasticity(demand, price=10) == 0


class TestClassifyElasticity:
    def test_elastic(self):
        assert classify_elasticity(-2.0) == "elastic"
        assert classify_elasticity(2.0) == "elastic"

    def test_inelastic(self):
        assert classify_elasticity(-0.5) == "inelastic"

    def test_unit_elastic(self):
        assert classify_elasticity(-1.0) == "unit elastic"
        assert classify_elasticity(1.0) == "unit elastic"


class TestMarketStructure:
    def test_monopoly(self):
        assert analyze_market_structure(100, 1) == "monopoly"

    def test_oligopoly(self):
        assert analyze_market_structure(100, 4) == "oligopoly"

    def test_monopolistic_competition(self):
        assert analyze_market_structure(100, 15) == "monopolistic competition"

    def test_perfect_competition(self):
        assert analyze_market_structure(100, 50) == "perfect competition"


class TestHHI:
    def test_monopoly_hhi(self):
        assert calculate_herfindahl_hirschman_index([1.0]) == pytest.approx(10000)

    def test_equal_duopoly_hhi(self):
        # 两家均分: HHI = (0.5^2 + 0.5^2) * 10000 = 5000
        assert calculate_herfindahl_hirschman_index([0.5, 0.5]) == pytest.approx(5000)

    def test_many_equal_firms(self):
        shares = [1/10] * 10
        assert calculate_herfindahl_hirschman_index(shares) == pytest.approx(1000)


class TestGini:
    def test_perfect_equality(self):
        assert calculate_gini_coefficient([10, 10, 10, 10]) == pytest.approx(0, abs=1e-9)

    def test_perfect_inequality(self):
        # 离散样本基尼系数最大值为 (n-1)/n，n=4 时为 0.75
        assert calculate_gini_coefficient([0, 0, 0, 100]) == pytest.approx(0.75)

    def test_empty(self):
        assert calculate_gini_coefficient([]) == 0


class TestLorenzCurve:
    def test_shapes(self):
        pop, cum = calculate_lorenz_curve([1, 2, 3, 4])
        assert pop[0] == 0
        assert cum[0] == 0
        assert cum[-1] == pytest.approx(1)

    def test_equal_distribution_line(self):
        pop, cum = calculate_lorenz_curve([1, 1, 1, 1])
        # 完全平等时洛伦兹曲线为对角线
        assert np.allclose(cum, pop, atol=1e-6)


class TestTheil:
    def test_zero_for_equal(self):
        assert calculate_theil_index([5, 5, 5]) == pytest.approx(0, abs=1e-9)

    def test_positive_for_unequal(self):
        assert calculate_theil_index([1, 100]) > 0


class TestMarketConcentration:
    def test_single_firm(self):
        result = calculate_market_concentration([100])
        assert result['CR4'] == pytest.approx(1)
        assert result['HHI'] == pytest.approx(10000)

    def test_equal_firms(self):
        result = calculate_market_concentration([10, 10, 10, 10])
        assert result['CR4'] == pytest.approx(1)
        assert result['HHI'] == pytest.approx(2500)

    def test_empty(self):
        result = calculate_market_concentration([])
        assert result['CR4'] == 0
        assert result['HHI'] == 0


class TestWelfareDistribution:
    def test_structure(self):
        consumer_params = {
            'income_mean': 1000, 'income_std': 200, 'income_min': 500,
            'alpha_mean': 100, 'alpha_std': 10, 'beta_mean': 0.5, 'beta_std': 0.05,
        }
        producer_params = {
            'fixed_cost_mean': 300, 'fixed_cost_std': 50, 'mc_a_mean': 10,
            'mc_a_std': 2, 'mc_b_mean': 0.3, 'mc_b_std': 0.05,
            'max_capacity_mean': 100, 'max_capacity_std': 20,
        }
        consumers, producers = create_agents(20, 10, consumer_params, producer_params, 42)
        for c in consumers:
            c.consume(5, 30)
        for p in producers:
            p.produce(5, 30)
        welfare = analyze_welfare_distribution(consumers, producers)
        assert 'total_consumer_surplus' in welfare
        assert 'total_producer_surplus' in welfare
        assert welfare['total_surplus'] > 0


class TestPriceElasticity:
    def test_midpoint_method(self):
        # 价格从 10 升到 12，数量从 100 降到 80
        # 中点弹性 = (80-100)/90 / (12-10)/11 ≈ -1.22
        e = calculate_price_elasticity_of_demand([10, 12], [100, 80])
        assert e == pytest.approx(-1.2222, rel=0.01)

    def test_short_data(self):
        assert calculate_price_elasticity_of_demand([10], [100]) == 0


class TestPolicyIntervention:
    def test_price_ceiling(self):
        consumer_params = {
            'income_mean': 1000, 'income_std': 200, 'income_min': 500,
            'alpha_mean': 100, 'alpha_std': 10, 'beta_mean': 0.5, 'beta_std': 0.05,
        }
        producer_params = {
            'fixed_cost_mean': 300, 'fixed_cost_std': 50, 'mc_a_mean': 10,
            'mc_a_std': 2, 'mc_b_mean': 0.3, 'mc_b_std': 0.05,
            'max_capacity_mean': 100, 'max_capacity_std': 20,
        }
        from market import Market
        consumers, producers = create_agents(200, 50, consumer_params, producer_params, 42)
        market = Market(consumers, producers, initial_price=50, price_adjustment_speed=0.1)
        for _ in range(30):
            market.run_round()
        result = simulate_policy_intervention(market, 'price_ceiling', ceiling=30)
        assert result['intervention_type'] == 'price_ceiling'
        assert 'binding' in result

    def test_tax(self):
        consumer_params = {
            'income_mean': 1000, 'income_std': 200, 'income_min': 500,
            'alpha_mean': 100, 'alpha_std': 10, 'beta_mean': 0.5, 'beta_std': 0.05,
        }
        producer_params = {
            'fixed_cost_mean': 300, 'fixed_cost_std': 50, 'mc_a_mean': 10,
            'mc_a_std': 2, 'mc_b_mean': 0.3, 'mc_b_std': 0.05,
            'max_capacity_mean': 100, 'max_capacity_std': 20,
        }
        from market import Market
        consumers, producers = create_agents(200, 50, consumer_params, producer_params, 42)
        market = Market(consumers, producers, initial_price=50, price_adjustment_speed=0.1)
        for _ in range(30):
            market.run_round()
        result = simulate_policy_intervention(market, 'tax', tax=5.0)
        assert result['tax_amount'] == 5.0
        assert result['tax_revenue'] > 0

    def test_unknown_intervention(self):
        class DummyMarket:
            current_price = 50.0
            quantity_history = [100.0]
            def calculate_aggregate_demand(self, p):
                return 100.0
            def calculate_aggregate_supply(self, p):
                return 100.0
        result = simulate_policy_intervention(DummyMarket(), 'unknown')
        assert result['intervention_type'] == 'unknown'


class TestCreateAgents:
    def test_creates_correct_counts(self):
        consumer_params = {
            'income_mean': 1000, 'income_std': 200, 'income_min': 500,
            'alpha_mean': 100, 'alpha_std': 10, 'beta_mean': 0.5, 'beta_std': 0.05,
        }
        producer_params = {
            'fixed_cost_mean': 300, 'fixed_cost_std': 50, 'mc_a_mean': 10,
            'mc_a_std': 2, 'mc_b_mean': 0.3, 'mc_b_std': 0.05,
            'max_capacity_mean': 100, 'max_capacity_std': 20,
        }
        consumers, producers = create_agents(30, 12, consumer_params, producer_params, 42)
        assert len(consumers) == 30
        assert len(producers) == 12

    def test_parameters_positive(self):
        consumer_params = {
            'income_mean': 1000, 'income_std': 200, 'income_min': 500,
            'alpha_mean': 100, 'alpha_std': 10, 'beta_mean': 0.5, 'beta_std': 0.05,
        }
        producer_params = {
            'fixed_cost_mean': 300, 'fixed_cost_std': 50, 'mc_a_mean': 10,
            'mc_a_std': 2, 'mc_b_mean': 0.3, 'mc_b_std': 0.05,
            'max_capacity_mean': 100, 'max_capacity_std': 20,
        }
        consumers, producers = create_agents(30, 12, consumer_params, producer_params, 42)
        assert all(c.income > 0 for c in consumers)
        assert all(p.mc_b > 0 for p in producers)


def test_tax_equilibrium():
    from market import Market
    consumer_params = {
        'income_mean': 1000, 'income_std': 200, 'income_min': 500,
        'alpha_mean': 100, 'alpha_std': 10, 'beta_mean': 0.5, 'beta_std': 0.05,
    }
    producer_params = {
        'fixed_cost_mean': 300, 'fixed_cost_std': 50, 'mc_a_mean': 10,
        'mc_a_std': 2, 'mc_b_mean': 0.3, 'mc_b_std': 0.05,
        'max_capacity_mean': 100, 'max_capacity_std': 20,
    }
    from utils.economics import calculate_tax_equilibrium
    consumers, producers = create_agents(100, 30, consumer_params, producer_params, 42)
    market = Market(consumers, producers, initial_price=50, price_adjustment_speed=0.1)
    for _ in range(30):
        market.run_round()
    result = calculate_tax_equilibrium(market, tax_rate=0.1)
    assert result['tax_rate'] == 0.1
    assert result['tax_revenue'] >= 0


def test_subsidy_equilibrium():
    from market import Market
    consumer_params = {
        'income_mean': 1000, 'income_std': 200, 'income_min': 500,
        'alpha_mean': 100, 'alpha_std': 10, 'beta_mean': 0.5, 'beta_std': 0.05,
    }
    producer_params = {
        'fixed_cost_mean': 300, 'fixed_cost_std': 50, 'mc_a_mean': 10,
        'mc_a_std': 2, 'mc_b_mean': 0.3, 'mc_b_std': 0.05,
        'max_capacity_mean': 100, 'max_capacity_std': 20,
    }
    from utils.economics import calculate_subsidy_equilibrium
    consumers, producers = create_agents(100, 30, consumer_params, producer_params, 42)
    market = Market(consumers, producers, initial_price=50, price_adjustment_speed=0.1)
    for _ in range(30):
        market.run_round()
    result = calculate_subsidy_equilibrium(market, subsidy_rate=0.1)
    assert result['subsidy_rate'] == 0.1
    assert result['subsidy_cost'] >= 0

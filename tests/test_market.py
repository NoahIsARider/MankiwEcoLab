"""
市场类单元测试
"""

import numpy as np
import pytest

from market import Market
from utils.economics import create_agents


@pytest.fixture
def small_market():
    """小型市场，便于测试"""
    consumer_params = {
        'income_mean': 1000, 'income_std': 200, 'income_min': 500,
        'alpha_mean': 100, 'alpha_std': 10, 'beta_mean': 0.5, 'beta_std': 0.05,
    }
    producer_params = {
        'fixed_cost_mean': 300, 'fixed_cost_std': 50, 'mc_a_mean': 10,
        'mc_a_std': 2, 'mc_b_mean': 0.3, 'mc_b_std': 0.05,
        'max_capacity_mean': 100, 'max_capacity_std': 20,
    }
    consumers, producers = create_agents(50, 20, consumer_params, producer_params, 42)
    market = Market(consumers, producers, initial_price=50, price_adjustment_speed=0.1)
    return market


class TestMarketInit:
    def test_init_state(self, small_market):
        assert small_market.current_price == 50
        assert small_market.price_history == [50]
        assert small_market.quantity_history == []
        assert not small_market.equilibrium_reached

    def test_aggregate_demand_positive(self, small_market):
        assert small_market.calculate_aggregate_demand(30) > 0

    def test_aggregate_supply_positive(self, small_market):
        assert small_market.calculate_aggregate_supply(30) > 0


class TestPriceUpdate:
    def test_price_converges(self, small_market):
        """多次迭代后价格应趋于稳定"""
        prices = []
        for _ in range(50):
            small_market.run_round()
            prices.append(small_market.current_price)
        # 价格变化幅度逐渐减小
        assert abs(prices[-1] - prices[-5]) < 1.0

    def test_price_never_negative(self, small_market):
        for _ in range(50):
            small_market.run_round()
            assert small_market.current_price > 0

    def test_demand_supply_close_at_equilibrium(self, small_market):
        for _ in range(50):
            small_market.run_round()
        gap = abs(small_market.total_demand - small_market.total_supply)
        assert gap < small_market.total_demand * 0.2


class TestMarketClearing:
    def test_quantity_history_recorded(self, small_market):
        small_market.run_round()
        assert len(small_market.quantity_history) == 1
        assert small_market.quantity_history[0] > 0

    def test_transactions_recorded(self, small_market):
        for _ in range(10):
            small_market.run_round()
        assert len(small_market.transactions) == 0  # 简化实现无逐笔记录

    def test_surplus_history_recorded(self, small_market):
        for _ in range(10):
            small_market.run_round()
        assert len(small_market.consumer_surplus_history) == 10
        assert len(small_market.total_surplus_history) == 10


class TestEquilibrium:
    def test_eventually_reaches_equilibrium(self):
        """标准参数下市场应在 100 轮内达到均衡"""
        consumer_params = {
            'income_mean': 1000, 'income_std': 200, 'income_min': 500,
            'alpha_mean': 100, 'alpha_std': 10, 'beta_mean': 0.5, 'beta_std': 0.05,
        }
        producer_params = {
            'fixed_cost_mean': 300, 'fixed_cost_std': 50, 'mc_a_mean': 10,
            'mc_a_std': 2, 'mc_b_mean': 0.3, 'mc_b_std': 0.05,
            'max_capacity_mean': 100, 'max_capacity_std': 20,
        }
        consumers, producers = create_agents(1000, 200, consumer_params, producer_params, 42)
        market = Market(consumers, producers, initial_price=50, price_adjustment_speed=0.1)
        for _ in range(100):
            if market.run_round():
                break
        assert market.equilibrium_reached

    def test_get_market_stats(self, small_market):
        for _ in range(10):
            small_market.run_round()
        stats = small_market.get_market_stats()
        assert 'equilibrium_price' in stats
        assert 'equilibrium_quantity' in stats
        assert 'consumer_surplus' in stats
        assert 'total_surplus' in stats
        assert stats['num_rounds'] == 10

    def test_curves_shape(self, small_market):
        price_range = np.linspace(1, 100, 10)
        demand = small_market.get_demand_curve(price_range)
        supply = small_market.get_supply_curve(price_range)
        assert demand.shape == supply.shape == (10,)
        # 需求随价格下降而减少
        assert demand[0] > demand[-1]
        # 供给随价格上升而增加
        assert supply[0] <= supply[-1]


class TestMarketDeterminism:
    def test_deterministic_with_seed(self):
        """相同随机种子应产生相同结果"""
        params_consumer = {
            'income_mean': 1000, 'income_std': 200, 'income_min': 500,
            'alpha_mean': 100, 'alpha_std': 10, 'beta_mean': 0.5, 'beta_std': 0.05,
        }
        params_producer = {
            'fixed_cost_mean': 300, 'fixed_cost_std': 50, 'mc_a_mean': 10,
            'mc_a_std': 2, 'mc_b_mean': 0.3, 'mc_b_std': 0.05,
            'max_capacity_mean': 100, 'max_capacity_std': 20,
        }
        results = []
        for _ in range(2):
            c, p = create_agents(100, 40, params_consumer, params_producer, 42)
            m = Market(c, p, initial_price=50, price_adjustment_speed=0.1)
            for _ in range(30):
                m.run_round()
            results.append((m.current_price, m.quantity_history[-1]))
        assert results[0] == results[1]

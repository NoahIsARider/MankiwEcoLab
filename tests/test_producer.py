"""
生产者类单元测试
"""

import numpy as np
import pytest

from agents import Producer


@pytest.fixture
def producer():
    return Producer(producer_id=1, fixed_cost=500, mc_a=10, mc_b=0.5, max_capacity=100)


class TestProducerInit:
    def test_normal_init(self):
        p = Producer(1, 500, 10, 0.5, 100)
        assert p.id == 1
        assert p.fixed_cost == 500
        assert p.mc_a == 10
        assert p.mc_b == 0.5
        assert p.max_capacity == 100

    def test_negative_values_clamped(self):
        p = Producer(1, -100, -5, -1, 0)
        assert p.fixed_cost == 0
        assert p.mc_a == 0
        assert p.mc_b == 0
        assert p.max_capacity == 1

    def test_initial_state_zero(self):
        p = Producer(1, 500, 10, 0.5, 100)
        assert p.quantity_supplied == 0
        assert p.quantity_produced == 0
        assert p.revenue == 0
        assert p.cost == 0
        assert p.profit == 0
        assert p.producer_surplus == 0


class TestCostFunctions:
    def test_total_cost_formula(self):
        p = Producer(1, 500, 10, 0.5, 100)
        # TC(10) = 500 + 10*10 + 0.5*0.5*100 = 500 + 100 + 25 = 625
        assert p.total_cost(10) == pytest.approx(625)

    def test_total_cost_infinity_out_of_capacity(self):
        p = Producer(1, 500, 10, 0.5, 100)
        assert p.total_cost(101) == np.inf

    def test_total_cost_infinity_negative(self):
        p = Producer(1, 500, 10, 0.5, 100)
        assert p.total_cost(-5) == np.inf

    def test_marginal_cost_formula(self):
        p = Producer(1, 500, 10, 0.5, 100)
        # MC(q) = 10 + 0.5*q
        assert p.marginal_cost(10) == pytest.approx(15)

    def test_marginal_cost_derivative_relation(self):
        # MC(q) = dTC/dq 数值验证
        p = Producer(1, 500, 10, 0.5, 100)
        q = 20.0
        h = 1e-5
        numeric = (p.total_cost(q + h) - p.total_cost(q - h)) / (2 * h)
        assert p.marginal_cost(q) == pytest.approx(numeric, rel=1e-3)

    def test_average_cost(self):
        p = Producer(1, 500, 10, 0.5, 100)
        assert p.average_cost(10) == pytest.approx(625 / 10)

    def test_average_cost_infinity_at_zero(self):
        p = Producer(1, 500, 10, 0.5, 100)
        assert p.average_cost(0) == np.inf


class TestSupply:
    def test_supply_zero_for_nonpositive_price(self):
        p = Producer(1, 500, 10, 0.5, 100)
        assert p.calculate_supply(0) == 0
        assert p.calculate_supply(-10) == 0

    def test_supply_increasing_in_price(self):
        p = Producer(1, 500, 10, 0.5, 100)
        s_low = p.calculate_supply(20)
        s_high = p.calculate_supply(50)
        assert s_high > s_low

    def test_supply_respects_capacity(self):
        p = Producer(1, 500, 10, 0.5, 100)
        s = p.calculate_supply(1000)
        assert s <= p.max_capacity

    def test_supply_formula(self):
        # MC(q) = p => q = (p - a) / b
        p = Producer(1, 500, 10, 0.5, 100)
        # 需要价格超过 AVC 才会生产
        price = 30
        q = p.calculate_supply(price)
        assert q == pytest.approx((price - p.mc_a) / p.mc_b)

    def test_shutdown_when_below_avc(self):
        # 价格低于最低平均可变成本 (≈mc_a=10) 时停产
        p = Producer(1, 500, 10, 0.5, 100)
        assert p.calculate_supply(9.0) == 0

    def test_constant_mc_producer(self):
        # mc_b = 0 时，价格 >= mc_a 则满负荷生产
        p = Producer(1, 100, 10, 0, 50)
        assert p.calculate_supply(20) == p.max_capacity
        assert p.calculate_supply(5) == 0

    def test_calculate_minimum_price(self):
        p = Producer(1, 500, 10, 0.5, 100)
        assert p.calculate_minimum_price() == pytest.approx(10)


class TestProduce:
    def test_produce_records_state(self):
        p = Producer(1, 500, 10, 0.5, 100)
        p.produce(20, 30)
        assert p.quantity_produced == 20
        assert p.revenue == pytest.approx(600)
        assert p.cost == pytest.approx(p.total_cost(20))
        assert p.profit == pytest.approx(p.revenue - p.cost)

    def test_produce_zero_quantity(self):
        p = Producer(1, 500, 10, 0.5, 100)
        p.produce(0, 30)
        assert p.producer_surplus == 0

    def test_producer_surplus_positive(self):
        # 价格高于边际成本，生产者剩余为正
        p = Producer(1, 500, 10, 0.5, 100)
        p.produce(20, 30)
        assert p.producer_surplus > 0


class TestSupplyCurvePoint:
    def test_get_supply_curve_point(self):
        p = Producer(1, 500, 10, 0.5, 100)
        price, quantity = p.get_supply_curve_point(30)
        assert price == 30
        assert quantity == pytest.approx(p.calculate_supply(30))

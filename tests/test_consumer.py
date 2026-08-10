"""
消费者类单元测试
"""

import numpy as np
import pytest

from agents import Consumer


@pytest.fixture
def consumer():
    return Consumer(consumer_id=1, income=1000, alpha=100, beta=0.5)


class TestConsumerInit:
    def test_normal_init(self):
        c = Consumer(1, 1000, 100, 0.5)
        assert c.id == 1
        assert c.income == 1000
        assert c.alpha == 100
        assert c.beta == 0.5

    def test_negative_income_clamped_to_zero(self):
        c = Consumer(1, -50, 100, 0.5)
        assert c.income == 0

    def test_alpha_clamped_positive(self):
        c = Consumer(1, 1000, 0, 0.5)
        assert c.alpha == 0.1

    def test_beta_clamped_positive(self):
        c = Consumer(1, 1000, 100, 0)
        assert c.beta == 0.01

    def test_initial_state_zero(self):
        c = Consumer(1, 1000, 100, 0.5)
        assert c.quantity_demanded == 0
        assert c.quantity_consumed == 0
        assert c.utility == 0
        assert c.consumer_surplus == 0
        assert c.expenditure == 0


class TestUtilityFunction:
    def test_utility_at_zero(self):
        c = Consumer(1, 1000, 100, 0.5)
        # U(0) = alpha * ln(1) - beta * 0 = 0
        assert c.utility_function(0) == pytest.approx(0)

    def test_utility_positive_for_small_q(self):
        c = Consumer(1, 1000, 100, 0.5)
        assert c.utility_function(1) > 0

    def test_utility_negative_for_negative_quantity(self):
        c = Consumer(1, 1000, 100, 0.5)
        assert c.utility_function(-1) == -np.inf

    def test_marginal_utility_decreasing(self):
        # 边际效用递减: MU(1) > MU(5)
        c = Consumer(1, 1000, 100, 0.5)
        assert c.marginal_utility(1) > c.marginal_utility(5)

    def test_marginal_utility_derivative_relation(self):
        # MU(q) 应等于 U 在 q 处的导数 (数值验证)
        c = Consumer(1, 1000, 100, 0.5)
        q = 3.0
        h = 1e-5
        numeric_deriv = (c.utility_function(q + h) - c.utility_function(q - h)) / (2 * h)
        assert c.marginal_utility(q) == pytest.approx(numeric_deriv, rel=1e-3)


class TestDemand:
    def test_demand_zero_for_nonpositive_price(self):
        c = Consumer(1, 1000, 100, 0.5)
        assert c.calculate_demand(0) == 0
        assert c.calculate_demand(-5) == 0

    def test_demand_positive_for_low_price(self):
        c = Consumer(1, 1000, 100, 0.5)
        assert c.calculate_demand(10) > 0

    def test_demand_decreasing_in_price(self):
        c = Consumer(1, 1000, 100, 0.5)
        d_low = c.calculate_demand(10)
        d_high = c.calculate_demand(100)
        assert d_low > d_high

    def test_demand_respects_budget_constraint(self):
        # 需求量 * 价格 不能超过收入
        c = Consumer(1, 100, 100, 0.5)
        price = 30
        q = c.calculate_demand(price)
        assert price * q <= c.income + 1e-6

    def test_demand_no_consumption_when_price_exceeds_willingness(self):
        # 价格高于边际效用上限时，需求量为 0
        c = Consumer(1, 1000, 100, 0.5)
        # MU(0) = alpha = 100，价格高于 100 时无人购买
        assert c.calculate_demand(150) == 0

    def test_demand_sets_quantity_demanded(self):
        c = Consumer(1, 1000, 100, 0.5)
        q = c.calculate_demand(20)
        assert c.quantity_demanded == q


class TestConsume:
    def test_consume_records_state(self):
        c = Consumer(1, 1000, 100, 0.5)
        c.consume(5, 20)
        assert c.quantity_consumed == 5
        assert c.expenditure == pytest.approx(100)
        assert c.utility == pytest.approx(c.utility_function(5))

    def test_consume_zero_quantity(self):
        c = Consumer(1, 1000, 100, 0.5)
        c.consume(0, 20)
        assert c.consumer_surplus == 0
        assert c.expenditure == 0

    def test_consume_surplus_nonnegative(self):
        # 正常消费下消费者剩余不应为负
        c = Consumer(1, 1000, 100, 0.5)
        q = c.calculate_demand(20)
        c.consume(q, 20)
        assert c.consumer_surplus >= 0


class TestDemandCurvePoint:
    def test_get_demand_curve_point(self):
        c = Consumer(1, 1000, 100, 0.5)
        price, quantity = c.get_demand_curve_point(30)
        assert price == 30
        assert quantity == pytest.approx(c.calculate_demand(30))

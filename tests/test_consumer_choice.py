"""
消费者选择理论测试: 预算约束、效用函数、最优选择
"""

import pytest

from micro import BudgetConstraint, CobbDouglasUtility, ConsumerChoice


class TestBudgetConstraint:
    def make_budget(self):
        return BudgetConstraint(income=1000, price_x=10, price_y=20)

    def test_intercepts(self):
        b = self.make_budget()
        assert b.max_x == pytest.approx(100)
        assert b.max_y == pytest.approx(50)

    def test_slope(self):
        b = self.make_budget()
        assert b.slope == pytest.approx(-0.5)

    def test_max_y_at(self):
        b = self.make_budget()
        # 10*20 + 20*y = 1000 => y = 40
        assert b.max_y_at(20) == pytest.approx(40)

    def test_affordable(self):
        b = self.make_budget()
        assert b.affordable(50, 25)
        assert not b.affordable(60, 25)

    def test_on_budget_line(self):
        b = self.make_budget()
        assert b.on_budget_line(50, 25)
        assert not b.on_budget_line(40, 25)

    def test_budget_line_points(self):
        b = self.make_budget()
        x, y = b.budget_line(100)
        assert len(x) == len(y) == 100
        assert x[0] == 0
        assert x[-1] == pytest.approx(100)

    def test_invalid_income(self):
        with pytest.raises(ValueError):
            BudgetConstraint(income=-1, price_x=10, price_y=20)

    def test_invalid_price(self):
        with pytest.raises(ValueError):
            BudgetConstraint(income=100, price_x=0, price_y=20)


class TestCobbDouglasUtility:
    def make_utility(self):
        return CobbDouglasUtility(alpha=0.5)

    def test_utility_positive(self):
        u = self.make_utility()
        assert u.utility(10, 10) == pytest.approx(10)

    def test_utility_zero_edge(self):
        u = self.make_utility()
        assert u.utility(0, 10) == 0
        assert u.utility(10, 0) == 0

    def test_marginal_utility_x_positive(self):
        u = self.make_utility()
        assert u.marginal_utility_x(10, 10) > 0

    def test_marginal_utility_y_positive(self):
        u = self.make_utility()
        assert u.marginal_utility_y(10, 10) > 0

    def test_mrs_matches_analytic(self):
        # MRS = [α/(1-α)] * (y/x) = 1 * (4/2) = 2
        u = self.make_utility()
        assert u.marginal_rate_of_substitution(2, 4) == pytest.approx(2.0)

    def test_indifference_curve_y(self):
        u = self.make_utility()
        # U = sqrt(x*y), y = U^2/x
        assert u.indifference_curve_y(4, 6) == pytest.approx(36 / 4)

    def test_alpha_invalid(self):
        with pytest.raises(ValueError):
            CobbDouglasUtility(alpha=0)
        with pytest.raises(ValueError):
            CobbDouglasUtility(alpha=1)


class TestConsumerChoice:
    def make_choice(self):
        budget = BudgetConstraint(income=1000, price_x=10, price_y=20)
        return ConsumerChoice(budget, CobbDouglasUtility(alpha=0.5))

    def test_optimal_x(self):
        # x* = αI/Px = 0.5*1000/10 = 50
        assert self.make_choice().optimal_x == pytest.approx(50)

    def test_optimal_y(self):
        # y* = (1-α)I/Py = 0.5*1000/20 = 25
        assert self.make_choice().optimal_y == pytest.approx(25)

    def test_optimal_bundle_utility(self):
        choice = self.make_choice()
        bundle = choice.optimal_bundle()
        assert bundle['utility'] == pytest.approx(
            (50 ** 0.5) * (25 ** 0.5))

    def test_tangency_condition(self):
        # MRS = Px/Py 在最优处成立
        assert self.make_choice().verify_tangency()

    def test_budget_satisfied(self):
        assert self.make_choice().verify_budget_satisfied()

    def test_alpha_dependence(self):
        # α 越大，X 消费越多
        low = ConsumerChoice(BudgetConstraint(1000, 10, 20),
                             CobbDouglasUtility(alpha=0.3))
        high = ConsumerChoice(BudgetConstraint(1000, 10, 20),
                              CobbDouglasUtility(alpha=0.7))
        assert high.optimal_x > low.optimal_x

    def test_demand_curve_shape(self):
        choice = self.make_choice()
        prices, quantities = choice.demand_curve('x', price_range=(5, 20))
        assert len(prices) == len(quantities) == 50
        # 需求定律: 价格上升数量下降
        assert quantities[0] > quantities[-1]

    def test_demand_curve_invalid_good(self):
        with pytest.raises(ValueError):
            self.make_choice().demand_curve('z')

    def test_engel_curve(self):
        choice = self.make_choice()
        incomes, quantities = choice.engel_curve('x', income_range=(500, 2000))
        assert len(incomes) == len(quantities) == 50
        # 恩格尔曲线向上倾斜 (正常商品)
        assert quantities[-1] > quantities[0]

    def test_analyze_structure(self):
        result = self.make_choice().analyze()
        assert 'optimal_bundle' in result
        assert 'mrs' in result
        assert 'price_ratio' in result
        assert result['tangency_condition'] < 1e-6

    def test_price_increase_reduces_demand(self):
        budget1 = BudgetConstraint(1000, 10, 20)
        budget2 = BudgetConstraint(1000, 15, 20)
        u = CobbDouglasUtility(alpha=0.5)
        c1 = ConsumerChoice(budget1, u)
        c2 = ConsumerChoice(budget2, u)
        assert c2.optimal_x < c1.optimal_x

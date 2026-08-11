"""
可贷资金市场测试: 均衡利率、财政政策与挤出效应
"""

import pytest

from macro import LoanableFundsModel


class TestLoanableFunds:
    def make_model(self, borrowing=0.0):
        return LoanableFundsModel(
            savings_autonomous=800, savings_sensitivity=200,
            investment_autonomous=1200, investment_sensitivity=400,
            government_borrowing=borrowing,
        )

    def test_savings_function(self):
        m = self.make_model()
        assert m.savings(0.05) == pytest.approx(800 + 200 * 0.05)

    def test_investment_function(self):
        m = self.make_model()
        assert m.investment(0.05) == pytest.approx(1200 - 400 * 0.05)

    def test_equilibrium_rate_no_borrowing(self):
        m = self.make_model()
        # r* = (1200 + 0 - 800) / (200 + 400) = 400/600 = 0.6667
        assert m.equilibrium_rate() == pytest.approx(400 / 600)

    def test_equilibrium_savings_equals_investment(self):
        m = self.make_model()
        eq = m.equilibrium()
        assert eq['savings'] == pytest.approx(eq['investment'])

    def test_government_borrowing_raises_rate(self):
        m0 = self.make_model(borrowing=0)
        m1 = self.make_model(borrowing=200)
        assert m1.equilibrium_rate() > m0.equilibrium_rate()

    def test_crowding_out(self):
        m = self.make_model()
        result = m.with_fiscal_policy(additional_borrowing=200)
        assert result['crowding_out'] > 0
        assert result['interest_rate_change'] > 0
        assert result['investment_change'] < 0

    def test_tax_incentive_lowers_rate(self):
        m = self.make_model()
        result = m.with_tax_incentive(savings_increase=200)
        assert result['interest_rate_change'] < 0
        assert result['investment_change'] > 0

    def test_invalid_sensitivity(self):
        with pytest.raises(ValueError):
            LoanableFundsModel(savings_sensitivity=0)

    def test_invalid_borrowing(self):
        with pytest.raises(ValueError):
            LoanableFundsModel(government_borrowing=-5)

    def test_analyze(self):
        result = self.make_model().analyze()
        assert 'equilibrium' in result
        assert 'savings_function' in result
        assert result['equilibrium']['interest_rate'] > 0

    def test_excess_demand_zero_at_equilibrium(self):
        m = self.make_model(borrowing=100)
        rate = m.equilibrium_rate()
        assert m.excess_demand(rate) == pytest.approx(0, abs=1e-6)

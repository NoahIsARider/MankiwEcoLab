"""
IS-LM 模型测试: 均衡、财政政策、货币政策
"""

import pytest

from macro import ISLMModel


class TestISLM:
    def make_model(self):
        return ISLMModel(
            consumption_autonomous=100, marginal_propensity_to_consume=0.8,
            tax_rate=0.25, investment_autonomous=200,
            investment_sensitivity=1000, government_spending=300,
            real_money_supply=500, money_demand_income=0.5,
            money_demand_interest=200,
        )

    def test_is_curve_slope_negative(self):
        m = self.make_model()
        assert m.is_curve(0.10) < m.is_curve(0.05)

    def test_lm_curve_slope_positive(self):
        m = self.make_model()
        assert m.lm_curve(0.10) > m.lm_curve(0.05)

    def test_equilibrium_output_positive(self):
        m = self.make_model()
        eq = m.equilibrium()
        assert eq['output'] > 0
        assert eq['interest_rate'] >= 0

    def test_equilibrium_on_both_curves(self):
        m = self.make_model()
        assert m.verify_on_curves()

    def test_fiscal_policy_increases_output(self):
        m = self.make_model()
        result = m.fiscal_policy(spending_change=50)
        assert result['output_change'] > 0
        assert result['interest_rate_change'] > 0

    def test_fiscal_policy_crowding_out(self):
        # 挤出效应: 财政扩张升利率，部分挤出投资
        m = self.make_model()
        result = m.fiscal_policy(spending_change=50)
        # 乘数效应 (无挤出): ΔY = ΔG / (1-b(1-t)) = 50/0.4 = 125
        # 实际产出增幅应小于完全乘数
        assert result['output_change'] < 50 / 0.4

    def test_monetary_policy_increases_output(self):
        m = self.make_model()
        result = m.monetary_policy(money_supply_change=100)
        assert result['output_change'] > 0
        assert result['interest_rate_change'] < 0

    def test_mpc_affects_multiplier(self):
        low = ISLMModel(marginal_propensity_to_consume=0.5)
        high = ISLMModel(marginal_propensity_to_consume=0.9)
        assert high._multiplier_denominator < low._multiplier_denominator

    def test_invalid_mpc(self):
        with pytest.raises(ValueError):
            ISLMModel(marginal_propensity_to_consume=1.5)

    def test_invalid_tax_rate(self):
        with pytest.raises(ValueError):
            ISLMModel(tax_rate=1.0)

    def test_invalid_money_supply(self):
        with pytest.raises(ValueError):
            ISLMModel(real_money_supply=0)

    def test_analyze(self):
        result = self.make_model().analyze()
        assert 'equilibrium' in result
        assert 'is_curve' in result
        assert 'lm_curve' in result
        assert result['spending_multiplier'] == pytest.approx(2.5)

    def test_contractionary_fiscal_policy(self):
        m = self.make_model()
        result = m.fiscal_policy(spending_change=-50)
        assert result['output_change'] < 0

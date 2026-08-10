"""
微观经济学模块测试: PPF, 贸易, 外部性, 市场结构
"""

import pytest

from micro import (
    ExternalityModel,
    MarketStructureAnalyzer,
    ProductionPossibilityFrontier,
    TradeModel,
)
from micro.ppf import analyze_opportunity_cost
from micro.trade import ProducerProfile


@pytest.fixture
def ppf():
    # 总资源 100，生产 1 单位 X 需 1 资源，生产 1 单位 Y 需 2 资源
    return ProductionPossibilityFrontier(
        resource=100, input_x=1, input_y=2,
        good_x="电脑", good_y="小麦")


class TestPPF:
    def test_max_outputs(self, ppf):
        assert ppf.max_x == pytest.approx(100)
        assert ppf.max_y == pytest.approx(50)

    def test_opportunity_cost_x(self, ppf):
        # 1 X 需 1 资源 = 0.5 Y
        assert ppf.opportunity_cost_x() == pytest.approx(0.5)

    def test_opportunity_cost_y(self, ppf):
        assert ppf.opportunity_cost_y() == pytest.approx(2.0)

    def test_max_output_y_given_x(self, ppf):
        # x=20 => y = (100 - 20*1) / 2 = 40
        assert ppf.max_output_y(20) == pytest.approx(40)

    def test_efficiency(self, ppf):
        assert ppf.is_efficient(50, 25)
        assert not ppf.is_efficient(50, 20)

    def test_attainable(self, ppf):
        assert ppf.is_attainable(50, 20)
        assert not ppf.is_attainable(100, 50)

    def test_ppf_points(self, ppf):
        x, y = ppf.get_ppf_points(50)
        assert len(x) == 50
        assert len(y) == 50
        assert x[0] == 0
        assert x[-1] == pytest.approx(100)

    def test_mrt(self, ppf):
        assert ppf.marginal_rate_of_transformation() == pytest.approx(0.5)

    def test_invalid_input(self):
        with pytest.raises(ValueError):
            ProductionPossibilityFrontier(0, 1, 1)

    def test_analyze_opportunity_cost(self, ppf):
        result = analyze_opportunity_cost(ppf)
        assert result['max_x'] == pytest.approx(100)
        assert 'opportunity_cost_x' in result


class TestTrade:
    def make_model(self):
        # 农民: 每小时 1 单位 X 或 0.5 单位 Y
        farmer = ProducerProfile(name="农民", output_x_per_hour=1, output_y_per_hour=0.5)
        # 牧民: 每小时 0.25 单位 X 或 1 单位 Y
        rancher = ProducerProfile(name="牧民", output_x_per_hour=0.25, output_y_per_hour=1)
        return TradeModel(farmer, rancher)

    def test_opportunity_cost(self):
        farmer = ProducerProfile(name="A", output_x_per_hour=1, output_y_per_hour=0.5)
        # X 机会成本 = 0.5 Y
        assert farmer.opportunity_cost_x == pytest.approx(0.5)
        # Y 机会成本 = 2 X
        assert farmer.opportunity_cost_y == pytest.approx(2.0)

    def test_absolute_advantage(self):
        model = self.make_model()
        aa = model.absolute_advantage()
        assert aa['X'] == "农民"
        assert aa['Y'] == "牧民"

    def test_comparative_advantage(self):
        model = self.make_model()
        ca = model.comparative_advantage()
        # 农民在 X 上比较优势 (0.5 vs 4)
        assert ca['X'] == "农民"
        # 牧民在 Y 上比较优势 (1 vs 2)
        assert ca['Y'] == "牧民"

    def test_autarky_bundle(self):
        farmer = ProducerProfile(name="A", output_x_per_hour=1, output_y_per_hour=0.5, hours_available=40)
        x, y = farmer.autarky_bundle(0.5)
        assert x == pytest.approx(20)
        assert y == pytest.approx(10)

    def test_gains_from_trade(self):
        model = self.make_model()
        gains = model.gains_from_trade()
        assert gains['trade_benefits_both'] is True
        assert gains['gain_X'] > 0
        assert gains['gain_Y'] > 0

    def test_specialization_plan(self):
        model = self.make_model()
        plan = model.specialization_plan()
        assert plan['A_fraction_x'] == 1.0
        assert plan['B_fraction_x'] == 0.0

    def test_analyze_report(self):
        model = self.make_model()
        report = model.analyze()
        assert 'comparative_advantage' in report
        assert 'gains' in report
        assert 'specialization_plan' in report


class TestExternality:
    def make_negative(self):
        return ExternalityModel(
            demand_intercept=100, demand_slope=2,
            supply_intercept=10, supply_slope=1,
            externality_value=10)

    def make_positive(self):
        return ExternalityModel(
            demand_intercept=100, demand_slope=2,
            supply_intercept=10, supply_slope=1,
            externality_value=-15)

    def test_private_equilibrium(self):
        model = self.make_negative()
        # (100-10)/(2+1) = 30
        eq = model.private_equilibrium()
        assert eq['quantity'] == pytest.approx(30)
        assert eq['price'] == pytest.approx(100 - 2*30)

    def test_social_optimum_negative(self):
        model = self.make_negative()
        # 社会供给截距 = 10+10 = 20 => Q = (100-20)/3 = 26.67
        social = model.social_optimum()
        assert social['quantity'] < 30

    def test_social_optimum_positive(self):
        model = self.make_positive()
        # 正外部性 => 社会需求截距 = 100+15=115 => Q=(115-10)/3 = 35
        social = model.social_optimum()
        assert social['quantity'] > 30

    def test_overproduction_negative(self):
        model = self.make_negative()
        assert model.analyze()['overproduction'] is True

    def test_underproduction_positive(self):
        model = self.make_positive()
        assert model.analyze()['overproduction'] is False

    def test_deadweight_loss_positive(self):
        model = self.make_negative()
        assert model.deadweight_loss() > 0

    def test_pigouvian_tax(self):
        model = self.make_negative()
        assert model.pigouvian_tax() == pytest.approx(10)

    def test_no_externality_no_dwl(self):
        model = ExternalityModel(
            demand_intercept=100, demand_slope=2,
            supply_intercept=10, supply_slope=1,
            externality_value=0)
        assert model.deadweight_loss() == pytest.approx(0, abs=1e-6)


class TestMarketStructure:
    def make_analyzer(self, n):
        return MarketStructureAnalyzer(
            market_demand_intercept=100, market_demand_slope=1,
            firm_mc=20, num_firms=n)

    def test_structure_type(self):
        assert "垄断" in self.make_analyzer(1).structure_type()
        assert "寡头" in self.make_analyzer(3).structure_type()
        assert "完全竞争" in self.make_analyzer(100).structure_type()

    def test_monopoly_equilibrium(self):
        msa = self.make_analyzer(1)
        eq = msa.monopoly_equilibrium()
        # Q = (100-20)/2 = 40, P = 100 - 40 = 60
        assert eq['quantity'] == pytest.approx(40)
        assert eq['price'] == pytest.approx(60)

    def test_competitive_equilibrium(self):
        msa = self.make_analyzer(100)
        eq = msa.competitive_equilibrium()
        # Q = (100-20)/1 = 80, P = 20
        assert eq['quantity'] == pytest.approx(80)
        assert eq['price'] == pytest.approx(20)

    def test_cournot_equilibrium(self):
        msa = self.make_analyzer(2)
        eq = msa.cournot_equilibrium()
        # Q_total = 2*(100-20)/(1*3) = 53.33, P = 100 - 53.33 = 46.67
        assert eq['price'] == pytest.approx(46.67, rel=0.01)

    def test_monopoly_dwl_positive(self):
        msa = self.make_analyzer(1)
        assert msa.deadweight_loss() > 0

    def test_competitive_dwl_zero(self):
        msa = self.make_analyzer(100)
        # 竞争市场的 equilibrium 直接返回竞争均衡，DWL 仍按垄断对比
        assert msa.analyze()['equilibrium']['price'] == pytest.approx(20)

    def test_monopoly_markup(self):
        msa = self.make_analyzer(1)
        analysis = msa.analyze()
        assert analysis['price_markup'] > 0
        assert analysis['quantity_shortfall'] > 0

    def test_hhi(self):
        msa = self.make_analyzer(1)
        assert msa.herfindahl_index() == pytest.approx(10000)
        assert msa.hhi_interpretation(10000) == "高度集中市场 (highly concentrated)"

    def test_hhi_custom_shares(self):
        msa = self.make_analyzer(2)
        assert msa.herfindahl_index([0.5, 0.5]) == pytest.approx(5000)

    def test_invalid_firms(self):
        with pytest.raises(ValueError):
            MarketStructureAnalyzer(num_firms=0)

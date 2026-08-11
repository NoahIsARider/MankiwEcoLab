"""
博弈论测试: 纳什均衡、占优策略、混合策略、古诺博弈
"""

import numpy as np
import pytest

from micro import (
    CournotGame,
    NormalFormGame,
    matching_pennies,
    prisoners_dilemma,
)


class TestNormalFormGame:
    def test_payoff_method(self):
        pd = prisoners_dilemma()
        assert pd.payoff(0, 0) == {'A': -1.0, 'B': -1.0}
        assert pd.payoff(1, 1) == {'A': -3.0, 'B': -3.0}

    def test_invalid_matrix(self):
        with pytest.raises(ValueError):
            NormalFormGame(np.zeros((3, 3)), np.zeros((3, 3)))

    def test_dominant_strategies_prisoner(self):
        pd = prisoners_dilemma()
        dom = pd.dominant_strategies()
        assert dom['A'] == 1  # Confess
        assert dom['B'] == 1  # Confess
        assert pd.has_dominant_strategy_equilibrium()

    def test_pure_nash_prisoner(self):
        pd = prisoners_dilemma()
        nash = pd.pure_nash_equilibria()
        assert len(nash) == 1
        assert nash[0]['A'] == 1 and nash[0]['B'] == 1

    def test_pareto_optimal_prisoner(self):
        pd = prisoners_dilemma()
        pareto = pd.pareto_optimal()
        # 合作 (0,0) 是帕累托最优之一
        coop = [p for p in pareto if p['A'] == 0 and p['B'] == 0]
        assert len(coop) == 1

    def test_mixed_equilibrium_matching_pennies(self):
        mp = matching_pennies()
        mixed = mp.mixed_strategy_equilibrium()
        assert mixed['valid']
        assert mixed['p'] == pytest.approx(0.5)
        assert mixed['q'] == pytest.approx(0.5)

    def test_no_pure_nash_matching_pennies(self):
        mp = matching_pennies()
        assert len(mp.pure_nash_equilibria()) == 0

    def test_analyze_structure(self):
        pd = prisoners_dilemma()
        result = pd.analyze()
        assert 'payoff_matrix' in result
        assert 'pure_nash_equilibria' in result
        assert 'mixed_strategy_equilibrium' in result
        assert result['num_nash_equilibria'] == 1

    def test_stag_hunt_coordination(self):
        # 协调博弈: 两个纯策略纳什均衡
        payoff_a = np.array([[3.0, 0.0], [0.0, 2.0]])
        payoff_b = np.array([[3.0, 0.0], [0.0, 2.0]])
        game = NormalFormGame(payoff_a, payoff_b,
                              strategies_a=('Hunt Stag', 'Hunt Hare'),
                              strategies_b=('Hunt Stag', 'Hunt Hare'))
        nash = game.pure_nash_equilibria()
        assert len(nash) == 2


class TestCournotGame:
    def make_game(self, n=2):
        return CournotGame(num_firms=n, demand_intercept=100,
                           demand_slope=1, marginal_cost=20)

    def test_two_firm_nash(self):
        game = self.make_game(2)
        nash = game.nash_equilibrium()
        # q* = (100-20)/(1*3) = 26.67, P = 46.67
        assert nash['per_firm_output'] == pytest.approx(26.67, rel=0.01)
        assert nash['total_output'] == pytest.approx(53.33, rel=0.01)
        assert nash['price'] == pytest.approx(46.67, rel=0.01)

    def test_best_response(self):
        game = self.make_game(2)
        # 对手产量 30 => q = (100-20-30)/2 = 25
        assert game.best_response(30) == pytest.approx(25)

    def test_more_firms_lower_price(self):
        duopoly = self.make_game(2)
        many = self.make_game(5)
        assert many.nash_equilibrium()['price'] < duopoly.nash_equilibrium()['price']

    def test_collusion_higher_price(self):
        game = self.make_game(2)
        collusion = game.collusion_output()
        nash = game.nash_equilibrium()
        assert collusion['price'] > nash['price']
        assert collusion['total_output'] < nash['total_output']
        assert collusion['total_profit'] > nash['total_profit']

    def test_competitive_lowest_price(self):
        game = self.make_game(2)
        comp = game.competitive_output()
        assert comp['price'] == pytest.approx(20)
        assert comp['total_profit'] == pytest.approx(0)

    def test_invalid_firms(self):
        with pytest.raises(ValueError):
            CournotGame(num_firms=0)

    def test_analyze(self):
        result = self.make_game(2).analyze()
        assert 'nash_equilibrium' in result
        assert 'collusion' in result
        assert 'competitive' in result

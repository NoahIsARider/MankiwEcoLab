"""
集成测试: 完整模拟流程与实验运行
"""

import pytest

import experiments
from market import Market
from utils.economics import create_agents
from utils.visualization import EconomicsVisualizer, MacroVisualizer


@pytest.fixture
def consumer_params():
    return {
        'income_mean': 1000, 'income_std': 200, 'income_min': 500,
        'alpha_mean': 100, 'alpha_std': 10, 'beta_mean': 0.5, 'beta_std': 0.05,
    }


@pytest.fixture
def producer_params():
    return {
        'fixed_cost_mean': 300, 'fixed_cost_std': 50, 'mc_a_mean': 10,
        'mc_a_std': 2, 'mc_b_mean': 0.3, 'mc_b_std': 0.05,
        'max_capacity_mean': 100, 'max_capacity_std': 20,
    }


def run_small_market(consumer_params, producer_params, rounds=40):
    consumers, producers = create_agents(
        300, 80, consumer_params, producer_params, 42)
    market = Market(consumers, producers, initial_price=50,
                    price_adjustment_speed=0.1)
    for _ in range(rounds):
        market.run_round()
    return market, consumers, producers


class TestFullSimulation:
    def test_full_market_flow(self, consumer_params, producer_params):
        """完整模拟流程: 创建主体 -> 运行 -> 分析"""
        market, consumers, producers = run_small_market(consumer_params, producer_params)
        assert market.equilibrium_reached or market.current_price > 0
        assert len(market.price_history) > 1
        assert market.quantity_history[-1] > 0

    def test_welfare_analysis_integration(self, consumer_params, producer_params):
        market, consumers, producers = run_small_market(consumer_params, producer_params)
        from utils.economics import analyze_welfare_distribution
        welfare = analyze_welfare_distribution(consumers, producers)
        assert welfare['total_surplus'] > 0
        assert 0 <= welfare['consumer_gini'] <= 1

    def test_market_stats_integration(self, consumer_params, producer_params):
        market, consumers, producers = run_small_market(consumer_params, producer_params)
        stats = market.get_market_stats()
        assert stats['total_surplus'] > 0
        assert stats['equilibrium_quantity'] > 0


class TestVisualization:
    def test_economics_visualizer_report(self, consumer_params, producer_params,
                                         tmp_path):
        """生成全部微观图表"""
        import matplotlib
        matplotlib.use('Agg')
        market, consumers, producers = run_small_market(
            consumer_params, producer_params, rounds=20)

        visualizer = EconomicsVisualizer(output_dir=str(tmp_path),
                                         figure_size=(8, 6), dpi=50)
        visualizer.generate_report(market, consumers, producers)

        expected_files = [
            'supply_demand_curves.png', 'price_convergence.png',
            'surplus_analysis.png', 'transaction_volume.png',
            'agent_distributions.png', 'welfare_analysis.png',
        ]
        for fname in expected_files:
            assert (tmp_path / fname).exists(), f"缺少图表: {fname}"

    def test_macro_visualizer_report(self, tmp_path):
        """生成全部宏观图表"""
        import matplotlib
        matplotlib.use('Agg')
        from macro import ADASModel, MoneyCreationModel, PhillipsCurve, SolowGrowthModel

        solow = SolowGrowthModel(savings_rate=0.2)
        adas = ADASModel()
        phillips = PhillipsCurve()
        money = MoneyCreationModel(reserve_ratio=0.1, initial_deposit=1000)

        visualizer = MacroVisualizer(output_dir=str(tmp_path), dpi=50)
        visualizer.generate_macro_report(solow, adas, phillips, money)

        expected_files = [
            'solow_growth.png', 'ad_as_model.png',
            'phillips_curve.png', 'money_creation.png',
        ]
        for fname in expected_files:
            assert (tmp_path / fname).exists(), f"缺少图表: {fname}"

    def test_macro_report_extended(self, tmp_path):
        """宏观报告应包含可贷资金与 IS-LM 图表"""
        import matplotlib
        matplotlib.use('Agg')
        from macro import (
            ADASModel,
            ISLMModel,
            LoanableFundsModel,
            MoneyCreationModel,
            PhillipsCurve,
            SolowGrowthModel,
        )

        solow = SolowGrowthModel(savings_rate=0.2)
        adas = ADASModel()
        phillips = PhillipsCurve()
        money = MoneyCreationModel(reserve_ratio=0.1, initial_deposit=1000)
        lf = LoanableFundsModel()
        islm = ISLMModel()

        visualizer = MacroVisualizer(output_dir=str(tmp_path), dpi=50)
        visualizer.generate_macro_report(solow, adas, phillips, money,
                                         loanable_funds=lf, islm=islm)

        for fname in ('loanable_funds.png', 'islm_model.png'):
            assert (tmp_path / fname).exists(), f"缺少图表: {fname}"

    def test_consumer_choice_plot(self, tmp_path):
        """消费者选择图应生成"""
        import matplotlib
        matplotlib.use('Agg')
        from micro import BudgetConstraint, CobbDouglasUtility, ConsumerChoice
        from utils.visualization import EconomicsVisualizer

        budget = BudgetConstraint(income=1000, price_x=10, price_y=20)
        choice = ConsumerChoice(budget, CobbDouglasUtility(alpha=0.5))
        visualizer = EconomicsVisualizer(output_dir=str(tmp_path), dpi=50)
        visualizer.plot_consumer_choice(choice, show=False)
        assert (tmp_path / 'consumer_choice.png').exists()

    def test_loanable_funds_plot(self, tmp_path):
        """可贷资金图应生成"""
        import matplotlib
        matplotlib.use('Agg')
        from macro import LoanableFundsModel
        from utils.visualization import MacroVisualizer

        model = LoanableFundsModel()
        visualizer = MacroVisualizer(output_dir=str(tmp_path), dpi=50)
        visualizer.plot_loanable_funds(model, save=True)
        assert (tmp_path / 'loanable_funds.png').exists()

    def test_islm_plot(self, tmp_path):
        """IS-LM 图应生成"""
        import matplotlib
        matplotlib.use('Agg')
        from macro import ISLMModel
        from utils.visualization import MacroVisualizer

        model = ISLMModel()
        visualizer = MacroVisualizer(output_dir=str(tmp_path), dpi=50)
        visualizer.plot_islm(model, save=True)
        assert (tmp_path / 'islm_model.png').exists()


class TestConsoleOutput:
    def test_print_table(self, capsys):
        from utils.output import print_table
        print_table(['商品', '数量', '价格'], [['X', 10, 5.5], ['Y', 20, 7.25]])
        captured = capsys.readouterr()
        assert '商品' in captured.out
        assert '7.25' in captured.out

    def test_print_section(self, capsys):
        from utils.output import print_section
        print_section('均衡分析')
        captured = capsys.readouterr()
        assert '均衡分析' in captured.out

    def test_format_pct(self):
        from utils.output import format_pct
        assert format_pct(15.6) == '15.60%'
        assert format_pct(50, precision=0) == '50%'


class TestExperiments:
    def test_experiment_1(self, capsys):
        experiments.experiment_1_basic_equilibrium()
        captured = capsys.readouterr()
        assert "最终均衡" in captured.out

    def test_experiment_2(self, capsys):
        experiments.experiment_2_demand_shift()
        captured = capsys.readouterr()
        assert "需求增加导致价格和数量同时上升" in captured.out

    def test_experiment_3(self, capsys):
        experiments.experiment_3_supply_shift()
        captured = capsys.readouterr()
        assert "供给增加导致价格下降" in captured.out

    def test_experiment_4(self, capsys):
        experiments.experiment_4_price_elasticity()
        captured = capsys.readouterr()
        assert "必需品对价格变化不敏感" in captured.out

    def test_experiment_5(self, capsys):
        experiments.experiment_5_market_intervention()
        captured = capsys.readouterr()
        assert "价格上限导致" in captured.out

    def test_experiment_6(self, capsys):
        experiments.experiment_6_externality()
        captured = capsys.readouterr()
        assert "外部性导致过度生产" in captured.out

    def test_experiment_7(self, capsys):
        experiments.experiment_7_market_structure()
        captured = capsys.readouterr()
        assert "垄断价格最高" in captured.out

    def test_experiment_8(self, capsys):
        experiments.experiment_8_macro_models()
        captured = capsys.readouterr()
        assert "宏观经济学研究整体经济现象" in captured.out

    def test_experiment_9(self, capsys):
        experiments.experiment_9_consumer_choice()
        captured = capsys.readouterr()
        assert "消费者选择理论" in captured.out

    def test_experiment_10(self, capsys):
        experiments.experiment_10_game_theory()
        captured = capsys.readouterr()
        assert "囚徒困境" in captured.out


class TestMainModule:
    def test_main_macro_demo(self, capsys):
        """主程序的宏观演示应能正常运行"""
        import main
        main.run_macro_demo()
        captured = capsys.readouterr()
        assert "宏观经济学模型演示" in captured.out

    def test_main_ten_principles(self, capsys):
        """十大原理演示应能正常运行"""
        import main
        demos = main.run_ten_principles_demo()
        assert len(demos) >= 10
        captured = capsys.readouterr()
        assert "十大原理演示完成" in captured.out


class TestNotebook:
    def test_notebook_executes(self, tmp_path):
        """交互式 Notebook 应可端到端执行"""
        import os

        pytest.importorskip('nbclient')
        pytest.importorskip('nbformat')

        import nbformat
        from nbclient import NotebookClient

        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        nb_path = os.path.join(repo_root, 'notebooks', 'interactive_lab.ipynb')
        nb = nbformat.read(nb_path, as_version=4)
        client = NotebookClient(nb, timeout=180, kernel_name='python3')
        client.execute()
        assert len(nb.cells) >= 10


class TestDeterminism:
    def test_reproducibility(self, consumer_params, producer_params):
        """相同种子结果可复现"""
        results = []
        for _ in range(3):
            market, _, _ = run_small_market(consumer_params, producer_params, rounds=25)
            results.append(round(market.current_price, 6))
        assert len(set(results)) == 1

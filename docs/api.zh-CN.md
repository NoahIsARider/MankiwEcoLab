# API 参考手册

本文档是经济学原理模拟系统的完整编程接口参考。

---

## 包结构

| 包 | 模块 | 内容 |
|----|------|------|
| `agents` | `consumer.py` | `Consumer` 类 |
| | `producer.py` | `Producer` 类 |
| `market` | `market.py` | `Market` 类 |
| | `equilibrium.py` | 均衡计算函数 |
| `micro` | `ppf.py` | 生产可能性边界 |
| | `trade.py` | 比较优势与贸易 |
| | `externality.py` | 外部性模型 |
| | `market_structure.py` | 市场结构分析 |
| | `consumer_choice.py` | 消费者选择理论 |
| | `game_theory.py` | 博弈论与古诺竞争 |
| `macro` | `gdp.py` | GDP 核算 |
| | `inflation.py` | CPI 与货币数量论 |
| | `unemployment.py` | 劳动力市场 |
| | `solow.py` | 索洛增长模型 |
| | `money.py` | 货币创造 |
| | `ad_as.py` | AD-AS 模型 |
| | `phillips.py` | 菲利普斯曲线 |
| | `loanable_funds.py` | 可贷资金市场 |
| | `islm.py` | IS-LM 模型 |
| `utils` | `economics.py` | 经济学工具函数 |
| | `visualization.py` | 可视化类 |
| | `output.py` | 控制台输出工具 |

---

## agents

### `Consumer(consumer_id, income, alpha, beta)`

参数:
- `consumer_id`: 消费者 ID
- `income`: 收入 (>=0)
- `alpha`: 效用参数 (>=0.1)
- `beta`: 边际效用递减率 (>=0.01)

方法:
- `utility_function(q)`: 总效用 `U(q) = α·ln(q+1) - β·q²`
- `marginal_utility(q)`: 边际效用
- `calculate_demand(price)`: 效用最大化需求量
- `calculate_willingness_to_pay(q)`: 支付意愿
- `consume(q, price)`: 记录消费并计算剩余
- `get_demand_curve_point(price)`: 需求曲线点

属性: `quantity_demanded`, `quantity_consumed`, `utility`, `consumer_surplus`, `expenditure`

### `Producer(producer_id, fixed_cost, mc_a, mc_b, max_capacity)`

参数:
- `producer_id`: 生产者 ID
- `fixed_cost`: 固定成本 (>=0)
- `mc_a`: 边际成本常数项 (>=0)
- `mc_b`: 边际成本斜率 (>=0)
- `max_capacity`: 最大产能 (>=1)

方法:
- `total_cost(q)`: 总成本 `TC = FC + a·q + 0.5·b·q²`
- `marginal_cost(q)`: 边际成本
- `average_cost(q)`: 平均成本
- `calculate_supply(price)`: 利润最大化供给量
- `produce(q, price)`: 记录生产并计算剩余
- `get_supply_curve_point(price)`: 供给曲线点

属性: `quantity_supplied`, `quantity_produced`, `revenue`, `cost`, `profit`, `producer_surplus`

---

## market

### `Market(consumers, producers, initial_price, price_adjustment_speed=0.1)`

方法:
- `calculate_aggregate_demand(price)`: 总需求
- `calculate_aggregate_supply(price)`: 总供给
- `update_price()`: 根据供需缺口调整价格 (tâtonnement)
- `clear_market()`: 市场出清，分配交易量
- `check_equilibrium(threshold=0.01)`: 均衡检验
- `run_round()`: 运行一轮交易
- `get_demand_curve(price_range)`: 需求曲线数组
- `get_supply_curve(price_range)`: 供给曲线数组
- `get_market_stats()`: 市场统计字典

### equilibrium 模块

- `find_equilibrium(demand_func, supply_func, price_range=(0.1, 500))`: 求均衡 (P*, Q*)
- `calculate_consumer_surplus_analytical(...)`: 解析消费者剩余
- `calculate_producer_surplus_analytical(...)`: 解析生产者剩余
- `calculate_deadweight_loss(...)`: 无谓损失
- `calculate_market_efficiency(cs, ps, dwl=0)`: 效率指标
- `calculate_elasticity(func, price, delta=0.01)`: 价格弹性
- `classify_elasticity(e)`: 弹性分类
- `analyze_market_structure(n_consumers, n_producers, hhi=None)`: 市场结构类型
- `calculate_herfindahl_hirschman_index(shares)`: HHI 指数

---

## micro

### `ProductionPossibilityFrontier(resource, input_x, input_y, good_x, good_y)`

方法:
- `max_x` / `max_y`: 最大产量
- `max_output_x(y)` / `max_output_y(x)`: 给定一种产量下另一种的最大产量
- `opportunity_cost_x()` / `opportunity_cost_y()`: 机会成本
- `is_efficient(x, y)` / `is_attainable(x, y)`: 效率/可行性判断
- `get_ppf_points(n)`: 绘图点
- `marginal_rate_of_transformation()`: MRT

### `ProducerProfile(name, output_x_per_hour, output_y_per_hour, hours_available=40)`

> 导入: `from micro.trade import ProducerProfile`

属性: `opportunity_cost_x`, `opportunity_cost_y`
方法: `autarky_bundle(fraction_x)`

### `TradeModel(producer_a, producer_b)`

方法:
- `absolute_advantage()`: 绝对优势
- `comparative_advantage()`: 比较优势
- `specialization_plan()`: 专业化方案
- `total_production(specialization=True)`: 总产量
- `gains_from_trade()`: 贸易收益
- `analyze()`: 完整报告

### `ExternalityModel(demand_intercept, demand_slope, supply_intercept, supply_slope, externality_value)`

方法:
- `private_equilibrium()`: 私人市场均衡
- `social_optimum()`: 社会最优
- `deadweight_loss()`: 无谓损失
- `pigouvian_tax()`: 最优庇古税
- `analyze()`: 完整报告

### `MarketStructureAnalyzer(market_demand_intercept, market_demand_slope, firm_mc, firm_fixed_cost, num_firms)`

方法:
- `structure_type()`: 市场结构类型
- `competitive_equilibrium()`: 完全竞争均衡
- `monopoly_equilibrium()`: 垄断均衡
- `cournot_equilibrium()`: 古诺均衡
- `herfindahl_index(shares=None)`: HHI
- `deadweight_loss()`: 无谓损失
- `analyze()`: 完整报告

### `BudgetConstraint(income, price_x, price_y)`

属性: `max_x`, `max_y`, `slope`
方法:
- `max_y_at(x)`: 给定 x 的最大可负担 y
- `affordable(x, y)`: 组合是否在预算内
- `on_budget_line(x, y)`: 组合是否在预算线上
- `budget_line(n=100)`: 预算线绘图点

### `CobbDouglasUtility(alpha)`

方法:
- `utility(x, y)`: `U = x^α · y^(1-α)`
- `marginal_utility_x(x, y)` / `marginal_utility_y(x, y)`: 边际效用
- `marginal_rate_of_substitution(x, y)`: `MRS = [α/(1-α)]·(y/x)`
- `indifference_curve_y(x, u)`: 无差异曲线

### `ConsumerChoice(budget, utility)`

方法:
- `optimal_bundle()`: 最优组合 `x*=αI/Px, y*=(1-α)I/Py`
- `verify_tangency()`: 相切条件 MRS = Px/Py
- `verify_budget_satisfied()`: 预算约束验证
- `demand_curve(good, price_range)`: 需求曲线
- `engel_curve(good, income_range)`: 恩格尔曲线
- `analyze()`: 完整报告

### `NormalFormGame(payoff_a, payoff_b, strategies_a, strategies_b)`

方法:
- `payoff(i, j)`: 双方收益
- `dominant_strategies()`: 占优策略
- `has_dominant_strategy_equilibrium()`: 占优策略均衡
- `pure_nash_equilibria()`: 纯策略纳什均衡
- `mixed_strategy_equilibrium()`: 混合策略纳什均衡
- `pareto_optimal()`: 帕累托最优组合
- `analyze()`: 完整报告

工厂函数:
- `prisoners_dilemma()`: 囚徒困境
- `matching_pennies()`: 猜硬币博弈 (仅混合均衡)

### `CournotGame(num_firms, demand_intercept, demand_slope, marginal_cost)`

方法:
- `best_response(other_output)`: 最优反应函数
- `nash_equilibrium()`: 纳什均衡 `q* = (a-c)/(b(n+1))`
- `collusion_output()`: 串谋产出
- `competitive_output()`: 完全竞争产出
- `analyze()`: 完整报告

---

## macro

### `GDPAccounts(consumption, investment, government_spending, net_exports=0)`

属性: `gdp`
方法: `components_share()`, `analyze()`

### `GDPDeflator(nominal_gdp, real_gdp)`

方法: `values()`, `inflation_rate()`

### `CPI(base_prices, base_quantities)`

方法: `compute(current_prices)`

### `QuantityTheory(money_supply, velocity, real_output)`

方法: `price_level()`, `inflation_from_money_growth()`, `required_money_supply()`, `analyze()`

### `LaborMarketStats(adult_population, employed, unemployed, not_in_labor_force=0)`

属性: `labor_force`
方法: `unemployment_rate()`, `labor_force_participation_rate()`, `employment_population_ratio()`, `analyze()`

### `SolowGrowthModel(alpha, savings_rate, depreciation_rate, population_growth_rate, capital_per_worker0, productivity)`

方法:
- `output_per_worker(k)`: 人均产出
- `investment_per_worker(k)`: 人均投资
- `breakeven_investment(k)`: 持平投资
- `steady_state_k()`: 稳态人均资本
- `steady_state()`: 稳态变量
- `golden_rule_k()`: 黄金律资本
- `golden_rule_savings_rate()`: 黄金律储蓄率
- `simulate(periods)`: 收敛路径
- `analyze()`: 完整报告

### `MoneyCreationModel(reserve_ratio, initial_deposit, currency_deposit_ratio=0)`

属性: `deposit_multiplier`, `money_multiplier`, `total_money_supply`, `total_loans`
方法: `deposit_creation_rounds()`, `analyze()`

### `ADASModel(potential_output, ad_intercept, ad_slope, sras_intercept, sras_slope)`

方法:
- `short_run_equilibrium()`: 短期均衡
- `long_run_equilibrium()`: 长期均衡
- `output_gap()`: 产出缺口
- `demand_shock(shift)`: 需求冲击
- `supply_shock(shift)`: 供给冲击
- `analyze()`: 完整报告

### `PhillipsCurve(expected_inflation, beta, natural_unemployment_rate)`

方法:
- `inflation_at(u)`: 给定失业率的通胀
- `unemployment_at(pi)`: 给定通胀的失业率
- `tradeoff_ratio()`: 权衡比率
- `sacrifice_ratio()`: 牺牲率
- `curve_points()`: 曲线点
- `analyze()`: 完整报告

### `LoanableFundsModel(savings_autonomous, savings_sensitivity, investment_autonomous, investment_sensitivity, government_borrowing)`

方法:
- `savings(r)`: 储蓄供给 `S = S0 + S1·r`
- `investment(r)`: 投资需求 `I = I0 - I1·r`
- `excess_demand(r)`: 可贷资金超额需求
- `equilibrium_rate()`: 均衡利率
- `equilibrium()`: 均衡状态
- `with_fiscal_policy(additional_borrowing)`: 财政政策与挤出效应
- `with_tax_incentive(savings_increase)`: 税收激励
- `analyze()`: 完整报告

### `ISLMModel(consumption_autonomous, marginal_propensity_to_consume, tax_rate, investment_autonomous, investment_sensitivity, government_spending, real_money_supply, money_demand_income, money_demand_interest)`

方法:
- `is_curve(r)`: IS 曲线上的产出
- `lm_curve(r)`: LM 曲线上的产出
- `equilibrium()`: 联立均衡 (Y*, r*)
- `verify_on_curves()`: 均衡是否同时在两条曲线上
- `fiscal_policy(spending_change)`: 财政政策
- `monetary_policy(money_supply_change)`: 货币政策
- `analyze()`: 完整报告 (含支出乘数)

---

## utils

### economics 模块

- `create_agents(n_consumers, n_producers, consumer_params, producer_params, seed)`: 批量创建主体
- `calculate_gini_coefficient(values)`: 基尼系数
- `calculate_lorenz_curve(values)`: 洛伦兹曲线
- `calculate_theil_index(values)`: 泰尔指数
- `calculate_market_concentration(quantities)`: 市场集中度
- `analyze_welfare_distribution(consumers, producers)`: 福利分布
- `calculate_price_elasticity_of_demand(prices, quantities)`: 需求弹性
- `simulate_policy_intervention(market, type, **kwargs)`: 政策干预
- `calculate_tax_equilibrium(market, tax_rate)`: 税收均衡
- `calculate_subsidy_equilibrium(market, subsidy_rate)`: 补贴均衡

### visualization 模块

- `EconomicsVisualizer(output_dir, figure_size, dpi, style)`: 微观可视化
  - `generate_report(market, consumers, producers)`: 生成全部图表
  - `plot_consumer_choice(choice)`: 消费者选择图
- `MacroVisualizer(output_dir, dpi, style)`: 宏观可视化
  - `generate_macro_report(solow, adas, phillips, money, loanable_funds=None, islm=None)`: 生成宏观图表
  - `plot_loanable_funds(model)`: 可贷资金市场图
  - `plot_islm(model)`: IS-LM 均衡图

### output 模块

- `print_table(columns, rows, title=None, float_precision=2)`: 对齐 ASCII 表格
- `print_section(title, width=70, char='=')`: 分隔标题
- `format_pct(value, precision=2)`: 百分比格式化

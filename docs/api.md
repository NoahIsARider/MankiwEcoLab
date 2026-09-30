# API Reference

This document is the complete programming interface reference for the economic principles simulation system.

---

## Package Structure

| Package | Module | Contents |
|----|------|------|
| `agents` | `consumer.py` | `Consumer` class |
| | `producer.py` | `Producer` class |
| `market` | `market.py` | `Market` class |
| | `equilibrium.py` | Equilibrium computation functions |
| `micro` | `ppf.py` | Production possibility frontier |
| | `trade.py` | Comparative advantage and trade |
| | `externality.py` | Externality model |
| | `market_structure.py` | Market structure analysis |
| | `consumer_choice.py` | Consumer choice theory |
| | `game_theory.py` | Game theory and Cournot competition |
| `macro` | `gdp.py` | GDP accounting |
| | `inflation.py` | CPI and quantity theory of money |
| | `unemployment.py` | Labor market |
| | `solow.py` | Solow growth model |
| | `money.py` | Money creation |
| | `ad_as.py` | AD-AS model |
| | `phillips.py` | Phillips curve |
| | `loanable_funds.py` | Loanable funds market |
| | `islm.py` | IS-LM model |
| `utils` | `economics.py` | Economics utility functions |
| | `visualization.py` | Visualization classes |
| | `output.py` | Console output utilities |

---

## agents

### `Consumer(consumer_id, income, alpha, beta)`

Parameters:
- `consumer_id`: consumer ID
- `income`: income (>=0)
- `alpha`: utility parameter (>=0.1)
- `beta`: rate of diminishing marginal utility (>=0.01)

Methods:
- `utility_function(q)`: total utility `U(q) = α·ln(q+1) - β·q²`
- `marginal_utility(q)`: marginal utility
- `calculate_demand(price)`: utility-maximizing quantity demanded
- `calculate_willingness_to_pay(q)`: willingness to pay
- `consume(q, price)`: record consumption and compute surplus
- `get_demand_curve_point(price)`: demand curve point

Attributes: `quantity_demanded`, `quantity_consumed`, `utility`, `consumer_surplus`, `expenditure`

### `Producer(producer_id, fixed_cost, mc_a, mc_b, max_capacity)`

Parameters:
- `producer_id`: producer ID
- `fixed_cost`: fixed cost (>=0)
- `mc_a`: constant term of marginal cost (>=0)
- `mc_b`: slope of marginal cost (>=0)
- `max_capacity`: maximum capacity (>=1)

Methods:
- `total_cost(q)`: total cost `TC = FC + a·q + 0.5·b·q²`
- `marginal_cost(q)`: marginal cost
- `average_cost(q)`: average cost
- `calculate_supply(price)`: profit-maximizing quantity supplied
- `produce(q, price)`: record production and compute surplus
- `get_supply_curve_point(price)`: supply curve point

Attributes: `quantity_supplied`, `quantity_produced`, `revenue`, `cost`, `profit`, `producer_surplus`

---

## market

### `Market(consumers, producers, initial_price, price_adjustment_speed=0.1)`

Methods:
- `calculate_aggregate_demand(price)`: aggregate demand
- `calculate_aggregate_supply(price)`: aggregate supply
- `update_price()`: adjust price based on the supply-demand gap (tâtonnement)
- `clear_market()`: clear the market, allocating transaction volume
- `check_equilibrium(threshold=0.01)`: equilibrium check
- `run_round()`: run one round of trading
- `get_demand_curve(price_range)`: demand curve array
- `get_supply_curve(price_range)`: supply curve array
- `get_market_stats()`: market statistics dictionary

### equilibrium module

- `find_equilibrium(demand_func, supply_func, price_range=(0.1, 500))`: find equilibrium (P*, Q*)
- `calculate_consumer_surplus_analytical(...)`: analytical consumer surplus
- `calculate_producer_surplus_analytical(...)`: analytical producer surplus
- `calculate_deadweight_loss(...)`: deadweight loss
- `calculate_market_efficiency(cs, ps, dwl=0)`: efficiency metrics
- `calculate_elasticity(func, price, delta=0.01)`: price elasticity
- `classify_elasticity(e)`: elasticity classification
- `analyze_market_structure(n_consumers, n_producers, hhi=None)`: market structure type
- `calculate_herfindahl_hirschman_index(shares)`: HHI index

---

## micro

### `ProductionPossibilityFrontier(resource, input_x, input_y, good_x, good_y)`

Methods:
- `max_x` / `max_y`: maximum output
- `max_output_x(y)` / `max_output_y(x)`: maximum output of one good given the other
- `opportunity_cost_x()` / `opportunity_cost_y()`: opportunity cost
- `is_efficient(x, y)` / `is_attainable(x, y)`: efficiency/feasibility check
- `get_ppf_points(n)`: plotting points
- `marginal_rate_of_transformation()`: MRT

### `ProducerProfile(name, output_x_per_hour, output_y_per_hour, hours_available=40)`

> Import: `from micro.trade import ProducerProfile`

Attributes: `opportunity_cost_x`, `opportunity_cost_y`
Methods: `autarky_bundle(fraction_x)`

### `TradeModel(producer_a, producer_b)`

Methods:
- `absolute_advantage()`: absolute advantage
- `comparative_advantage()`: comparative advantage
- `specialization_plan()`: specialization plan
- `total_production(specialization=True)`: total output
- `gains_from_trade()`: gains from trade
- `analyze()`: full report

### `ExternalityModel(demand_intercept, demand_slope, supply_intercept, supply_slope, externality_value)`

Methods:
- `private_equilibrium()`: private market equilibrium
- `social_optimum()`: social optimum
- `deadweight_loss()`: deadweight loss
- `pigouvian_tax()`: optimal Pigouvian tax
- `analyze()`: full report

### `MarketStructureAnalyzer(market_demand_intercept, market_demand_slope, firm_mc, firm_fixed_cost, num_firms)`

Methods:
- `structure_type()`: market structure type
- `competitive_equilibrium()`: perfectly competitive equilibrium
- `monopoly_equilibrium()`: monopoly equilibrium
- `cournot_equilibrium()`: Cournot equilibrium
- `herfindahl_index(shares=None)`: HHI
- `deadweight_loss()`: deadweight loss
- `analyze()`: full report

### `BudgetConstraint(income, price_x, price_y)`

Attributes: `max_x`, `max_y`, `slope`
Methods:
- `max_y_at(x)`: maximum affordable y given x
- `affordable(x, y)`: whether the bundle is within budget
- `on_budget_line(x, y)`: whether the bundle lies on the budget line
- `budget_line(n=100)`: budget line plotting points

### `CobbDouglasUtility(alpha)`

Methods:
- `utility(x, y)`: `U = x^α · y^(1-α)`
- `marginal_utility_x(x, y)` / `marginal_utility_y(x, y)`: marginal utility
- `marginal_rate_of_substitution(x, y)`: `MRS = [α/(1-α)]·(y/x)`
- `indifference_curve_y(x, u)`: indifference curve

### `ConsumerChoice(budget, utility)`

Methods:
- `optimal_bundle()`: optimal bundle `x*=αI/Px, y*=(1-α)I/Py`
- `verify_tangency()`: tangency condition MRS = Px/Py
- `verify_budget_satisfied()`: budget constraint verification
- `demand_curve(good, price_range)`: demand curve
- `engel_curve(good, income_range)`: Engel curve
- `analyze()`: full report

### `NormalFormGame(payoff_a, payoff_b, strategies_a, strategies_b)`

Methods:
- `payoff(i, j)`: payoffs to both players
- `dominant_strategies()`: dominant strategies
- `has_dominant_strategy_equilibrium()`: dominant-strategy equilibrium
- `pure_nash_equilibria()`: pure-strategy Nash equilibria
- `mixed_strategy_equilibrium()`: mixed-strategy Nash equilibrium
- `pareto_optimal()`: Pareto-optimal combinations
- `analyze()`: full report

Factory functions:
- `prisoners_dilemma()`: prisoner's dilemma
- `matching_pennies()`: matching pennies (mixed equilibrium only)

### `CournotGame(num_firms, demand_intercept, demand_slope, marginal_cost)`

Methods:
- `best_response(other_output)`: best response function
- `nash_equilibrium()`: Nash equilibrium `q* = (a-c)/(b(n+1))`
- `collusion_output()`: collusive output
- `competitive_output()`: perfectly competitive output
- `analyze()`: full report

---

## macro

### `GDPAccounts(consumption, investment, government_spending, net_exports=0)`

Attributes: `gdp`
Methods: `components_share()`, `analyze()`

### `GDPDeflator(nominal_gdp, real_gdp)`

Methods: `values()`, `inflation_rate()`

### `CPI(base_prices, base_quantities)`

Methods: `compute(current_prices)`

### `QuantityTheory(money_supply, velocity, real_output)`

Methods: `price_level()`, `inflation_from_money_growth()`, `required_money_supply()`, `analyze()`

### `LaborMarketStats(adult_population, employed, unemployed, not_in_labor_force=0)`

Attributes: `labor_force`
Methods: `unemployment_rate()`, `labor_force_participation_rate()`, `employment_population_ratio()`, `analyze()`

### `SolowGrowthModel(alpha, savings_rate, depreciation_rate, population_growth_rate, capital_per_worker0, productivity)`

Methods:
- `output_per_worker(k)`: output per worker
- `investment_per_worker(k)`: investment per worker
- `breakeven_investment(k)`: breakeven investment
- `steady_state_k()`: steady-state capital per worker
- `steady_state()`: steady-state variables
- `golden_rule_k()`: golden-rule capital
- `golden_rule_savings_rate()`: golden-rule savings rate
- `simulate(periods)`: convergence path
- `analyze()`: full report

### `MoneyCreationModel(reserve_ratio, initial_deposit, currency_deposit_ratio=0)`

Attributes: `deposit_multiplier`, `money_multiplier`, `total_money_supply`, `total_loans`
Methods: `deposit_creation_rounds()`, `analyze()`

### `ADASModel(potential_output, ad_intercept, ad_slope, sras_intercept, sras_slope)`

Methods:
- `short_run_equilibrium()`: short-run equilibrium
- `long_run_equilibrium()`: long-run equilibrium
- `output_gap()`: output gap
- `demand_shock(shift)`: demand shock
- `supply_shock(shift)`: supply shock
- `analyze()`: full report

### `PhillipsCurve(expected_inflation, beta, natural_unemployment_rate)`

Methods:
- `inflation_at(u)`: inflation given the unemployment rate
- `unemployment_at(pi)`: unemployment rate given inflation
- `tradeoff_ratio()`: tradeoff ratio
- `sacrifice_ratio()`: sacrifice ratio
- `curve_points()`: curve points
- `analyze()`: full report

### `LoanableFundsModel(savings_autonomous, savings_sensitivity, investment_autonomous, investment_sensitivity, government_borrowing)`

Methods:
- `savings(r)`: savings supply `S = S0 + S1·r`
- `investment(r)`: investment demand `I = I0 - I1·r`
- `excess_demand(r)`: excess demand for loanable funds
- `equilibrium_rate()`: equilibrium interest rate
- `equilibrium()`: equilibrium state
- `with_fiscal_policy(additional_borrowing)`: fiscal policy and the crowding-out effect
- `with_tax_incentive(savings_increase)`: tax incentive
- `analyze()`: full report

### `ISLMModel(consumption_autonomous, marginal_propensity_to_consume, tax_rate, investment_autonomous, investment_sensitivity, government_spending, real_money_supply, money_demand_income, money_demand_interest)`

Methods:
- `is_curve(r)`: output on the IS curve
- `lm_curve(r)`: output on the LM curve
- `equilibrium()`: simultaneous equilibrium (Y*, r*)
- `verify_on_curves()`: whether the equilibrium lies on both curves
- `fiscal_policy(spending_change)`: fiscal policy
- `monetary_policy(money_supply_change)`: monetary policy
- `analyze()`: full report (including the expenditure multiplier)

---

## utils

### economics module

- `create_agents(n_consumers, n_producers, consumer_params, producer_params, seed)`: batch-create agents
- `calculate_gini_coefficient(values)`: Gini coefficient
- `calculate_lorenz_curve(values)`: Lorenz curve
- `calculate_theil_index(values)`: Theil index
- `calculate_market_concentration(quantities)`: market concentration
- `analyze_welfare_distribution(consumers, producers)`: welfare distribution
- `calculate_price_elasticity_of_demand(prices, quantities)`: demand elasticity
- `simulate_policy_intervention(market, type, **kwargs)`: policy intervention
- `calculate_tax_equilibrium(market, tax_rate)`: tax equilibrium
- `calculate_subsidy_equilibrium(market, subsidy_rate)`: subsidy equilibrium

### visualization module

- `EconomicsVisualizer(output_dir, figure_size, dpi, style)`: microeconomic visualization
  - `generate_report(market, consumers, producers)`: generate all charts
  - `plot_consumer_choice(choice)`: consumer choice chart
- `MacroVisualizer(output_dir, dpi, style)`: macroeconomic visualization
  - `generate_macro_report(solow, adas, phillips, money, loanable_funds=None, islm=None)`: generate macroeconomic charts
  - `plot_loanable_funds(model)`: loanable funds market chart
  - `plot_islm(model)`: IS-LM equilibrium chart

### output module

- `print_table(columns, rows, title=None, float_precision=2)`: aligned ASCII table
- `print_section(title, width=70, char='=')`: section separator
- `format_pct(value, precision=2)`: percentage formatting

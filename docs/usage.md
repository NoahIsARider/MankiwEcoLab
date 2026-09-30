# Usage Guide

> This document covers: CLI commands, configuration parameters, custom experiments, macro and micro model invocation, output files, and FAQ.

## Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Python 3.9+ is recommended. The development and test environment uses Python 3.11.

### 2. Run the Full Microeconomic Market Simulation

```bash
python main.py
```

Creates 1000 consumers and 200 producers; the simulated market converges to equilibrium through 35 rounds of trading, writing data and charts to `output/`.

### 3. Run the Macro Demo

```bash
python main.py --macro
```

Demonstrates four major macro models: Solow growth, AD-AS, the Phillips curve, and money creation.

### 4. Run the Ten Principles Demo

```bash
python main.py --demo
```

Reviews the ten principles from Mankiw's *Principles of Economics* as ten standalone items.

### 5. Run All Experiments

```bash
python experiments.py
```

Runs 10 economics experiments (supply-demand equilibrium, demand/supply shifts, elasticity, price controls, externalities, market structure, macro models, consumer choice, game theory, and oligopoly).

### 6. Interactive Notebook

```bash
jupyter notebook notebooks/interactive_lab.ipynb
```

Interactive demos of consumer choice, game theory, the loanable funds market, and the IS-LM model.

### 7. Run the Tests

```bash
python -m pytest tests/ -q
```

280 unit and integration tests covering all models.

## Command-Line Interface

```
usage: main.py [-h] [--rounds ROUNDS] [--consumers CONSUMERS]
               [--producers PRODUCERS] [--seed SEED] [--macro]
               [--demo] [--experiments] [--version]

optional arguments:
  --rounds N        market trading rounds (default 100)
  --consumers N     number of consumers (default 1000)
  --producers N     number of producers (default 1000)
  --seed S          random seed (default 42)
  --macro           run the macroeconomics demo
  --demo            run the ten principles demo
  --experiments     run all economics experiments
  --version         show version number
```

## Configuration Parameters

All parameters live in `config.py`, grouped by module:

### Number of Economic Agents
```python
NUM_CONSUMERS = 1000
NUM_PRODUCERS = 1000
```

### Simulation Parameters
```python
NUM_ROUNDS = 100                 # market trading rounds
CONVERGENCE_THRESHOLD = 0.01     # price convergence threshold
PRICE_ADJUSTMENT_SPEED = 0.1     # price adjustment speed
```

### Consumer Parameters
```python
CONSUMER_INCOME_MEAN = 1000.0    # mean income
CONSUMER_ALPHA_MEAN = 100.0      # utility function α (base utility)
CONSUMER_BETA_MEAN = 0.5         # utility function β (decay speed)
```

### Producer Parameters
```python
PRODUCER_FIXED_COST_MEAN = 500.0 # average fixed cost
PRODUCER_MC_A_MEAN = 10.0        # marginal cost constant term
PRODUCER_MC_B_MEAN = 0.5         # marginal cost slope
```

### Macro Model Parameters
```python
SOLOW_ALPHA = 0.3                # capital output elasticity
SOLOW_SAVINGS_RATE = 0.2         # savings rate
SOLOW_DEPRECIATION = 0.05        # depreciation rate
RESERVE_RATIO = 0.10             # reserve ratio
PHILLIPS_BETA = 0.5              # inflation-unemployment trade-off coefficient
```

## Custom Experiments

### Example 1: Simulating an Economic Shock

```python
from utils.economics import create_agents
from market import Market

consumer_params = {'income_mean': 1000, 'income_std': 200, 'income_min': 500,
                   'alpha_mean': 100, 'alpha_std': 10, 'beta_mean': 0.5, 'beta_std': 0.05}
producer_params = {'fixed_cost_mean': 300, 'fixed_cost_std': 50, 'mc_a_mean': 10,
                   'mc_a_std': 2, 'mc_b_mean': 0.3, 'mc_b_std': 0.05,
                   'max_capacity_mean': 100, 'max_capacity_std': 20}

consumers, producers = create_agents(1000, 200, consumer_params, producer_params, random_seed=42)
market = Market(consumers, producers, initial_price=50)

for _ in range(50):
    market.run_round()
print(f"Initial price: {market.current_price:.2f}")

for producer in producers:           # cost increase shock
    producer.mc_a *= 1.3

for _ in range(50):
    market.run_round()
print(f"Post-shock price: {market.current_price:.2f}")
```

### Example 2: Externality Analysis

```python
from micro import ExternalityModel

model = ExternalityModel(demand_intercept=100, demand_slope=2,
                         supply_intercept=10, supply_slope=1, externality_value=10)
result = model.analyze()
print(f"Private quantity {result['private_quantity']:.2f}, "
      f"social optimum {result['social_quantity']:.2f}, "
      f"deadweight loss {result['deadweight_loss']:.2f}")
```

### Example 3: Solow Growth Model

```python
from macro import SolowGrowthModel

solow = SolowGrowthModel(alpha=0.3, savings_rate=0.2,
                         depreciation_rate=0.05, population_growth_rate=0.01)
analysis = solow.analyze()
print(f"Steady-state capital per capita: {analysis['steady_state']['k']:.2f}")
print(f"Golden-rule capital: {analysis['golden_rule']['k_gold']:.2f}")
```

### Example 4: Income Inequality Analysis

```python
from utils.economics import calculate_gini_coefficient, calculate_lorenz_curve

surpluses = [c.consumer_surplus for c in consumers]
print(f"Gini coefficient of consumer surplus: {calculate_gini_coefficient(surpluses):.4f}")
population, cumulative = calculate_lorenz_curve(surpluses)  # Lorenz curve
```

### Example 5: Consumer Choice Theory

```python
from micro import BudgetConstraint, CobbDouglasUtility, ConsumerChoice

budget = BudgetConstraint(income=1000, price_x=10, price_y=20)
utility = CobbDouglasUtility(alpha=0.5)
choice = ConsumerChoice(budget, utility)

bundle = choice.optimal_bundle()
print(f"Optimal bundle: x*={bundle['x']:.2f}, y*={bundle['y']:.2f}")
print(f"Tangency condition satisfied: {choice.verify_tangency()}")

# Demand curve and Engel curve
prices, quantities = choice.demand_curve('x', price_range=(5, 20))
incomes, engel_q = choice.engel_curve('x', income_range=(500, 2000))
```

### Example 6: Game Theory and Cournot Competition

```python
from micro import prisoners_dilemma, CournotGame

pd = prisoners_dilemma()
nash = pd.pure_nash_equilibria()
print(f"Prisoner's dilemma Nash equilibrium: {nash[0]['A_strategy']}/{nash[0]['B_strategy']}")

cg = CournotGame(num_firms=2, demand_intercept=100, demand_slope=1, marginal_cost=20)
eq = cg.nash_equilibrium()
print(f"Cournot equilibrium: per-firm output {eq['per_firm_output']:.2f}, price {eq['price']:.2f}")

# Mixed-strategy equilibrium
from micro import matching_pennies
mp = matching_pennies()
print(f"Matching pennies mixed equilibrium: p={mp.mixed_strategy_equilibrium()['p']:.2f}")
```

### Example 7: Loanable Funds Market

```python
from macro import LoanableFundsModel

lf = LoanableFundsModel(
    savings_autonomous=800, savings_sensitivity=200,
    investment_autonomous=1200, investment_sensitivity=400,
    government_borrowing=0,
)
print(f"Equilibrium interest rate: {lf.equilibrium_rate():.2%}")

fiscal = lf.with_fiscal_policy(additional_borrowing=200)
print(f"Crowding-out effect after fiscal expansion: {fiscal['crowding_out']:.2f}")
```

### Example 8: IS-LM Model

```python
from macro import ISLMModel

islm = ISLMModel()
eq = islm.equilibrium()
print(f"IS-LM equilibrium: Y={eq['output']:.2f}, r={eq['interest_rate']:.2%}")

fp = islm.fiscal_policy(spending_change=50)
mp = islm.monetary_policy(money_supply_change=100)
print(f"Fiscal expansion ΔY={fp['output_change']:.2f}, monetary expansion ΔY={mp['output_change']:.2f}")
```

## Core Concepts

### 1. Utility Function
```
U(q) = α·ln(q+1) - β·q²
MU(q) = α/(q+1) - 2β·q
```
The consumer maximizes utility subject to the budget constraint; the optimality condition is `MU(q) = p`, and the quantity demanded is found analytically by solving a quadratic equation.

### 2. Production Cost
```
TC(q) = FC + a·q + 0.5·b·q²
MC(q) = a + b·q
```
Under perfect competition the supply condition is `P = MC`, subject to capacity and shutdown conditions.

### 3. Market Equilibrium and Adjustment
```
Excess demand ED = D(p) - S(p)
Δp = α·[ED/(D+S)]·p
```
Demand > supply → price rises; supply > demand → price falls, until convergence.

### 4. Surplus and Efficiency
- Consumer surplus CS = area below the WTP curve - expenditure
- Producer surplus PS = revenue - area below the MC curve
- Total surplus = CS + PS, maximized at the perfectly competitive equilibrium (Pareto optimal)

### 5. Core Macroeconomic Models
- Quantity theory of money: `M·V = P·Y`
- Solow steady state: `k* = [s·A/(δ+n)]^(1/(1-α))`
- Money multiplier: `m = 1/(r+c)`
- Phillips curve: `π = πᵉ - β·(u-u_n)`
- Loanable funds equilibrium: `S0 + S1·r = I0 - I1·r + G`
- IS-LM equilibrium: the goods market `Y = C+I+G` combined with the money market `M/P = L(Y,r)`

Detailed derivations are in `docs/models.md`.

## Output Files

The `output/` directory (microeconomic simulation):

### Data Files
- `market_data.csv`: price, supply and demand, transaction volume, and surplus for each round
- `consumer_data.csv`: income, utility, quantity demanded, and surplus of each consumer
- `producer_data.csv`: cost, output, profit, and surplus of each producer
- `summary.csv`: statistical summary (elasticity, Gini coefficient, efficiency metrics)

### Chart Files
- `supply_demand_curves.png`: supply and demand curves and the equilibrium point
- `price_convergence.png`: price convergence process
- `surplus_analysis.png`: consumer/producer surplus
- `transaction_volume.png`: changes in transaction volume
- `agent_distributions.png`: parameter distributions of economic agents
- `welfare_analysis.png`: welfare analysis

The macro demo (`--macro`) additionally generates:
- `solow_growth.png`: Solow convergence path and golden rule
- `ad_as_model.png`: AD-AS model
- `phillips_curve.png`: Phillips curve
- `money_creation.png`: money creation process
- `loanable_funds.png`: loanable funds market and crowding-out effect
- `islm_model.png`: IS-LM equilibrium

Micro models can also be generated separately:
- `consumer_choice.png`: consumer choice and optimal bundle

## FAQ

### Q1: Why doesn't the market converge to equilibrium?

1. `PRICE_ADJUSTMENT_SPEED` is too large and causes oscillation → lower it
2. Unreasonable parameters → check the consumer/producer parameters
3. Insufficient rounds → increase `--rounds`

### Q2: How do I simulate different types of goods?

| Type | α | β |
|------|-----|-----|
| Necessity | 100-200 | 0.1-0.3 |
| Normal good | 80-120 | 0.4-0.6 |
| Luxury good | 40-80 | 0.8-1.5 |

### Q3: How can I make it run faster?

- Reduce the number of agents: `--consumers 1000 --producers 200`
- Disable visualization/saving: see `SAVE_PLOTS` and `SAVE_RESULTS` in `config.py`

### Q4: How do I analyze the output data?

```python
import pandas as pd
market_data = pd.read_csv('output/market_data.csv')
print(market_data['Price'].describe())
market_data.plot(x='Round', y=['Price', 'Volume'])
```

### Q5: Chinese characters render as boxes in charts?

Install a Chinese font: `apt-get install fonts-noto-cjk`, then delete the matplotlib cache with
`rm -rf ~/.cache/matplotlib` and rerun.

## References

- Mankiw, *Principles of Economics*, microeconomics volume / macroeconomics volume
- Varian, *Microeconomics: A Modern Approach*
- Blanchard, *Macroeconomics*

## Documentation Map

- [index.md](index.md) - Documentation
- [models.md](models.md) - Mathematical models and derivations
- [api.md](api.md) - API reference
- [structure.md](structure.md) - Project structure and data flow
- [verification.md](verification.md) - System acceptance report
- [tutorials/01-supply-demand.md](tutorials/01-supply-demand.md) - Topic-based tutorials (5 in total)

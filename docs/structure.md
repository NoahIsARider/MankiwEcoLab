# Project Structure

```
MankiwEcoLab/
│
├── README.md                    # Project overview and badges
├── CONTRIBUTING.md              # Contribution guidelines
├── requirements.txt             # Python dependency list
├── pyproject.toml               # Package configuration (ruff, pytest, setuptools)
├── mkdocs.yml                   # Docs site config (Read the Docs)
├── LICENSE                      # MIT License
├── .gitignore                   # Git ignore rules
├── config.py                    # All configurable parameters
├── main.py                      # CLI entry point (micro/macro/ten principles)
├── experiments.py               # 10 economics experiments
│
├── agents/                      # Microeconomic agents
│   ├── __init__.py
│   ├── consumer.py              # Consumer class (utility/demand)
│   └── producer.py              # Producer class (cost/supply)
│
├── market/                      # Market mechanism
│   ├── __init__.py
│   ├── market.py                # Market class (price discovery/clearing)
│   └── equilibrium.py           # Equilibrium/surplus/elasticity/DWL
│
├── micro/                       # Microeconomic extension models
│   ├── __init__.py
│   ├── ppf.py                   # Production possibilities frontier
│   ├── trade.py                 # Comparative advantage and trade
│   ├── externality.py           # Externalities and Pigouvian tax
│   ├── market_structure.py      # Perfect competition/monopoly/oligopoly
│   ├── consumer_choice.py       # Budget constraint/Cobb-Douglas/optimal choice
│   └── game_theory.py           # Nash/dominant/mixed strategy/Cournot
│
├── macro/                       # Macroeconomic models
│   ├── __init__.py
│   ├── gdp.py                   # GDP accounting and deflator
│   ├── inflation.py             # CPI, inflation rate, quantity theory of money
│   ├── unemployment.py          # Unemployment rate/labor force participation rate
│   ├── solow.py                 # Solow growth model
│   ├── money.py                 # Money creation and multiplier
│   ├── ad_as.py                 # AD-AS model
│   ├── phillips.py              # Phillips curve
│   ├── loanable_funds.py        # Loanable funds market and crowding out
│   └── islm.py                  # IS-LM model
│
├── utils/                       # Utility modules
│   ├── __init__.py
│   ├── economics.py             # Gini coefficient/tax equilibrium/policy
│   ├── visualization.py         # EconomicsVisualizer + MacroVisualizer
│   └── output.py                # Console tables/dividers/formatting
│
├── notebooks/                   # Interactive Notebooks
│   └── interactive_lab.ipynb    # Interactive demonstration of the model toolbox
│
├── tests/                       # Test suite (280 tests)
│   ├── test_consumer.py
│   ├── test_producer.py
│   ├── test_market.py
│   ├── test_equilibrium.py
│   ├── test_micro.py
│   ├── test_macro.py
│   ├── test_integration.py
│   ├── test_consumer_choice.py
│   ├── test_game_theory.py
│   ├── test_loanable_funds.py
│   └── test_islm.py
│
├── docs/                        # Documentation (Read the Docs / MkDocs)
│   ├── index.md                 # Documentation index
│   ├── usage.md                 # Usage guide
│   ├── structure.md             # Project structure (this document)
│   ├── verification.md          # System verification report
│   ├── models.md                # Mathematical models and derivations
│   ├── api.md                   # API reference
│   └── tutorials/               # Topic-specific tutorials (5 articles)
│
└── output/                      # Auto-generated after running
    ├── market_data.csv
    ├── consumer_data.csv
    ├── producer_data.csv
    ├── summary.csv
    └── *.png                    # Micro and macro charts
```

## Module Description

### agents/ - Economic Agents
- **consumer.py**: Utility function `U=α·ln(q+1)-β·q²`, analytic demand solution, willingness to pay and surplus
- **producer.py**: Cost function `TC=FC+a·q+0.5·b·q²`, `MC=p` supply, shutdown condition

### market/ - Market Mechanism
- **market.py**: tâtonnement price adjustment, market clearing, equilibrium check
- **equilibrium.py**: `find_equilibrium`, analytic surplus, elasticity classification, deadweight loss, HHI, market structure determination

### micro/ - Microeconomic Extensions
- **ppf.py**: Production frontier under resource constraints, opportunity cost, MRT
- **trade.py**: Absolute/comparative advantage, specialization plan, gains from trade
- **externality.py**: Private equilibrium vs. social optimum, Pigouvian tax, DWL
- **market_structure.py**: Equilibrium comparison across three market structures
- **consumer_choice.py**: Budget constraint, Cobb-Douglas utility, optimal bundle `x*=αI/Px`, demand/Engel curves
- **game_theory.py**: Pure/mixed-strategy Nash equilibrium, dominant strategy, Pareto optimality, Cournot competition

### macro/ - Macroeconomics
- **gdp.py**: Expenditure-method GDP, deflator, inflation rate
- **inflation.py**: CPI, quantity theory of money (MV=PY)
- **unemployment.py**: Unemployment rate, participation rate, unemployment decomposition
- **solow.py**: Steady state, golden rule, convergence path
- **money.py**: Deposit/money multiplier, derived deposits
- **ad_as.py**: Short/long-run equilibrium, demand and supply shocks
- **phillips.py**: Inflation-unemployment tradeoff, sacrifice ratio
- **loanable_funds.py**: Loanable funds market equilibrium, fiscal policy, crowding out
- **islm.py**: IS/LM curves, equilibrium, fiscal and monetary policy, spending multiplier

### utils/ - Utilities
- **economics.py**: Gini coefficient, Lorenz curve, Theil index, tax/subsidy equilibrium, policy intervention
- **visualization.py**: 6 micro charts + 6 macro charts + consumer choice chart (English labels)
- **output.py**: Aligned tables, section dividers, percentage formatting

## Data Flow

```
config.py → main.py / experiments.py
                ↓
      create_agents (utils/economics.py)
                ↓
        Market (market/market.py)
                ├─ Compute supply and demand (agents/)
                ├─ Update prices (tâtonnement)
                ├─ Market clearing
                └─ Equilibrium check (market/equilibrium.py)
                ↓
     Analysis (utils/economics.py, micro/, macro/)
                ↓
     Visualization (utils/visualization.py)
                ↓
     Output (output/)
```

## Key Algorithms

### Analytic Demand Solution (consumer.py)
```
MU(q) = p ⇒ 2βq² + (p+2β)q + (p-α) = 0
```
Root of a quadratic equation, take the smaller value against the budget constraint `income/p`.

### Price Adjustment (market.py)
```
ED = D(p) - S(p)
p_new = p + α·[ED/(D+S)]·p
```

### Equilibrium Check (market.py)
```
std(P_recent)/mean < threshold  and  |D-S|/(D+S) < threshold
```

### Solow Steady State (solow.py)
```
k* = (s·A/(δ+n))^(1/(1-α))
λ = (1-α)(δ+n)   # convergence speed
```

## Extension Points

1. **Add an economic agent**: Add a class in `agents/` implementing the same interface
2. **New market mechanism**: Subclass `Market` and override `update_price()`
3. **Policy simulation**: Add functions in `utils/economics.py`
4. **New macroeconomic model**: Add a module in `macro/`, following the existing docstring and `analyze()` pattern
5. **Interactive interface**: Wrap the `main.py` flow with Streamlit / Dash

## Performance Optimization Suggestions

- Use NumPy-vectorized supply/demand computation for large-scale simulations
- Use `multiprocessing` to parallelize multiple scenarios
- Cache repeated demand/supply curve computations
- Sample a subset of agents when visualizing

## Testing Strategy

- Unit tests: independent methods of each class (tests/test_consumer.py, etc.)
- Integration tests: full simulation flow (tests/test_integration.py)
- Regression tests: fixed random seeds to guarantee reproducibility
- Run: `python -m pytest tests/ -q` (280 tests)

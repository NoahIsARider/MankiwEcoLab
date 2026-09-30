# Tutorial 5: Macroeconomics Overview

> Corresponds to the macro volume of Mankiw's *Principles of Economics*, and to Ten Principles 8, 9, and 10.
> Related code: the entire `macro/` package

## Overview

Macroeconomics studies economy-wide phenomena, including:
- Aggregate output (GDP)
- The price level (CPI, inflation)
- Employment conditions (unemployment rate)
- Economic growth (Solow model)
- Short-run fluctuations (AD-AS, Phillips curve)

## Running the Macro Demo

```bash
python main.py --macro
```

## Model by Model

### 1. GDP Accounting (Principle 8)

```python
from macro import GDPAccounts

gdp = GDPAccounts(consumption=6000, investment=1500,
                  government_spending=2000, net_exports=-500)
print(f"GDP = {gdp.gdp:.2f}")
print(gdp.analyze()['interpretation'])
```

### 2. CPI and Inflation (Principle 9)

```python
from macro import CPI, inflation_rate

cpi = CPI(base_prices=[10, 20, 30], base_quantities=[4, 3, 2])
current_cpi = cpi.compute([12, 22, 31])
print(f"CPI = {current_cpi:.2f}")
print(f"Inflation rate = {inflation_rate(100, current_cpi):.2f}%")
```

### 3. Quantity Theory of Money (Principle 9)

```python
from macro import QuantityTheory

qt1 = QuantityTheory(money_supply=1000, velocity=5, real_output=100)
qt2 = QuantityTheory(money_supply=2000, velocity=5, real_output=100)
print(f"M=1000 => P={qt1.price_level():.2f}")
print(f"M=2000 => P={qt2.price_level():.2f}  (money doubles, prices double)")
```

### 4. Unemployment Analysis

```python
from macro import LaborMarketStats, unemployment_decomposition

labor = LaborMarketStats(adult_population=10000, employed=9000, unemployed=500)
print(f"Unemployment rate: {labor.unemployment_rate():.2f}%")

decomp = unemployment_decomposition(5.5, 2.0, 2.5)
print(decomp['interpretation'])
```

### 5. Solow Growth Model (Principle 8)

```python
from macro import SolowGrowthModel

solow = SolowGrowthModel(alpha=0.3, savings_rate=0.2,
                         depreciation_rate=0.05, population_growth_rate=0.01)
analysis = solow.analyze()
print(f"Steady-state capital per worker: {analysis['steady_state']['k']:.2f}")
print(f"Golden-rule capital: {analysis['golden_rule']['k_gold']:.2f}")
```

### 6. Money Creation

```python
from macro import MoneyCreationModel

money = MoneyCreationModel(reserve_ratio=0.10, initial_deposit=1000)
print(f"Money multiplier: {money.money_multiplier:.2f}")
print(f"Money supply: {money.total_money_supply:.2f}")
```

### 7. AD-AS Model

```python
from macro import ADASModel

adas = ADASModel()
analysis = adas.analyze()
print(f"Short-run equilibrium: Y={analysis['short_run']['output']:.2f}, "
      f"P={analysis['short_run']['price']:.2f}")
print(f"Output gap: {analysis['output_gap']:+.2f}")
```

### 8. Phillips Curve (Principle 10)

```python
from macro import PhillipsCurve

pc = PhillipsCurve(expected_inflation=3.0, beta=0.5, natural_unemployment_rate=5.0)
print(f"Unemployment 4% => inflation {pc.inflation_at(4.0):.2f}%")
print(f"Unemployment 6% => inflation {pc.inflation_at(6.0):.2f}%")
```

## The Four Core Questions of Macroeconomics

1. **Growth**: What determines the long-run standard of living? (Solow model)
2. **Inflation**: Why do prices rise? (quantity theory of money)
3. **Unemployment**: Why are some people unable to find work? (unemployment decomposition)
4. **Fluctuations**: Why does the economy have cycles? (AD-AS, Phillips curve)

## Discussion Questions

- Why can a central bank control long-run inflation simply by controlling the money supply?
- Must lowering inflation in the short run come at the cost of high unemployment? (the role of expectations)

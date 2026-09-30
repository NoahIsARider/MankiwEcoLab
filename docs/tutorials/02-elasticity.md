# Tutorial 2: Price Elasticity

> Corresponds to Chapter 5 of Mankiw's *Principles of Economics*.
> Related code: `market/equilibrium.py`, `utils/economics.py`

## Concept Review

**Price elasticity of demand**: How responsive the quantity demanded is to a change in price.

```
ε = (ΔQ/Q) / (ΔP/P) = (dQ/dP) × (P/Q)
```

| Elasticity value | Type | Meaning |
|--------|------|------|
| \|ε\| > 1 | Elastic demand | Quantity demanded is sensitive to price |
| \|ε\| = 1 | Unit elastic | Total expenditure is unchanged |
| \|ε\| < 1 | Inelastic demand | Quantity demanded is insensitive to price |

**Relationship between income and elasticity**:
- Necessities (e.g., food): inelastic
- Luxuries (e.g., jewelry): elastic

## Running the Experiment

```bash
python experiments.py
```

Experiment 4 compares the difference in demand elasticity between necessities and luxuries.

## Computing with Code

```python
from market.equilibrium import calculate_elasticity, classify_elasticity

# Demand function: q = 100 - 2p
def demand(p):
    return max(0.0, 100 - 2 * p)

# Compute elasticity at different price points
for price in [10, 25, 40]:
    e = calculate_elasticity(demand, price)
    print(f"Price {price}: elasticity = {e:.3f}, type = {classify_elasticity(e)}")
```

## Midpoint Method

For discrete price-quantity data, use the midpoint method:

```python
from utils.economics import calculate_price_elasticity_of_demand

# Price rises from 10 to 12, quantity falls from 100 to 80
e = calculate_price_elasticity_of_demand([10, 12], [100, 80])
print(f"Midpoint-method elasticity: {e:.3f}")
```

## What to Observe

1. Along a linear demand curve, elasticity differs from point to point (elastic in the upper part, inelastic in the lower part)
2. The relationship between elasticity and total expenditure (P×Q)
3. How necessities vs. luxuries respond differently to the same price change

## Discussion Questions

- Why "a good harvest hurts the farmer"? What does this have to do with elasticity?
- How is the tax burden distributed across markets with different elasticities?

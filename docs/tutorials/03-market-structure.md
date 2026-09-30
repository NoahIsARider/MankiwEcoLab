# Tutorial 3: Market Structure

> Corresponds to Chapters 14-17 of Mankiw's *Principles of Economics*.
> Related code: `micro/market_structure.py`, `market/equilibrium.py`

## Concept Review

| Structure | Number of firms | Pricing power | Long-run profit |
|------|---------|--------|---------|
| Perfect competition | Very many | None (price taker) | Zero |
| Monopolistic competition | Many | Limited | Zero (product differentiation) |
| Oligopoly | A few | Yes (strategic interaction) | Positive |
| Monopoly | One | Complete | Positive |

**Market efficiency comparison**: Perfect competition P=MC is the most efficient; monopoly P>MC creates deadweight loss.

## Running the Experiment

```bash
python experiments.py
```

Experiment 7 compares prices and quantities across perfect competition, oligopoly, and monopoly.

## Code Analysis

```python
from micro import MarketStructureAnalyzer

# Three market structures
for num_firms, name in [(100, "Perfect competition"), (3, "Oligopoly"), (1, "Monopoly")]:
    msa = MarketStructureAnalyzer(
        market_demand_intercept=100, market_demand_slope=1,
        firm_mc=20, num_firms=num_firms,
    )
    analysis = msa.analyze()
    eq = analysis['equilibrium']
    print(f"{name} ({num_firms} firms): price = {eq['price']:.2f}, "
          f"quantity = {eq['quantity']:.2f}, deadweight loss = {analysis['deadweight_loss']:.2f}")
```

## HHI Market Concentration

```python
from market.equilibrium import calculate_herfindahl_hirschman_index

# Two firms split the market evenly
hhi = calculate_herfindahl_hirschman_index([0.5, 0.5])
print(f"Duopoly HHI = {hhi}")  # 5000

# Ten firms split the market evenly
hhi2 = calculate_herfindahl_hirschman_index([0.1] * 10)
print(f"Ten-firm HHI = {hhi2}")  # 1000
```

## What to Observe

1. The monopoly price is above marginal cost, and output is below the social optimum
2. Deadweight loss grows as the number of firms decreases
3. The higher the HHI, the more concentrated the market

## Discussion Questions

- Why does antitrust law focus on markets with an HHI above 2500?
- The Cournot oligopoly equilibrium quantity lies between monopoly and competition; why?

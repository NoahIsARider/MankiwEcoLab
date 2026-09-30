# Tutorial 1: Supply and Demand Equilibrium

> Corresponds to Chapters 4 and 5 of Mankiw's *Principles of Economics*, and to Ten Principles 3 and 6.
> Related code: `agents/consumer.py`, `agents/producer.py`, `market/market.py`

## Concept Review

**Law of demand**: Other things equal, when the price rises → the quantity demanded falls.

**Law of supply**: Other things equal, when the price rises → the quantity supplied rises.

**Market equilibrium**: At the equilibrium price P\*, quantity demanded = quantity supplied, and the market clears.

## Running the Experiment

```bash
python experiments.py
```

Experiment 1 shows how the market converges step by step from the initial price to equilibrium.

## Hands-on Experiment

```python
from agents import Consumer, Producer
from market import Market
from utils.economics import create_agents

# Create 1000 consumers and 200 producers
consumer_params = {
    'income_mean': 1000, 'income_std': 200, 'income_min': 500,
    'alpha_mean': 100, 'alpha_std': 10, 'beta_mean': 0.5, 'beta_std': 0.05,
}
producer_params = {
    'fixed_cost_mean': 300, 'fixed_cost_std': 50, 'mc_a_mean': 10,
    'mc_a_std': 2, 'mc_b_mean': 0.3, 'mc_b_std': 0.05,
    'max_capacity_mean': 100, 'max_capacity_std': 20,
}

consumers, producers = create_agents(1000, 200, consumer_params, producer_params, random_seed=42)
market = Market(consumers, producers, initial_price=50, price_adjustment_speed=0.1)

for round_num in range(100):
    if market.run_round():
        print(f"Round {round_num+1} reached equilibrium!")
        break
    if (round_num + 1) % 10 == 0:
        print(f"Round {round_num+1}: price = {market.current_price:.2f}, "
              f"gap = {abs(market.total_demand - market.total_supply):.2f}")

print(f"Final equilibrium price: {market.current_price:.2f}")
print(f"Equilibrium quantity: {market.quantity_history[-1]:.2f}")
```

## What to Observe

1. When the initial price deviates from equilibrium, the market shows a shortage or a surplus
2. How the price adjustment mechanism (tâtonnement) drives the market toward convergence
3. After convergence, total surplus is maximized and the market is efficient

## Discussion Questions

- What happens if you increase `PRICE_ADJUSTMENT_SPEED`? Why might it oscillate?
- If you lower consumers' income, how do the equilibrium price and quantity change?

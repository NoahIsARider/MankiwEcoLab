# Tutorial 4: Externalities and Market Failure

> Corresponds to Chapter 10 of Mankiw's *Principles of Economics*, and to Ten Principles 7.
> Related code: `micro/externality.py`

## Concept Review

**Negative externality** (e.g., pollution): The producer's activity imposes a cost on third parties, but the producer does not bear it.
- Private supply curve < social supply curve
- Market quantity > socially optimal quantity (overproduction)

**Positive externality** (e.g., education): Economic activity yields benefits for third parties.
- Private demand curve < social demand curve
- Market quantity < socially optimal quantity (underproduction)

**Pigouvian tax**: A tax on a negative externality equal to the external cost, which makes private cost = social cost.

## Running the Experiment

```bash
python experiments.py
```

Experiment 6 shows how positive and negative externalities affect the market equilibrium.

## Code Analysis

```python
from micro import ExternalityModel

# Negative externality (pollution): external cost = 10
model = ExternalityModel(
    demand_intercept=100, demand_slope=2,
    supply_intercept=10, supply_slope=1,
    externality_value=10,
)

analysis = model.analyze()
print(f"Private market quantity: {analysis['private_quantity']:.2f}")
print(f"Socially optimal quantity: {analysis['social_quantity']:.2f}")
print(f"Deadweight loss: {analysis['deadweight_loss']:.2f}")
print(f"Optimal Pigouvian tax: {analysis['pigouvian_tax']:.2f}")
```

## Mathematical Derivation

**Negative externality** (external cost `e`):

```
Social supply: P = a_s + b_s·Q + e
Social optimum: a_d - b_d·Q = a_s + b_s·Q + e
Q_social = (a_d - a_s - e) / (b_d + b_s)
```

**Deadweight loss**: the triangle of net social loss between the market quantity and the social optimum.

```
DWL = 0.5 × |Q_private - Q_social| × |e|
```

## What to Observe

1. A negative externality leads to overproduction, and a positive externality leads to underproduction
2. Deadweight loss measures the social cost of market failure
3. A Pigouvian tax brings the private market equilibrium back to the social optimum

## Discussion Questions

- What kind of externality-correcting instrument is a carbon tax? What is its economic logic?
- How does an education subsidy solve the problem of a positive externality?

# Documentation

All documentation for the Mankiw *Principles of Economics* code learning project.

## Quick Navigation

| Document | Description |
|------|------|
| [usage.md](usage.md) | How to run, CLI entry points, and custom experiments |
| [models.md](models.md) | All mathematical models and formula derivations |
| [api.md](api.md) | API reference manual |
| [structure.md](structure.md) | Project structure and module descriptions |
| [verification.md](verification.md) | System acceptance report (full verification) |

## Tutorials

| Tutorial | Topic |
|------|------|
| [tutorials/01-supply-demand.md](tutorials/01-supply-demand.md) | Supply-demand equilibrium |
| [tutorials/02-elasticity.md](tutorials/02-elasticity.md) | Price elasticity |
| [tutorials/03-market-structure.md](tutorials/03-market-structure.md) | Market structure |
| [tutorials/04-externality.md](tutorials/04-externality.md) | Externalities and market failure |
| [tutorials/05-macro-overview.md](tutorials/05-macro-overview.md) | Macroeconomics overview |

## Learning Path

### Microeconomics (Principles 1-7)

1. Read [tutorials/01-supply-demand.md](tutorials/01-supply-demand.md) to understand supply-demand equilibrium
2. Run `python main.py` to observe the market convergence process
3. Read [tutorials/02-elasticity.md](tutorials/02-elasticity.md) to understand the concept of elasticity
4. Read [tutorials/03-market-structure.md](tutorials/03-market-structure.md) to compare different market structures
5. Read [tutorials/04-externality.md](tutorials/04-externality.md) to understand market failure
6. Advanced: consumer choice theory (`micro/consumer_choice.py`) and game theory (`micro/game_theory.py`)

### Macroeconomics (Principles 8-10)

1. Read [tutorials/05-macro-overview.md](tutorials/05-macro-overview.md)
2. Run `python main.py --macro` to observe the macroeconomic model demos (including loanable funds and IS-LM)
3. Run `python main.py --demo` to review all ten principles
4. Interactive experience: `notebooks/interactive_lab.ipynb`

## Reference

- [models.md](models.md) - All mathematical formulas
- [api.md](api.md) - Programming interface reference

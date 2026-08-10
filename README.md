<p align="center">
  <img src="https://img.shields.io/badge/曼昆经济学原理-Code%20Lab-2ea44f?style=for-the-badge&logo=bookstack&logoColor=white" alt="Mankiw Economics Lab"/>
</p>

<p align="center">
  <img src="https://img.shields.io/pypi/v/mankiwecolab?style=flat-square&color=blue" alt="PyPI version"/>
  <img src="https://img.shields.io/pypi/pyversions/mankiwecolab?style=flat-square&color=green" alt="Python Versions"/>
  <img src="https://img.shields.io/github/stars/NoahIsARider/MankiwEcoLab?style=flat-square&color=yellow" alt="GitHub Stars"/>
  <img src="https://img.shields.io/github/license/NoahIsARider/MankiwEcoLab?style=flat-square&color=blue" alt="License"/>
  <img src="https://img.shields.io/github/actions/workflow/status/NoahIsARider/MankiwEcoLab/ci.yml?style=flat-square" alt="CI"/>
  <img src="https://img.shields.io/badge/pytest-204%20passed-brightgreen?style=flat-square" alt="Tests"/>
  <img src="https://img.shields.io/badge/PRs-welcome-orange?style=flat-square" alt="PRs Welcome"/>
</p>

# Mankiw Economics Lab (Principles of Economics Simulation System)

> **An interactive, code-first learning project based on Mankiw's *Principles of Economics*** — implement every core model of microeconomics and macroeconomics by hand in Python.

This project takes the classic models in Mankiw's *Principles of Economics* textbook — from the "production possibilities frontier" to the "Phillips curve" — and **turns each one into runnable, experimentable, testable Python code**. Instead of just reading the graphs and formulas in a textbook, you can run the code, tweak parameters, and watch how markets converge and how the economy fluctuates.

---

## ✨ Highlights

- **Covers Mankiw's ten principles of economics** — every principle has a corresponding runnable experiment
- **Complete micro + macro system** — from supply-demand equilibrium to the Solow growth model, all covered
- **Dual-entry CLI** — `--macro` and `--demo` demo the macro models and the ten principles with one command
- **204 unit and integration tests** — every economic model is mathematically verified for correctness
- **Full visualization** — supply/demand curves, price convergence, Solow convergence paths, AD-AS equilibrium, Phillips curve…
- **Deterministic and reproducible** — fixed random seeds make experimental results exactly reproducible
- **Teaching-friendly** — Chinese comments + line-by-line formula derivations + mathematical verification tests

---

## 📚 Ten Principles × Code Implementations

| Principle | Economic Concept | Code Location |
|------|-----------|---------|
| 1. People face trade-offs | Production possibilities frontier (PPF) | `micro/ppf.py` |
| 2. The cost of something is what you give up to get it | Marginal rate of transformation (MRT) | `micro/ppf.py` |
| 3. Rational people think at the margin | Marginal utility maximization | `agents/consumer.py` |
| 4. People respond to incentives | Taxes / subsidies / price controls | `utils/economics.py` |
| 5. Trade can make everyone better off | Comparative advantage and gains from trade | `micro/trade.py` |
| 6. Markets are usually a good way to organize economic activity | Supply-demand equilibrium and market efficiency | `market/market.py` |
| 7. Governments can sometimes improve market outcomes | Externalities and Pigouvian taxes | `micro/externality.py` |
| 8. A country's standard of living depends on its ability to produce goods and services | GDP accounting and Solow growth | `macro/gdp.py`, `macro/solow.py` |
| 9. Prices rise when the government prints too much money | Quantity theory of money MV=PY | `macro/inflation.py` |
| 10. Society faces a short-run trade-off between inflation and unemployment | Phillips curve | `macro/phillips.py` |

---

## 📂 Project Structure

```
mankiwecolab/
├── main.py                    # CLI entry (full simulation / macro demo / ten principles)
├── config.py                  # All tunable parameters
├── experiments.py             # 8 classic economics experiments
├── agents/                    # Microeconomic agents
│   ├── consumer.py            #   Consumer: utility function + demand
│   └── producer.py            #   Producer: cost function + supply
├── market/                    # Market mechanisms
│   ├── market.py              #   Supply-demand aggregation + price discovery + market clearing
│   └── equilibrium.py         #   Equilibrium solving + surplus + elasticity
├── micro/                     # Microeconomics modules
│   ├── ppf.py                 #   Production possibilities frontier
│   ├── trade.py               #   Comparative advantage and trade
│   ├── externality.py         #   Externalities and Pigouvian taxes
│   └── market_structure.py    #   Perfect competition / oligopoly / monopoly
├── macro/                     # Macroeconomics modules
│   ├── gdp.py                 #   GDP accounting and deflator
│   ├── inflation.py           #   CPI and the quantity theory of money
│   ├── unemployment.py        #   Unemployment rate and natural rate of unemployment
│   ├── solow.py               #   Solow growth model
│   ├── money.py               #   Money creation and multiplier
│   ├── ad_as.py               #   Aggregate demand – aggregate supply model
│   └── phillips.py            #   Phillips curve
├── utils/                     # Utility functions
│   ├── economics.py           #   Gini coefficient, welfare analysis, policy interventions
│   └── visualization.py       #   Micro/macro visualization
├── tests/                     # 204 unit and integration tests
└── output/                    # Charts and CSV data generated at runtime
```

---

## 🚀 Quick Start

### Install from PyPI (recommended)

```bash
pip install mankiwecolab
```

> Domestic mirrors (Tencent Cloud, Tsinghua, etc.) may have a sync delay for new packages. If installation fails, temporarily use the official index:
>
> ```bash
> pip install -i https://pypi.org/simple mankiwecolab
> ```

After installation, use the command-line tool:

```bash
mankiw-econ --help          # View all commands
mankiw-econ                 # Full microeconomic market simulation
mankiw-econ --macro         # Macroeconomics model demo
mankiw-econ --demo          # Mankiw's ten principles demo
mankiw-econ --experiments   # Run all economics experiments
```

You can also download the `.whl` file from [GitHub Releases](https://github.com/NoahIsARider/MankiwEcoLab/releases) and install it:

```bash
pip install ./mankiwecolab-2.0.1-py3-none-any.whl
```

### Run from Source (development mode)

```bash
git clone https://github.com/NoahIsARider/MankiwEcoLab.git
cd MankiwEcoLab
pip install -r requirements.txt
python main.py
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Full Market Simulation

```bash
python main.py
```

Simulates a market with 1,000 consumers and 200 producers; observe how prices gradually converge to equilibrium.

### Run the Macroeconomics Model Demo

```bash
python main.py --macro
```

Walks through GDP accounting, CPI, unemployment, Solow growth, money creation, the AD-AS model, and the Phillips curve in sequence.

### Run Mankiw's Ten Principles Demo

```bash
python main.py --demo
```

### Run All Economics Experiments

```bash
python experiments.py
```

or:

```bash
python main.py --experiments
```

### Run the Tests

```bash
pip install pytest
pytest tests/
```

---

## 🖼️ Visualization Examples

> After running `python main.py`, the following charts are generated in the `output/` directory.

| Microeconomic market simulation | Macroeconomic model demos |
|-------------|-------------|
| Supply/demand curves and market equilibrium | Solow growth convergence paths |
| Price convergence process | AD-AS model equilibrium |
| Market surplus distribution | Phillips curve |
| Welfare distribution analysis | Money creation process |

All charts support Chinese labels; see [docs/](docs/) for detailed documentation.

---

## 📖 Documentation

| Document | Description |
|------|------|
| [USAGE.md](USAGE.md) | Usage guide and custom experiments |
| [STRUCTURE.md](STRUCTURE.md) | Architecture and module descriptions |
| [docs/tutorials/](docs/tutorials/) | Step-by-step tutorials for the ten principles |
| [docs/models.md](docs/models.md) | All mathematical models and formula derivations |
| [docs/api.md](docs/api.md) | API reference |
| [VERIFICATION.md](VERIFICATION.md) | System acceptance report (full verification) |

---

## 🧪 Quality Assurance

This project verifies every economic model with **204 automated tests**:

- **Mathematical correctness tests**: marginal utility = derivative of the utility function, steady-state investment = break-even investment, golden rule f'(k) = δ+n…
- **Economic law tests**: demand falls as price rises, supply rises as price rises, monopoly prices are higher than competitive prices…
- **Determinism tests**: identical random seeds produce exactly identical experimental results
- **Integration tests**: complete simulation flows and generation of all visualizations

Run `pytest tests/` to reproduce all tests.

---

## 🤝 Contributing

Any form of contribution is welcome!

1. **Add new economic models**: create a new module under `micro/` or `macro/` with accompanying tests
2. **Improve visualization**: add more intuitive charts to `utils/visualization.py`
3. **Improve tutorials**: write teaching documentation under `docs/tutorials/`
4. **Fix issues**: submit an issue or pull request

Please make sure `pytest tests/` passes before submitting.

---

## 📄 License

[MIT](LICENSE)

---

## 📚 References

- Mankiw, *Principles of Microeconomics* (8th edition)
- Mankiw, *Principles of Macroeconomics* (8th edition)
- Romer, *Advanced Macroeconomics*
- Varian, *Intermediate Microeconomics*

<p align="center">
  <sub>Built with ❤️ for economics learners around the world</sub>
</p>

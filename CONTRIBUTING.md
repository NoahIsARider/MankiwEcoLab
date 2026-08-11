# Contributing to Mankiw Economics Lab

Thank you for considering contributing to this project! Contributions of all kinds are welcome — new models, bug fixes, documentation, tutorials, and ideas.

## How to Contribute

### 1. Report an Issue

Found a bug or a wrong model derivation? Open an [issue](https://github.com/NoahIsARider/MankiwEcoLab/issues) and include:

- The exact command or code snippet that triggered the problem
- The expected vs. actual output
- Your environment (Python version, platform)

### 2. Add a New Economic Model

The core value of this project is turning textbook models into runnable, tested code. Follow the existing pattern:

1. Create a new module, e.g. `micro/my_model.py` or `macro/my_model.py`
2. Implement the model as a class with **analytic** methods (not just plotting)
3. Add a `verify_*` method where possible so correctness can be asserted mathematically
4. Export the new classes from `micro/__init__.py` or `macro/__init__.py`
5. Add tunable parameters to `config.py`
6. Optionally add a demo section in `main.py` and an experiment in `experiments.py`

### 3. Write Tests

Every new model **must** ship with tests. Tests live in `tests/` and use `pytest`.

```bash
python -m pytest tests/ -q
```

Test style guidance:

- Test mathematical relationships (e.g. optimal bundle satisfies `MRS = Px/Py`)
- Test economic laws (e.g. demand falls when price rises)
- Test edge cases (zero consumption, invalid parameters raising `ValueError`)
- Keep tests deterministic — no randomness without a fixed seed

### 4. Run the Linter

This project uses [ruff](https://github.com/astral-sh/ruff). Before submitting:

```bash
ruff check .
```

The configuration in `pyproject.toml` selects `E`, `F`, `W`, `I` rules (line-length 100, E501 and W293 are ignored).

### 5. Update Documentation

If you add a model or change behaviour, update:

- `docs/models.md` — the mathematical formulation
- `docs/api.md` — the public API reference
- `STRUCTURE.md` — the module tree
- `README.md` — the feature list, if the change is user-facing

### 6. Open a Pull Request

1. Fork the repository and create a feature branch (`git checkout -b feature/my-model`)
2. Make your changes with tests
3. Run `pytest tests/` and `ruff check .` until both pass
4. Push and open a PR against `master`
5. In the PR description, summarise the model, its tests, and any documentation changes

## Development Environment

```bash
git clone https://github.com/NoahIsARider/MankiwEcoLab.git
cd MankiwEcoLab
pip install -e ".[test]"
```

## Code of Conduct

Be respectful and constructive. This project is built for learners around the world, and a friendly environment matters more than any single contribution.

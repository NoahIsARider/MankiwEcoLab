# Mathematical Models and Derivations

This document summarizes all economic models implemented in the project along with their mathematical formulas.

---

## Microeconomics

### 1. Consumer Utility

Consumer utility function:

```
U(q) = α · ln(q + 1) - β · q²
```

- `α` (alpha): the good's base utility value
- `β` (beta): rate of diminishing marginal utility

Marginal utility (derivative with respect to q):

```
MU(q) = dU/dq = α / (q + 1) - 2β · q
```

**Demand solving**: The consumer maximizes utility subject to the budget constraint; the optimality condition is `MU(q) = p`, i.e.:

```
2β · q² + (p + 2β) · q + (p - α) = 0
```

After solving the quadratic equation analytically, take the smaller of the result and the budget constraint `q ≤ income / p`.

### 2. Producer Cost

Total cost function:

```
TC(q) = FC + a · q + 0.5 · b · q²
```

- `FC`: fixed cost
- `a`: constant term of marginal cost
- `b`: slope of marginal cost (diminishing returns to scale)

Marginal cost:

```
MC(q) = dTC/dq = a + b · q
```

**Supply solving**: Under perfect competition `P = MC`, i.e. `q = (P - a) / b`, further constrained by capacity and the shutdown condition (`P ≥ AVC`).

### 3. Market Equilibrium

- Aggregate demand: `D(p) = Σ D_i(p)`
- Aggregate supply: `S(p) = Σ S_j(p)`
- Equilibrium condition: `D(p*) = S(p*)`

**Price adjustment (tâtonnement)**: excess demand `ED = D - S`

```
Δp = α · [ED / (D + S)] · p
```

**Equilibrium checks**:
- Price stability: `std(P_recent) / mean(P_recent) < threshold`
- Balance of supply and demand: `|S - D| / (S + D) < threshold`

### 4. Consumer Surplus and Producer Surplus

Consumer surplus (area under the WTP curve minus expenditure):

```
CS = ∫₀^Q WTP(q) dq - P·Q
```

Producer surplus (revenue minus area under the MC curve):

```
PS = P·Q - ∫₀^Q MC(q) dq
```

Total surplus = CS + PS.

### 5. Production Possibility Frontier (PPF)

Fixed resource `R`, producing X requires `a` resources/unit, producing Y requires `b` resources/unit:

```
a·X + b·Y = R
```

Opportunity cost:

```
OC_x = a / b    (Y given up to produce 1 more unit of X)
OC_y = b / a    (X given up to produce 1 more unit of Y)
```

Marginal rate of transformation MRT = a / b.

### 6. Comparative Advantage and Trade

A producer's hourly output is `ox` units of X or `oy` units of Y:

```
OC_x = oy / ox
OC_y = ox / oy
```

Comparative advantage = the producer with the lower opportunity cost. Gains from trade = total output under specialization - total output under autarky.

### 7. Externalities

Linear supply and demand: `P_d = a_d - b_d·Q`, `P_s = a_s + b_s·Q`

- Negative externality: social supply curve = private supply + external cost `e`
- Social optimum: `Q_social = (a_d - a_s - e) / (b_d + b_s)`
- Deadweight loss: `DWL = 0.5 · |Q_private - Q_social| · |e|`
- Optimal Pigouvian tax = `e`

### 8. Market Structure

Market demand `P = a - b·Q`, firm marginal cost `MC`:

| Structure | Equilibrium condition | Quantity Q | Price P |
|------|---------|--------|--------|
| Perfect competition | P = MC | `(a - MC) / b` | MC |
| Monopoly | MR = MC | `(a - MC) / (2b)` | `a - b·Q` |
| Cournot oligopoly (n firms) | Reaction function | `n(a-MC)/(b(n+1))` | `a - b·Q` |

Herfindahl index: `HHI = Σ s_i² × 10000`

---

## Macroeconomics

### 9. GDP Accounting

Expenditure approach:

```
GDP = C + I + G + NX
```

- `C`: consumption
- `I`: investment
- `G`: government purchases
- `NX`: net exports

Real GDP and the deflator:

```
real_GDP_t = nominal_GDP_t / P_t × P_base
GDP_deflator_t = nominal_GDP_t / real_GDP_t × 100
```

### 10. CPI and Inflation

```
CPI_t = (basket_cost_t / basket_cost_base) × 100
π = (CPI_t - CPI_{t-1}) / CPI_{t-1} × 100
```

### 11. Quantity Theory

```
M · V = P · Y
```

- `M`: money supply
- `V`: velocity of money
- `P`: price level
- `Y`: real output

Money neutrality: with V and Y held constant, `π = ΔM/M`.

### 12. Unemployment Statistics

```
unemployment_rate = unemployed / labor_force × 100
labor_force_participation_rate = labor_force / adult_population × 100
natural_unemployment_rate = frictional + structural
cyclical_unemployment = actual_unemployment_rate - natural_unemployment_rate
```

### 13. Solow Growth Model

Cobb-Douglas production function:

```
Y = A·K^α · L^(1-α)
y = A·k^α          (per-capita form)
```

Capital accumulation equation:

```
Δk = s·f(k) - (δ + n)·k
```

Steady-state capital per worker:

```
k* = [s·A / (δ + n)]^(1/(1-α))
```

Golden rule (maximum steady-state consumption):

```
f'(k_gold) = δ + n
s_gold = α
```

Speed of convergence:

```
λ = (1-α)·(δ+n)
```

### 14. Money Creation

```
deposit_multiplier = 1 / reserve_ratio
money_multiplier = 1 / (reserve_ratio + currency_deposit_ratio)
money_supply = monetary_base × money_multiplier
```

### 15. AD-AS Model

```
AD:   Y = a - b·P
SRAS: Y = c + d·P
LRAS: Y = Y_potential (vertical)
```

- Short-run equilibrium: intersection of AD and SRAS
- Long-run equilibrium: intersection of AD and LRAS (output = potential output)
- Output gap = actual output - potential output

### 16. Phillips Curve

```
π = π^e - β·(u - u_n)
```

- `π^e`: expected inflation
- `u_n`: natural rate of unemployment
- `β`: tradeoff coefficient

Unemployment increase needed to reduce inflation by 1 percentage point: `Δu = 1/β`
Sacrifice ratio: `2/β`

### 17. Consumer Choice Theory

Budget constraint and Cobb-Douglas utility:

```
Px·x + Py·y = I          (budget line)
U(x, y) = x^α · y^(1-α)  (utility function)
```

First-order condition for utility maximization (tangency condition):

```
MRS = MUx / MUy = [α/(1-α)] · (y/x) = Px / Py
```

Analytical solution (optimal consumption bundle):

```
x* = α·I / Px
y* = (1-α)·I / Py
```

- Demand curve: holding I, Py, and α constant, x* varies with Px
- Engel curve: holding prices constant, x* varies with income I

### 18. Game Theory

**Pure-strategy Nash equilibrium**: each player is best-responding given the opponent's strategy, and no one has an incentive to deviate unilaterally:

```
u_i(a_i*, a_{-i}*) ≥ u_i(a_i, a_{-i}*)  ∀a_i
```

**Mixed-strategy Nash equilibrium**: players choose pure strategies according to a probability distribution that leaves the opponent indifferent. For a 2×2 game, the row player's mixed-equilibrium probability is:

```
p = (d - c) / (a - b - c + d)
```

where a, b, c, d are elements of the column player's payoff matrix.

**Dominant strategy**: a strategy that is strictly optimal regardless of the opponent's action; when both players have a dominant strategy, this constitutes a dominant-strategy equilibrium.

**Pareto optimality**: there is no combination that raises one party's payoff without lowering the other's.

**Cournot oligopoly (n symmetric firms)**: market demand `P = a - b·Q`, marginal cost `c`:

```
Best response: q_i = (a - c - b·Σq_j) / (2b)
Nash equilibrium: q* = (a - c) / (b·(n+1))
Equilibrium price: P = (a + n·c) / (n+1)
```

- Collusive output: monopoly solution `Q_m = (a-c)/(2b)`
- Perfectly competitive output: `Q_c = (a-c)/b`

### 19. Loanable Funds Market

Both savings supply and investment demand are functions of the interest rate:

```
S(r) = S0 + S1·r   (upward-sloping supply)
I(r) = I0 - I1·r   (downward-sloping demand)
```

Equilibrium condition (including government borrowing):

```
S0 + S1·r = I0 - I1·r + G
```

Equilibrium interest rate:

```
r* = (I0 + G - S0) / (S1 + I1)
```

**Crowding-out effect**: government borrowing `ΔG` shifts demand right, raises the interest rate, and reduces private investment:

```
ΔI = -I1·Δr < 0
```

**Tax incentive**: raising savings supply `ΔS0` lowers the interest rate and raises investment.

### 20. IS-LM Model

**IS curve** (goods market equilibrium `Y = C + I + G`):

```
Y = [C0 + I0 + G - b·r] / [1 - c·(1 - t)]
```

- `c`: marginal propensity to consume
- `t`: tax rate
- `b`: sensitivity of investment to the interest rate
- Slope: `-b/[1-c(1-t)]` (downward-sloping)

**LM curve** (money market equilibrium `M/P = L(Y, r)`):

```
M/P = k·Y - h·r
```

- `k`: sensitivity of money demand to income
- `h`: sensitivity of money demand to the interest rate
- Slope: `k/h` (upward-sloping)

**Simultaneous equilibrium**:

```
Y* = [ (M/P)·b + h·(C0+I0+G) ] / [ h·(1-c(1-t)) + b·k ]
r* = [ k·(C0+I0+G) - (1-c(1-t))·(M/P) ] / [ h·(1-c(1-t)) + b·k ]
```

**Expenditure multiplier** (no crowding out):

```
α = 1 / [1 - c·(1-t)]
```

Fiscal expansion (`ΔG>0`) raises both output and the interest rate (partially crowding out investment); monetary expansion (`ΔM>0`) raises output and lowers the interest rate.

# 使用指南

> 本文档涵盖：CLI 命令、配置参数、自定义实验、宏微观模型调用、输出文件与常见问题。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

Python 3.9+ 推荐。开发测试环境为 Python 3.11。

### 2. 运行完整微观市场模拟

```bash
python main.py
```

创建 1000 个消费者、200 个生产者，模拟市场通过 35 轮交易收敛到均衡，输出数据与图表到 `output/`。

### 3. 运行宏观演示

```bash
python main.py --macro
```

展示索洛增长、AD-AS、菲利普斯曲线、货币创造四大宏观模型。

### 4. 运行十大原理演示

```bash
python main.py --demo
```

以十个独立条目回顾曼昆《经济学原理》的十大原理。

### 5. 运行全部实验

```bash
python experiments.py
```

运行 10 个经济学实验（供需均衡、需求/供给移动、弹性、价格管制、外部性、市场结构、宏观模型、消费者选择、博弈论与寡头）。

### 6. 交互式 Notebook

```bash
jupyter notebook notebooks/interactive_lab.ipynb
```

交互式演示消费者选择、博弈论、可贷资金市场与 IS-LM 模型。

### 7. 运行测试

```bash
python -m pytest tests/ -q
```

280 个单元与集成测试，覆盖全部模型。

## 命令行接口

```
usage: main.py [-h] [--rounds ROUNDS] [--consumers CONSUMERS]
               [--producers PRODUCERS] [--seed SEED] [--macro]
               [--demo] [--experiments] [--version]

可选参数:
  --rounds N        市场交易轮次 (默认 100)
  --consumers N     消费者数量 (默认 1000)
  --producers N     生产者数量 (默认 1000)
  --seed S          随机种子 (默认 42)
  --macro           运行宏观经济学演示
  --demo            运行十大原理演示
  --experiments     运行全部经济学实验
  --version         显示版本号
```

## 配置参数

所有参数在 `config.py` 中，按模块分组：

### 经济主体数量
```python
NUM_CONSUMERS = 1000
NUM_PRODUCERS = 1000
```

### 模拟参数
```python
NUM_ROUNDS = 100                 # 市场交易轮次
CONVERGENCE_THRESHOLD = 0.01     # 价格收敛阈值
PRICE_ADJUSTMENT_SPEED = 0.1     # 价格调整速度
```

### 消费者参数
```python
CONSUMER_INCOME_MEAN = 1000.0    # 平均收入
CONSUMER_ALPHA_MEAN = 100.0      # 效用函数 α (基本效用)
CONSUMER_BETA_MEAN = 0.5         # 效用函数 β (递减速度)
```

### 生产者参数
```python
PRODUCER_FIXED_COST_MEAN = 500.0 # 平均固定成本
PRODUCER_MC_A_MEAN = 10.0        # 边际成本常数项
PRODUCER_MC_B_MEAN = 0.5         # 边际成本斜率
```

### 宏观模型参数
```python
SOLOW_ALPHA = 0.3                # 资本产出弹性
SOLOW_SAVINGS_RATE = 0.2         # 储蓄率
SOLOW_DEPRECIATION = 0.05        # 折旧率
RESERVE_RATIO = 0.10             # 准备金率
PHILLIPS_BETA = 0.5              # 通胀-失业权衡系数
```

## 自定义实验

### 示例1: 模拟经济冲击

```python
from utils.economics import create_agents
from market import Market

consumer_params = {'income_mean': 1000, 'income_std': 200, 'income_min': 500,
                   'alpha_mean': 100, 'alpha_std': 10, 'beta_mean': 0.5, 'beta_std': 0.05}
producer_params = {'fixed_cost_mean': 300, 'fixed_cost_std': 50, 'mc_a_mean': 10,
                   'mc_a_std': 2, 'mc_b_mean': 0.3, 'mc_b_std': 0.05,
                   'max_capacity_mean': 100, 'max_capacity_std': 20}

consumers, producers = create_agents(1000, 200, consumer_params, producer_params, random_seed=42)
market = Market(consumers, producers, initial_price=50)

for _ in range(50):
    market.run_round()
print(f"初始价格: {market.current_price:.2f}")

for producer in producers:           # 成本上升冲击
    producer.mc_a *= 1.3

for _ in range(50):
    market.run_round()
print(f"冲击后价格: {market.current_price:.2f}")
```

### 示例2: 外部性分析

```python
from micro import ExternalityModel

model = ExternalityModel(demand_intercept=100, demand_slope=2,
                         supply_intercept=10, supply_slope=1, externality_value=10)
result = model.analyze()
print(f"私人产量 {result['private_quantity']:.2f}, "
      f"社会最优 {result['social_quantity']:.2f}, "
      f"无谓损失 {result['deadweight_loss']:.2f}")
```

### 示例3: 索洛增长模型

```python
from macro import SolowGrowthModel

solow = SolowGrowthModel(alpha=0.3, savings_rate=0.2,
                         depreciation_rate=0.05, population_growth_rate=0.01)
analysis = solow.analyze()
print(f"稳态人均资本: {analysis['steady_state']['k']:.2f}")
print(f"黄金律资本: {analysis['golden_rule']['k_gold']:.2f}")
```

### 示例4: 收入不平等分析

```python
from utils.economics import calculate_gini_coefficient, calculate_lorenz_curve

surpluses = [c.consumer_surplus for c in consumers]
print(f"消费者剩余基尼系数: {calculate_gini_coefficient(surpluses):.4f}")
population, cumulative = calculate_lorenz_curve(surpluses)  # 洛伦兹曲线
```

### 示例5: 消费者选择理论

```python
from micro import BudgetConstraint, CobbDouglasUtility, ConsumerChoice

budget = BudgetConstraint(income=1000, price_x=10, price_y=20)
utility = CobbDouglasUtility(alpha=0.5)
choice = ConsumerChoice(budget, utility)

bundle = choice.optimal_bundle()
print(f"最优组合: x*={bundle['x']:.2f}, y*={bundle['y']:.2f}")
print(f"相切条件满足: {choice.verify_tangency()}")

# 需求曲线与恩格尔曲线
prices, quantities = choice.demand_curve('x', price_range=(5, 20))
incomes, engel_q = choice.engel_curve('x', income_range=(500, 2000))
```

### 示例6: 博弈论与古诺竞争

```python
from micro import prisoners_dilemma, CournotGame

pd = prisoners_dilemma()
nash = pd.pure_nash_equilibria()
print(f"囚徒困境纳什均衡: {nash[0]['A_strategy']}/{nash[0]['B_strategy']}")

cg = CournotGame(num_firms=2, demand_intercept=100, demand_slope=1, marginal_cost=20)
eq = cg.nash_equilibrium()
print(f"古诺均衡: 每企业产量 {eq['per_firm_output']:.2f}, 价格 {eq['price']:.2f}")

# 混合策略均衡
from micro import matching_pennies
mp = matching_pennies()
print(f"猜硬币混合均衡: p={mp.mixed_strategy_equilibrium()['p']:.2f}")
```

### 示例7: 可贷资金市场

```python
from macro import LoanableFundsModel

lf = LoanableFundsModel(
    savings_autonomous=800, savings_sensitivity=200,
    investment_autonomous=1200, investment_sensitivity=400,
    government_borrowing=0,
)
print(f"均衡利率: {lf.equilibrium_rate():.2%}")

fiscal = lf.with_fiscal_policy(additional_borrowing=200)
print(f"财政扩张后挤出效应: {fiscal['crowding_out']:.2f}")
```

### 示例8: IS-LM 模型

```python
from macro import ISLMModel

islm = ISLMModel()
eq = islm.equilibrium()
print(f"IS-LM 均衡: Y={eq['output']:.2f}, r={eq['interest_rate']:.2%}")

fp = islm.fiscal_policy(spending_change=50)
mp = islm.monetary_policy(money_supply_change=100)
print(f"财政扩张 ΔY={fp['output_change']:.2f}, 货币扩张 ΔY={mp['output_change']:.2f}")
```

## 核心概念解释

### 1. 效用函数
```
U(q) = α·ln(q+1) - β·q²
MU(q) = α/(q+1) - 2β·q
```
消费者预算约束下效用最大化，最优条件 `MU(q) = p`，解析求解一元二次方程得到需求量。

### 2. 生产成本
```
TC(q) = FC + a·q + 0.5·b·q²
MC(q) = a + b·q
```
完全竞争下供给条件 `P = MC`，受产能与关闭条件约束。

### 3. 市场均衡与调整
```
超额需求 ED = D(p) - S(p)
Δp = α·[ED/(D+S)]·p
```
需求 > 供给 → 价格上升；供给 > 需求 → 价格下降，直至收敛。

### 4. 剩余与效率
- 消费者剩余 CS = WTP 曲线下方 - 支出
- 生产者剩余 PS = 收入 - MC 曲线下方
- 总剩余 = CS + PS，完全竞争均衡下最大化（帕累托最优）

### 5. 宏观核心模型
- 货币数量论: `M·V = P·Y`
- 索洛稳态: `k* = [s·A/(δ+n)]^(1/(1-α))`
- 货币乘数: `m = 1/(r+c)`
- 菲利普斯曲线: `π = πᵉ - β·(u-u_n)`
- 可贷资金均衡: `S0 + S1·r = I0 - I1·r + G`
- IS-LM 均衡: 商品市场 `Y = C+I+G` 与货币市场 `M/P = L(Y,r)` 联立

详细推导见 `docs/models.md`。

## 输出文件说明

`output/` 目录（微观模拟）：

### 数据文件
- `market_data.csv`: 每轮价格、供需、交易量、剩余
- `consumer_data.csv`: 每个消费者的收入、效用、需求量、剩余
- `producer_data.csv`: 每个生产者的成本、产量、利润、剩余
- `summary.csv`: 统计摘要（弹性、基尼系数、效率指标）

### 图表文件
- `supply_demand_curves.png`: 供需曲线与均衡点
- `price_convergence.png`: 价格收敛过程
- `surplus_analysis.png`: 消费者/生产者剩余
- `transaction_volume.png`: 交易量变化
- `agent_distributions.png`: 经济主体参数分布
- `welfare_analysis.png`: 福利分析

宏观演示 (`--macro`) 额外生成:
- `solow_growth.png`: 索洛收敛路径与黄金律
- `ad_as_model.png`: AD-AS 模型
- `phillips_curve.png`: 菲利普斯曲线
- `money_creation.png`: 货币创造过程
- `loanable_funds.png`: 可贷资金市场与挤出效应
- `islm_model.png`: IS-LM 均衡

微观模型也可单独生成:
- `consumer_choice.png`: 消费者选择与最优组合

## 常见问题

### Q1: 为什么市场不收敛到均衡？

1. `PRICE_ADJUSTMENT_SPEED` 过大导致震荡 → 调低
2. 参数不合理 → 检查消费者/生产者参数
3. 轮次不足 → 增加 `--rounds`

### Q2: 如何模拟不同商品类型？

| 类型 | α | β |
|------|-----|-----|
| 必需品 | 100-200 | 0.1-0.3 |
| 正常商品 | 80-120 | 0.4-0.6 |
| 奢侈品 | 40-80 | 0.8-1.5 |

### Q3: 如何加快运行速度？

- 减少主体数量: `--consumers 1000 --producers 200`
- 关闭可视化/保存: 见 `config.py` 中 `SAVE_PLOTS`、`SAVE_RESULTS`

### Q4: 如何分析输出数据？

```python
import pandas as pd
market_data = pd.read_csv('output/market_data.csv')
print(market_data['价格'].describe())
market_data.plot(x='轮次', y=['价格', '交易量'])
```

### Q5: 图表中文显示为方块？

需安装中文字体: `apt-get install fonts-noto-cjk`，然后删除 matplotlib 缓存
`rm -rf ~/.cache/matplotlib` 后重新运行。

## 参考资料

- 曼昆《经济学原理》微观经济学分册 / 宏观经济学分册
- 范里安《微观经济学：现代观点》
- 布兰查德《宏观经济学》

## 文档导航

- README.md - 项目概述
- STRUCTURE.md - 项目结构与数据流
- docs/index.md - 文档索引
- docs/models.md - 数学模型与推导
- docs/api.md - API 参考
- docs/tutorials/ - 分主题教程

# 教程 5: 宏观经济学导览

> 对应曼昆《经济学原理》宏观分册，以及十大原理 8、9、10。
> 关联代码: `macro/` 整个包

## 概述

宏观经济学研究整体经济现象，包括:
- 经济总量 (GDP)
- 物价水平 (CPI, 通胀)
- 就业状况 (失业率)
- 经济增长 (索洛模型)
- 短期波动 (AD-AS, 菲利普斯曲线)

## 运行宏观演示

```bash
python main.py --macro
```

## 逐个模型

### 1. GDP 核算 (原理 8)

```python
from macro import GDPAccounts

gdp = GDPAccounts(consumption=6000, investment=1500,
                  government_spending=2000, net_exports=-500)
print(f"GDP = {gdp.gdp:.2f}")
print(gdp.analyze()['interpretation'])
```

### 2. CPI 与通货膨胀 (原理 9)

```python
from macro import CPI, inflation_rate

cpi = CPI(base_prices=[10, 20, 30], base_quantities=[4, 3, 2])
current_cpi = cpi.compute([12, 22, 31])
print(f"CPI = {current_cpi:.2f}")
print(f"通胀率 = {inflation_rate(100, current_cpi):.2f}%")
```

### 3. 货币数量论 (原理 9)

```python
from macro import QuantityTheory

qt1 = QuantityTheory(money_supply=1000, velocity=5, real_output=100)
qt2 = QuantityTheory(money_supply=2000, velocity=5, real_output=100)
print(f"M=1000 => P={qt1.price_level():.2f}")
print(f"M=2000 => P={qt2.price_level():.2f}  (货币翻倍,物价翻倍)")
```

### 4. 失业分析

```python
from macro import LaborMarketStats, unemployment_decomposition

labor = LaborMarketStats(adult_population=10000, employed=9000, unemployed=500)
print(f"失业率: {labor.unemployment_rate():.2f}%")

decomp = unemployment_decomposition(5.5, 2.0, 2.5)
print(decomp['interpretation'])
```

### 5. 索洛增长模型 (原理 8)

```python
from macro import SolowGrowthModel

solow = SolowGrowthModel(alpha=0.3, savings_rate=0.2,
                         depreciation_rate=0.05, population_growth_rate=0.01)
analysis = solow.analyze()
print(f"稳态人均资本: {analysis['steady_state']['k']:.2f}")
print(f"黄金律资本: {analysis['golden_rule']['k_gold']:.2f}")
```

### 6. 货币创造

```python
from macro import MoneyCreationModel

money = MoneyCreationModel(reserve_ratio=0.10, initial_deposit=1000)
print(f"货币乘数: {money.money_multiplier:.2f}")
print(f"货币供给: {money.total_money_supply:.2f}")
```

### 7. AD-AS 模型

```python
from macro import ADASModel

adas = ADASModel()
analysis = adas.analyze()
print(f"短期均衡: Y={analysis['short_run']['output']:.2f}, "
      f"P={analysis['short_run']['price']:.2f}")
print(f"产出缺口: {analysis['output_gap']:+.2f}")
```

### 8. 菲利普斯曲线 (原理 10)

```python
from macro import PhillipsCurve

pc = PhillipsCurve(expected_inflation=3.0, beta=0.5, natural_unemployment_rate=5.0)
print(f"失业率 4% => 通胀 {pc.inflation_at(4.0):.2f}%")
print(f"失业率 6% => 通胀 {pc.inflation_at(6.0):.2f}%")
```

## 宏观经济学四大核心问题

1. **增长**: 什么决定了长期生活水平? (索洛模型)
2. **通胀**: 为什么物价会上升? (货币数量论)
3. **失业**: 为什么有人找不到工作? (失业分解)
4. **波动**: 为什么经济有周期? (AD-AS, 菲利普斯曲线)

## 思考题

- 为什么央行控制货币供给就能控制长期通胀?
- 短期中降低通胀必然要以高失业为代价吗? (预期的作用)

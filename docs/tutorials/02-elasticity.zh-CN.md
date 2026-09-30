# 教程 2: 价格弹性

> 对应曼昆《经济学原理》第5章。
> 关联代码: `market/equilibrium.py`, `utils/economics.py`

## 概念回顾

**需求价格弹性**: 需求量对价格变化的反应程度。

```
ε = (ΔQ/Q) / (ΔP/P) = (dQ/dP) × (P/Q)
```

| 弹性值 | 类型 | 含义 |
|--------|------|------|
| \|ε\| > 1 | 弹性需求 | 需求量对价格敏感 |
| \|ε\| = 1 | 单位弹性 | 总支出不变 |
| \|ε\| < 1 | 非弹性需求 | 需求量对价格不敏感 |

**收入与弹性的关系**:
- 必需品 (如食物): 非弹性
- 奢侈品 (如珠宝): 弹性

## 运行实验

```bash
python experiments.py
```

实验4会比较必需品和奢侈品的需求弹性差异。

## 代码计算

```python
from market.equilibrium import calculate_elasticity, classify_elasticity

# 需求函数: q = 100 - 2p
def demand(p):
    return max(0.0, 100 - 2 * p)

# 在不同价格点计算弹性
for price in [10, 25, 40]:
    e = calculate_elasticity(demand, price)
    print(f"价格 {price}: 弹性 = {e:.3f}, 类型 = {classify_elasticity(e)}")
```

## 中点法

对于离散的价格-数量数据，使用中点法:

```python
from utils.economics import calculate_price_elasticity_of_demand

# 价格从 10 升至 12，数量从 100 降至 80
e = calculate_price_elasticity_of_demand([10, 12], [100, 80])
print(f"中点法弹性: {e:.3f}")
```

## 观察要点

1. 线性需求曲线上，不同点的弹性不同 (上部弹性，下部非弹性)
2. 弹性与总支出 (P×Q) 的关系
3. 必需品 vs 奢侈品在相同价格变动下的反应差异

## 思考题

- 为什么"谷贱伤农"？这与弹性有什么关系？
- 税收负担在弹性不同的市场上如何分配？

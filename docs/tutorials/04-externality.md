# 教程 4: 外部性与市场失灵

> 对应曼昆《经济学原理》第10章，以及十大原理 7。
> 关联代码: `micro/externality.py`

## 概念回顾

**负外部性** (如污染): 生产者的活动给第三方带来成本，但生产者不承担。
- 私人供给曲线 < 社会供给曲线
- 市场产量 > 社会最优产量 (过度生产)

**正外部性** (如教育): 经济活动给第三方带来收益。
- 私人需求曲线 < 社会需求曲线
- 市场产量 < 社会最优产量 (生产不足)

**庇古税**: 对负外部性征收等于外部成本的税收，使私人成本 = 社会成本。

## 运行实验

```bash
python experiments.py
```

实验6会展示正负外部性对市场均衡的影响。

## 代码分析

```python
from micro import ExternalityModel

# 负外部性 (污染): 外部成本 = 10
model = ExternalityModel(
    demand_intercept=100, demand_slope=2,
    supply_intercept=10, supply_slope=1,
    externality_value=10,
)

analysis = model.analyze()
print(f"私人市场产量: {analysis['private_quantity']:.2f}")
print(f"社会最优产量: {analysis['social_quantity']:.2f}")
print(f"无谓损失: {analysis['deadweight_loss']:.2f}")
print(f"最优庇古税: {analysis['pigouvian_tax']:.2f}")
```

## 数学推导

**负外部性** (外部成本 `e`):

```
社会供给: P = a_s + b_s·Q + e
社会最优: a_d - b_d·Q = a_s + b_s·Q + e
Q_social = (a_d - a_s - e) / (b_d + b_s)
```

**无谓损失**: 市场产量与社会最优之间的社会净损失三角形。

```
DWL = 0.5 × |Q_private - Q_social| × |e|
```

## 观察要点

1. 负外部性导致过度生产，正外部性导致生产不足
2. 无谓损失衡量市场失灵的社会成本
3. 庇古税使私人市场均衡回到社会最优

## 思考题

- 碳税是哪种外部性矫正手段？它的经济学逻辑是什么？
- 教育补贴如何解决正外部性问题？

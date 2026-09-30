# 教程 3: 市场结构

> 对应曼昆《经济学原理》第14-17章。
> 关联代码: `micro/market_structure.py`, `market/equilibrium.py`

## 概念回顾

| 结构 | 企业数量 | 定价权 | 长期利润 |
|------|---------|--------|---------|
| 完全竞争 | 极多 | 无 (价格接受者) | 零 |
| 垄断竞争 | 较多 | 有限 | 零 (产品差异化) |
| 寡头 | 少数 | 有 (策略互动) | 正 |
| 垄断 | 一家 | 完全 | 正 |

**市场效率对比**: 完全竞争 P=MC 最有效率；垄断 P>MC 产生无谓损失。

## 运行实验

```bash
python experiments.py
```

实验7会对比完全竞争、寡头、垄断的价格与产量差异。

## 代码分析

```python
from micro import MarketStructureAnalyzer

# 三种市场结构
for num_firms, name in [(100, "完全竞争"), (3, "寡头"), (1, "垄断")]:
    msa = MarketStructureAnalyzer(
        market_demand_intercept=100, market_demand_slope=1,
        firm_mc=20, num_firms=num_firms,
    )
    analysis = msa.analyze()
    eq = analysis['equilibrium']
    print(f"{name} ({num_firms}家): 价格 = {eq['price']:.2f}, "
          f"数量 = {eq['quantity']:.2f}, 无谓损失 = {analysis['deadweight_loss']:.2f}")
```

## HHI 市场集中度

```python
from market.equilibrium import calculate_herfindahl_hirschman_index

# 两家企业均分市场
hhi = calculate_herfindahl_hirschman_index([0.5, 0.5])
print(f"双寡头 HHI = {hhi}")  # 5000

# 十家企业均分市场
hhi2 = calculate_herfindahl_hirschman_index([0.1] * 10)
print(f"十家企业 HHI = {hhi2}")  # 1000
```

## 观察要点

1. 垄断价格高于边际成本，产量低于社会最优
2. 无谓损失随企业数量减少而增大
3. HHI 越高，市场集中度越高

## 思考题

- 为什么反垄断法关注 HHI 超过 2500 的市场？
- 古诺寡头均衡产量介于垄断与竞争之间，为什么？

# 教程 1: 供需均衡

> 对应曼昆《经济学原理》第4、5章，以及十大原理 3、6。
> 关联代码: `agents/consumer.py`, `agents/producer.py`, `market/market.py`

## 概念回顾

**需求定律**: 其他条件不变时，价格上升 → 需求量下降。

**供给定律**: 其他条件不变时，价格上升 → 供给量上升。

**市场均衡**: 在均衡价格 P\* 处，需求量 = 供给量，市场出清。

## 运行实验

```bash
python experiments.py
```

实验1会展示市场如何从初始价格逐步收敛到均衡。

## 亲手实验

```python
from agents import Consumer, Producer
from market import Market
from utils.economics import create_agents

# 创建 1000 个消费者、200 个生产者
consumer_params = {
    'income_mean': 1000, 'income_std': 200, 'income_min': 500,
    'alpha_mean': 100, 'alpha_std': 10, 'beta_mean': 0.5, 'beta_std': 0.05,
}
producer_params = {
    'fixed_cost_mean': 300, 'fixed_cost_std': 50, 'mc_a_mean': 10,
    'mc_a_std': 2, 'mc_b_mean': 0.3, 'mc_b_std': 0.05,
    'max_capacity_mean': 100, 'max_capacity_std': 20,
}

consumers, producers = create_agents(1000, 200, consumer_params, producer_params, random_seed=42)
market = Market(consumers, producers, initial_price=50, price_adjustment_speed=0.1)

for round_num in range(100):
    if market.run_round():
        print(f"第 {round_num+1} 轮达到均衡!")
        break
    if (round_num + 1) % 10 == 0:
        print(f"第 {round_num+1} 轮: 价格 = {market.current_price:.2f}, "
              f"缺口 = {abs(market.total_demand - market.total_supply):.2f}")

print(f"最终均衡价格: {market.current_price:.2f}")
print(f"均衡数量: {market.quantity_history[-1]:.2f}")
```

## 观察要点

1. 初始价格偏离均衡时，市场出现短缺或过剩
2. 价格调整机制 (tâtonnement) 如何推动市场收敛
3. 收敛后总剩余达到最大化，市场有效率

## 思考题

- 如果提高 `PRICE_ADJUSTMENT_SPEED` 会发生什么？为什么可能震荡？
- 如果降低消费者收入，均衡价格和数量如何变化？

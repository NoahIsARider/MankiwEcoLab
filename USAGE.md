# 使用指南

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行基本模拟

```bash
python main.py
```

这将运行一个完整的经济系统模拟，创建5000个消费者和1000个生产者，并展示市场如何达到均衡。

### 3. 运行实验示例

```bash
python experiments.py
```

这将运行一系列经济学实验，展示不同经济现象。

## 详细说明

### 配置参数

所有参数都在 `config.py` 中配置。主要参数包括：

#### 经济主体数量
```python
NUM_CONSUMERS = 5000  # 消费者数量
NUM_PRODUCERS = 1000  # 生产者数量
```

#### 模拟参数
```python
NUM_ROUNDS = 100  # 市场交易轮次
CONVERGENCE_THRESHOLD = 0.01  # 价格收敛阈值
PRICE_ADJUSTMENT_SPEED = 0.1  # 价格调整速度
```

#### 消费者参数
```python
CONSUMER_INCOME_MEAN = 1000.0  # 平均收入
CONSUMER_ALPHA_MEAN = 100.0  # 效用函数参数
CONSUMER_BETA_MEAN = 0.5  # 边际效用递减率
```

#### 生产者参数
```python
PRODUCER_FIXED_COST_MEAN = 500.0  # 平均固定成本
PRODUCER_MC_A_MEAN = 10.0  # 边际成本常数项
PRODUCER_MC_B_MEAN = 0.5  # 边际成本斜率
```

### 自定义实验

#### 示例1: 模拟经济冲击

```python
from agents import Consumer, Producer
from market import Market
from utils.economics import create_agents

# 创建经济主体
consumer_params = {...}
producer_params = {...}
consumers, producers = create_agents(1000, 200, consumer_params, producer_params)

# 创建市场
market = Market(consumers, producers, initial_price=50)

# 达到初始均衡
for i in range(50):
    market.run_round()

print(f"初始价格: {market.current_price}")

# 模拟外部冲击 - 生产成本上升
for producer in producers:
    producer.mc_a *= 1.3  # 成本上升30%

# 观察新均衡
for i in range(50):
    market.run_round()

print(f"冲击后价格: {market.current_price}")
```

#### 示例2: 比较不同市场结构

```python
# 完全竞争市场 (大量生产者)
consumers1, producers1 = create_agents(1000, 500, consumer_params, producer_params)
market1 = Market(consumers1, producers1, initial_price=50)

# 寡头市场 (少量生产者)
consumers2, producers2 = create_agents(1000, 10, consumer_params, producer_params)
market2 = Market(consumers2, producers2, initial_price=50)

# 运行并比较
for i in range(100):
    market1.run_round()
    market2.run_round()

print(f"完全竞争均衡价格: {market1.current_price}")
print(f"寡头市场均衡价格: {market2.current_price}")
```

#### 示例3: 分析收入不平等

```python
from utils.economics import calculate_gini_coefficient, calculate_lorenz_curve
import matplotlib.pyplot as plt

# 运行模拟
market, consumers, producers = initialize_simulation()
run_simulation(market, consumers, producers)

# 计算基尼系数
consumer_surpluses = [c.consumer_surplus for c in consumers]
gini = calculate_gini_coefficient(consumer_surpluses)
print(f"消费者剩余基尼系数: {gini:.4f}")

# 绘制洛伦兹曲线
population, cumulative_surplus = calculate_lorenz_curve(consumer_surpluses)
plt.plot(population, cumulative_surplus, label='洛伦兹曲线')
plt.plot([0, 1], [0, 1], 'r--', label='完全平等线')
plt.xlabel('累积人口比例')
plt.ylabel('累积剩余比例')
plt.legend()
plt.show()
```

## 核心概念解释

### 1. 效用函数

消费者的效用函数为：
```
U(q) = α * ln(q + 1) - β * q²
```

- **α (alpha)**: 商品的基本效用价值，α越大，消费者越看重该商品
- **β (beta)**: 边际效用递减速度，β越大，边际效用递减越快

### 2. 边际效用

边际效用是多消费一单位商品带来的额外效用：
```
MU(q) = α / (q + 1) - 2β * q
```

消费者在预算约束下追求效用最大化，最优条件是边际效用等于价格。

### 3. 生产成本

生产者的总成本函数为：
```
TC(q) = FC + a * q + 0.5 * b * q²
```

- **FC**: 固定成本（与产量无关）
- **a**: 边际成本的常数项
- **b**: 边际成本的斜率（体现规模报酬递减）

边际成本为：
```
MC(q) = a + b * q
```

### 4. 市场均衡

市场均衡满足：
```
总需求(p*) = 总供给(p*)
```

系统通过迭代调整价格达到均衡：
- 需求 > 供给 → 价格上升
- 供给 > 需求 → 价格下降

### 5. 市场剩余

- **消费者剩余**: 消费者愿意支付的总额 - 实际支付的总额
- **生产者剩余**: 实际收入 - 生产的总可变成本
- **总剩余**: 消费者剩余 + 生产者剩余（衡量市场效率）

## 输出文件说明

运行后会在 `output/` 目录生成以下文件：

### 数据文件
- `market_data.csv`: 每轮的价格、供需、交易量、剩余数据
- `consumer_data.csv`: 每个消费者的详细信息
- `producer_data.csv`: 每个生产者的详细信息
- `summary.csv`: 模拟统计摘要

### 图表文件
- `supply_demand_curves.png`: 供需曲线和均衡点
- `price_convergence.png`: 价格收敛过程
- `surplus_analysis.png`: 市场剩余分析
- `transaction_volume.png`: 交易量变化
- `agent_distributions.png`: 经济主体参数分布
- `welfare_analysis.png`: 福利分析

## 常见问题

### Q1: 为什么市场不收敛到均衡？

可能原因：
1. 价格调整速度太大，导致震荡
2. 参数设置不合理
3. 需要更多轮次

解决方法：
- 降低 `PRICE_ADJUSTMENT_SPEED`
- 增加 `NUM_ROUNDS`
- 检查消费者和生产者参数是否合理

### Q2: 如何模拟不同商品类型？

通过调整效用函数参数：
- **必需品**: 高α（100-200），低β（0.1-0.3）
- **正常商品**: 中α（80-120），中β（0.4-0.6）
- **奢侈品**: 低α（40-80），高β（0.8-1.5）

### Q3: 如何加快运行速度？

- 减少经济主体数量
- 减少模拟轮次
- 设置 `SAVE_PLOTS = False` 跳过可视化
- 设置 `SAVE_RESULTS = False` 跳过数据保存

### Q4: 如何模拟垄断市场？

```python
# 只创建一个生产者
consumers, _ = create_agents(1000, 1, consumer_params, producer_params)
monopolist = Producer(0, fixed_cost=1000, mc_a=5, mc_b=0.2, max_capacity=10000)
producers = [monopolist]

market = Market(consumers, producers, initial_price=100)
```

### Q5: 如何导出数据进行进一步分析？

所有数据都以CSV格式保存，可以用Pandas读取：

```python
import pandas as pd

# 读取市场数据
market_data = pd.read_csv('output/market_data.csv')

# 分析价格趋势
print(market_data['价格'].describe())

# 绘制自定义图表
market_data.plot(x='轮次', y=['价格', '交易量'])
```

## 扩展建议

### 1. 添加时间因素
- 模拟多期投资决策
- 考虑折现因素
- 模拟库存动态

### 2. 添加不确定性
- 随机供给/需求冲击
- 信息不对称
- 预期形成机制

### 3. 多商品市场
- 替代品和互补品
- 交叉价格弹性
- 一般均衡分析

### 4. 宏观经济因素
- 通货膨胀
- 经济周期
- 货币政策影响

### 5. 行为经济学
- 有限理性
- 心理账户
- 羊群效应

## 教学建议

### 课堂演示
1. 先运行基本模拟，展示均衡过程
2. 修改参数，观察结果变化
3. 进行实验，验证经济学理论

### 作业练习
1. 让学生修改参数，观察影响
2. 要求学生设计新的实验
3. 分析实际经济现象

### 项目扩展
1. 实现新的市场机制
2. 添加政府政策模拟
3. 研究市场失灵情况

## 参考资料

- 曼昆《经济学原理》（微观经济学分册）
- 范里安《微观经济学：现代观点》
- Mas-Colell, Whinston, Green《微观经济理论》

## 技术支持

如有问题或建议，请查看：
- README.md - 项目概述
- experiments.py - 实验示例
- 源代码注释 - 详细实现说明

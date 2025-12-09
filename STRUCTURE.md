# 项目结构

```
PrinciplesOfEconomy/
│
├── README.md                    # 项目说明文档
├── USAGE.md                     # 详细使用指南
├── requirements.txt             # Python依赖包列表
├── config.py                    # 配置文件（所有参数）
├── main.py                      # 主程序入口
├── experiments.py               # 经济学实验示例
├── .gitignore                   # Git忽略文件
│
├── agents/                      # 经济主体模块
│   ├── __init__.py             # 模块初始化
│   ├── consumer.py             # 消费者类
│   └── producer.py             # 生产者类
│
├── market/                      # 市场机制模块
│   ├── __init__.py             # 模块初始化
│   ├── market.py               # 市场类
│   └── equilibrium.py          # 均衡计算
│
├── utils/                       # 工具模块
│   ├── __init__.py             # 模块初始化
│   ├── economics.py            # 经济学工具函数
│   └── visualization.py        # 可视化工具
│
└── output/                      # 输出目录（运行后自动创建）
    ├── market_data.csv         # 市场数据
    ├── consumer_data.csv       # 消费者数据
    ├── producer_data.csv       # 生产者数据
    ├── summary.csv             # 统计摘要
    └── *.png                   # 各种图表
```

## 模块说明

### 核心模块

#### agents/ - 经济主体
- **consumer.py**: 实现消费者类，包含效用函数、预算约束、需求计算等
- **producer.py**: 实现生产者类，包含成本函数、利润最大化、供给计算等

#### market/ - 市场机制
- **market.py**: 实现市场类，包含价格发现、市场出清、均衡检验等
- **equilibrium.py**: 均衡计算函数，包括消费者剩余、生产者剩余、弹性等

#### utils/ - 工具函数
- **economics.py**: 经济学相关工具函数（基尼系数、洛伦兹曲线等）
- **visualization.py**: 可视化工具类，生成各种图表

### 主要文件

#### config.py
包含所有可配置参数：
- 经济主体数量和参数分布
- 市场参数（初始价格、调整速度等）
- 模拟参数（轮次、收敛阈值等）
- 输出设置（是否保存图表等）

#### main.py
主程序，执行完整的模拟流程：
1. 初始化经济主体
2. 创建市场
3. 运行模拟
4. 分析结果
5. 生成可视化报告

#### experiments.py
包含5个经济学实验示例：
1. 基本供需均衡
2. 需求曲线移动（收入增加）
3. 供给曲线移动（技术进步）
4. 价格弹性比较（必需品vs奢侈品）
5. 政府干预（价格上限）

## 数据流

```
配置参数 (config.py)
    ↓
创建经济主体 (agents/)
    ↓
初始化市场 (market/)
    ↓
运行模拟循环 ←──┐
    ├ 计算供需      │
    ├ 更新价格      │
    ├ 市场出清      │
    └ 检查均衡 ─────┘
    ↓
分析结果 (utils/economics.py)
    ↓
生成可视化 (utils/visualization.py)
    ↓
保存输出 (output/)
```

## 类关系图

```
┌─────────────┐
│   Consumer  │
│             │
│ - income    │
│ - alpha     │
│ - beta      │
│             │
│ + utility() │
│ + demand()  │
└──────┬──────┘
       │
       │  聚合
       │
┌──────▼──────────────┐
│      Market         │
│                     │      ┌─────────────┐
│ - consumers[]   ────┼─────▶│  Producer   │
│ - producers[]       │      │             │
│ - current_price     │      │ - mc_a      │
│                     │      │ - mc_b      │
│ + run_round()       │      │             │
│ + clear_market()    │      │ + supply()  │
│ + check_equilibrium()│     │ + produce() │
└─────────────────────┘      └─────────────┘
       │
       │  使用
       │
┌──────▼──────────────┐
│   Equilibrium       │
│                     │
│ + find_equilibrium()│
│ + calc_surplus()    │
│ + calc_elasticity() │
└─────────────────────┘
```

## 关键算法

### 1. 需求计算算法
```python
# consumer.py: calculate_demand()
1. 给定价格 p
2. 计算预算约束: max_q = income / p
3. 在 [0, max_q] 范围内搜索
4. 找到使 utility(q) 最大的 q
5. 返回最优需求量
```

### 2. 供给计算算法
```python
# producer.py: calculate_supply()
1. 给定价格 p
2. 从 MC(q) = p 求解: q = (p - a) / b
3. 应用产能约束: q = min(q, capacity)
4. 检查关闭条件: p >= AVC
5. 返回最优供给量
```

### 3. 价格调整算法
```python
# market.py: update_price()
1. 计算总需求 D(p) 和总供给 S(p)
2. 计算超额需求: ED = D - S
3. 标准化调整率: rate = ED / (D + S)
4. 更新价格: p_new = p + α × rate × p
5. 其中 α 是价格调整速度
```

### 4. 均衡检验算法
```python
# market.py: check_equilibrium()
1. 检查价格稳定性: std(recent_prices) / mean < threshold
2. 检查供需平衡: |D - S| / (D + S) < threshold
3. 两个条件都满足 → 达到均衡
```

## 扩展点

### 容易扩展的功能

1. **新的经济主体类型**
   - 在 `agents/` 目录添加新类
   - 实现相同的接口方法

2. **不同的市场机制**
   - 继承 `Market` 类
   - 重写 `update_price()` 方法

3. **政策干预**
   - 在 `utils/economics.py` 添加政策函数
   - 修改市场参数或主体行为

4. **新的分析指标**
   - 在 `market/equilibrium.py` 添加计算函数
   - 在可视化中展示

5. **交互式界面**
   - 使用 Streamlit 或 Dash
   - 实时调整参数并观察结果

## 性能优化建议

1. **大规模模拟**: 使用 NumPy 向量化计算
2. **并行计算**: 使用 multiprocessing 并行模拟多个场景
3. **缓存**: 缓存重复计算的需求/供给曲线
4. **采样**: 对于可视化，只采样部分经济主体

## 测试建议

建议创建 `tests/` 目录，包含：
- 单元测试：测试各个类的方法
- 集成测试：测试完整的模拟流程
- 回归测试：确保结果可重现
- 性能测试：测试大规模模拟的性能

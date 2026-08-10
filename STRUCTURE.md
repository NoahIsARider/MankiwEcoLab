# 项目结构

```
PrinciplesOfEconomy/
│
├── README.md                    # 项目概览与徽章
├── USAGE.md                     # 使用指南
├── STRUCTURE.md                 # 本文档（项目结构）
├── requirements.txt             # Python 依赖包列表
├── pyproject.toml               # 包配置（ruff、pytest、setuptools）
├── LICENSE                      # MIT 许可证
├── .gitignore                   # Git 忽略文件
├── config.py                    # 全部可配置参数
├── main.py                      # CLI 入口（微观/宏观/十大原理）
├── experiments.py               # 8 个经济学实验
│
├── agents/                      # 微观经济主体
│   ├── __init__.py
│   ├── consumer.py              # Consumer 类（效用/需求）
│   └── producer.py              # Producer 类（成本/供给）
│
├── market/                      # 市场机制
│   ├── __init__.py
│   ├── market.py                # Market 类（价格发现/出清）
│   └── equilibrium.py           # 均衡/剩余/弹性/DWL
│
├── micro/                       # 微观扩展模型
│   ├── __init__.py
│   ├── ppf.py                   # 生产可能性边界
│   ├── trade.py                 # 比较优势与贸易
│   ├── externality.py           # 外部性与庇古税
│   └── market_structure.py      # 完全竞争/垄断/寡头
│
├── macro/                       # 宏观经济模型
│   ├── __init__.py
│   ├── gdp.py                   # GDP 核算与平减指数
│   ├── inflation.py             # CPI、通胀率、货币数量论
│   ├── unemployment.py          # 失业率/劳动力参与率
│   ├── solow.py                 # 索洛增长模型
│   ├── money.py                 # 货币创造与乘数
│   ├── ad_as.py                 # AD-AS 模型
│   └── phillips.py              # 菲利普斯曲线
│
├── utils/                       # 工具模块
│   ├── __init__.py
│   ├── economics.py             # 基尼系数/税收均衡/政策模拟
│   └── visualization.py         # EconomicsVisualizer + MacroVisualizer
│
├── tests/                       # 测试套件（204 个测试）
│   ├── test_consumer.py
│   ├── test_producer.py
│   ├── test_market.py
│   ├── test_equilibrium.py
│   ├── test_micro.py
│   ├── test_macro.py
│   └── test_integration.py
│
├── docs/                        # 文档
│   ├── index.md                 # 文档索引
│   ├── models.md                # 数学模型与推导
│   ├── api.md                   # API 参考
│   └── tutorials/               # 分主题教程（5 篇）
│
└── output/                      # 运行后自动生成
    ├── market_data.csv
    ├── consumer_data.csv
    ├── producer_data.csv
    ├── summary.csv
    └── *.png                    # 微观与宏观图表
```

## 模块说明

### agents/ - 经济主体
- **consumer.py**: 效用函数 `U=α·ln(q+1)-β·q²`，解析求解需求，支付意愿与剩余
- **producer.py**: 成本函数 `TC=FC+a·q+0.5·b·q²`，`MC=p` 供给，关闭条件

### market/ - 市场机制
- **market.py**: tâtonnement 价格调整、市场出清、均衡检验
- **equilibrium.py**: `find_equilibrium`、解析剩余、弹性分类、无谓损失、HHI、市场结构判定

### micro/ - 微观扩展
- **ppf.py**: 资源约束下生产边界、机会成本、MRT
- **trade.py**: 绝对/比较优势、专业化方案、贸易收益
- **externality.py**: 私人均衡 vs 社会最优、庇古税、DWL
- **market_structure.py**: 三种市场结构均衡对比

### macro/ - 宏观经济
- **gdp.py**: 支出法 GDP、平减指数、通胀率
- **inflation.py**: CPI、货币数量论 (MV=PY)
- **unemployment.py**: 失业率、参与率、失业分解
- **solow.py**: 稳态、黄金律、收敛路径
- **money.py**: 存款/货币乘数、派生存款
- **ad_as.py**: 短/长期均衡、需求与供给冲击
- **phillips.py**: 通胀-失业权衡、牺牲率

### utils/ - 工具
- **economics.py**: 基尼系数、洛伦兹曲线、泰尔指数、税收/补贴均衡、政策干预
- **visualization.py**: 微观 6 图 + 宏观 4 图（中文标注）

## 数据流

```
config.py → main.py / experiments.py
                ↓
      create_agents (utils/economics.py)
                ↓
        Market (market/market.py)
                ├─ 计算供需 (agents/)
                ├─ 更新价格 (tâtonnement)
                ├─ 市场出清
                └─ 均衡检验 (market/equilibrium.py)
                ↓
     分析 (utils/economics.py, micro/, macro/)
                ↓
     可视化 (utils/visualization.py)
                ↓
     输出 (output/)
```

## 关键算法

### 需求解析求解（consumer.py）
```
MU(q) = p ⇒ 2βq² + (p+2β)q + (p-α) = 0
```
一元二次方程根，与预算约束 `income/p` 取较小值。

### 价格调整（market.py）
```
ED = D(p) - S(p)
p_new = p + α·[ED/(D+S)]·p
```

### 均衡检验（market.py）
```
std(P_recent)/mean < threshold  且  |D-S|/(D+S) < threshold
```

### 索洛稳态（solow.py）
```
k* = (s·A/(δ+n))^(1/(1-α))
λ = (1-α)(δ+n)   # 收敛速度
```

## 扩展点

1. **新增经济主体**: 在 `agents/` 添加类，实现相同接口
2. **新市场机制**: 继承 `Market` 重写 `update_price()`
3. **政策模拟**: 在 `utils/economics.py` 添加函数
4. **新宏观模型**: 在 `macro/` 添加模块，遵循现有 docstring 与 `analyze()` 模式
5. **交互式界面**: Streamlit / Dash 封装 `main.py` 流程

## 性能优化建议

- 大规模模拟用 NumPy 向量化供需计算
- 用 `multiprocessing` 并行多个场景
- 缓存重复计算的需求/供给曲线
- 可视化时采样部分主体

## 测试策略

- 单元测试: 每个类的独立方法（tests/test_consumer.py 等）
- 集成测试: 完整模拟流程（tests/test_integration.py）
- 回归测试: 固定随机种子保证可重现
- 运行: `python -m pytest tests/ -q`（约 25 秒，204 个测试）

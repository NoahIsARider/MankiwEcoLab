# 文档索引

本目录包含曼昆《经济学原理》代码学习项目的全部文档。

## 快速导航

| 文档 | 说明 |
|------|------|
| [models.md](models.md) | 全部数学模型与公式推导 |
| [api.md](api.md) | API 参考手册 |
| [../VERIFICATION.md](../VERIFICATION.md) | 系统验收报告（全量验证） |
| [tutorials/01-supply-demand.md](tutorials/01-supply-demand.md) | 教程：供需均衡 |
| [tutorials/02-elasticity.md](tutorials/02-elasticity.md) | 教程：价格弹性 |
| [tutorials/03-market-structure.md](tutorials/03-market-structure.md) | 教程：市场结构 |
| [tutorials/04-externality.md](tutorials/04-externality.md) | 教程：外部性与市场失灵 |
| [tutorials/05-macro-overview.md](tutorials/05-macro-overview.md) | 教程：宏观经济学导览 |

## 学习路径

### 微观经济学 (Principles 1-7)

1. 阅读 [tutorials/01-supply-demand.md](tutorials/01-supply-demand.md) 理解供需均衡
2. 运行 `python main.py` 观察市场收敛过程
3. 阅读 [tutorials/02-elasticity.md](tutorials/02-elasticity.md) 理解弹性概念
4. 阅读 [tutorials/03-market-structure.md](tutorials/03-market-structure.md) 比较不同市场结构
5. 阅读 [tutorials/04-externality.md](tutorials/04-externality.md) 理解市场失灵
6. 进阶: 消费者选择理论 (`micro/consumer_choice.py`) 与博弈论 (`micro/game_theory.py`)

### 宏观经济学 (Principles 8-10)

1. 阅读 [tutorials/05-macro-overview.md](tutorials/05-macro-overview.md)
2. 运行 `python main.py --macro` 观察宏观模型演示（含可贷资金与 IS-LM）
3. 运行 `python main.py --demo` 回顾全部十大原理
4. 交互式体验: `notebooks/interactive_lab.ipynb`

## 参考

- [models.md](models.md) - 全部数学公式
- [api.md](api.md) - 编程接口参考

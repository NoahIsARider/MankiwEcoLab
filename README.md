<p align="center">
  <img src="https://img.shields.io/badge/曼昆经济学原理-Code%20Lab-2ea44f?style=for-the-badge&logo=bookstack&logoColor=white" alt="Mankiw Economics Lab"/>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/NoahIsARider/PrinciplesOfEconomics?style=flat-square&label=Stars&color=yellow" alt="GitHub Stars"/>
  <img src="https://img.shields.io/github/license/NoahIsARider/PrinciplesOfEconomics?style=flat-square&color=blue" alt="License"/>
  <img src="https://img.shields.io/pypi/pyversions/NoahIsARider/PrinciplesOfEconomics?style=flat-square&color=green" alt="Python Versions"/>
  <img src="https://img.shields.io/badge/pytest-204%20passed-brightgreen?style=flat-square" alt="Tests"/>
  <img src="https://img.shields.io/badge/coverage-comprehensive-brightgreen?style=flat-square" alt="Coverage"/>
  <img src="https://img.shields.io/badge/PRs-welcome-orange?style=flat-square" alt="PRs Welcome"/>
</p>

# 经济学原理模拟系统 (Mankiw Economics Lab)

> **基于曼昆《经济学原理》的交互式代码学习项目** —— 用 Python 亲手实现微观经济学与宏观经济学的每一个核心模型。

本项目把曼昆《经济学原理》教材中从"生产可能性边界"到"菲利普斯曲线"的经典模型，
**逐一翻译为可运行、可实验、可测试的 Python 代码**。你不再只是阅读课本上的图形与公式，
而是可以运行代码、调整参数、观察市场如何收敛、经济如何波动。

---

## ✨ 特性亮点

- **覆盖曼昆十大经济学原理** —— 每个原理都有对应的可运行实验
- **微观 + 宏观全体系** —— 从供给需求均衡到索洛增长模型，一网打尽
- **双入口 CLI** —— `--macro` 与 `--demo` 一键演示宏观模型与十大原理
- **204 个单元与集成测试** —— 每个经济模型都有数学验证，保证正确性
- **完整可视化** —— 供需曲线、价格收敛、索洛收敛路径、AD-AS 均衡、菲利普斯曲线……
- **确定性可复现** —— 固定随机种子，实验结果精确可复现
- **教学友好** —— 中文注释 + 逐行公式推导 + 数学验证测试

---

## 📚 十大原理 × 代码实现

| 原理 | 经济学概念 | 代码位置 |
|------|-----------|---------|
| 1. 人们面临权衡取舍 | 生产可能性边界 PPF | `micro/ppf.py` |
| 2. 机会成本 | 边际转换率 MRT | `micro/ppf.py` |
| 3. 理性人考虑边际量 | 边际效用最大化 | `agents/consumer.py` |
| 4. 人们会对激励做出反应 | 税收/补贴/价格管制 | `utils/economics.py` |
| 5. 贸易能使每个人状况更好 | 比较优势与贸易收益 | `micro/trade.py` |
| 6. 市场通常是组织经济的好方法 | 供需均衡与市场效率 | `market/market.py` |
| 7. 政府有时可以改善市场结果 | 外部性与庇古税 | `micro/externality.py` |
| 8. 生活水平取决于生产能力 | GDP 核算与索洛增长 | `macro/gdp.py`, `macro/solow.py` |
| 9. 过多货币导致物价上升 | 货币数量论 MV=PY | `macro/inflation.py` |
| 10. 通胀与失业的短期权衡 | 菲利普斯曲线 | `macro/phillips.py` |

---

## 📂 项目结构

```
mankiw-economics/
├── main.py                    # CLI 入口 (完整模拟 / 宏观演示 / 十大原理)
├── config.py                  # 全部可调参数
├── experiments.py             # 8 个经典经济学实验
├── agents/                    # 微观主体
│   ├── consumer.py            #   消费者: 效用函数 + 需求
│   └── producer.py            #   生产者: 成本函数 + 供给
├── market/                    # 市场机制
│   ├── market.py              #   供需聚合 + 价格发现 + 市场出清
│   └── equilibrium.py         #   均衡求解 + 剩余 + 弹性
├── micro/                     # 微观经济学模块
│   ├── ppf.py                 #   生产可能性边界
│   ├── trade.py               #   比较优势与贸易
│   ├── externality.py         #   外部性与庇古税
│   └── market_structure.py    #   完全竞争/寡头/垄断
├── macro/                     # 宏观经济学模块
│   ├── gdp.py                 #   GDP 核算与平减指数
│   ├── inflation.py           #   CPI 与货币数量论
│   ├── unemployment.py        #   失业率与自然失业率
│   ├── solow.py               #   索洛增长模型
│   ├── money.py               #   货币创造与乘数
│   ├── ad_as.py               #   总需求-总供给模型
│   └── phillips.py            #   菲利普斯曲线
├── utils/                     # 工具函数
│   ├── economics.py           #   基尼系数、福利分析、政策干预
│   └── visualization.py       #   微观/宏观可视化
├── tests/                     # 204 个单元与集成测试
└── output/                    # 运行生成的图表与 CSV 数据
```

---

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行完整市场模拟

```bash
python main.py
```

运行 1000 个消费者与 200 个生产者的市场，观察价格如何逐步收敛到均衡。

### 运行宏观经济学模型演示

```bash
python main.py --macro
```

依次演示 GDP 核算、CPI、失业、索洛增长、货币创造、AD-AS 模型与菲利普斯曲线。

### 运行曼昆十大原理演示

```bash
python main.py --demo
```

### 运行全部经济学实验

```bash
python experiments.py
```

或：

```bash
python main.py --experiments
```

### 运行测试

```bash
pip install pytest
pytest tests/
```

---

## 🖼️ 可视化示例

> 运行 `python main.py` 后，以下图表会生成到 `output/` 目录。

| 微观市场模拟 | 宏观模型演示 |
|-------------|-------------|
| 供需曲线与市场均衡 | 索洛增长收敛路径 |
| 价格收敛过程 | AD-AS 模型均衡 |
| 市场剩余分配 | 菲利普斯曲线 |
| 福利分配分析 | 货币创造过程 |

所有图表均支持中文标注，详细文档见 [docs/](docs/)。

---

## 📖 详细文档

| 文档 | 说明 |
|------|------|
| [USAGE.md](USAGE.md) | 使用指南与自定义实验 |
| [STRUCTURE.md](STRUCTURE.md) | 架构与模块说明 |
| [docs/tutorials/](docs/tutorials/) | 十大原理分步教程 |
| [docs/models.md](docs/models.md) | 全部数学模型与公式推导 |
| [docs/api.md](docs/api.md) | API 参考 |
| [VERIFICATION.md](VERIFICATION.md) | 系统验收报告（全量验证） |

---

## 🧪 质量保证

本项目通过 **204 个自动化测试** 验证每个经济模型：

- **数学正确性测试**：边际效用 = 效用函数导数、稳态投资 = 持平投资、黄金律 f'(k) = δ+n……
- **经济规律测试**：需求随价格下降、供给随价格上升、垄断价格高于竞争价格……
- **确定性测试**：相同随机种子产生完全相同的实验结果
- **集成测试**：完整模拟流程与所有可视化生成

运行 `pytest tests/` 即可复现全部测试。

---

## 🤝 贡献指南

欢迎任何形式的贡献！

1. **新增经济学模型**：在 `micro/` 或 `macro/` 下新建模块，并配套测试
2. **改进可视化**：为 `utils/visualization.py` 添加更直观的图表
3. **完善教程**：在 `docs/tutorials/` 下撰写教学文档
4. **修复问题**：提交 issue 或 pull request

请确保提交前运行 `pytest tests/` 全部通过。

---

## 📄 License

[MIT](LICENSE)

---

## 📚 参考资料

- 曼昆《经济学原理：微观经济学分册》(第8版)
- 曼昆《经济学原理：宏观经济学分册》(第8版)
- Romer, *Advanced Macroeconomics*
- Varian, *Intermediate Microeconomics*

<p align="center">
  <sub>Built with ❤️ for economics learners around the world</sub>
</p>

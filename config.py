"""
配置文件 - 经济学原理模拟系统
Configuration for Economics Principles Simulation
"""

# ==================== 模拟参数 ====================
# 经济主体数量
NUM_CONSUMERS = 1000  # 消费者数量 (减少以提高速度)
NUM_PRODUCERS = 200   # 生产者数量 (减少以提高速度)

# 模拟轮次
NUM_ROUNDS = 100  # 市场交易轮次
CONVERGENCE_THRESHOLD = 0.01  # 价格收敛阈值

# ==================== 市场参数 ====================
# 初始价格设置
INITIAL_PRICE = 50.0  # 初始市场价格
MIN_PRICE = 1.0  # 最低价格
MAX_PRICE = 200.0  # 最高价格

# 价格调整参数
PRICE_ADJUSTMENT_SPEED = 0.1  # 价格调整速度 (0-1)

# ==================== 消费者参数 ====================
# 收入分布 (正态分布)
CONSUMER_INCOME_MEAN = 1000.0  # 平均收入
CONSUMER_INCOME_STD = 300.0  # 收入标准差
CONSUMER_INCOME_MIN = 100.0  # 最低收入

# 效用函数参数
# 效用函数: U(q) = alpha * ln(q + 1) - beta * q^2
CONSUMER_ALPHA_MEAN = 100.0  # 效用系数alpha的均值
CONSUMER_ALPHA_STD = 20.0  # 效用系数alpha的标准差
CONSUMER_BETA_MEAN = 0.5  # 效用系数beta的均值
CONSUMER_BETA_STD = 0.1  # 效用系数beta的标准差

# ==================== 生产者参数 ====================
# 固定成本分布
PRODUCER_FIXED_COST_MEAN = 500.0  # 平均固定成本
PRODUCER_FIXED_COST_STD = 150.0  # 固定成本标准差

# 边际成本参数
# 边际成本: MC(q) = a + b * q
PRODUCER_MC_A_MEAN = 10.0  # 边际成本常数项均值
PRODUCER_MC_A_STD = 3.0  # 边际成本常数项标准差
PRODUCER_MC_B_MEAN = 0.5  # 边际成本斜率均值
PRODUCER_MC_B_STD = 0.1  # 边际成本斜率标准差

# 生产能力约束
PRODUCER_MAX_CAPACITY_MEAN = 100.0  # 平均最大产能
PRODUCER_MAX_CAPACITY_STD = 30.0  # 产能标准差

# ==================== 可视化参数 ====================
# 图表设置
FIGURE_SIZE = (15, 10)  # 图表大小
DPI = 100  # 图像分辨率
PLOT_STYLE = 'seaborn-v0_8-darkgrid'  # 绘图风格

# 动画设置
ANIMATION_INTERVAL = 200  # 动画间隔(毫秒)
SAVE_ANIMATION = False  # 是否保存动画

# ==================== 输出设置 ====================
# 输出目录
OUTPUT_DIR = 'output'  # 输出目录
SAVE_RESULTS = True  # 是否保存结果
SAVE_PLOTS = True  # 是否保存图表

# 日志设置
LOG_LEVEL = 'INFO'  # 日志级别: DEBUG, INFO, WARNING, ERROR
LOG_INTERVAL = 10  # 每隔多少轮输出一次日志

# ==================== 高级参数 ====================
# 市场类型
MARKET_TYPE = 'competitive'  # 市场类型: competitive, monopoly, oligopoly

# 是否考虑外部性
EXTERNALITY = False  # 是否考虑外部性
EXTERNALITY_COST = 0.0  # 外部成本

# 是否有政府干预
GOVERNMENT_INTERVENTION = False  # 是否有政府干预
TAX_RATE = 0.0  # 税率
SUBSIDY = 0.0  # 补贴

# 随机种子(用于结果可重复)
RANDOM_SEED = 42  # None表示随机

# ==================== 宏观经济学模型参数 ====================
# GDP 核算
MACRO_CONSUMPTION = 6000.0    # 消费 C
MACRO_INVESTMENT = 1500.0     # 投资 I
MACRO_GOVERNMENT = 2000.0     # 政府购买 G
MACRO_NET_EXPORTS = -500.0    # 净出口 NX

# CPI 一篮子商品
CPI_BASE_PRICES = [10.0, 20.0, 30.0]   # 基期价格
CPI_BASE_QUANTITIES = [4.0, 3.0, 2.0]  # 篮子数量
CPI_CURRENT_PRICES = [12.0, 22.0, 31.0]  # 当前价格

# 货币数量论
MONEY_SUPPLY = 1000.0   # 货币供给 M
MONEY_VELOCITY = 5.0    # 货币流通速度 V
REAL_OUTPUT = 100.0     # 实际产出 Y

# 劳动力市场
LABOR_ADULT_POPULATION = 10000.0  # 成年人口
LABOR_EMPLOYED = 9000.0           # 就业人数
LABOR_UNEMPLOYED = 500.0          # 失业人数

# 索洛增长模型
SOLOW_ALPHA = 0.3           # 资本收入份额
SOLOW_SAVINGS_RATE = 0.2    # 储蓄率
SOLOW_DEPRECIATION = 0.05   # 折旧率
SOLOW_POPULATION_GROWTH = 0.01  # 人口增长率

# 货币创造
RESERVE_RATIO = 0.10    # 法定准备金率
INITIAL_DEPOSIT = 1000.0  # 初始存款

# AD-AS 模型
ADAS_POTENTIAL_OUTPUT = 100.0  # 潜在产出
ADAS_AD_INTERCEPT = 150.0      # AD 截距
ADAS_AD_SLOPE = 0.5            # AD 斜率
ADAS_SRAS_INTERCEPT = 50.0     # SRAS 截距
ADAS_SRAS_SLOPE = 0.4          # SRAS 斜率

# 菲利普斯曲线
PHILLIPS_EXPECTED_INFLATION = 3.0  # 预期通胀
PHILLIPS_BETA = 0.5                # 通胀-失业权衡系数
PHILLIPS_NATURAL_UNEMPLOYMENT = 5.0  # 自然失业率

# ==================== 微观补充模型参数 ====================
# 生产可能性边界
PPF_RESOURCE = 100.0   # 总资源
PPF_INPUT_X = 1.0      # 单位X所需资源
PPF_INPUT_Y = 2.0      # 单位Y所需资源

# 外部性
EXTERNALITY_DEMAND_INTERCEPT = 100.0  # 需求截距
EXTERNALITY_DEMAND_SLOPE = 2.0        # 需求斜率
EXTERNALITY_SUPPLY_INTERCEPT = 10.0   # 供给截距
EXTERNALITY_SUPPLY_SLOPE = 1.0        # 供给斜率
EXTERNALITY_VALUE = 10.0              # 外部性价值 (正=负外部性)

# 市场结构
STRUCTURE_DEMAND_INTERCEPT = 100.0  # 市场需求截距
STRUCTURE_DEMAND_SLOPE = 1.0        # 市场需求斜率
STRUCTURE_FIRM_MC = 20.0            # 企业边际成本
STRUCTURE_NUM_FIRMS = 3             # 企业数量

# ==================== 消费者选择理论 ====================
# 预算约束
CHOICE_INCOME = 1000.0      # 消费者收入 I
CHOICE_PRICE_X = 10.0       # 商品 X 价格
CHOICE_PRICE_Y = 20.0       # 商品 Y 价格
CHOICE_ALPHA = 0.5          # 柯布-道格拉斯效用参数 α

# ==================== 博弈论 ====================
# 古诺博弈
COURNOT_FIRMS = 2               # 企业数量
COURNOT_DEMAND_INTERCEPT = 100.0  # 市场需求截距
COURNOT_DEMAND_SLOPE = 1.0        # 市场需求斜率
COURNOT_MARGINAL_COST = 20.0      # 企业边际成本

# ==================== 可贷资金市场 ====================
LOANABLE_SAVINGS_AUTONOMOUS = 800.0       # 自主储蓄 S0
LOANABLE_SAVINGS_SENSITIVITY = 200.0      # 储蓄对利率敏感度 S1
LOANABLE_INVESTMENT_AUTONOMOUS = 1200.0   # 自主投资 I0
LOANABLE_INVESTMENT_SENSITIVITY = 400.0   # 投资对利率敏感度 I1
LOANABLE_GOVERNMENT_BORROWING = 0.0       # 政府借款 G

# ==================== IS-LM 模型 ====================
ISLM_CONSUMPTION_AUTONOMOUS = 100.0      # 自主消费 a
ISLM_MPC = 0.8                            # 边际消费倾向 b
ISLM_TAX_RATE = 0.25                      # 税率 t
ISLM_INVESTMENT_AUTONOMOUS = 200.0        # 自主投资 d
ISLM_INVESTMENT_SENSITIVITY = 1000.0      # 投资对利率敏感度 e
ISLM_GOVERNMENT_SPENDING = 300.0          # 政府购买 G
ISLM_REAL_MONEY_SUPPLY = 500.0            # 实际货币供给 M/P
ISLM_MONEY_DEMAND_INCOME = 0.5            # 货币需求收入敏感度 k
ISLM_MONEY_DEMAND_INTEREST = 200.0        # 货币需求利率敏感度 h

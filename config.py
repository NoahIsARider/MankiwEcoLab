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

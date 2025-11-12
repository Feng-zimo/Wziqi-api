## Wuziqi-API: 高性能五子棋AI引擎

## 简介

Wuziqi-API 是一个基于Python开发的高性能五子棋人工智能接口库，专为五子棋游戏开发者设计。该库提供了一个智能的AI对手，能够进行快速、精准的棋局分析和决策，让开发者可以轻松地将强大的五子棋AI集成到自己的应用中。

## 主要特性

🚀 **卓越性能**
- 采用优化的Minimax算法与Alpha-Beta剪枝技术
- 智能搜索范围限制，大幅提升计算效率
- 多维度棋型评估体系，确保决策质量
- 使用NumPy进行向量化计算，超级加速！

🧠 **智能决策**
- 进攻性策略：主动寻找获胜机会，形成连续攻击
- 防御性思维：及时识别并阻断对手的威胁
- 开局优化：内置专业开局库，确保开局优势
- 局势评估：实时分析棋盘局势，做出最优选择

🔧 **易用接口**
```python
from Wziqi_api import init, Runapi

# 快速初始化
QiPan = init(15, 15).init_board()

# 智能对弈
ai_move = Runapi(QiPan, auto_add=True)
```

## 核心技术

### 算法核心
- Minimax决策树搜索
- Alpha-Beta剪枝优化
- 启发式评估函数
- 棋型识别

### 棋型识别
- 五连、活四、冲四检测
- 活三、冲三评估
- 活二、冲二识别

### 搜索优化
- 局部搜索策略
- 深度可调搜索
- 优先级移动生成
- NumPy向量化计算加速

## 安装与使用

### 基本安装
```bash
pip install wuziqi-api
```

或者从源码安装：
```bash
git clone https://github.com/Feng-zimo/Wziqi-api.git
cd Wziqi-api
pip install -e .
```

### 快速开始
```python
from Wziqi_api import init, Runapi

# 初始化15×15棋盘
QiPan = init(15, 15).init_board()

# 用户先行
QiPan["8,8"] = "users"

# AI响应（自动更新棋盘）
ai_move = Runapi(QiPan, auto_add=True)
print(f"AI落子: {ai_move}")

# 继续对弈
QiPan["7,7"] = "users"
next_ai_move = Runapi(QiPan, auto_add=True)
```

## 核心功能详解

### 棋盘系统
- 坐标格式: "行,列" 字符串键（如 "1,1", "15,15"）
- 状态值: "users"(用户棋子), "api"(AI棋子), "None"(空位)
- 自动更新: auto_add=True 时自动将AI落子加入棋盘

### AI能力层级
- 初级模式 (深度2): 快速响应，适合实时对弈
- 中级模式 (深度3): 平衡速度与强度
- 高级模式 (深度4+): 强力分析，接近专业水平

## 示例代码

我们提供了丰富的示例代码帮助您快速上手：

1. [基础使用示例](./examples/basic_example.py) - 展示最基本的API使用方法
2. [高级使用示例](./examples/advanced_example.py) - 展示自定义难度和其他高级功能
3. [性能测试示例](./examples/performance_test.py) - 测试不同搜索深度下的性能表现
4. [交互式游戏示例](./examples/interactive_game.py) - 命令行人机对弈游戏

## 开发指南

### 安装开发环境
```bash
# 克隆项目
git clone https://github.com/Feng-zimo/Wziqi-api.git
cd Wziqi-api

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 以开发模式安装包
pip install -e .
```

### 运行示例
```bash
# 运行基础示例
python examples/basic_example.py

# 运行交互式游戏
python examples/interactive_game.py
```

### 运行测试
```bash
# 运行性能测试
python examples/performance_test.py
```

### 项目结构
```
wuziqi-api/
├── Wziqi_api/           # 核心模块
│   ├── __init__.py
│   └── core.py         # 核心AI算法实现
├── examples/            # 示例代码
│   ├── basic_example.py
│   ├── advanced_example.py
│   ├── performance_test.py
│   └── interactive_game.py
├── tests/               # 测试代码
├── requirements.txt     # 依赖列表
├── setup.py             # 安装配置（向后兼容）
├── pyproject.toml       # 现代化构建配置
├── README.md            # 说明文档
└── LICENSE              # 许可证
```

## 应用场景

### 🎮 游戏开发
- 单机五子棋游戏
- 在线对战平台AI对手
- 移动端棋类应用

### 🏫 教育学习
- 五子棋策略教学
- AI算法学习案例
- 棋力训练工具

### 🔬 人工智能研究
- 博弈算法验证
- 搜索策略优化
- 评估函数设计

## 性能表现

- 响应时间: 通常 < 3秒（深度3搜索）
- 棋力水平: 业余中级至高级
- 内存占用: 轻量级设计，适合嵌入式环境

## 自定义配置

开发者可以通过调整以下参数来自定义AI行为：

```python
# 创建自定义AI实例
api = WuziqiAPI(rows=15, cols=15, search_depth=4)

# 或者在运行时指定搜索深度
ai_move = Runapi(QiPan, auto_add=True, search_depth=5)
```

## 开源贡献

Wuziqi-API 采用开源模式开发，欢迎开发者：

- 提交Issue和功能建议
- 参与代码优化
- 贡献评估函数改进
- 扩展开局库资源

## 版本信息

当前版本: v1.0.0
Python要求: 3.6+
依赖库: 纯Python实现，无外部依赖

---

让智能五子棋AI为你的应用增添智慧魅力！ 🎯

无论是游戏开发、算法学习还是人工智能研究，Wuziqi-API 都能为你提供强大而可靠的五子棋智能解决方案。
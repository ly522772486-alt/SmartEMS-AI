# SmartEMS-AI

SmartEMS-AI 是一个面向电力市场/储能 EMS 场景的 Python 原型项目。项目围绕指定机组的日前/实时电价与出力数据，完成数据清洗、特征工程、电价预测、策略回测和可视化输出。

当前主流程是：

```text
原始 Excel 数据
-> 多日时间序列数据集
-> 特征工程数据集
-> RandomForest / LightGBM 电价预测
-> 跟价调度策略回测
-> 收益、成本、利润和图表输出
```

## 图形化界面

项目已提供基于 Streamlit 的图形化操作界面，入口文件为：

```bash
streamlit run app.py
```

启动后会先进入登录界面，输入账号和密码后进入系统功能页面。

默认演示账号：

```text
账号：admin
密码：123456
```

Windows / Anaconda Prompt 启动示例：

```bat
streamlit run app.py
```

如需覆盖默认账号密码，可以在启动前设置环境变量。PowerShell 示例：

```powershell
$env:SMARTEMS_USERNAME="your_username"
$env:SMARTEMS_PASSWORD="your_password"
streamlit run app.py
```

界面包含以下功能页面：

| 页面 | 功能 |
| --- | --- |
| 系统总览 | 查看原始数据、处理数据、预测结果和回测结果的生成状态 |
| 数据管理 | 预览原始 Excel，按机组名称构建多日基础数据集 |
| 特征工程 | 生成滞后、滚动、差分和时间特征数据集 |
| 模型训练预测 | 训练 RandomForest、LightGBM、XGBoost 电价预测模型并输出误差指标 |
| 策略回测 | 基于预测电价执行跟价调度策略，生成收益、成本、利润和日度汇总 |
| 报表分析 | 查看预测结果、策略明细、日度汇总和 PNG 图表 |

图形化界面适用于软件著作权说明书中的系统功能展示、操作流程截图和输出结果展示。

## 项目结构

```text
SmartEMS-AI/
├── data/
│   ├── raw/origin_dataset/      # 原始 Excel 数据
│   ├── processed/               # 处理后的数据集
│   └── output/                  # 模型预测结果和图表
├── models/                      # 本地训练好的模型文件
├── output/                      # 策略回测结果
├── reports/                     # 基础分析图表
├── scripts/                     # 数据处理、训练、绘图、回测脚本
├── src/                         # 核心源码
│   ├── analysis/                # 收益、KPI、尖峰、动态分时等分析
│   ├── config/                  # 机组参数和运行约束
│   ├── dataset/                 # 数据预处理与多日数据集构建
│   ├── feature_engineering/     # 滞后、滚动、差分、时间特征
│   ├── forecast/                # 基础预测模型、指标、时间切分
│   ├── models/                  # RandomForest、XGBoost、LightGBM 封装
│   ├── strategy/                # 跟价策略、爬坡约束、收益计算
│   ├── utils/                   # 数据读取工具
│   └── visualization/           # 曲线图、模型对比、特征重要性
├── README.md
└── requirements.txt
```

## 环境准备

建议使用 Python 3.10 或更高版本。

```bash
cd E:/AIProject/SmartEMS-AI
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
```

如果在 Linux/macOS 环境中运行，激活虚拟环境命令为：

```bash
source .venv/bin/activate
```

## 数据说明

原始数据位于：

```text
data/raw/origin_dataset/
```

当前项目使用每日 Excel 文件作为输入，文件名通常为日期，例如：

```text
2026-04-01.xlsx
2026-04-02.xlsx
...
2026-04-30.xlsx
```

数据处理后会生成：

```text
data/processed/merged_dataset.csv
data/processed/feature_dataset.csv
```

`merged_dataset.csv` 的主要字段：

| 字段 | 含义 |
| --- | --- |
| `datetime` | 时间戳 |
| `time` | 当日 96 点时间 |
| `power` | 机组出力 |
| `price` | 市场电价 |
| `revenue` | 当前时段收益 |
| `date` | 日期 |

`feature_dataset.csv` 在基础字段上增加预测特征，例如：

| 字段 | 含义 |
| --- | --- |
| `price_lag_1` | 上一个 15 分钟电价 |
| `price_lag_4` | 前 1 小时电价 |
| `price_lag_96` | 昨天同一时刻电价 |
| `power_lag_1` | 上一个 15 分钟出力 |
| `revenue_lag_1` | 上一个 15 分钟收益 |
| `price_rolling_mean_4` | 最近 4 个点平均电价 |
| `price_rolling_std_4` | 最近 4 个点电价标准差 |
| `price_diff_1` | 当前电价与上一点电价差 |
| `hour` | 小时 |
| `weekday` | 星期 |

## 运行流程

以下命令默认在项目根目录执行。

### 1. 构建多日基础数据集

```bash
python scripts/test_dataset_builder.py
```

输出：

```text
data/processed/merged_dataset.csv
```

### 2. 构建特征数据集

```bash
python scripts/test_feature_engineering.py
```

输出：

```text
data/processed/feature_dataset.csv
```

### 3. 训练 RandomForest 模型

```bash
python scripts/test_randomforest.py
```

输出：

```text
models/random_forest.pkl
data/output/randomforest_prediction_result.csv
```

### 4. 训练 LightGBM 模型

```bash
python scripts/test_lightgbm.py
```

输出：

```text
models/lightgbm.pkl
data/output/lightgbm_prediction_result.csv
```

### 5. 绘制预测和模型对比图

```bash
python scripts/run_randomforest_plot.py
python scripts/run_model_compare.py
python scripts/run_feature_importance.py
```

输出：

```text
data/output/prediction_plot.png
data/output/model_compare.png
data/output/feature_importance.png
```

### 6. 执行策略回测

```bash
python scripts/run_strategy_backtest.py
```

输出：

```text
output/strategy_backtest_result.csv
output/daily_strategy_summary.csv
```

## 核心模块说明

### 数据模块

| 文件 | 说明 |
| --- | --- |
| `src/utils/data_loader.py` | 读取原始 Excel 文件 |
| `src/dataset/preprocess.py` | 提取指定机组数据，并整理为 `time/power/price` 时间序列 |
| `src/dataset/dataset_builder.py` | 合并多日 Excel，生成 `merged_dataset.csv` |

### 特征工程模块

| 文件 | 说明 |
| --- | --- |
| `src/feature_engineering/lag_features.py` | 构建电价、出力、收益滞后特征 |
| `src/feature_engineering/rolling_features.py` | 构建滚动均值和滚动标准差 |
| `src/feature_engineering/diff_features.py` | 构建价格差分特征 |
| `src/feature_engineering/time_features.py` | 构建小时、星期等时间特征 |
| `src/feature_engineering/feature_engineering.py` | 特征工程统一入口 |

### 模型模块

| 文件 | 说明 |
| --- | --- |
| `src/forecast/ml_model.py` | 线性回归基础模型 |
| `src/forecast/price_forecast.py` | 移动平均预测基线 |
| `src/forecast/metrics.py` | MAE、RMSE 指标 |
| `src/models/tree/randomforest.py` | RandomForestRegressor 封装 |
| `src/models/tree/xgboost.py` | XGBRegressor 封装 |
| `src/models/tree/lightgbm.py` | LGBMRegressor 封装 |

### 策略模块

| 文件 | 说明 |
| --- | --- |
| `src/config/unit_config.py` | 机组容量、最小/最大出力、爬坡约束、边际成本 |
| `src/strategy/price_follow_strategy.py` | 根据预测电价给出目标出力 |
| `src/strategy/dispatch_optimizer.py` | 根据爬坡约束修正实际出力 |
| `src/strategy/revenue_calculator.py` | 计算收益、成本和利润 |

### 可视化模块

| 文件 | 说明 |
| --- | --- |
| `src/visualization/plotter.py` | 电价、出力、收益和预测曲线 |
| `src/visualization/randomforest_plot.py` | RandomForest 预测结果曲线 |
| `src/visualization/model_compare_plot.py` | RandomForest 与 LightGBM 对比 |
| `src/visualization/feature_importance_plot.py` | 特征重要性图 |

## 机组参数

机组参数定义在 `src/config/unit_config.py`：

| 参数 | 当前值 | 含义 |
| --- | --- | --- |
| `UNIT_CAPACITY` | 350 | 机组容量 |
| `MIN_POWER` | 120 | 最小出力 |
| `MAX_POWER` | 350 | 最大出力 |
| `RAMP_UP` | 60 | 单步最大升负荷 |
| `RAMP_DOWN` | 60 | 单步最大降负荷 |
| `MARGINAL_COST` | 180 | 边际成本 |
| `TIME_INTERVAL` | 0.25 | 时间间隔，15 分钟 |

## 策略逻辑

`PriceFollowStrategy` 根据预测电价设置目标出力：

| 预测电价区间 | 目标出力 |
| --- | --- |
| `< 260` | 120 MW |
| `260 - 380` | 240 MW |
| `380 - 420` | 300 MW |
| `>= 420` | 350 MW |

随后 `DispatchOptimizer` 根据爬坡约束修正目标出力，`RevenueCalculator` 使用真实市场电价计算收益、成本和利润。

## 注意事项

1. `models/` 目录被 `.gitignore` 忽略，重新拉取项目后需要重新训练模型。
2. `scripts/test_ml_model.py` 和 `scripts/test_xgboost.py` 中仍有旧接口调用，当前推荐优先运行 `test_dataset_builder.py`、`test_feature_engineering.py`、`test_randomforest.py`、`test_lightgbm.py` 和 `run_strategy_backtest.py`。
3. `src/deployment/` 和 `src/optimization/` 下目前多为空文件，部署 API 和高级优化器尚未实现。
4. 部分源码中的中文注释可能存在编码错显，建议后续统一转换为 UTF-8。
5. 当前 `scripts/test_*.py` 更接近可执行实验脚本，不是严格的 pytest 单元测试。

## 后续建议

1. 修复旧脚本接口不一致问题。
2. 补充 pytest 自动化测试。
3. 将数据路径、机组名称、模型参数改为配置文件。
4. 增加模型训练日志和实验版本管理。
5. 实现 `src/deployment/api_service.py`，对外提供预测和策略计算接口。

# SmartEMS-AI

SmartEMS-AI 是一个面向电力现货出清数据的智能分析与预测原型项目。当前版本以机组 96 点出清电力、出清电价数据为输入，完成数据读取、时间序列转换、收益分析、运行评价、尖峰识别、特征工程、价格预测和基础优化策略输出。

## 项目目标

项目当前阶段的目标是建立一条可运行、可解释、可逐步扩展的智能能源管理分析链路：

1. 将横向 Excel 出清数据标准化为 `time / power / price` 时间序列表。
2. 基于 15 分钟粒度计算机组收益、总发电量、最高电价、最高收益时段等关键指标。
3. 分析机组出力与电价之间的相关性，评价是否具备跟价运行能力。
4. 按价格阈值识别尖峰、高价、平价、低价时段，为报价和调度策略提供依据。
5. 构建滞后价格、滚动均值、滚动波动率、小时等机器学习特征。
6. 提供移动平均、线性回归、随机森林、XGBoost、LightGBM 等价格预测路径。
7. 输出基础调度、报价和收益优化建议，为后续接入储能、负荷和多日数据打基础。

## 当前数据

默认数据文件：

```text
data/raw/01日偏差分析.xlsx
```

该文件当前包含 8 行、98 列：

- `名称`：机组名称
- `数据类型`：例如 `出清电力`、`出清电价`
- `00:15` 到 `24:00`：一天 96 个 15 分钟时点

当前脚本默认使用机组：

```text
华北.昱光/20kV.3#机组
```

## 目录说明

```text
src/
  analysis/              收益、KPI、尖峰、动态时段、运行评价
  feature_engineering/   滞后、滚动、时间特征和特征流水线
  forecast/              预测模型、移动平均、评估指标、时间序列切分
  models/tree/           随机森林、XGBoost、LightGBM 模型封装
  optimization/          调度、报价、收益优化基础策略
  utils/                 数据读取工具
  visualization/         Matplotlib 图表输出
  deployment/            轻量 API 服务入口

scripts/                 演示和验证脚本
reports/                 预测结果和图表输出
data/raw/                原始数据
```

## 安装依赖

建议使用 Python 3.9+。

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

其中 `xgboost` 和 `lightgbm` 用于对应树模型脚本。macOS 环境如果缺少 `libomp`，原生 XGBoost/LightGBM 可能无法加载；项目封装会自动降级到 sklearn 的梯度提升模型，保证演示脚本仍可运行。

## 常用运行方式

从项目根目录可以直接运行演示脚本：

```bash
python scripts/test_loader.py
python scripts/test_preprocess.py
python scripts/test_feature_engineering.py
python scripts/test_split.py
python scripts/test_metrics.py
python scripts/test_ml_model.py
python scripts/test_randomforest.py
```

可选模型脚本：

```bash
python scripts/test_xgboost.py
python scripts/test_lightgbm.py
```

无界面环境生成图表时可使用：

```bash
MPLBACKEND=Agg python scripts/test_preprocess.py
```

## 核心功能说明

### 数据读取与标准化

`DataLoader` 负责从 `data/raw` 读取 Excel，并在文件不存在时给出明确异常。`DataPreprocessor` 将原始横向 96 点表转换为标准时间序列：

```text
time, power, price
```

该结构是后续收益分析、特征工程、模型训练和可视化的统一输入。

### 收益与 KPI 分析

`RevenueAnalyzer` 使用 15 分钟结算粒度计算收益：

```text
revenue = price * power * 0.25
```

`KPIAnalyzer` 输出最大电价时段、最大收益时段、平均电价和全天发电量。当前样例机组的日总收益为 `1231323.125`，全天发电量为 `3282.5 MWh`。

### 动态时段与尖峰识别

`DynamicTOUAnalyzer` 基于电价阈值将时段标记为：

- `尖峰`：价格大于等于 450
- `高价`：价格大于等于 350
- `平价`：价格大于等于 250
- `低价`：价格低于 250

`SpikeAnalyzer` 使用 `均值 + 标准差` 作为尖峰阈值，识别异常高价时段。当前样例的尖峰阈值约为 `435.25`。

### 运行评价

`OperationAnalyzer` 计算电价与出力之间的相关系数，并给出跟价运行评价。当前样例相关系数约为 `0.63`，评价为 `较好跟价运行`。

### 特征工程

`FeaturePipeline` 是推荐使用的统一特征入口，会生成：

- `price_lag_1`
- `price_lag_2`
- `price_lag_4`
- `rolling_mean_4`
- `rolling_std_4`
- `hour`

底层模块也可单独使用：`LagFeatures` 构建滞后特征，`RollingFeatures` 构建滚动统计特征，`TimeFeatures` 构建时间特征。

### 价格预测

当前提供五类预测路径：

- 移动平均：`PriceForecaster.moving_average_forecast`
- 线性回归：`MLModel`
- 随机森林：`RandomForestModel`
- XGBoost：`XGBoostModel`
- LightGBM：`LightGBMModel`

XGBoost 和 LightGBM 在缺少原生运行库时会自动降级到 sklearn 的梯度提升模型，并在脚本输出中展示 `Backend`。

### 优化策略

`optimization` 目录提供基础规则策略：

- `DispatchOptimizer`：按电价给出 `增发/放电`、`降发/充电`、`保持`
- `BiddingStrategy`：按电价给出报价策略标签
- `RevenueOptimizer`：对比原收益和优化出力收益

这些策略当前是规则基线，用于后续接入储能约束、负荷预测和市场规则。

### 可视化与部署入口

`Plotter` 生成电价、出力、收益、电价-出力联动和预测曲线，结果保存到 `reports/`。绘图模块会自动选择可用中文字体，并在无界面后端下跳过窗口展示。

`src/deployment/api_service.py` 提供轻量摘要入口，当前可直接输出指定机组的点数、平均电价、总电量和总收益。

## 核心业务流程

1. `DataLoader` 从 `data/raw` 读取 Excel。
2. `DataPreprocessor` 提取指定机组，并构建 96 点标准时间序列。
3. `RevenueAnalyzer` 计算每 15 分钟收益和日总收益。
4. `KPIAnalyzer`、`SpikeAnalyzer`、`DynamicTOUAnalyzer`、`OperationAnalyzer` 输出经营分析结果。
5. `FeatureEngineering` 构造机器学习特征。
6. `MLModel` 或 `src.models.tree` 下的模型完成训练和预测。
7. `ForecastMetrics` 输出 MAE、RMSE。
8. `Plotter` 将曲线保存到 `reports/`。

## Review 与测试

当前已覆盖的验证命令：

```bash
python -m compileall src scripts
python scripts/test_loader.py
python scripts/test_split.py
python scripts/test_feature_engineering.py
python scripts/test_metrics.py
python scripts/test_ml_model.py
python scripts/test_randomforest.py
python scripts/test_xgboost.py
python scripts/test_lightgbm.py
python src/deployment/api_service.py
MPLBACKEND=Agg python scripts/test_preprocess.py
```

当前样例数据下的模型评估结果：

| 脚本 | 模型 | MAE | RMSE |
| --- | --- | ---: | ---: |
| `test_metrics.py` | 移动平均 | 13.09 | 18.97 |
| `test_ml_model.py` | 线性回归 | 10.79 | 13.77 |
| `test_randomforest.py` | 随机森林 | 23.63 | 26.04 |
| `test_xgboost.py` | XGBoost / sklearn fallback | 33.95 | 35.86 |
| `test_lightgbm.py` | LightGBM / sklearn fallback | 33.95 | 35.86 |
 
本轮 review 已修复的问题：

- 脚本直接运行时 `src` 包路径不稳定。
- `test_ml_model.py` 引用了不存在的 `src.forecast.feature_engineering`。
- XGBoost 和 LightGBM 在 macOS 缺少 `libomp` 时直接失败。
- `src/models/` 被 `.gitignore` 的 `models/` 规则误忽略。
- 图表脚本依赖固定 `SimHei` 字体，在当前机器上产生中文字体告警。
- 无界面后端下调用 `plt.show()` 产生告警。
- 多个模型脚本重复手写特征工程流程，已改为统一使用 `FeaturePipeline`。
- 预处理缺少明确的机组/数据类型校验。
- 部分分析函数会原地修改传入 DataFrame，已改为返回副本，降低调用副作用。

## 当前边界

当前项目是单日、单机组、原型级实现，适合验证分析链路和模型接口。后续可扩展方向包括：

- 多日连续时间序列训练和回测
- 多机组批量分析
- 储能充放电约束建模
- 报价策略与现货市场规则结合
- API 服务和前端看板
- 标准 pytest 测试集和持续集成

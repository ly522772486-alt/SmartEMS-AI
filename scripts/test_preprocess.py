import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from src.utils.data_loader import DataLoader
from src.dataset.preprocess import DataPreprocessor


loader = DataLoader()

df = loader.load_excel("01日偏差分析.xlsx")

# 获取96点时间列
time_cols = DataPreprocessor.extract_time_columns(df)

print("时间列数量:", len(time_cols))

print(time_cols[:5])

# 提取不同机组 以3#为例
unit_df = DataPreprocessor.extract_unit_data(
    df,
    "华北.昱光/20kV.3#机组"
)

print(unit_df)

# 构建时间序列表
ts_df = DataPreprocessor.build_unit_timeseries(unit_df)

print(ts_df)

from src.analysis.revenue_analysis import RevenueAnalyzer

# 收益计算
ts_df = RevenueAnalyzer.calculate_revenue(ts_df)

print(ts_df)

# 日总收益
total_revenue = RevenueAnalyzer.calculate_total_revenue(ts_df)

print()

print("日总收益:", total_revenue)

from src.visualization.plotter import Plotter

# 电价曲线
Plotter.plot_price_curve(ts_df)

# 出力曲线
Plotter.plot_power_curve(ts_df)

# 收益曲线
Plotter.plot_revenue_curve(ts_df)

# 电价-出力曲线
Plotter.plot_price_power(ts_df)

from src.analysis.kpi_analysis import KPIAnalyzer

print()
print("========== KPI分析 ==========")

# 最大电价
max_price_row = KPIAnalyzer.get_max_price(ts_df)

print()
print("最大电价时段:")
print(max_price_row)

# 最大收益
max_revenue_row = KPIAnalyzer.get_max_revenue(ts_df)

print()
print("最大收益时段:")
print(max_revenue_row)

# 平均电价
avg_price = KPIAnalyzer.get_average_price(ts_df)

print()
print("平均电价:", avg_price)

# 全天发电量
total_energy = KPIAnalyzer.get_total_energy(ts_df)

print()
print("全天发电量(MWh):", total_energy)

from src.analysis.dynamic_tou_analysis import DynamicTOUAnalyzer

# 动态标签
ts_df = DynamicTOUAnalyzer.add_dynamic_label(ts_df)

print()
print("========== 动态时段标签 ==========")

print(ts_df)

# 动态汇总
dynamic_summary = DynamicTOUAnalyzer.summarize_dynamic(ts_df)

print()
print("========== 动态时段统计 ==========")

print(dynamic_summary)

from src.analysis.operation_analysis import OperationAnalyzer

print()
print("========== 跟价运行分析 ==========")

correlation = OperationAnalyzer.calculate_correlation(
    ts_df
)

print("电价-出力相关系数:", correlation)

evaluation = OperationAnalyzer.evaluate_operation(
    correlation
)

print("经营评价:", evaluation)

from src.analysis.spike_analysis import SpikeAnalyzer

print()
print("========== 尖峰分析 ==========")

spikes, threshold = SpikeAnalyzer.detect_spikes(
    ts_df
)

print("尖峰阈值:", threshold)

print()
print("尖峰时段:")

print(
    spikes[
        ["time", "price", "power", "revenue"]
    ]
)

from src.forecast.price_forecast import PriceForecaster

# 移动平均预测
ts_df = PriceForecaster.moving_average_forecast(
    ts_df
)

print()
print("========== AI价格预测 ==========")

print(
    ts_df[
        ["time", "price", "price_ma"]
    ].head(10)
)

# 保存预测结果
ts_df.to_csv(
    "reports/forecast_result.csv",
    index=False,
    encoding="utf-8-sig"
)

print()
print("预测结果已保存")

# AI预测图
Plotter.plot_forecast(ts_df)
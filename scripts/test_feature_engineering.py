import _bootstrap  # noqa: F401

from src.utils.data_loader import DataLoader
from src.analysis.preprocess import DataPreprocessor

from src.feature_engineering.feature_engineering import (
    FeatureEngineering
)


# ======================
# 1. 读取数据
# ======================

loader = DataLoader()

raw_df = loader.load_excel(
    "01日偏差分析.xlsx"
)


# ======================
# 2. 提取机组数据
# ======================

unit_df = DataPreprocessor.extract_unit_data(
    raw_df,
    "华北.昱光/20kV.3#机组"   # 改成真实机组名
)


# ======================
# 3. 构建时间序列
# ======================

df = DataPreprocessor.build_unit_timeseries(
    unit_df
)


# ======================
# 4. 构建特征
# ======================

df = FeatureEngineering.add_lag_features(df)

df = FeatureEngineering.add_rolling_features(df)

df = FeatureEngineering.add_time_features(df)


# ======================
# 5. 删除空值
# ======================

df = df.dropna()


# ======================
# 6. 查看结果
# ======================

print(df.head())

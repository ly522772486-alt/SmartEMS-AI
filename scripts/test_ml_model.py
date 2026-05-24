from sklearn.model_selection import train_test_split

from src.utils.data_loader import DataLoader
from src.dataset.preprocess import DataPreprocessor
from src.feature_engineering.feature_engineering import FeatureEngineering
from src.forecast.ml_model import MLModel

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)

import numpy as np


# =========================
# 1. 读取数据
# =========================

loader = DataLoader()

raw_df = loader.load_excel(
    "01日偏差分析.xlsx"
)

# =========================
# 2. 提取机组数据
# =========================

unit_df = DataPreprocessor.extract_unit_data(
    raw_df,
    "华北.昱光/20kV.3#机组"
)

# =========================
# 3. 构建时间序列
# =========================

df = DataPreprocessor.build_unit_timeseries(
    unit_df
)

# =========================
# 4. 特征工程
# =========================

df = FeatureEngineering.add_lag_features(df)

df = FeatureEngineering.add_rolling_features(df)

df = FeatureEngineering.add_time_features(df)

# 删除空值
df = df.dropna()

# =========================
# 5. 构建 X/y    X是什么？AI输入，即：AI看到的市场信息；本质是告诉AI当前市场是什么状态。 y是什么？真实市场答案；即：真正市场价格
# =========================

X = df[
    [
        "price_lag_1",
        "price_lag_2",
        "price_lag_4",
        "rolling_mean_4",
        "rolling_std_4",
        "hour"
    ]
]

y = df["price"]

# =========================
# 6. 划分训练测试集
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    shuffle=False
)

# =========================
# 7. 模型训练
# =========================

model = MLModel.train_linear_regression(
    X_train,
    y_train
)

# =========================
# 8. 模型预测
# =========================

predictions = MLModel.predict(
    model,
    X_test
)

# =========================
# 9. 模型评估
# =========================

mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        predictions
    )
)

print("\n========== AI模型评估 ==========")

print(f"MAE: {mae:.2f}")

print(f"RMSE: {rmse:.2f}")

# =========================
# 10. 查看预测结果
# =========================

result_df = X_test.copy()

result_df["real_price"] = y_test.values

result_df["pred_price"] = predictions

print("\n========== 预测结果 ==========")

print(
    result_df[
        [
            "real_price",
            "pred_price"
        ]
    ].head(10)
)
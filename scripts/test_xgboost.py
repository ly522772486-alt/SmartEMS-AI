import _bootstrap  # noqa: F401

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)

import numpy as np

from src.utils.data_loader import DataLoader
from src.analysis.preprocess import DataPreprocessor

from src.feature_engineering.feature_pipeline import FeaturePipeline

from src.models.tree.xgboost import (
    XGBoostModel
)


# =====================================
# 1. 读取数据
# =====================================

loader = DataLoader()

raw_df = loader.load_excel(
    "01日偏差分析.xlsx"
)

# =====================================
# 2. 提取机组数据
# =====================================

unit_df = DataPreprocessor.extract_unit_data(
    raw_df,
    "华北.昱光/20kV.3#机组"
)

# =====================================
# 3. 构建时间序列
# =====================================

df = DataPreprocessor.build_unit_timeseries(
    unit_df
)

# =====================================
# 4. 特征工程
# =====================================

X, y, df = FeaturePipeline.split_xy(df)

# =====================================
# 5. 构建特征 X
# =====================================

print("特征列:", list(X.columns))


# =====================================
# 6. 构建目标 y
# =====================================

# =====================================
# 7. 划分训练集测试集
# =====================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    shuffle=False
)

# =====================================
# 8. 训练 XGBoost
# =====================================

model = XGBoostModel.train(
    X_train,
    y_train
)

# =====================================
# 9. 模型预测
# =====================================

predictions = XGBoostModel.predict(
    model,
    X_test
)

# =====================================
# 10. 模型评估
# =====================================

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

print("\n========== XGBoost模型评估 ==========")

print("Backend:", getattr(model, "backend_name", "xgboost"))

print(f"MAE: {mae:.2f}")

print(f"RMSE: {rmse:.2f}")

# =====================================
# 11. 查看预测结果
# =====================================

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

# =====================================
# 12. 特征重要性
# =====================================

importance_df = FeaturePipeline.get_feature_importance(
    model,
    X.columns
)

print("\n========== 特征重要性 ==========")

print(importance_df)

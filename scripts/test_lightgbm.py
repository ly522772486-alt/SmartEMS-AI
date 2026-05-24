import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import (
    train_test_split
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)

from src.models.tree.lightgbm import (
    LightGBMModel
)

# =====================================
# 读取数据
# =====================================

df = pd.read_csv(

    "data/processed/feature_dataset.csv",

    index_col="datetime",

    parse_dates=True
)

# =====================================
# 构建Target
# =====================================

df["target_price"] = (
    df["price"].shift(-1)
)

df = df.dropna()

# =====================================
# 特征列
# =====================================

feature_columns = [

    "price_lag_1",
    "price_lag_4",
    "price_lag_96",

    "power_lag_1",

    "revenue_lag_1",

    "price_rolling_mean_4",
    "price_rolling_std_4",

    "price_diff_1",

    "hour",
    "weekday"
]

# =====================================
# X / y
# =====================================

X = df[feature_columns]

y = df["target_price"]

# =====================================
# 划分数据集
# =====================================

X_train, X_test, y_train, y_test = (

    train_test_split(

        X,
        y,

        test_size=0.2,

        shuffle=False
    )
)

# =====================================
# 构建模型
# =====================================

model = (
    LightGBMModel
    .build_model()
)

# =====================================
# 模型训练
# =====================================

print("开始训练 LightGBM...")

model.fit(

    X_train,

    y_train
)

print("训练完成")

# =====================================
# 模型预测
# =====================================

pred = model.predict(X_test)

# =====================================
# 模型评估
# =====================================

mae = mean_absolute_error(

    y_test,

    pred
)

rmse = (
    mean_squared_error(
        y_test,
        pred
    ) ** 0.5
)

print("\n========== LightGBM模型评估 ==========")

print(f"MAE: {mae:.2f}")

print(f"RMSE: {rmse:.2f}")

# =====================================
# 保存模型
# =====================================

Path("models").mkdir(

    exist_ok=True
)

model_path = (
    "models/lightgbm.pkl"
)

joblib.dump(

    model,

    model_path
)

print("\n模型已保存:")

print(model_path)

# =====================================
# 保存预测结果
# =====================================

Path("output").mkdir(

    exist_ok=True
)

result_df = pd.DataFrame({

    "real_price": y_test,

    "pred_price": pred

}, index=y_test.index)

result_path = (
    "data/output/lightgbm_prediction_result.csv"
)

result_df.to_csv(

    result_path,

    encoding="utf-8-sig"
)

print("\n预测结果已保存:")

print(result_path)
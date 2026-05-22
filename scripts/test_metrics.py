import _bootstrap  # noqa: F401

import pandas as pd

from src.forecast.metrics import ForecastMetrics


# ======================
# 1. 读取预测结果
# ======================

df = pd.read_csv(
    "reports/forecast_result.csv"
)


# ======================
# 2. 删除空值
# ======================

df = df.dropna()


# ======================
# 3. 真实值
# ======================

y_true = df["price"].values


# ======================
# 4. 预测值
# ======================

y_pred = df["price_ma"].values


# ======================
# 5. MAE
# ======================

mae = ForecastMetrics.mae(
    y_true,
    y_pred
)


# ======================
# 6. RMSE
# ======================

rmse = ForecastMetrics.rmse(
    y_true,
    y_pred
)


# ======================
# 7. 输出结果
# ======================

print("\n========== 模型评估 ==========")

print("MAE:", round(mae, 2))

print("RMSE:", round(rmse, 2))

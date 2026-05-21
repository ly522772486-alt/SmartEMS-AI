import numpy as np

from src.forecast.metrics import ForecastMetrics


# 真实值
y_true = np.array([
    390,
    385,
    400,
    420,
    450
])

# 预测值
y_pred = np.array([
    392,
    380,
    410,
    415,
    440
])


# 计算MAE
mae = ForecastMetrics.mae(
    y_true,
    y_pred
)

# 计算RMSE
rmse = ForecastMetrics.rmse(
    y_true,
    y_pred
)


print("MAE:", mae)

print("RMSE:", rmse)
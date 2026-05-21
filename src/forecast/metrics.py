import numpy as np


class ForecastMetrics:

    @staticmethod
    def mae(y_true, y_pred):

        """
        平均绝对误差
        """

        return np.mean(
            np.abs(y_true - y_pred)
        )

    @staticmethod
    def rmse(y_true, y_pred):

        """
        均方根误差
        """

        return np.sqrt(
            np.mean((y_true - y_pred) ** 2)
        )
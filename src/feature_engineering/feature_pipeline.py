from src.feature_engineering.lag_features import LagFeatures
from src.feature_engineering.rolling_features import RollingFeatures
from src.feature_engineering.time_features import TimeFeatures
import pandas as pd


class FeaturePipeline:
    """Reusable feature pipeline for price forecasting."""

    DEFAULT_FEATURE_COLUMNS = [
        "price_lag_1",
        "price_lag_2",
        "price_lag_4",
        "rolling_mean_4",
        "rolling_std_4",
        "hour",
    ]

    @staticmethod
    def build(df, dropna=True):
        result = LagFeatures.add_price_lags(df, lags=(1, 2, 4))
        result = RollingFeatures.add_price_rolling(result, windows=(4,))
        result = TimeFeatures.add_hour(result)

        if dropna:
            result = result.dropna()

        return result

    @classmethod
    def split_xy(cls, df, target="price"):
        feature_df = cls.build(df, dropna=True)
        X = feature_df[cls.DEFAULT_FEATURE_COLUMNS].astype(float)
        y = feature_df[target].astype(float)

        return X, y, feature_df

    @staticmethod
    def get_feature_importance(model, feature_names):
        if not hasattr(model, "feature_importances_"):
            raise AttributeError("当前模型不支持 feature_importances_")

        importance_df = pd.DataFrame({
            "feature": feature_names,
            "importance": model.feature_importances_,
        })

        return importance_df.sort_values(by="importance", ascending=False)

from src.feature_engineering.lag_features import (
    LagFeatures
)

from src.feature_engineering.rolling_features import (
    RollingFeatures
)

from src.feature_engineering.time_features import (
    TimeFeatures
)

from src.feature_engineering.diff_features import (
    DiffFeatures
)


class FeatureEngineering:

    @staticmethod
    def build_features(df):

        # =====================================
        # Lag Features
        # =====================================

        df = (
            LagFeatures
            .add_price_lag_features(df)
        )

        df = (
            LagFeatures
            .add_power_lag_features(df)
        )

        df = (
            LagFeatures
            .add_revenue_lag_features(df)
        )

        # =====================================
        # Rolling Features
        # =====================================

        df = (
            RollingFeatures
            .add_price_rolling_features(df)
        )

        # =====================================
        # Diff Features
        # =====================================

        df = (
            DiffFeatures
            .add_price_diff_features(df)
        )

        # =====================================
        # Time Features
        # =====================================

        df = (
            TimeFeatures
            .add_time_features(df)
        )

        return df
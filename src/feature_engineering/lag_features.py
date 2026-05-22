class LagFeatures:
    """Price lag feature builders for 15-minute market series."""

    @staticmethod
    def add_price_lags(df, lags=(1, 2, 4)):
        result = df.copy()

        for lag in lags:
            result[f"price_lag_{lag}"] = result["price"].shift(lag)

        return result

class RollingFeatures:
    """Rolling statistics for market state features."""

    @staticmethod
    def add_price_rolling(df, windows=(4,)):
        result = df.copy()

        for window in windows:
            result[f"rolling_mean_{window}"] = (
                result["price"].rolling(window=window).mean()
            )
            result[f"rolling_std_{window}"] = (
                result["price"].rolling(window=window).std()
            )

        return result

class RevenueOptimizer:
    """Basic revenue comparison helpers for dispatch strategies."""

    @staticmethod
    def estimate_revenue(price, power, interval_hours=0.25):
        return price * power * interval_hours

    @classmethod
    def add_revenue_delta(cls, df, optimized_power_col="optimized_power"):
        result = df.copy()
        if optimized_power_col not in result.columns:
            raise KeyError(f"缺少优化出力列: {optimized_power_col}")

        result["optimized_revenue"] = cls.estimate_revenue(
            result["price"],
            result[optimized_power_col],
        )
        result["revenue_delta"] = result["optimized_revenue"] - result["revenue"]

        return result

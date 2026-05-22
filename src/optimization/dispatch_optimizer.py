class DispatchOptimizer:
    """Rule-based dispatch hints based on dynamic price periods."""

    @staticmethod
    def recommend_action(price, high_threshold=350, low_threshold=250):
        if price >= high_threshold:
            return "增发/放电"
        if price < low_threshold:
            return "降发/充电"
        return "保持"

    @classmethod
    def add_dispatch_action(cls, df):
        result = df.copy()
        result["dispatch_action"] = result["price"].apply(cls.recommend_action)

        return result

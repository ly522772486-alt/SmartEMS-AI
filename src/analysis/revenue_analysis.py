class RevenueAnalyzer:

    @staticmethod
    def calculate_revenue(df):

        result = df.copy()

        # 计算每15分钟收益
        result["revenue"] = (
            result["price"] *
            result["power"] *
            0.25
        )

        return result

    @staticmethod
    def calculate_total_revenue(df):

        return df["revenue"].sum()

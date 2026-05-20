class RevenueAnalyzer:

    @staticmethod
    def calculate_revenue(df):

        # 计算每15分钟收益
        df["revenue"] = (
            df["price"] *
            df["power"] *
            0.25
        )

        return df

    @staticmethod
    def calculate_total_revenue(df):

        return df["revenue"].sum()
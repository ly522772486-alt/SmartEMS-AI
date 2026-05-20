class KPIAnalyzer:

    @staticmethod
    def get_max_price(df):

        idx = df["price"].idxmax()

        return df.loc[idx]

    @staticmethod
    def get_max_revenue(df):

        idx = df["revenue"].idxmax()

        return df.loc[idx]

    @staticmethod
    def get_average_price(df):

        return df["price"].mean()

    @staticmethod
    def get_total_energy(df):

        # 15分钟 -> 小时
        return (df["power"] * 0.25).sum()
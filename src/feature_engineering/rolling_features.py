class RollingFeatures:

    @staticmethod
    def add_price_rolling_features(df):

        # 最近1小时平均价格
        df["price_rolling_mean_4"] = (
            df["price"]
            .rolling(window=4)
            .mean()
        )

        # 最近1小时价格波动
        df["price_rolling_std_4"] = (
            df["price"]
            .rolling(window=4)
            .std()
        )

        return df
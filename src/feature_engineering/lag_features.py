class LagFeatures:

    @staticmethod
    def add_price_lag_features(df):

        # 上一个15分钟价格
        df["price_lag_1"] = (
            df["price"].shift(1)
        )

        # 上一个1小时价格
        df["price_lag_4"] = (
            df["price"].shift(4)
        )

        # 昨天同一时刻价格
        df["price_lag_96"] = (
            df["price"].shift(96)
        )

        return df

    @staticmethod
    def add_power_lag_features(df):

        # 上一个15分钟功率
        df["power_lag_1"] = (
            df["power"].shift(1)
        )

        return df

    @staticmethod
    def add_revenue_lag_features(df):

        # 上一个15分钟收益
        df["revenue_lag_1"] = (
            df["revenue"].shift(1)
        )

        return df
class PriceForecaster:   # 最基础的移动平均，window=4 代表取一个小时内4个点的平均

    @staticmethod
    def moving_average_forecast(df, window=4):

        # 计算移动平均
        df["price_ma"] = (
            df["price"]
            .rolling(window=window)
            .mean()
        )

        return df
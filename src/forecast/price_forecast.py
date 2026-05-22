class PriceForecaster:   # 最基础的移动平均，window=4 代表取一个小时内4个点的平均

    @staticmethod
    def moving_average_forecast(df, window=4):

        result = df.copy()

        # 计算移动平均
        result["price_ma"] = (
            result["price"]
            .rolling(window=window)
            .mean()
        )

        return result

class DiffFeatures:    # 变化率

    @staticmethod
    def add_price_diff_features(df):

        # 当前价格 - 上一个价格
        df["price_diff_1"] = (
            df["price"].diff(1)
        )

        return df
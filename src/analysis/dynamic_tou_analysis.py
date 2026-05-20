class DynamicTOUAnalyzer:

    @staticmethod
    def classify_dynamic_period(price):

        # 尖峰
        if price >= 450:
            return "尖峰"

        # 高价
        elif price >= 350:
            return "高价"

        # 正常
        elif price >= 250:
            return "平价"

        # 低价
        else:
            return "低价"

    @staticmethod
    def add_dynamic_label(df):

        df["dynamic_period"] = df["price"].apply(
            DynamicTOUAnalyzer.classify_dynamic_period
        )

        return df

    @staticmethod
    def summarize_dynamic(df):

        summary = df.groupby(
            "dynamic_period"
        ).agg({

            "revenue": "sum",

            "power": "mean",

            "price": "mean"

        })

        return summary
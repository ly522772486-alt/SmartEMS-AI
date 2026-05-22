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

        result = df.copy()

        result["dynamic_period"] = result["price"].apply(
            DynamicTOUAnalyzer.classify_dynamic_period
        )

        return result

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

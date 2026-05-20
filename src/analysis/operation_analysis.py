class OperationAnalyzer:

    @staticmethod
    def calculate_correlation(df):

        correlation = df["price"].corr(
            df["power"]
        )

        return correlation

    @staticmethod
    def evaluate_operation(correlation):

        if correlation >= 0.7:
            return "优秀跟价运行"

        elif correlation >= 0.4:
            return "较好跟价运行"

        elif correlation >= 0:
            return "一般"

        else:
            return "未跟价运行"
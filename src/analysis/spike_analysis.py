class SpikeAnalyzer:

    @staticmethod
    def detect_spikes(df):

        avg_price = df["price"].mean()

        std_price = df["price"].std()

        # 尖峰阈值
        threshold = avg_price + std_price

        spikes = df[
            df["price"] > threshold
        ]

        return spikes, threshold
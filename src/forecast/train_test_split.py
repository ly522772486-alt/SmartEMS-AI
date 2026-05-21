import pandas as pd


class TimeSeriesSplit:

    def __init__(self, df):

        self.df = df

    def split(self, train_ratio=0.8):

        """
        时间序列训练集/测试集切分
        """

        train_size = int(len(self.df) * train_ratio)

        train_df = self.df.iloc[:train_size]

        test_df = self.df.iloc[train_size:]

        return train_df, test_df
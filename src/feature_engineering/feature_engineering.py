import pandas as pd


class FeatureEngineering:

    @staticmethod
    def add_lag_features(df):

        """
        构建滞后特征 # 更像是"记忆" 市场历史记忆
        """

        df = df.copy()

        # 前1个点价格
        df["price_lag_1"] = (
            df["price"].shift(1)
        )

        # 前2个点价格
        df["price_lag_2"] = (
            df["price"].shift(2)
        )

        # 前4个点价格
        df["price_lag_4"] = (
            df["price"].shift(4)
        )

        return df

    @staticmethod
    def add_rolling_features(df):

        """
        构建滚动统计特征 # 高级特征 市场当前状态
        """

        df = df.copy()

        # 4点移动平均,趋势特征
        df["rolling_mean_4"] = (
            df["price"]
            .rolling(window=4)
            .mean()
        )

        # 4点波动率（标准差）
        df["rolling_std_4"] = (
            df["price"]
            .rolling(window=4)
            .std()
        )

        return df

    @staticmethod
    def add_time_features(df):

        """
        构建时间特征   # 当前市场阶段
        """

        df = df.copy()

        # ======================
        # 时间字段清洗
        # ======================

        # 转字符串
        df["time"] = (
            df["time"]
            .astype(str)
        )

        # 去除空格
        df["time"] = (
            df["time"]
            .str.strip()
        )

        # 替换24:00
        df["time"] = (
            df["time"]
            .str.replace(
                "24:00",
                "00:00"
            )
        )

        # ======================
        # 转datetime
        # ======================

        time_dt = pd.to_datetime(
            df["time"],
            format="%H:%M",
            errors="coerce"
        )

        # ======================
        # 提取小时
        # ======================

        df["hour"] = (
            time_dt.dt.hour
        )

        return df
        
    @staticmethod
    def get_feature_importance(
         model,
        feature_names
         ):

         importance_df = pd.DataFrame({

        "feature": feature_names,

        "importance": model.feature_importances_

         })

         importance_df = importance_df.sort_values(
        by="importance",
        ascending=False
         )

         return importance_df
    
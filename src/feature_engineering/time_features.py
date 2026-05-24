class TimeFeatures:

    @staticmethod
    def add_time_features(df):

        # 小时
        df["hour"] = df.index.hour

        # 星期 
        df["weekday"] = df.index.weekday   

        df["day_name"] = (
        df.index.day_name()
          )

        return df
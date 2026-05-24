import pandas as pd


class DataPreprocessor:

    @staticmethod
    def extract_time_columns(df):

        # 获取96点时间列
        time_columns = df.columns[2:]

        return list(time_columns)

    @staticmethod
    def extract_unit_data(df, unit_name):

        # 提取指定机组数据
        unit_df = df[df["名称"] == unit_name]

        return unit_df
    
    @staticmethod
    def build_unit_timeseries(unit_df):

        # 时间列
        time_columns = unit_df.columns[2:]

        # 电力行
        power_row = unit_df[
            unit_df["数据类型"] == "出清电力"
        ]

        # 电价行
        price_row = unit_df[
            unit_df["数据类型"] == "出清电价"
        ]

        # 构建标准表
        result_df = pd.DataFrame({

            "time": time_columns,

            "power": power_row.iloc[0, 2:].values,

            "price": price_row.iloc[0, 2:].values

        })

        result_df["power"] = pd.to_numeric(
        result_df["power"],
        errors="coerce"
           )

        result_df["price"] = pd.to_numeric(
        result_df["price"],
         errors="coerce"
            )

        return result_df
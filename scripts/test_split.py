import _bootstrap  # noqa: F401

from src.utils.data_loader import DataLoader
from src.analysis.preprocess import DataPreprocessor

from src.forecast.train_test_split import TimeSeriesSplit


# 读取数据
loader = DataLoader()

raw_df = loader.load_excel("01日偏差分析.xlsx")


# 提取机组数据
unit_df = DataPreprocessor.extract_unit_data(
    raw_df,
    "华北.昱光/20kV.3#机组"
)

# 构建标准时间序列
df = DataPreprocessor.build_unit_timeseries(
    unit_df
)


# 切分数据
splitter = TimeSeriesSplit(df)

train_df, test_df = splitter.split()


print("训练集长度：", len(train_df))
print("测试集长度：", len(test_df))

print("\n训练集：")
print(train_df.head())

print("\n测试集：")
print(test_df.head())

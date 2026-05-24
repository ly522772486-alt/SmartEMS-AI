from src.dataset.dataset_builder import DatasetBuilder


folder_path = (
    r"E:\AIProject\SmartEMS-AI\data\raw\origin_dataset"
)

# 机组名称
unit_name = "华北.昱光/20kV.3#机组"

df = DatasetBuilder.build_multi_day_dataset(
    folder_path,
    unit_name
)

print(df.head())

print(df.info())

print(df.shape)
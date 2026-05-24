import pandas as pd

from src.feature_engineering.feature_engineering import (
    FeatureEngineering
)

# =====================================
# 读取数据
# =====================================

df = pd.read_csv(

    "data/processed/merged_dataset.csv",

    index_col="datetime",

    parse_dates=True
)

# =====================================
# 构建Feature
# =====================================

df = (
    FeatureEngineering
    .build_features(df)
)

# =====================================
# 删除NaN
# =====================================

df = df.dropna()

# =====================================
# 查看结果
# =====================================

print(df)

print("\n数据维度:")
print(df.shape)

print("\n字段列表:")
print(df.columns.tolist())

# =====================================
# 保存Feature数据集
# =====================================

save_path = (
    "data/processed/"
    "feature_dataset.csv"
)

df.to_csv(

    save_path,

    encoding="utf-8-sig"
)

print("\nFeature数据集已保存:")

print(save_path)
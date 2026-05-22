import _bootstrap  # noqa: F401

from src.utils.data_loader import DataLoader

loader = DataLoader()

df = loader.load_excel("01日偏差分析.xlsx")

print(df.head())

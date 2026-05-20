import sys
from pathlib import Path

# 项目根目录
project_root = Path(__file__).resolve().parents[1]

# 添加到Python路径
sys.path.append(str(project_root))

from src.utils.data_loader import DataLoader

loader = DataLoader()

df = loader.load_excel("01日偏差分析.xlsx")

print(df.head())
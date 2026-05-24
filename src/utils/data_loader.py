from pathlib import Path
import pandas as pd


class DataLoader:

    def __init__(self):

        # 项目根目录
        self.project_root = Path(__file__).resolve().parents[2]

        # 原始数据目录
        self.raw_data_dir = (
            self.project_root / "data" / "raw" / "origin_dataset"
        )

    def load_excel(self, filename):

        file_path = self.raw_data_dir / filename

        # 文件存在检查
        if not file_path.exists():
            raise FileNotFoundError(
                f"文件不存在: {file_path}"
            )

        print(f"正在读取文件: {file_path}")

        df = pd.read_excel(file_path)

        print("读取成功")

        return df
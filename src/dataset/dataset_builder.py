from pathlib import Path
import pandas as pd

from src.utils.data_loader import DataLoader
from src.dataset.preprocess import DataPreprocessor


class DatasetBuilder:

    @staticmethod
    def build_multi_day_dataset(
        folder_path,
        unit_name
    ):

        # =====================================
        # 保存所有天的数据
        # =====================================

        all_df = []

        # =====================================
        # DataLoader实例化
        # =====================================

        loader = DataLoader()

        # =====================================
        # 获取所有Excel文件
        # =====================================

        excel_files = sorted(
            Path(folder_path).glob("*.xlsx")
        )

        print(f"共发现 {len(excel_files)} 个Excel文件")

        # =====================================
        # 遍历文件
        # =====================================

        for file in excel_files:

            print(f"\n正在处理: {file.name}")

            # =====================================
            # 1. 读取Excel
            # =====================================

            raw_df = loader.load_excel(
                file
            )

            # =====================================
            # 2. 提取指定机组
            # =====================================

            unit_df = (
                DataPreprocessor.extract_unit_data(
                    raw_df,
                    unit_name
                )
            )

            # =====================================
            # 3. 构建96点标准时间序列
            # =====================================

            df = (
                DataPreprocessor.build_unit_timeseries(
                    unit_df
                )
            )

            # =====================================
            # 4. 从文件名提取日期
            # =====================================

            date_str = file.stem

            # =====================================
            # 5. 构建 datetime
            # =====================================

            datetime_list = []

            for t in df["time"]:

                t = str(t)

                # =================================
                # 处理24:00
                # =================================

                if t == "24:00":

                    current_date = pd.to_datetime(
                        date_str
                    )

                    next_day = (
                        current_date +
                        pd.Timedelta(days=1)
                    )

                    dt = pd.to_datetime(
                        next_day.strftime("%Y-%m-%d")
                        + " 00:00"
                    )

                else:

                    dt = pd.to_datetime(
                        f"{date_str} {t}"
                    )

                # append必须在for内部
                datetime_list.append(dt)

            # =====================================
            # 6. 添加datetime列
            # =====================================

            df["datetime"] = datetime_list

            # =====================================
            # 7. 收益计算
            # =====================================

            df["revenue"] = (
                df["price"] *
                df["power"] *
                0.25
            )

            # =====================================
            # 8. 添加日期列
            # =====================================

            df["date"] = date_str

            # =====================================
            # 9. 添加到总列表
            # =====================================

            all_df.append(df)

        # =====================================
        # 10. 合并所有数据
        # =====================================

        final_df = pd.concat(
            all_df,
            ignore_index=True
        )

        # =====================================
        # 11. 按时间排序
        # =====================================

        final_df = final_df.sort_values(
            "datetime"
        )

        # =====================================
        # 12. 重置索引
        # =====================================

        final_df = final_df.reset_index(
            drop=True
        )

        # =====================================
        # 13. 设置时间索引
        # =====================================

        final_df = final_df.set_index(
            "datetime"
        )

        # =====================================
        # 14. 保存CSV
        # =====================================

        save_dir = Path(
            "data/processed"
        )

        save_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        csv_path = (
            save_dir /
            "merged_dataset.csv"
        )

        final_df.to_csv(
            csv_path,
            encoding="utf-8-sig"
        )

        # =====================================
        # 15. 输出信息
        # =====================================

        print("\n数据集构建完成")
        print(f"总样本数: {len(final_df)}")

        print("\n数据集已保存:")
        print(csv_path)

        return final_df
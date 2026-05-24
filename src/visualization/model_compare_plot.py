import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path


class ModelComparePlot:

    @staticmethod
    def plot_compare():

        # =====================================
        # 读取RandomForest结果
        # =====================================

        rf_df = pd.read_csv(

            "data/output/randomforest_prediction_result.csv",

            index_col="datetime",

            parse_dates=True
        )

        # =====================================
        # 读取LightGBM结果
        # =====================================

        lgb_df = pd.read_csv(

            "data/output/lightgbm_prediction_result.csv",

            index_col="datetime",

            parse_dates=True
        )

        # =====================================
        # 创建结果DataFrame
        # =====================================

        compare_df = pd.DataFrame({

            "real_price":

                rf_df["real_price"],

            "rf_pred":

                rf_df["pred_price"],

            "lgb_pred":

                lgb_df["pred_price"]
        })

        # =====================================
        # 创建画布
        # =====================================

        plt.figure(figsize=(18, 7))

        # =====================================
        # 真实价格
        # =====================================

        plt.plot(

            compare_df.index,

            compare_df["real_price"],

            label="Real Price",

            linewidth=2
        )

        # =====================================
        # RandomForest
        # =====================================

        plt.plot(

            compare_df.index,

            compare_df["rf_pred"],

            label="RandomForest"
        )

        # =====================================
        # LightGBM
        # =====================================

        plt.plot(

            compare_df.index,

            compare_df["lgb_pred"],

            label="LightGBM"
        )

        # =====================================
        # 图标题
        # =====================================

        plt.title(

            "Model Compare"
        )

        # =====================================
        # 坐标轴
        # =====================================

        plt.xlabel("Datetime")

        plt.ylabel("Price")

        # =====================================
        # 图例
        # =====================================

        plt.legend()

        # =====================================
        # 网格
        # =====================================

        plt.grid(True)

        # =====================================
        # 自动布局
        # =====================================

        plt.tight_layout()

        # =====================================
        # 创建output目录
        # =====================================

        Path("output").mkdir(

            exist_ok=True
        )

        # =====================================
        # 保存图片
        # =====================================

        save_path = (

            "data/"
            "output/"
            "model_compare.png"
        )

        plt.savefig(save_path)

        print("\n模型对比图已保存:")

        print(save_path)

        # =====================================
        # 显示图像
        # =====================================

        plt.show()
import pandas as pd
import matplotlib.pyplot as plt


class PredictionPlot:

    @staticmethod
    def plot_prediction():

        # =====================================
        # 读取预测结果
        # =====================================

        df = pd.read_csv(

            "data/output/randomforest_prediction_result.csv",

            index_col="datetime",

            parse_dates=True
        )

        # =====================================
        # 创建画布
        # =====================================

        plt.figure(figsize=(16, 6))

        # =====================================
        # 真实价格
        # =====================================

        plt.plot(

            df.index,

            df["real_price"],

            label="Real Price"
        )

        # =====================================
        # 预测价格
        # =====================================

        plt.plot(

            df.index,

            df["pred_price"],

            label="Pred Price"
        )

        # =====================================
        # 图标题
        # =====================================

        plt.title(
            "RandomForest Price Prediction"
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
        # 保存图片
        # =====================================
        from pathlib import Path
        Path("output").mkdir(
        
         exist_ok=True
        )

        save_path = (
            "data/"
            "output/"
            "prediction_plot.png"
        )

        plt.savefig(save_path)

        print("\n预测图已保存:")

        print(save_path)

        # =====================================
        # 显示图像
        # =====================================

        plt.show()
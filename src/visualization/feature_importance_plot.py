import joblib
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path


class FeatureImportancePlot:

    @staticmethod
    def plot_feature_importance():

        # =====================================
        # 读取模型
        # =====================================

        model = joblib.load(

            "models/random_forest.pkl"
        )

        # =====================================
        # 特征名称
        # =====================================

        feature_columns = [

            "price_lag_1",
            "price_lag_4",
            "price_lag_96",

            "power_lag_1",

            "revenue_lag_1",

            "price_rolling_mean_4",
            "price_rolling_std_4",

            "price_diff_1",

            "hour",
            "weekday"
        ]

        # =====================================
        # 获取importance
        # =====================================

        importance = (
            model.feature_importances_
        )

        # =====================================
        # 构建DataFrame
        # =====================================

        importance_df = pd.DataFrame({

            "feature": feature_columns,

            "importance": importance
        })

        # =====================================
        # 排序
        # =====================================

        importance_df = (
            importance_df
            .sort_values(

                "importance",

                ascending=False
            )
        )

        print(importance_df)

        # =====================================
        # 创建画布
        # =====================================

        plt.figure(figsize=(10, 6))

        # =====================================
        # 条形图
        # =====================================

        plt.bar(

            importance_df["feature"],

            importance_df["importance"]
        )

        # =====================================
        # 图标题
        # =====================================

        plt.title(
            "Feature Importance"
        )

        # =====================================
        # 坐标轴
        # =====================================

        plt.xlabel("Feature")

        plt.ylabel("Importance")

        # =====================================
        # 旋转X轴
        # =====================================

        plt.xticks(rotation=45)

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
            "feature_importance.png"
        )

        plt.savefig(save_path)

        print("\n特征重要性图已保存:")

        print(save_path)

        # =====================================
        # 显示图像
        # =====================================

        plt.show()
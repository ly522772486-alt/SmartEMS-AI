import os
from pathlib import Path


os.environ.setdefault(
    "MPLCONFIGDIR",
    str(Path("/tmp") / "smartems-ai-matplotlib"),
)

import matplotlib.pyplot as plt
from matplotlib import font_manager

# 设置中文字体
available_fonts = {font.name for font in font_manager.fontManager.ttflist}
preferred_fonts = [
    "SimHei",
    "PingFang SC",
    "Heiti SC",
    "Songti SC",
    "Arial Unicode MS",
]
selected_fonts = [
    font_name for font_name in preferred_fonts if font_name in available_fonts
]

if selected_fonts:
    plt.rcParams['font.sans-serif'] = selected_fonts

# 正常显示负号
plt.rcParams['axes.unicode_minus'] = False

class Plotter:

    @staticmethod
    def _show_if_interactive():
        if "agg" not in plt.get_backend().lower():
            plt.show()

    @staticmethod
    def plot_price_curve(df):

        plt.figure(figsize=(14, 5))

        plt.plot(
            df["time"],
            df["price"]
        )

        plt.title("3#机组96点电价曲线")

        plt.xlabel("时间")

        plt.ylabel("电价（元/MWh）")

        plt.xticks(
             ticks=range(0, len(df["time"]), 4),
             labels=df["time"][::4],
             rotation=45
          )

        plt.grid(True)

        plt.tight_layout()

        plt.savefig("reports/price_curve.png")

        Plotter._show_if_interactive()

    @staticmethod
    def plot_power_curve(df):

        plt.figure(figsize=(14, 5))

        plt.plot(
            df["time"],
            df["power"]
        )

        plt.title("3#机组96点电力曲线")

        plt.xlabel("时间")

        plt.ylabel("出力(MW)")

        plt.xticks(
             ticks=range(0, len(df["time"]), 4),
             labels=df["time"][::4],
             rotation=45
          )

        plt.grid(True)

        plt.tight_layout()

        plt.savefig("reports/power_curve.png")

        Plotter._show_if_interactive()

    @staticmethod
    def plot_revenue_curve(df):

        plt.figure(figsize=(14, 5))

        plt.plot(
            df["time"],
            df["revenue"]
        )

        plt.title("3#机组96点收益曲线")

        plt.xlabel("时间")

        plt.ylabel("收益(元)")

        plt.xticks(
             ticks=range(0, len(df["time"]), 4),
             labels=df["time"][::4],
             rotation=45
          )

        plt.grid(True)

        plt.tight_layout()

        plt.savefig("reports/revenue_curve.png")

        Plotter._show_if_interactive()

    @staticmethod
    def plot_price_power(df):

        fig, ax1 = plt.subplots(figsize=(14, 5))

        # 电价轴
        ax1.plot(
            df["time"],
            df["price"],
            label="电价",
            color="red",
            linewidth=2,
            linestyle="--"
        )

        ax1.set_xlabel("时间")

        ax1.set_ylabel("电价（元/MWh）")

        ax1.legend(loc="upper left")

        ax1.tick_params(axis='y')

        # 第二个Y轴
        ax2 = ax1.twinx()

        ax2.plot(
            df["time"],
            df["power"],
            label="出力",
            color="blue",
            linewidth=2
        )

        ax2.set_ylabel("出力（MW）")

        ax2.legend(loc="upper right")

        ax2.tick_params(axis='y')

        # X轴优化
        plt.xticks(
            ticks=range(0, len(df["time"]), 4),
            labels=df["time"][::4],
            rotation=45
        )

        plt.title("3#机组电价-出力联动曲线")

        fig.tight_layout()

        plt.grid(True)

        plt.savefig("reports/price_power_curve.png")

        Plotter._show_if_interactive()

    @staticmethod
    def plot_forecast(df):

        plt.figure(figsize=(14, 5))

        # 原始价格
        plt.plot(
            df["time"],
            df["price"],
            label="实时电价",
            color="red"
        )

        # 移动平均趋势
        plt.plot(
            df["time"],
            df["price_ma"],
            label="预测趋势",
            color="blue",
            linewidth=2
        )

        plt.title("AI电价趋势预测")

        plt.xlabel("时间")

        plt.ylabel("电价（元/MWh）")

        plt.xticks(
            ticks=range(0, len(df["time"]), 4),
            labels=df["time"][::4],
            rotation=45
        )

        plt.legend()

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(
            "reports/forecast_curve.png"
        )

        Plotter._show_if_interactive()

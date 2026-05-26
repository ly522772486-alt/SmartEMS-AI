import pandas as pd

from src.strategy.price_follow_strategy import (
    PriceFollowStrategy
)

from src.strategy.dispatch_optimizer import (
    DispatchOptimizer
)

from src.strategy.revenue_calculator import (
    RevenueCalculator
)

from src.config.unit_config import (
    MIN_POWER
)

# =========================
# 读取预测结果
# =========================

df = pd.read_csv(
    "data/output/randomforest_prediction_result.csv"
)

# 时间列转datetime
df["datetime"] = pd.to_datetime(
    df["datetime"]
)

# 提取日期（后面做每日收益统计）
df["date"] = df["datetime"].dt.date

# =========================
# 初始化模块
# =========================

strategy = PriceFollowStrategy()

optimizer = DispatchOptimizer()

calculator = RevenueCalculator()

# =========================
# 初始机组出力
# =========================

current_power = MIN_POWER

# =========================
# 保存结果
# =========================

target_power_list = []

actual_power_list = []

revenue_list = []

cost_list = []

profit_list = []

# =========================
# 回测循环
# =========================

for idx, row in df.iterrows():

    # -------------------------
    # 预测价格（模型输出）
    # -------------------------

    pred_price = row["pred_price"]

    # -------------------------
    # 真实市场价格（最终结算）
    # -------------------------

    market_price = row["real_price"]

    # -------------------------
    # 1. 跟价策略
    # -------------------------

    target_power = strategy.get_target_power(
        pred_price
    )

    # -------------------------
    # 2. 爬坡约束优化
    # -------------------------

    actual_power = optimizer.optimize(
        current_power=current_power,
        target_power=target_power
    )

    # -------------------------
    # 3. 收益计算
    # -------------------------

    revenue = calculator.calculate_revenue(
        market_price=market_price,
        power=actual_power
    )

    cost = calculator.calculate_cost(
        power=actual_power
    )

    profit = calculator.calculate_profit(
        market_price=market_price,
        power=actual_power
    )

    # -------------------------
    # 保存结果
    # -------------------------

    target_power_list.append(
        target_power
    )

    actual_power_list.append(
        actual_power
    )

    revenue_list.append(
        revenue
    )

    cost_list.append(
        cost
    )

    profit_list.append(
        profit
    )

    # 更新当前出力
    current_power = actual_power

# =========================
# 保存结果到DataFrame
# =========================

df["target_power"] = target_power_list

df["actual_power"] = actual_power_list

df["revenue"] = revenue_list

df["cost"] = cost_list

df["profit"] = profit_list

# =========================
# 总体统计
# =========================

print("\n========== Strategy Backtest ==========\n")

print(
    f"Total Revenue: "
    f"{df['revenue'].sum():,.2f} 元"
)

print(
    f"Total Cost: "
    f"{df['cost'].sum():,.2f} 元"
)

print(
    f"Total Profit: "
    f"{df['profit'].sum():,.2f} 元"
)

print(
    f"Average Power: "
    f"{df['actual_power'].mean():.2f} MW"
)

print(
    f"Max Power: "
    f"{df['actual_power'].max():.2f} MW"
)

print(
    f"Min Power: "
    f"{df['actual_power'].min():.2f} MW"
)

# =========================
# 每日经营统计
# =========================

daily_summary = (
    df.groupby("date")
    .agg({
        "revenue": "sum",
        "cost": "sum",
        "profit": "sum",
        "actual_power": "mean"
    })
    .reset_index()
)

daily_summary.columns = [
    "date",
    "daily_revenue",
    "daily_cost",
    "daily_profit",
    "avg_power"
]

print("\n========== Daily Summary ==========\n")

print(daily_summary)

# =========================
# 保存详细回测结果
# =========================

detail_output_path = (
    "output/strategy_backtest_result.csv"
)

df.to_csv(
    detail_output_path,
    index=False
)

print(
    f"\n详细回测结果已保存："
    f"{detail_output_path}"
)

# =========================
# 保存每日经营结果
# =========================

daily_output_path = (
    "output/daily_strategy_summary.csv"
)

daily_summary.to_csv(
    daily_output_path,
    index=False
)

print(
    f"\n每日经营结果已保存："
    f"{daily_output_path}"
)
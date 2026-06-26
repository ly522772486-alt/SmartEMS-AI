import os
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

from src.config.unit_config import MIN_POWER
from src.dataset.dataset_builder import DatasetBuilder
from src.feature_engineering.feature_engineering import FeatureEngineering
from src.models.tree.lightgbm import LightGBMModel
from src.models.tree.randomforest import RandomForestModel
from src.models.tree.xgboost import XGBoostModel
from src.strategy.dispatch_optimizer import DispatchOptimizer
from src.strategy.price_follow_strategy import PriceFollowStrategy
from src.strategy.revenue_calculator import RevenueCalculator


APP_TITLE = "SmartEMS-AI 智能能源管理电价预测与调度优化平台"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw" / "origin_dataset"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "models"
PREDICTION_DIR = PROJECT_ROOT / "data" / "output"
BACKTEST_DIR = PROJECT_ROOT / "output"

FEATURE_COLUMNS = [
    "price_lag_1",
    "price_lag_4",
    "price_lag_96",
    "power_lag_1",
    "revenue_lag_1",
    "price_rolling_mean_4",
    "price_rolling_std_4",
    "price_diff_1",
    "hour",
    "weekday",
]


def ensure_project_cwd():
    os.chdir(PROJECT_ROOT)


def list_raw_excel_files():
    return sorted(RAW_DATA_DIR.glob("*.xlsx"))


def load_prediction_files():
    return sorted(PREDICTION_DIR.glob("*prediction_result.csv"))


def load_csv(path, parse_datetime=False):
    path = Path(path)
    if parse_datetime:
        preview = pd.read_csv(path, nrows=1)
        if "datetime" in preview.columns:
            return pd.read_csv(path, index_col="datetime", parse_dates=True)
    return pd.read_csv(path)


def preview_excel_file(path, rows=30):
    return pd.read_excel(path, nrows=rows)


def get_file_status():
    return {
        "raw_count": len(list_raw_excel_files()),
        "merged_exists": (PROCESSED_DATA_DIR / "merged_dataset.csv").exists(),
        "feature_exists": (PROCESSED_DATA_DIR / "feature_dataset.csv").exists(),
        "prediction_count": len(load_prediction_files()),
        "backtest_exists": (BACKTEST_DIR / "strategy_backtest_result.csv").exists(),
    }


def build_multi_day_dataset(unit_name):
    ensure_project_cwd()
    return DatasetBuilder.build_multi_day_dataset(
        folder_path=RAW_DATA_DIR,
        unit_name=unit_name,
    )


def build_feature_dataset():
    ensure_project_cwd()
    merged_path = PROCESSED_DATA_DIR / "merged_dataset.csv"
    df = pd.read_csv(
        merged_path,
        index_col="datetime",
        parse_dates=True,
    )

    feature_df = FeatureEngineering.build_features(df)
    feature_df = feature_df.dropna()

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    feature_path = PROCESSED_DATA_DIR / "feature_dataset.csv"
    feature_df.to_csv(feature_path, encoding="utf-8-sig")
    return feature_df


def _build_model(model_name):
    if model_name == "RandomForest":
        return RandomForestModel.build_model()
    if model_name == "LightGBM":
        return LightGBMModel.build_model()
    if model_name == "XGBoost":
        return None
    raise ValueError(f"Unsupported model: {model_name}")


def train_price_model(model_name, test_size=0.2, save_model=True):
    ensure_project_cwd()
    feature_path = PROCESSED_DATA_DIR / "feature_dataset.csv"
    df = pd.read_csv(
        feature_path,
        index_col="datetime",
        parse_dates=True,
    )

    missing_columns = [column for column in FEATURE_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Feature dataset missing columns: {missing_columns}")

    df["target_price"] = df["price"].shift(-1)
    df = df.dropna()

    X = df[FEATURE_COLUMNS]
    y = df["target_price"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        shuffle=False,
    )

    if model_name == "XGBoost":
        model = XGBoostModel.train(X_train, y_train)
        pred = XGBoostModel.predict(model, X_test)
    else:
        model = _build_model(model_name)
        model.fit(X_train, y_train)
        pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, pred)
    rmse = mean_squared_error(y_test, pred) ** 0.5

    result_df = pd.DataFrame(
        {
            "real_price": y_test,
            "pred_price": pred,
        },
        index=y_test.index,
    )
    result_df.index.name = "datetime"

    PREDICTION_DIR.mkdir(parents=True, exist_ok=True)
    result_path = PREDICTION_DIR / f"{model_name.lower()}_prediction_result.csv"
    result_df.to_csv(result_path, encoding="utf-8-sig")

    model_path = None
    if save_model:
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        model_path = MODEL_DIR / f"{model_name.lower()}.pkl"
        joblib.dump(model, model_path)

    return {
        "model_name": model_name,
        "mae": mae,
        "rmse": rmse,
        "train_size": len(X_train),
        "test_size": len(X_test),
        "result_df": result_df,
        "result_path": result_path,
        "model_path": model_path,
    }


def run_strategy_backtest(prediction_path, initial_power=MIN_POWER):
    ensure_project_cwd()
    df = load_csv(prediction_path, parse_datetime=True).copy()

    if not {"real_price", "pred_price"}.issubset(df.columns):
        raise ValueError("Prediction file must contain real_price and pred_price columns.")

    if "datetime" not in df.columns:
        if isinstance(df.index, pd.DatetimeIndex):
            df["datetime"] = df.index
        else:
            df["datetime"] = pd.to_datetime(df.index)

    df["datetime"] = pd.to_datetime(df["datetime"])
    df["date"] = df["datetime"].dt.date

    strategy = PriceFollowStrategy()
    optimizer = DispatchOptimizer()
    calculator = RevenueCalculator()

    current_power = initial_power
    target_power_list = []
    actual_power_list = []
    revenue_list = []
    cost_list = []
    profit_list = []

    for _, row in df.iterrows():
        target_power = strategy.get_target_power(row["pred_price"])
        actual_power = optimizer.optimize(
            current_power=current_power,
            target_power=target_power,
        )
        revenue = calculator.calculate_revenue(row["real_price"], actual_power)
        cost = calculator.calculate_cost(actual_power)
        profit = calculator.calculate_profit(row["real_price"], actual_power)

        target_power_list.append(target_power)
        actual_power_list.append(actual_power)
        revenue_list.append(revenue)
        cost_list.append(cost)
        profit_list.append(profit)
        current_power = actual_power

    df["target_power"] = target_power_list
    df["actual_power"] = actual_power_list
    df["revenue"] = revenue_list
    df["cost"] = cost_list
    df["profit"] = profit_list

    daily_df = (
        df.groupby("date")
        .agg(
            daily_revenue=("revenue", "sum"),
            daily_cost=("cost", "sum"),
            daily_profit=("profit", "sum"),
            avg_power=("actual_power", "mean"),
        )
        .reset_index()
    )

    BACKTEST_DIR.mkdir(parents=True, exist_ok=True)
    detail_path = BACKTEST_DIR / "strategy_backtest_result.csv"
    daily_path = BACKTEST_DIR / "daily_strategy_summary.csv"
    df.to_csv(detail_path, index=False, encoding="utf-8-sig")
    daily_df.to_csv(daily_path, index=False, encoding="utf-8-sig")

    return {
        "detail_df": df,
        "daily_df": daily_df,
        "detail_path": detail_path,
        "daily_path": daily_path,
        "summary": {
            "total_revenue": df["revenue"].sum(),
            "total_cost": df["cost"].sum(),
            "total_profit": df["profit"].sum(),
            "avg_power": df["actual_power"].mean(),
            "max_power": df["actual_power"].max(),
            "min_power": df["actual_power"].min(),
        },
    }

import sys
from pathlib import Path


project_root = Path(__file__).resolve().parents[2]

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.analysis.preprocess import DataPreprocessor
from src.analysis.revenue_analysis import RevenueAnalyzer
from src.utils.data_loader import DataLoader


def build_unit_summary(filename="01日偏差分析.xlsx", unit_name="华北.昱光/20kV.3#机组"):
    """Return a lightweight summary payload for one unit."""

    raw_df = DataLoader().load_excel(filename)
    unit_df = DataPreprocessor.extract_unit_data(raw_df, unit_name)
    ts_df = DataPreprocessor.build_unit_timeseries(unit_df)
    ts_df = RevenueAnalyzer.calculate_revenue(ts_df)

    return {
        "unit_name": unit_name,
        "points": len(ts_df),
        "average_price": float(ts_df["price"].mean()),
        "total_energy_mwh": float((ts_df["power"] * 0.25).sum()),
        "total_revenue": float(ts_df["revenue"].sum()),
    }


if __name__ == "__main__":
    print(build_unit_summary())

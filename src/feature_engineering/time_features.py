import pandas as pd


class TimeFeatures:
    """Time-derived features for 96-point daily market data."""

    @staticmethod
    def add_hour(df):
        result = df.copy()
        normalized_time = (
            result["time"]
            .astype(str)
            .str.strip()
            .str.replace("24:00", "00:00", regex=False)
        )
        time_dt = pd.to_datetime(normalized_time, format="%H:%M", errors="coerce")
        result["hour"] = time_dt.dt.hour

        return result

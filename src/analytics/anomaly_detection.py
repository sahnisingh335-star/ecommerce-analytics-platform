
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "reports" / "monthly_sales_trends.csv"
OUTPUT = ROOT / "reports" / "sales_anomalies.csv"


def main():
    print("STARTING SALES ANOMALY DETECTION")

    if not INPUT.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT}"
        )

    df = pd.read_csv(INPUT)
    df["month"] = pd.to_datetime(
        df["month"], errors="coerce"
    )
    df["total_revenue"] = pd.to_numeric(
        df["total_revenue"], errors="coerce"
    )

    df = df.dropna(
        subset=["month", "total_revenue"]
    ).sort_values("month").reset_index(drop=True)

    # Incomplete months are already removed in time_series.py,
    # so every month in the input is a full month.

    # Compare each month against the previous 6 months.
    df["baseline_avg"] = (
        df["total_revenue"]
        .shift(1)
        .rolling(window=6, min_periods=3)
        .mean()
    )

    df["baseline_std"] = (
        df["total_revenue"]
        .shift(1)
        .rolling(window=6, min_periods=3)
        .std()
    )

    df["deviation_pct"] = (
        (df["total_revenue"] - df["baseline_avg"])
        / df["baseline_avg"].where(
            df["baseline_avg"] != 0
        )
        * 100
    ).round(2)

    df["anomaly_score"] = (
        (df["total_revenue"] - df["baseline_avg"])
        / df["baseline_std"].where(
            df["baseline_std"] != 0
        )
    )

    df["anomaly_status"] = "Normal"

    # Flag unusually high or low monthly revenue.
    df.loc[
        df["anomaly_score"] > 2,
        "anomaly_status"
    ] = "Unusually High"

    df.loc[
        df["anomaly_score"] < -2,
        "anomaly_status"
    ] = "Unusually Low"

    ROOT.joinpath("reports").mkdir(
        parents=True, exist_ok=True
    )

    df.to_csv(OUTPUT, index=False)

    print("\nANALYSIS COMPLETE")
    print(df[[
        "month",
        "total_revenue",
        "baseline_avg",
        "deviation_pct",
        "anomaly_status"
    ]].tail(12).to_string(index=False))

    print(f"\nReport saved: {OUTPUT}")


if __name__ == "__main__":
    main()

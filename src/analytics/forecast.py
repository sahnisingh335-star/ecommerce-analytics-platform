"""Sales forecasting: predict the next 3 months of revenue.

Three simple models are tested on the last 6 known months (backtest).
The model with the lowest error (MAPE) is used for the real forecast.
Output: reports/sales_forecast.csv
Run:  python src/analytics/forecast.py
"""
from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
SRC = BASE_DIR / "reports" / "monthly_sales_trends.csv"
OUT = BASE_DIR / "reports" / "sales_forecast.csv"
HORIZON, TEST = 3, 6


def moving_avg(y, h, window=3):
    return np.repeat(y[-window:].mean(), h)


def linear_trend(y, h):
    x = np.arange(len(y))
    slope, intercept = np.polyfit(x, y, 1)
    return intercept + slope * np.arange(len(y), len(y) + h)


def holt(y, h):
    """Holt's linear exponential smoothing; alpha/beta picked by lowest training error."""
    best = None
    for a in np.arange(0.1, 1.0, 0.1):
        for b in np.arange(0.1, 1.0, 0.1):
            level, trend, err = y[0], y[1] - y[0], 0.0
            for v in y[1:]:
                err += (v - (level + trend)) ** 2
                new_level = a * v + (1 - a) * (level + trend)
                trend = b * (new_level - level) + (1 - b) * trend
                level = new_level
            if best is None or err < best[0]:
                best = (err, level, trend)
    _, level, trend = best
    return level + trend * np.arange(1, h + 1)


MODELS = {"3-month moving average": moving_avg,
          "Linear trend": linear_trend,
          "Holt exponential smoothing": holt}


def mape(actual, pred):
    return float(np.mean(np.abs((actual - pred) / actual)) * 100)


def main():
    df = pd.read_csv(SRC)
    df = df[df["month"] < "2026-10"]  # drop the 1-day October 2026
    y = df["total_revenue"].to_numpy(dtype=float)
    months = pd.PeriodIndex(df["month"], freq="M")

    # Backtest: hide the last 6 months, forecast them, compare with the real values
    scores = {name: mape(y[-TEST:], fn(y[:-TEST], TEST)) for name, fn in MODELS.items()}
    best = min(scores, key=scores.get)
    print("Backtest error (MAPE, lower is better):")
    for name, s in scores.items():
        print(f"  {name}: {s:.1f}%")
    print(f"Best model: {best}")

    # Real forecast with the best model; band = typical backtest error
    pred = MODELS[best](y, HORIZON)
    resid = y[-TEST:] - MODELS[best](y[:-TEST], TEST)
    band = 1.28 * resid.std()  # about an 80% range
    future = pd.period_range(months[-1] + 1, periods=HORIZON, freq="M")
    out = pd.DataFrame({
        "month": future.astype(str),
        "forecast_revenue": pred.round(0),
        "lower_80": (pred - band).round(0),
        "upper_80": (pred + band).round(0),
        "model": best,
        "backtest_mape_pct": round(scores[best], 1),
    })
    out.to_csv(OUT, index=False)
    print(out.to_string(index=False))
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()

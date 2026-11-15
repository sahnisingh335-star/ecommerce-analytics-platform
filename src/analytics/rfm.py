
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

ORDERS_FILE = BASE_DIR / "data" / "cleaned" / "orders.csv"
OUTPUT_DIR = BASE_DIR / "reports"
OUTPUT_FILE = OUTPUT_DIR / "rfm_customer_segments.csv"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    orders = pd.read_csv(ORDERS_FILE)

    # Use completed orders only
    orders["order_date"] = pd.to_datetime(
        orders["order_date"], errors="coerce"
    )

    orders = orders[
        orders["status"].astype(str).str.lower() == "completed"
    ].dropna(subset=["customer_id", "order_date"])

    if orders.empty:
        raise ValueError("No completed orders found.")

    # Calculate revenue from cleaned order items
    items = pd.read_csv(
        BASE_DIR / "data" / "cleaned" / "order_items.csv"
    )

    items["net_revenue"] = (
        items["quantity"]
        * items["unit_price"]
        * (1 - items["discount_pct"] / 100)
    )

    order_revenue = items.groupby("order_id")[
        "net_revenue"
    ].sum()

    orders["order_id"] = pd.to_numeric(
        orders["order_id"], errors="coerce"
    )
    orders = orders.dropna(subset=["order_id"])
    orders["order_id"] = orders["order_id"].astype(int)

    orders["revenue"] = orders["order_id"].map(
        order_revenue
    ).fillna(0)

    # Snapshot date = day after the latest order in the dataset
    snapshot_date = orders["order_date"].max() + pd.Timedelta(days=1)

    rfm = orders.groupby("customer_id").agg(
        last_order_date=("order_date", "max"),
        frequency=("order_id", "nunique"),
        monetary=("revenue", "sum"),
    )

    rfm["recency"] = (
        snapshot_date - rfm["last_order_date"]
    ).dt.days

    # Score 1-5; higher is better
    rfm["R_score"] = pd.qcut(
        rfm["recency"].rank(method="first"),
        5, labels=[5, 4, 3, 2, 1]
    ).astype(int)

    rfm["F_score"] = pd.qcut(
        rfm["frequency"].rank(method="first"),
        5, labels=[1, 2, 3, 4, 5]
    ).astype(int)

    rfm["M_score"] = pd.qcut(
        rfm["monetary"].rank(method="first"),
        5, labels=[1, 2, 3, 4, 5]
    ).astype(int)

    rfm["RFM_score"] = (
        rfm["R_score"].astype(str)
        + rfm["F_score"].astype(str)
        + rfm["M_score"].astype(str)
    )

    def segment_customer(row):
        if row["R_score"] >= 4 and row["F_score"] >= 4:
            return "Champions"
        elif row["F_score"] >= 4 and row["R_score"] >= 2:
            return "Loyal Customers"
        elif row["R_score"] >= 4 and row["F_score"] <= 2:
            return "New / Potential Loyalists"
        elif row["R_score"] <= 2 and row["F_score"] >= 3:
            return "At Risk"
        elif row["R_score"] <= 2 and row["F_score"] <= 2:
            return "Lost Customers"
        else:
            return "Needs Attention"

    rfm["segment"] = rfm.apply(segment_customer, axis=1)

    rfm = rfm.reset_index()
    rfm.to_csv(OUTPUT_FILE, index=False)

    print("=" * 50)
    print("RFM ANALYSIS COMPLETED")
    print("=" * 50)
    print(f"Customers analyzed: {len(rfm):,}")
    print(f"Snapshot date: {snapshot_date.date()}")
    print("\nCustomer segments:")
    print(rfm["segment"].value_counts().to_string())
    print(f"\nSaved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

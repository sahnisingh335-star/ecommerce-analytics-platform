
from pathlib import Path
import pandas as pd


# ==================================================
# 1. PROJECT PATHS
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ORDERS_FILE = PROJECT_ROOT / "data" / "cleaned" / "orders.csv"
ITEMS_FILE = PROJECT_ROOT / "data" / "cleaned" / "order_items.csv"

REPORTS_DIR = PROJECT_ROOT / "reports"

OUTPUT_FILE = REPORTS_DIR / "monthly_sales_trends.csv"


# ==================================================
# 2. TIME-SERIES ANALYSIS
# ==================================================

def main():

    print("=" * 60)
    print("E-COMMERCE TIME-SERIES ANALYSIS")
    print("=" * 60)

    # --------------------------------------------------
    # STEP 1: CHECK INPUT FILES
    # --------------------------------------------------

    if not ORDERS_FILE.exists():
        raise FileNotFoundError(
            f"Orders file not found: {ORDERS_FILE}"
        )

    if not ITEMS_FILE.exists():
        raise FileNotFoundError(
            f"Order items file not found: {ITEMS_FILE}"
        )

    # --------------------------------------------------
    # STEP 2: LOAD DATA
    # --------------------------------------------------

    orders = pd.read_csv(ORDERS_FILE)
    items = pd.read_csv(ITEMS_FILE)

    print(f"\nTotal orders loaded: {len(orders):,}")
    print(f"Total order items loaded: {len(items):,}")

    required_order_columns = {
        "order_id",
        "order_date",
        "status"
    }

    required_item_columns = {
        "order_id",
        "quantity",
        "unit_price",
        "discount_pct"
    }

    missing_order_columns = (
        required_order_columns - set(orders.columns)
    )

    missing_item_columns = (
        required_item_columns - set(items.columns)
    )

    if missing_order_columns:
        raise ValueError(
            f"Missing order columns: {missing_order_columns}"
        )

    if missing_item_columns:
        raise ValueError(
            f"Missing order item columns: {missing_item_columns}"
        )

    # --------------------------------------------------
    # STEP 3: CLEAN REQUIRED DATA TYPES
    # --------------------------------------------------

    orders["order_date"] = pd.to_datetime(
        orders["order_date"],
        errors="coerce"
    )

    orders["status"] = (
        orders["status"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    for column in [
        "quantity",
        "unit_price",
        "discount_pct"
    ]:
        items[column] = pd.to_numeric(
            items[column],
            errors="coerce"
        )

    # --------------------------------------------------
    # STEP 4: FILTER COMPLETED ORDERS
    # --------------------------------------------------

    completed_orders = orders[
        (orders["status"] == "completed")
        & orders["order_date"].notna()
        & orders["order_id"].notna()
    ].copy()

    if completed_orders.empty:
        raise ValueError(
            "No valid completed orders found."
        )

    # Drop the last month if it is incomplete (data ends before
    # that month's last day, e.g. only 1 Oct 2026). An incomplete
    # month would show a fake -98% revenue drop.
    last_date = orders["order_date"].max()

    if last_date != last_date + pd.offsets.MonthEnd(0):

        partial_start = last_date.to_period("M").to_timestamp()

        dropped = (
            completed_orders["order_date"] >= partial_start
        ).sum()

        completed_orders = completed_orders[
            completed_orders["order_date"] < partial_start
        ].copy()

        print(
            f"Incomplete month {partial_start:%Y-%m} excluded "
            f"({dropped} completed orders)"
        )

    print(
        "Completed orders used:",
        f"{len(completed_orders):,}"
    )

    # --------------------------------------------------
    # STEP 5: CALCULATE ITEM REVENUE
    # --------------------------------------------------

    # Net revenue = quantity * unit price
    #               * (1 - discount percentage / 100)

    items["item_revenue"] = (
        items["quantity"]
        * items["unit_price"]
        * (1 - items["discount_pct"] / 100)
    )

    # Keep only valid numeric revenue values
    valid_items = items[
        items["item_revenue"].notna()
        & items["item_revenue"].ge(0)
    ].copy()

    # Sum item revenue for each order
    order_revenue = (
        valid_items.groupby("order_id")["item_revenue"]
        .sum()
        .reset_index(name="revenue")
    )

    # --------------------------------------------------
    # STEP 6: JOIN ORDERS WITH REVENUE
    # --------------------------------------------------

    sales = completed_orders.merge(
        order_revenue,
        on="order_id",
        how="left",
        validate="one_to_one"
    )

    # Orders without valid item revenue are set to zero
    sales["revenue"] = sales["revenue"].fillna(0)

    # --------------------------------------------------
    # STEP 7: AGGREGATE MONTHLY METRICS
    # --------------------------------------------------

    sales["month"] = (
        sales["order_date"].dt.to_period("M").astype(str)
    )

    monthly = (
        sales.groupby("month")
        .agg(
            total_revenue=("revenue", "sum"),
            completed_orders=("order_id", "nunique"),
            average_order_value=("revenue", "mean")
        )
        .reset_index()
        .sort_values("month")
        .reset_index(drop=True)
    )

    # --------------------------------------------------
    # STEP 8: CALCULATE MONTH-OVER-MONTH GROWTH
    # --------------------------------------------------

    monthly["previous_month_revenue"] = (
        monthly["total_revenue"].shift(1)
    )

    monthly["revenue_change"] = (
        monthly["total_revenue"]
        - monthly["previous_month_revenue"]
    )

    monthly["revenue_growth_pct"] = (
        monthly["total_revenue"]
        .div(monthly["previous_month_revenue"].where(
            monthly["previous_month_revenue"] != 0
        ))
        .sub(1)
        .mul(100)
        .round(2)
    )

    # First month has no previous month for comparison
    monthly["revenue_change"] = (
        monthly["revenue_change"].round(2)
    )

    # --------------------------------------------------
    # STEP 9: CALCULATE MOVING AVERAGES
    # --------------------------------------------------

    # Current month + previous 2 months
    monthly["revenue_3_month_avg"] = (
        monthly["total_revenue"]
        .rolling(window=3, min_periods=3)
        .mean()
        .round(2)
    )

    # Current month + previous 5 months
    monthly["revenue_6_month_avg"] = (
        monthly["total_revenue"]
        .rolling(window=6, min_periods=6)
        .mean()
        .round(2)
    )

    # --------------------------------------------------
    # STEP 10: ADD ADDITIONAL BUSINESS METRICS
    # --------------------------------------------------

    monthly["total_revenue"] = (
        monthly["total_revenue"].round(2)
    )

    monthly["average_order_value"] = (
        monthly["average_order_value"].round(2)
    )

    monthly["revenue_change"] = (
        monthly["revenue_change"].round(2)
    )

    # --------------------------------------------------
    # STEP 11: SAVE REPORT
    # --------------------------------------------------

    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    monthly.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # --------------------------------------------------
    # STEP 12: DISPLAY RESULTS
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("TIME-SERIES ANALYSIS COMPLETED")
    print("=" * 60)

    print(f"\nMonths analyzed: {len(monthly)}")

    print("\nMonthly sales results:")

    print(
        monthly.tail(12).to_string(index=False)
    )

    print("\nReport saved successfully:")
    print(OUTPUT_FILE)

    print("\nSUCCESS: Time-series report generated!")


# ==================================================
# 3. RUN PROGRAM
# ==================================================

if __name__ == "__main__":
    main()

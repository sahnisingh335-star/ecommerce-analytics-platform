
from pathlib import Path
import pandas as pd


# ==================================================
# 1. PROJECT PATHS
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ORDERS_FILE = PROJECT_ROOT / "data" / "cleaned" / "orders.csv"
REPORTS_DIR = PROJECT_ROOT / "reports"

LONG_REPORT = REPORTS_DIR / "cohort_retention.csv"
MATRIX_REPORT = REPORTS_DIR / "cohort_retention_matrix.csv"


# ==================================================
# 2. COHORT RETENTION ANALYSIS
# ==================================================

def main():

    print("=" * 60)
    print("CUSTOMER COHORT RETENTION ANALYSIS")
    print("=" * 60)

    # --------------------------------------------------
    # STEP 1: CHECK AND LOAD DATA
    # --------------------------------------------------

    if not ORDERS_FILE.exists():
        raise FileNotFoundError(
            f"Orders file not found: {ORDERS_FILE}"
        )

    orders = pd.read_csv(ORDERS_FILE)

    required_columns = {
        "order_id",
        "customer_id",
        "order_date",
        "status"
    }

    missing_columns = required_columns - set(orders.columns)

    if missing_columns:
        raise ValueError(
            f"Missing columns in orders.csv: {missing_columns}"
        )

    print(f"\nTotal order records: {len(orders):,}")

    # --------------------------------------------------
    # STEP 2: CLEAN REQUIRED COLUMNS
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

    # Drop an incomplete final month (data ends on 1 Oct 2026),
    # same rule as SQL Q12 and time_series.py
    last_date = orders["order_date"].max()

    if last_date != last_date + pd.offsets.MonthEnd(0):
        partial_start = last_date.to_period("M").to_timestamp()
        orders = orders[orders["order_date"] < partial_start].copy()
        print(f"Incomplete month {partial_start:%Y-%m} excluded")

    # Use completed orders only
    orders = orders[
        (orders["status"] == "completed")
        & orders["customer_id"].notna()
        & orders["order_date"].notna()
    ].copy()

    if orders.empty:
        raise ValueError(
            "No valid completed orders found."
        )

    print(f"Completed orders: {len(orders):,}")

    # --------------------------------------------------
    # STEP 3: IDENTIFY EACH ORDER'S MONTH
    # --------------------------------------------------

    orders["order_month"] = (
        orders["order_date"].dt.to_period("M")
    )

    # Find each customer's first completed order month
    first_purchase = (
        orders.groupby("customer_id")["order_month"]
        .min()
    )

    orders["cohort_month"] = (
        orders["customer_id"].map(first_purchase)
    )

    print(
        "Unique customers:",
        f"{orders['customer_id'].nunique():,}"
    )

    # --------------------------------------------------
    # STEP 4: CALCULATE COHORT INDEX
    # --------------------------------------------------

    orders["cohort_index"] = (
        (orders["order_month"].dt.year
         - orders["cohort_month"].dt.year) * 12
        + orders["order_month"].dt.month
        - orders["cohort_month"].dt.month
    )

    # Cohort index:
    # 0 = first purchase month
    # 1 = one month after first purchase
    # 2 = two months after first purchase

    # --------------------------------------------------
    # STEP 5: COUNT ACTIVE CUSTOMERS
    # --------------------------------------------------

    cohort_data = (
        orders.groupby(
            ["cohort_month", "cohort_index"]
        )["customer_id"]
        .nunique()
        .reset_index(name="active_customers")
    )

    # Count the original customers in each cohort
    cohort_sizes = (
        cohort_data[
            cohort_data["cohort_index"] == 0
        ][["cohort_month", "active_customers"]]
        .rename(
            columns={
                "active_customers": "cohort_size"
            }
        )
    )

    cohort_data = cohort_data.merge(
        cohort_sizes,
        on="cohort_month",
        how="left"
    )

    # --------------------------------------------------
    # STEP 6: CALCULATE RETENTION PERCENTAGE
    # --------------------------------------------------

    cohort_data["retention_pct"] = (
        cohort_data["active_customers"]
        / cohort_data["cohort_size"]
        * 100
    ).round(2)

    # --------------------------------------------------
    # STEP 7: FORMAT AND SORT RESULTS
    # --------------------------------------------------

    cohort_data["cohort_month"] = (
        cohort_data["cohort_month"].astype(str)
    )

    cohort_data = cohort_data.sort_values(
        ["cohort_month", "cohort_index"]
    ).reset_index(drop=True)

    # --------------------------------------------------
    # STEP 8: CREATE RETENTION MATRIX
    # --------------------------------------------------

    retention_matrix = cohort_data.pivot(
        index="cohort_month",
        columns="cohort_index",
        values="retention_pct"
    )

    retention_matrix.columns = [
        f"Month_{int(month)}"
        for month in retention_matrix.columns
    ]

    retention_matrix = retention_matrix.reset_index()

    # --------------------------------------------------
    # STEP 9: SAVE CSV REPORTS
    # --------------------------------------------------

    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    cohort_data.to_csv(
        LONG_REPORT,
        index=False
    )

    retention_matrix.to_csv(
        MATRIX_REPORT,
        index=False
    )

    # --------------------------------------------------
    # STEP 10: DISPLAY SUMMARY
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("COHORT ANALYSIS COMPLETED")
    print("=" * 60)

    print(
        "\nTotal customer cohorts:",
        cohort_data["cohort_month"].nunique()
    )

    print(
        "Total customers analyzed:",
        f"{orders['customer_id'].nunique():,}"
    )

    print("\nRetention results preview:")

    print(
        cohort_data.head(15).to_string(index=False)
    )

    print("\nRetention matrix preview:")

    print(
        retention_matrix.head(10).to_string(index=False)
    )

    print("\nReports saved successfully:")
    print(f"1. {LONG_REPORT}")
    print(f"2. {MATRIX_REPORT}")

    print(
        "\nNote: Recent cohorts have fewer months "
        "of follow-up."
    )

    print(
        "Missing future months are not zero retention."
    )

    print("\nSUCCESS: Cohort reports generated!")


# ==================================================
# 11. RUN THE PROGRAM
# ==================================================

if __name__ == "__main__":
    main()

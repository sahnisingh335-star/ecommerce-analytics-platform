"""
Prepare clean, Power BI-ready CSV files in powerbi/data/.

Star schema (one fact table + dimension tables):

    dim_date ──┐
    dim_customers ──┤
    dim_products ───┼──> fact_sales  (one row per order item)
    dim_campaigns ──┘
    fact_payments, fact_returns -> linked by order_id / order_item_id

Plus ready-made analytics tables (monthly trends, RFM, cohort,
anomalies) and the key SQL results with clean dates.

Run:  python src/prepare_powerbi_data.py
"""

from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_DIR = BASE_DIR / "data" / "cleaned"
REPORTS_DIR = BASE_DIR / "reports"
SQL_DIR = REPORTS_DIR / "sql_results"
OUT_DIR = BASE_DIR / "powerbi" / "data"

OUT_DIR.mkdir(parents=True, exist_ok=True)


def load(name):
    return pd.read_csv(CLEAN_DIR / f"{name}.csv")


def save(df, name):
    df.to_csv(OUT_DIR / f"{name}.csv", index=False)
    print(f"  {name + '.csv':38s} {len(df):>8,} rows")


def clean_dates(df):
    """'2024-01-01 00:00:00+00:00' -> '2024-01-01' for any date-like column."""
    for col in df.columns:
        if df[col].dtype == object and df[col].astype(str).str.match(
            r"^\d{4}-\d{2}-\d{2}( 00:00:00.*)?$"
        ).all():
            df[col] = df[col].astype(str).str[:10]
    return df


print("=" * 60)
print("PREPARING POWER BI DATA")
print("=" * 60)

# ------------------------------------------------------------------
# Dimensions
# ------------------------------------------------------------------

print("\nDimension tables:")

dim_date = load("date_dimension").rename(columns={"date_id": "date"})
save(dim_date, "dim_date")

customers = load("customers")
save(customers, "dim_customers")

products = load("products").merge(
    load("categories"), on="category_id", how="left"
)
save(products, "dim_products")

campaigns = load("marketing_campaigns").rename(
    columns={"name": "campaign_name", "discount_pct": "campaign_discount_pct"}
)
save(campaigns, "dim_campaigns")

# ------------------------------------------------------------------
# Facts
# ------------------------------------------------------------------

print("\nFact tables:")

orders = load("orders")
items = load("order_items")

sales = items.merge(orders, on="order_id", how="left", validate="many_to_one")

sales["gross_amount"] = (sales["quantity"] * sales["unit_price"]).round(2)
sales["net_revenue"] = (
    sales["quantity"] * sales["unit_price"] * (1 - sales["discount_pct"] / 100)
).round(2)
sales["cost"] = (sales["quantity"] * sales["unit_cost"]).round(2)
sales["profit"] = (sales["net_revenue"] - sales["cost"]).round(2)

# Same rule as the SQL analysis: October 2026 has only 1 day of data
last_date = pd.to_datetime(sales["order_date"]).max()
sales["is_complete_month"] = (
    pd.to_datetime(sales["order_date"]).dt.to_period("M")
    < last_date.to_period("M")
) | (last_date == last_date + pd.offsets.MonthEnd(0))

campaign_id = sales["campaign_id"].astype("Int64")
sales["campaign_id"] = campaign_id

save(sales, "fact_sales")

save(load("payments"), "fact_payments")
save(load("returns"), "fact_returns")
save(load("inventory"), "fact_inventory")

# ------------------------------------------------------------------
# Analytics outputs
# ------------------------------------------------------------------

print("\nAnalytics tables:")

for name in [
    "monthly_sales_trends",
    "rfm_customer_segments",
    "cohort_retention_matrix",
    "sales_anomalies",
]:
    path = REPORTS_DIR / f"{name}.csv"
    if path.exists():
        save(clean_dates(pd.read_csv(path)), name)
    else:
        print(f"  MISSING: {path.name} (run the analytics scripts first)")

# ------------------------------------------------------------------
# Key SQL results with readable names
# ------------------------------------------------------------------

print("\nSQL result tables:")

sql_tables = {
    "q02": "sql_monthly_revenue",
    "q04": "sql_top_products",
    "q06": "sql_low_margin_categories",
    "q07": "sql_brand_share",
    "q08": "sql_aov_by_segment",
    "q09": "sql_repeat_purchase_rate",
    "q10": "sql_top10pct_customer_share",
    "q13": "sql_region_revenue",
    "q14": "sql_discount_bands",
    "q15": "sql_high_return_products",
    "q16": "sql_return_reasons",
    "q17": "sql_payment_methods",
    "q18": "sql_campaign_roi",
}

for prefix, name in sql_tables.items():
    files = sorted(SQL_DIR.glob(f"{prefix}_*.csv"))
    if files:
        save(clean_dates(pd.read_csv(files[0])), name)
    else:
        print(f"  MISSING: {prefix} result (run src/run_sql_analysis.py)")

# ------------------------------------------------------------------
# Quick checks
# ------------------------------------------------------------------

print("\nChecks:")

checks = {
    "Every sale has an order": sales["order_date"].notna().all(),
    "Every sale has a known product": sales["product_id"].isin(products["product_id"]).all(),
    "Every order's customer exists": sales["customer_id"].isin(customers["customer_id"]).all(),
    "Every order date is in dim_date": pd.to_datetime(sales["order_date"]).isin(pd.to_datetime(dim_date["date"])).all(),
    "No negative quantities": (sales["quantity"] > 0).all(),
}

all_ok = True
for label, ok in checks.items():
    print(f"  [{'OK' if ok else 'FAIL'}] {label}")
    all_ok = all_ok and bool(ok)

print()
print("SUCCESS: Power BI data ready in powerbi/data/" if all_ok else "Some checks FAILED - see above.")

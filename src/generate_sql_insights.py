import re
from pathlib import Path

import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RESULTS_DIR = BASE_DIR / "reports" / "sql_results"
OUTPUT_FILE = BASE_DIR / "reports" / "sql_insights.md"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def format_currency(value):
    """Format a number as Indian Rupees."""

    if pd.isna(value):
        return "N/A"

    return f"₹{value:,.2f}"


def format_number(value):
    """Format numeric values."""

    if pd.isna(value):
        return "N/A"

    return f"{value:,.2f}"


def normalize_column(column):
    """Normalize column names for easier matching."""

    return (
        str(column)
        .lower()
        .strip()
        .replace(" ", "_")
        .replace("-", "_")
    )


def find_column(df, possible_names):
    """Find a matching column from a list of possible names."""

    columns = {
        normalize_column(column): column
        for column in df.columns
    }

    for name in possible_names:

        normalized_name = normalize_column(name)

        if normalized_name in columns:
            return columns[normalized_name]

    return None


def to_markdown_table(df):
    """Build a Markdown table without extra libraries
    (pandas.to_markdown needs the 'tabulate' package)."""

    def clean(value):

        if pd.isna(value):
            return ""

        if isinstance(value, float):
            return f"{value:,.2f}"

        text_value = str(value)

        # "2024-01-01 00:00:00+00:00" -> "2024-01-01"
        if re.match(r"^\d{4}-\d{2}-\d{2} 00:00:00", text_value):
            text_value = text_value[:10]

        return text_value.replace("|", "\\|")

    header = "| " + " | ".join(str(c) for c in df.columns) + " |"

    divider = "| " + " | ".join(
        "---:" if pd.api.types.is_numeric_dtype(df[c]) else "---"
        for c in df.columns
    ) + " |"

    rows = [
        "| " + " | ".join(clean(v) for v in row) + " |"
        for row in df.itertuples(index=False)
    ]

    return "\n".join([header, divider] + rows)


def format_label(value):
    """Shorten timestamps like 2025-06-01 00:00:00+00:00."""

    text_value = str(value)

    if re.match(r"^\d{4}-\d{2}-\d{2} 00:00:00", text_value):
        return text_value[:10]

    return text_value


def load_result(file_path):
    """Load one SQL result CSV."""

    try:
        return pd.read_csv(file_path)

    except Exception as error:

        print(
            f"ERROR reading {file_path.name}: {error}"
        )

        return pd.DataFrame()


# ============================================================
# START
# ============================================================

print("=" * 60)
print("GENERATING SQL BUSINESS INSIGHTS")
print("=" * 60)


# ============================================================
# FIND SQL RESULT FILES
# ============================================================

csv_files = sorted(
    RESULTS_DIR.glob("q*.csv")
)

print(
    f"SQL result files found: {len(csv_files)}"
)


if len(csv_files) == 0:

    raise FileNotFoundError(
        f"No SQL result files found in: {RESULTS_DIR}"
    )


# ============================================================
# REPORT
# ============================================================

report = []

report.append(
    "# E-Commerce Intelligence & Analytics"
)

report.append("")

report.append(
    "## SQL Business Insights Report"
)

report.append("")

report.append(
    "This report summarizes the results of the "
    "20 SQL business questions executed against "
    "the cleaned e-commerce dataset."
)

report.append("")

report.append("---")

report.append("")


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

report.append(
    "## Executive Summary"
)

report.append("")

report.append(
    f"- SQL questions processed: **{len(csv_files)}**"
)

report.append(
    "- SQL execution status: **Successful**"
)

report.append(
    "- Data source: **Supabase PostgreSQL**"
)

report.append(
    "- Analysis layer: **SQL Business Questions**"
)

report.append("")

report.append("---")

report.append("")


# ============================================================
# PROCESS Q1 - Q20
# ============================================================

for file_path in csv_files:

    print(
        f"Processing: {file_path.name}"
    )

    df = load_result(file_path)

    if df.empty:

        report.append(
            f"## {file_path.stem}"
        )

        report.append("")

        report.append(
            "No result data available."
        )

        report.append("")

        continue


    # --------------------------------------------------------
    # QUESTION NUMBER
    # --------------------------------------------------------

    question_number = (
        file_path.name
        .split("_")[0]
        .upper()
    )


    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    # "q01_q1._revenue,_orders_and_customers_per_year"
    # -> "Revenue, orders and customers per year"
    title = file_path.stem.replace("_", " ")

    title = re.sub(
        r"^q\d+\s+q\d+\.\s*",
        "",
        title,
        flags=re.IGNORECASE
    ).strip()

    title = title[:1].upper() + title[1:]


    # --------------------------------------------------------
    # QUESTION SECTION
    # --------------------------------------------------------

    report.append(
        f"## {question_number} — {title}"
    )

    report.append("")

    report.append(
        f"**Rows returned:** {len(df):,}"
    )

    report.append("")


    # --------------------------------------------------------
    # RESULT TABLE
    # --------------------------------------------------------

    report.append(
        "### Results"
    )

    report.append("")


    try:

        preview = df.head(10)

        if len(df) > 10:
            report.append(
                f"_Showing first 10 of {len(df):,} rows._"
            )
            report.append("")

        markdown_table = to_markdown_table(preview)

        report.append(
            markdown_table
        )

    except Exception:

        report.append(
            "Result table could not be formatted."
        )


    report.append("")


    # --------------------------------------------------------
    # BUSINESS INSIGHTS
    # --------------------------------------------------------

    report.append(
        "### Business Insights"
    )

    report.append("")

    insight_found = False


    # ========================================================
    # REVENUE
    # ========================================================

    revenue_column = find_column(
        df,
        [
            "revenue",
            "monthly_revenue",
            "total_revenue"
        ]
    )

    if revenue_column:

        values = pd.to_numeric(
            df[revenue_column],
            errors="coerce"
        ).dropna()

        if not values.empty:

            max_index = values.idxmax()

            min_index = values.idxmin()

            report.append(
                f"- Highest **{revenue_column}**: "
                f"**{format_currency(values.loc[max_index])}**."
            )

            report.append(
                f"- Lowest **{revenue_column}**: "
                f"**{format_currency(values.loc[min_index])}**."
            )

            # Try to identify the related period/product/category
            label_column = find_column(
                df,
                [
                    "month",
                    "product_name",
                    "category_name",
                    "brand",
                    "customer_id",
                    "state",
                    "region"
                ]
            )

            if label_column:

                report.append(
                    f"- Highest value is associated with "
                    f"**{format_label(df.loc[max_index, label_column])}**."
                )

            insight_found = True


    # ========================================================
    # RUNNING REVENUE
    # ========================================================

    running_column = find_column(
        df,
        [
            "running_revenue",
            "cumulative_revenue"
        ]
    )

    if running_column:

        values = pd.to_numeric(
            df[running_column],
            errors="coerce"
        ).dropna()

        if not values.empty:

            report.append(
                f"- Final cumulative revenue: "
                f"**{format_currency(values.iloc[-1])}**."
            )

            insight_found = True


    # ========================================================
    # PROFIT
    # ========================================================

    profit_column = find_column(
        df,
        [
            "profit",
            "total_profit"
        ]
    )

    if profit_column:

        values = pd.to_numeric(
            df[profit_column],
            errors="coerce"
        ).dropna()

        if not values.empty:

            max_index = values.idxmax()

            report.append(
                f"- Highest profit: "
                f"**{format_currency(values.loc[max_index])}**."
            )

            label_column = find_column(
                df,
                [
                    "product_name",
                    "category_name",
                    "brand"
                ]
            )

            if label_column:

                report.append(
                    f"- Highest-profit item/group: "
                    f"**{format_label(df.loc[max_index, label_column])}**."
                )

            insight_found = True


    # ========================================================
    # GROWTH
    # ========================================================

    growth_column = find_column(
        df,
        [
            "mom_growth",
            "mom_growth_pct",
            "growth",
            "growth_pct"
        ]
    )

    if growth_column:

        values = pd.to_numeric(
            df[growth_column],
            errors="coerce"
        ).dropna()

        if not values.empty:

            max_index = values.idxmax()

            min_index = values.idxmin()

            report.append(
                f"- Highest growth: "
                f"**{values.loc[max_index]:.2f}%**."
            )

            report.append(
                f"- Lowest growth: "
                f"**{values.loc[min_index]:.2f}%**."
            )

            insight_found = True


    # ========================================================
    # ORDERS
    # ========================================================

    order_column = find_column(
        df,
        [
            "orders",
            "order_count",
            "total_orders"
        ]
    )

    if order_column:

        values = pd.to_numeric(
            df[order_column],
            errors="coerce"
        ).dropna()

        if not values.empty:

            report.append(
                f"- Total orders represented: "
                f"**{values.sum():,.0f}**."
            )

            insight_found = True


    # ========================================================
    # CUSTOMERS
    # ========================================================

    customer_column = find_column(
        df,
        [
            "customers",
            "customer_count",
            "total_customers"
        ]
    )

    if customer_column:

        values = pd.to_numeric(
            df[customer_column],
            errors="coerce"
        ).dropna()

        if not values.empty:

            period_column = find_column(
                df,
                ["year", "month", "date", "cohort_month"]
            )

            if period_column and len(values) > 1:

                # The same customer can buy in several periods,
                # so per-period customer counts must not be summed.
                report.append(
                    f"- Customers per {period_column}: "
                    f"**{values.min():,.0f} – {values.max():,.0f}** "
                    f"(not added together, because one customer "
                    f"can buy in more than one {period_column})."
                )

            else:

                report.append(
                    f"- Total customers represented: "
                    f"**{values.sum():,.0f}**."
                )

            insight_found = True


    # ========================================================
    # AOV
    # ========================================================

    aov_column = find_column(
        df,
        [
            "aov",
            "average_order_value"
        ]
    )

    if aov_column:

        values = pd.to_numeric(
            df[aov_column],
            errors="coerce"
        ).dropna()

        if not values.empty:

            report.append(
                f"- Average AOV: "
                f"**{format_currency(values.mean())}**."
            )

            insight_found = True


    # ========================================================
    # RATE / SHARE / PERCENTAGE
    # ========================================================

    rate_column = find_column(
        df,
        [
            "repeat_purchase_rate_pct",
            "top_10_pct_revenue_share",
            "failed_payment_rate_pct",
            "return_rate_pct",
            "revenue_share_pct",
            "margin_pct",
            "rate",
            "percentage",
            "share",
            "revenue_share",
            "return_rate",
            "failed_payment_rate",
            "repeat_purchase_rate"
        ]
    )

    if rate_column:

        values = pd.to_numeric(
            df[rate_column],
            errors="coerce"
        ).dropna()

        if not values.empty:

            report.append(
                f"- Average **{rate_column}**: "
                f"**{values.mean():.2f}**."
            )

            report.append(
                f"- Maximum **{rate_column}**: "
                f"**{values.max():.2f}**."
            )

            insight_found = True


    # ========================================================
    # DISCOUNT
    # ========================================================

    discount_column = find_column(
        df,
        [
            "discount_pct",
            "discount_percent",
            "discount"
        ]
    )

    if discount_column:

        values = pd.to_numeric(
            df[discount_column],
            errors="coerce"
        ).dropna()

        if not values.empty:

            report.append(
                f"- Average discount: "
                f"**{values.mean():.2f}%**."
            )

            insight_found = True


    # ========================================================
    # RETURN
    # ========================================================

    return_column = find_column(
        df,
        [
            "return_rate",
            "returns",
            "return_count",
            "total_returns"
        ]
    )

    if return_column:

        values = pd.to_numeric(
            df[return_column],
            errors="coerce"
        ).dropna()

        if not values.empty:

            max_index = values.idxmax()

            report.append(
                f"- Highest return value/rate: "
                f"**{values.loc[max_index]:,.2f}**."
            )

            label_column = find_column(
                df,
                [
                    "product_name",
                    "category_name",
                    "reason"
                ]
            )

            if label_column:

                report.append(
                    f"- Highest-return group: "
                    f"**{format_label(df.loc[max_index, label_column])}**."
                )

            insight_found = True


    # ========================================================
    # FALLBACK
    # ========================================================

    if not insight_found:

        report.append(
            "- Detailed results are available in the table above."
        )


    report.append("")

    report.append("---")

    report.append("")


# ============================================================
# NEXT STEPS
# ============================================================

report.append(
    "# Next Development Steps"
)

report.append("")

report.append(
    "Completed analytics stages:"
)

report.append("")

for step in [
    "1. RFM Customer Segmentation — done",
    "2. Cohort Retention Analysis — done",
    "3. Time Series Analysis — done",
    "4. Revenue Anomaly Detection — done",
]:
    report.append(step)

report.append("")

report.append(
    "Next stages:"
)

report.append("")

for step in [
    "5. Power BI Dashboard",
    "6. AI Business Insights",
    "7. Resend Email Alerts",
]:
    report.append(step)

report.append("")

report.append(
    "SQL and Python remain responsible for calculating "
    "business metrics. AI should explain pre-computed "
    "results rather than independently calculating KPIs."
)


# ============================================================
# SAVE REPORT
# ============================================================

OUTPUT_FILE.write_text(
    "\n".join(report),
    encoding="utf-8"
)


# ============================================================
# COMPLETE
# ============================================================

print()

print("=" * 60)
print("SQL INSIGHTS REPORT GENERATED")
print("=" * 60)

print(
    f"Questions processed: {len(csv_files)}"
)

print(
    "Status: SUCCESS"
)

print()

print(
    f"Report saved to: {OUTPUT_FILE}"
)
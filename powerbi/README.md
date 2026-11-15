# Power BI Dashboard Guide

All files for the dashboard are in `powerbi/data/`.
Rebuild them any time with:

```powershell
python src\prepare_powerbi_data.py
```

## 1. Files to import (Home → Get Data → Text/CSV)

| File | Type | What it holds |
|---|---|---|
| `fact_sales.csv` | Fact | One row per order item with `net_revenue`, `cost`, `profit`, order status, channel, region |
| `fact_payments.csv` | Fact | Payment method, status, amount (85 amounts are blank on purpose) |
| `fact_returns.csv` | Fact | Returns with reason and refund amount |
| `dim_date.csv` | Dimension | Calendar: year, quarter, month name, weekend flag |
| `dim_customers.csv` | Dimension | City, state, region, acquisition channel, gender |
| `dim_products.csv` | Dimension | Product, brand, category, list price |
| `dim_campaigns.csv` | Dimension | Campaign name, channel, budget |
| `rfm_customer_segments.csv` | Analytics | Customer segment (Champions, At Risk, ...) |
| `monthly_sales_trends.csv` | Analytics | Monthly revenue, orders, AOV, growth %, moving averages |
| `cohort_retention_matrix.csv` | Analytics | Retention % by cohort month |
| `sales_anomalies.csv` | Analytics | Unusually high / low revenue months |
| `sql_*.csv` | SQL results | Ready answers to the business questions |

After loading, set types: dates → **Date**, money → **Decimal number**,
IDs and counts → **Whole number**.

## 2. Relationships (Model view)

| From (many) | To (one) | Column |
|---|---|---|
| `fact_sales[order_date]` | `dim_date[date]` | date |
| `fact_sales[customer_id]` | `dim_customers[customer_id]` | customer |
| `fact_sales[product_id]` | `dim_products[product_id]` | product |
| `fact_sales[campaign_id]` | `dim_campaigns[campaign_id]` | campaign |
| `rfm_customer_segments[customer_id]` | `dim_customers[customer_id]` | segment (one-to-one) |

Keep filter direction **Single** (dimension → fact).

## 3. DAX measures (create in `fact_sales`)

```dax
Revenue =
CALCULATE (
    SUM ( fact_sales[net_revenue] ),
    fact_sales[status] = "Completed"
)

Profit =
CALCULATE (
    SUM ( fact_sales[profit] ),
    fact_sales[status] = "Completed"
)

Profit Margin % = DIVIDE ( [Profit], [Revenue] )

Orders =
CALCULATE (
    DISTINCTCOUNT ( fact_sales[order_id] ),
    fact_sales[status] = "Completed"
)

Avg Order Value = DIVIDE ( [Revenue], [Orders] )

Customers =
CALCULATE (
    DISTINCTCOUNT ( fact_sales[customer_id] ),
    fact_sales[status] = "Completed"
)

Revenue Prev Month =
CALCULATE ( [Revenue], DATEADD ( dim_date[date], -1, MONTH ) )

MoM Growth % = DIVIDE ( [Revenue] - [Revenue Prev Month], [Revenue Prev Month] )

Return Count = COUNTROWS ( fact_returns )
```

Add a page-level filter `fact_sales[is_complete_month] = True` so the
1-day October 2026 does not show a false drop. Mark `dim_date` as the
date table (Table tools → Mark as date table → `date`).

## 4. Suggested pages

1. **Overview:** KPI cards (Revenue, Profit, Orders, AOV, Customers),
   monthly revenue line, revenue by category bar, region map/bar.
2. **Products:** top products (`sql_top_products`), brand share,
   low-margin categories, discount bands.
3. **Customers:** RFM segment donut, AOV by segment, repeat rate,
   cohort retention heatmap (matrix + conditional formatting).
4. **Operations:** payment methods & failed rate, return reasons,
   high-return products, campaign ROI.
5. **Anomalies:** `sales_anomalies` line with `anomaly_status` as legend.

Slicers: year/month (`dim_date`), region (`dim_customers[region]`),
sales channel (`fact_sales[sales_channel]`), category (`dim_products[category_name]`).

Save the report as `powerbi/Ecommerce_Dashboard.pbix`.

---
name: powerbi-dashboard-builder
description: Step-by-step guide to build a Power BI dashboard for the E-Commerce Intelligence & Analytics project. Use when user wants to create visuals, DAX measures, KPI cards, slicers, relationships, or troubleshoot Power BI errors. Explains in simple Hinglish for beginners. Verifies file paths before suggesting imports. One small task at a time with confirmation.
---

# Power BI Dashboard Builder Skill

## Project Context

This skill is for the **E-Commerce Intelligence & Analytics** project at:
`C:\Users\shiva\E-Commerce-Intelligence-Analytics`

### Your Data Files (Ready to Import)

**Main Reports** (`reports/`):
- `monthly_sales_trends.csv` → Monthly revenue, orders, AOV, growth%, moving averages
- `rfm_customer_segments.csv` → Customer segments (Champions, Loyal, At Risk, etc.)
- `cohort_retention_matrix.csv` → Retention heatmap by cohort month
- `sales_anomalies.csv` → Unusual revenue months flagged

**SQL Results** (`reports/sql_results/` - 20 files):
- `q01_*` Yearly summary, `q02_*` Monthly revenue + MoM growth, `q03_*` Running total
- `q04_*` Top 10 products, `q05_*` Top 3 per category, `q06_*` Low margin categories
- `q07_*` Brand share, `q08_*` AOV by segment, `q09_*` Repeat purchase rate
- `q10_*` Top 10% customer share, `q11_*` Churn risk, `q12_*` Cohort retention
- `q13_*` Region revenue, `q14_*` Discount bands, `q15_*` High return products
- `q16_*` Return reasons, `q17_*` Payment methods, `q18_*` Campaign ROI
- `q19_*` Repeat timing, `q20_*` Revenue anomalies

**Cleaned Data** (`data/cleaned/`):
- `orders.csv`, `customers.csv`, `products.csv`, `categories.csv`, `marketing_campaigns.csv`

---

## How This Skill Works

**Rules I follow:**
1. **One small task at a time** - I give you ONE step, you confirm, then next
2. **Simple Hinglish** - Explain technical terms with examples (e.g., "DAX = Excel formulas on steroids")
3. **Verify first** - Never assume file imported; ask you to confirm
4. **Use your actual files** - Reference exact paths from your project
5. **Wait for approval** - No changes without your "yes" or "done"

**Your replies:**
- `"done"` or `"yes"` → Next step
- `"stuck"` + error/screenshot → I troubleshoot
- `"skip"` → Skip this visual/task
- Question → I clarify

---

## Phase 1: Import All Files (One by One)

### Task 1.1: Open Power BI Desktop
1. Launch **Power BI Desktop** from Start Menu
2. Close any startup window → blank canvas
3. Reply `"done"` when open

### Task 1.2: Import First File - Monthly Sales
1. **Home** tab → **Get Data** → **Text/CSV**
2. Navigate to: `C:\Users\shiva\E-Commerce-Intelligence-Analytics\reports\monthly_sales_trends.csv`
3. Click **Open** → Preview → **Load**
4. In **Fields** pane (right): Right-click table → **Rename** → `MonthlySales`
5. Reply `"done"` when loaded

### Task 1.3: Import RFM Segments
Same steps for: `reports\rfm_customer_segments.csv` → Rename to `RFM_Segments`
Reply `"done"`

### Task 1.4: Import Cohort Retention
`reports\cohort_retention_matrix.csv` → Rename to `CohortRetention`
Reply `"done"`

### Task 1.5: Import Sales Anomalies
`reports\sales_anomalies.csv` → Rename to `SalesAnomalies`
Reply `"done"`

### Task 1.6: Import SQL Results (Optional - 20 files)
We can import key ones only. Reply `"all"` to import all 20, or `"key"` for just 5 important ones:
- `q02_*` Monthly Revenue, `q04_*` Top Products, `q08_*` AOV by Segment, `q13_*` Region Revenue, `q18_*` Campaign ROI

### Task 1.7: Import Cleaned Data (For Slicers)
`data\cleaned\orders.csv` → `Orders`, `customers.csv` → `Customers`, `products.csv` → `Products`, `categories.csv` → `Categories`, `marketing_campaigns.csv` → `Campaigns`

---

## Phase 2: Fix Data Types

After each import, I'll ask you to fix types:
- `month` columns → **Date**
- Revenue/money columns → **Decimal Number**
- Count/ID columns → **Whole Number**

**How:** Click column in Fields → **Column tools** tab → **Data Type** dropdown

---

## Phase 3: Create Relationships (Model View)

Click **Model** icon (left sidebar, diagram icon). Drag to connect:

| From Table | Column | To Table | Column |
|------------|--------|----------|--------|
| `MonthlySales` | `month` | `SQL_MonthlyRevenue` | `month` |
| `Orders` | `customer_id` | `Customers` | `customer_id` |
| `Orders` | `order_id` | `Order_Items` | `order_id` |
| `Products` | `product_id` | `Order_Items` | `product_id` |
| `Categories` | `category_id` | `Products` | `category_id` |
| `Campaigns` | `campaign_id` | `Orders` | `campaign_id` |

---

## Phase 4: Create DAX Measures (One by One)

**DAX = Data Analysis Expressions = Excel formulas for Power BI**

### Measure 1: Total Revenue
```dax
Total Revenue = SUM(MonthlySales[total_revenue])
```

### Measure 2: Total Orders
```dax
Total Orders = SUM(MonthlySales[completed_orders])
```

### Measure 3: Average Order Value
```dax
Avg Order Value = DIVIDE([Total Revenue], [Total Orders], 0)
```

### Measure 4: Revenue Growth %
```dax
Revenue Growth % = 
VAR CurrentMonth = MAX(MonthlySales[month])
VAR PrevMonth = CALCULATE(MAX(MonthlySales[month]), FILTER(ALL(MonthlySales), MonthlySales[month] < CurrentMonth))
RETURN
DIVIDE(
    CALCULATE([Total Revenue], MonthlySales[month] = CurrentMonth) - 
    CALCULATE([Total Revenue], MonthlySales[month] = PrevMonth),
    CALCULATE([Total Revenue], MonthlySales[month] = PrevMonth),
    0
)
```

### Measure 5: Active Customers
```dax
Active Customers = DISTINCTCOUNT(RFM_Segments[customer_id])
```

### Measure 6: Repeat Purchase Rate
```dax
Repeat Rate = 
DIVIDE(
    CALCULATE(COUNTROWS(RFM_Segments), RFM_Segments[segment] IN {"Champions", "Loyal Customers", "New / Potential Loyalists"}),
    COUNTROWS(RFM_Segments),
    0
)
```

---

## Phase 5: Build Visuals (One at a Time)

### Visual 1: KPI Cards (Top Row)
**Card 1:** Total Revenue → Format: Currency ₹, Title: "Total Revenue"
**Card 2:** Total Orders → Format: Whole number, Title: "Total Orders"
**Card 3:** Avg Order Value → Format: Currency ₹, Title: "Avg Order Value"
**Card 4:** Active Customers → Format: Whole number, Title: "Active Customers"

### Visual 2: Monthly Revenue Trend (Line Chart)
- Axis: `MonthlySales[month]`
- Values: `MonthlySales[total_revenue]`
- Title: "Monthly Revenue Trend"

### Visual 3: MoM Growth % (Column Chart)
- Axis: `MonthlySales[month]`
- Values: `MonthlySales[revenue_growth_pct]`
- Title: "Month-over-Month Growth %"

### Visual 4: Customer Segments (Donut Chart)
- Legend: `RFM_Segments[segment]`
- Values: `RFM_Segments[customer_id]` (Count)
- Title: "Customer Segments (RFM)"

### Visual 5: Segment Revenue (Bar Chart)
- Y Axis: `RFM_Segments[segment]`
- X Axis: `RFM_Segments[monetary]` (Sum)
- Title: "Revenue by Customer Segment"

### Visual 6: Cohort Retention (Matrix Heatmap)
- Rows: `CohortRetention[cohort_month]`
- Values: `Month_0`, `Month_1`, `Month_2`... (use Conditional Formatting → Background Color: Red to Green)
- Title: "Cohort Retention Matrix (%)"

### Visual 7: Revenue Anomalies (Scatter Plot)
- X Axis: `SalesAnomalies[month]`
- Y Axis: `SalesAnomalies[total_revenue]`
- Legend: `SalesAnomalies[anomaly_status]`
- Title: "Revenue Anomalies Detection"

### Visual 8: Top 10 Products (Bar Chart from SQL)
- Import `q04_*` → `SQL_TopProducts`
- Y Axis: `product_name`
- X Axis: `revenue` (Sum)
- Title: "Top 10 Products by Revenue"

### Visual 9: AOV by Segment (Column Chart from SQL)
- Import `q08_*` → `SQL_AOVBySegment`
- Axis: `customer_segment`
- Values: `average_order_value`
- Title: "AOV by Customer Segment"

### Visual 10: Region Revenue (Map or Bar from SQL)
- Import `q13_*` → `SQL_RegionRevenue`
- Axis: `state` or `region`
- Values: `revenue`
- Title: "Revenue by Region/State"

---

## Phase 6: Add Slicers (Filters)

1. **Date Slicer:** `MonthlySales[month]` → Between/Relative date
2. **Region Slicer:** `Orders[ship_region]` → Dropdown
3. **Channel Slicer:** `Orders[sales_channel]` → Checkbox
4. **Segment Slicer:** `RFM_Segments[segment]` → Checkbox

---

## Phase 7: Format & Polish

- **Theme:** View → Themes → Executive (or Custom)
- **Colors:** Consistent palette (Blue for revenue, Green for growth, Red for anomalies)
- **Fonts:** Title 16pt bold, Labels 12pt
- **Borders:** Subtle on cards/visuals
- **Tooltips:** Add detail on hover

---

## Phase 8: Save & Publish

1. **File** → **Save As** → `Ecommerce_Dashboard.pbix` in project folder
2. **Optional:** File → **Publish** → Power BI Service → Schedule refresh

---

## Troubleshooting Common Errors

| Error | Fix |
|-------|-----|
| "Column not found" | Check Fields pane spelling, refresh data |
| "Relationship ambiguous" | Model view → delete extra relationships |
| "DAX syntax error" | Check parentheses, commas, table/column names |
| "Circular dependency" | Use `CALCULATE` with `ALL` or `REMOVEFILTERS` |
| "Slow performance" | Reduce visuals, use measures not calculated columns |
| "Data not refreshing" | Check file paths, use relative paths, enable Fast Combine |

---

## How to Invoke This Skill

**In OpenCode, type:**
```
/skill powerbi-dashboard-builder
```

Or mention: **"Use powerbi-dashboard-builder skill"**

The skill will start from **Task 1.1** and guide you step by step.

---

## Quick Reference: Your File Paths

```
Project Root: C:\Users\shiva\E-Commerce-Intelligence-Analytics
├── reports\
│   ├── monthly_sales_trends.csv
│   ├── rfm_customer_segments.csv
│   ├── cohort_retention_matrix.csv
│   ├── sales_anomalies.csv
│   └── sql_results\ (20 files)
└── data\cleaned\
    ├── orders.csv
    ├── customers.csv
    ├── products.csv
    ├── categories.csv
    └── marketing_campaigns.csv
```

---

**Ready to start? Reply `"done"` when Power BI Desktop is open (Task 1.1 complete).**
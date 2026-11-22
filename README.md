# E-Commerce Intelligence & Analytics Platform

An end-to-end data analytics project that turns raw e-commerce data into
business insights: data generation → validation → cleaning → PostgreSQL
(Supabase) → SQL analysis → advanced analytics → interactive dashboard → automated insights.

🔗 **Live Dashboard:**https://sahnisingh335-star.github.io/ecommerce-analytics-platform/dashboard.html
> All data is synthetic (generated with Python and Faker). No real customer data is used.

## 📌 Key Results (Jan 2024 – Sep 2026)

| Metric | Value |
|---|---:|
| Net revenue (completed orders) | ₹3.20 billion |
| Completed orders | 33,308 |
| Profit margin | 24.4% |
| Repeat purchase rate | 88.06% |
| Revenue from top 10% of customers | 23.56% |
| Top brand by revenue | GlowCare (9.88%) |

- **Discounts hurt margin:** the 1–10% discount band earns about 34% profit margin,
  while orders above 30% discount earn only about 7%.
- **Lowest-margin categories:** Home & Kitchen, Fashion, Grocery and Footwear sit
  below the company average margin.
- **Revenue anomalies:** June 2025 was unusually high and February 2026 unusually low.
- **Customer segments (RFM):** 2,096 Champions, 984 At Risk and 2,236 Lost customers
  are the main targets for retention campaigns.

Full details: [`reports/sql_insights.md`](reports/sql_insights.md)

## ❓ Business Questions

1. What is the monthly revenue trend?
2. Which products generate the highest revenue?
3. Which categories are most profitable?
4. Which customers are most valuable?
5. What is the repeat purchase rate?
6. Which regions perform best?
7. What is the return rate?
8. How do discounts affect profitability?

20 SQL questions answer these in [`sql/analysis/business_questions.sql`](sql/analysis/business_questions.sql).

## 📊 Interactive Dashboard

An interactive HTML dashboard built with Chart.js and hosted on GitHub Pages.
It has KPI cards, filters and charts for revenue trends, categories, regions,
discounts and customer segments.

Open it here: [Live Dashboard](https://sahnisingh335-star.github.io/ecommerce-analytics-platform/dashboard.html)

## 🤖 Automated Business Insights

`src/ai_insights.py` reads the analytics result files and writes a plain-English
report with 6 findings and a recommended action for each (revenue trend,
discounts, low-margin categories, customer segments, anomalies, payments and returns).

- Output: [`reports/ai_insights.md`](reports/ai_insights.md)
- Rule-based (no API key needed). Next upgrade: connect an LLM for richer summaries.

## 🗂️ Data

| Table | Rows |
|---|---:|
| orders | 50,000 |
| order_items | 93,308 |
| payments | 50,000 |
| inventory | 36,000 |
| customers | 10,000 |
| returns | 5,590 |
| products | 1,000 |
| date_dimension | 1,096 |
| marketing_campaigns | 200 |
| categories | 10 |

Cleaning rules are documented in [`docs/cleaning_plan.md`](docs/cleaning_plan.md).

## 🛠️ Tech Stack

Python (pandas, NumPy, statsmodels, Faker) · SQL / PostgreSQL (Supabase) ·
SQLAlchemy · Chart.js · HTML/CSS/JavaScript · GitHub Pages · Git & GitHub

## 📁 Project Structure

```text
├── dashboard.html      # interactive dashboard (GitHub Pages)
├── data/
│   ├── raw/            # generated data (not committed)
│   └── cleaned/        # cleaned data
├── docs/               # charter, data model, dataset spec, cleaning plan
├── notebooks/          # exploratory data analysis
├── powerbi/
│   ├── data/           # dashboard-ready star schema + analytics tables
│   └── README.md       # data model guide (relationships, DAX measures)
├── reports/
│   ├── sql_results/    # 20 SQL query outputs
│   ├── sql_insights.md # SQL insights report
│   ├── ai_insights.md  # automated business insights
│   └── *.csv           # RFM, cohort, monthly trends, anomalies
├── sql/analysis/       # business_questions.sql
└── src/
    ├── generate_data.py
    ├── clean_data.py
    ├── apply_cleaning_fixes_to_db.py
    ├── test_db_connection.py
    ├── run_sql_analysis.py
    ├── generate_sql_insights.py
    ├── prepare_powerbi_data.py
    ├── ai_insights.py
    └── analytics/      # rfm, cohort, time_series, anomaly_detection
```

## ▶️ How to Run

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env      # then add your own SUPABASE_DB_URL

python src\generate_data.py
python src\clean_data.py
python src\test_db_connection.py
python src\run_sql_analysis.py
python src\generate_sql_insights.py
python src\analytics\time_series.py
python src\analytics\anomaly_detection.py
python src\analytics\rfm.py
python src\analytics\cohort.py
python src\prepare_powerbi_data.py
python src\ai_insights.py
```

## ✅ Status

- [x] Data generation and documentation
- [x] Data validation and cleaning
- [x] Supabase PostgreSQL database
- [x] 20 SQL business questions and insights report
- [x] RFM, cohort retention, time series, anomaly detection
- [x] Dashboard-ready data model
- [x] Interactive HTML dashboard (Chart.js, GitHub Pages)
- [x] Automated business insights (rule-based)
- [ ] Email alerts (Resend) and GitHub Actions automation

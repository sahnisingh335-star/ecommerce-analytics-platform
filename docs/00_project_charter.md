# Project Charter

## Project
E-Commerce Intelligence & Analytics Platform

## Objective
Build an end-to-end analytics pipeline that turns raw e-commerce data
into reliable business insights: data generation, validation, cleaning,
a PostgreSQL (Supabase) database, SQL analysis, advanced analytics and
a Power BI dashboard.

## Scope
- 10 related tables: customers, products, categories, orders,
  order items, payments, returns, inventory, marketing campaigns, dates
- Period: January 2024 – October 1, 2026 (synthetic data)
- 20 SQL business questions
- RFM segmentation, cohort retention, time-series trends,
  revenue anomaly detection
- Power BI dashboard

## Out of Scope
- Real customer data (all data is synthetic, generated with Faker)
- Live production deployment

## Key Business Questions
1. How is revenue trending month over month?
2. Which products, brands and categories drive revenue and profit?
3. Who are the most valuable customers, and how many come back?
4. Which regions perform best?
5. Where are returns and failed payments concentrated?
6. Do discounts and campaigns pay off?

## Success Criteria
- Every cleaning rule is documented and reproducible
- SQL results match the Python analysis
- Dashboard answers each business question on one page or less
- No credentials are committed to GitHub

## Tools
Python (pandas, NumPy, statsmodels), SQL (PostgreSQL / Supabase),
Power BI, Git & GitHub

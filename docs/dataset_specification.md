# Dataset Specification

## Project
E-Commerce Intelligence & Analytics Platform

## Data Type

Synthetic E-Commerce Data

The dataset will be generated using Python.
It will not contain real customer or business data.

## Dataset Scale

| Dataset | Approximate Records |
|---|---:|
| Customers | 10,000 |
| Products | 1,000 |
| Categories | 20 |
| Orders | 50,000 |
| Order Items | 100,000+ |
| Payments | 50,000 |
| Returns | 5,000–8,000 |
| Inventory | 30,000+ |
| Marketing Campaigns | ~200 |
| Date Dimension | Based on project date range |

## Data Generation Tools

- Python
- Pandas
- NumPy
- Faker

## Data Quality Issues

The synthetic dataset will intentionally contain realistic
data-quality problems for the cleaning and validation phase.

Examples:

- Missing values
- Duplicate records
- Invalid quantities
- Incorrect dates
- Inconsistent category names
- Abnormal discounts
- Outliers

## Output Location

Generated raw datasets will be stored in:

data/raw/

## Output Files

- customers.csv
- products.csv
- categories.csv
- orders.csv
- order_items.csv
- payments.csv
- returns.csv
- inventory.csv
- marketing_campaigns.csv
- date_dimension.csv

## Data Pipeline

Python Data Generation
        ↓
Synthetic Raw Data
        ↓
data/raw/
        ↓
Validation
        ↓
Cleaning
        ↓
data/cleaned/
        ↓
SQL / PostgreSQL
        ↓
Power BI
        ↓
Business Insights
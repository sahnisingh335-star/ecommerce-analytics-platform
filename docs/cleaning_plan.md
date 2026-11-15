# Data Cleaning Plan

## 1. Customers
- Issue: Missing customer emails
- Count: 100
- Action: Handle missing emails without inventing fake values.

## 2. Products
- Issue: Inconsistent product naming patterns
- Action: Standardize product names.

## 3. Orders
- Issue: Delivery date occurs before order date
- Count: 250
- Action: Flag/fix invalid delivery dates during cleaning.

## 4. Order Items
- Issue: Invalid quantity (zero or negative)
- Count: 187
- Action: Handle invalid quantity records.

## 5. Order Items
- Issue: Discount above 100%
- Count: 187
- Action: Handle abnormal discount values.

## 6. Order Items
- Issue: Missing unit price
- Count: 468
- Action: Derive or handle missing unit prices using a documented rule.

## 7. Payments
- Issue: Payment amount is zero or negative
- Count: 189
- Action: Investigate and handle invalid payment amounts.

## Cleaning Principles

- Never modify raw CSV files.
- Keep original data in `data/raw/`.
- Save cleaned datasets in `data/cleaned/`.
- Document every cleaning rule.
- Validate the cleaned data again after cleaning.

## Cleaning Rules Applied (src/clean_data.py)

| Table | Issue | Rows | Rule applied |
|---|---|---:|---|
| order_items | Quantity zero or negative | 187 | Row removed |
| order_items | Discount below 0% or above 100% | 187 | Row removed |
| order_items | Missing unit price | 465 | Filled with the product's `list_price` |
| customers | Missing email | 100 | Kept as missing (no fake emails) |
| orders | Delivery date before order date | 250 | `delivery_date` set to missing |
| products | Name ends with " - new" | 10 | Suffix removed, extra spaces collapsed |
| payments | Amount zero or negative | 189 | 104 replaced with the order total from cleaned order items; 85 set to missing because the order has no valid items left |
| returns | Linked to a removed order item | 30 | Row removed |

## Analysis Rule: Incomplete Months

The data ends on 2026-10-01, so October 2026 has only one day of orders.
Monthly analyses (SQL Q2, Q3, Q12 and `time_series.py`) exclude an
incomplete final month, otherwise it shows a false -98% revenue drop.
Yearly figures for 2026 cover January–October 1 only.

## Applying the Rules to Supabase

After running `python src/clean_data.py`, run
`python src/apply_cleaning_fixes_to_db.py` once. It updates only the
changed product names and payment amounts in a single transaction.

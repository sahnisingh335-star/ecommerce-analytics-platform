# E-Commerce Intelligence & Analytics

## SQL Business Insights Report

This report summarizes the results of the 20 SQL business questions executed against the cleaned e-commerce dataset.

---

## Executive Summary

- SQL questions processed: **20**
- SQL execution status: **Successful**
- Data source: **Supabase PostgreSQL**
- Analysis layer: **SQL Business Questions**

---

## Q01 — Revenue, orders and customers per year

**Rows returned:** 3

### Results

| year | revenue | total_orders | total_customers |
| ---: | ---: | ---: | ---: |
| 2024 | 1,163,848,628.48 | 12158 | 7080 |
| 2025 | 1,168,781,047.58 | 12133 | 7078 |
| 2026 | 865,483,135.41 | 9045 | 6015 |

### Business Insights

- Highest **revenue**: **₹1,168,781,047.58**.
- Lowest **revenue**: **₹865,483,135.41**.
- Total orders represented: **33,336**.
- Customers per year: **6,015 – 7,080** (not added together, because one customer can buy in more than one year).

---

## Q02 — Monthly revenue and mom growth

**Rows returned:** 33

### Results

_Showing first 10 of 33 rows._

| month | revenue | mom_growth_pct |
| --- | ---: | ---: |
| 2024-01-01 | 98,776,666.26 |  |
| 2024-02-01 | 89,227,814.19 | -9.67 |
| 2024-03-01 | 101,435,746.93 | 13.68 |
| 2024-04-01 | 95,867,716.98 | -5.49 |
| 2024-05-01 | 97,669,212.35 | 1.88 |
| 2024-06-01 | 94,313,615.78 | -3.44 |
| 2024-07-01 | 96,319,938.12 | 2.13 |
| 2024-08-01 | 96,024,920.15 | -0.31 |
| 2024-09-01 | 101,430,786.48 | 5.63 |
| 2024-10-01 | 96,772,274.26 | -4.59 |

### Business Insights

- Highest **revenue**: **₹104,710,459.78**.
- Lowest **revenue**: **₹83,040,983.33**.
- Highest value is associated with **2025-06-01**.
- Highest growth: **22.39%**.
- Lowest growth: **-12.29%**.

---

## Q03 — Running total of revenue

**Rows returned:** 33

### Results

_Showing first 10 of 33 rows._

| month | monthly_revenue | running_revenue |
| --- | ---: | ---: |
| 2024-01-01 | 98,776,666.26 | 98,776,666.26 |
| 2024-02-01 | 89,227,814.19 | 188,004,480.45 |
| 2024-03-01 | 101,435,746.93 | 289,440,227.38 |
| 2024-04-01 | 95,867,716.98 | 385,307,944.36 |
| 2024-05-01 | 97,669,212.35 | 482,977,156.71 |
| 2024-06-01 | 94,313,615.78 | 577,290,772.49 |
| 2024-07-01 | 96,319,938.12 | 673,610,710.61 |
| 2024-08-01 | 96,024,920.15 | 769,635,630.76 |
| 2024-09-01 | 101,430,786.48 | 871,066,417.24 |
| 2024-10-01 | 96,772,274.26 | 967,838,691.50 |

### Business Insights

- Highest **monthly_revenue**: **₹104,710,459.78**.
- Lowest **monthly_revenue**: **₹83,040,983.33**.
- Highest value is associated with **2025-06-01**.
- Final cumulative revenue: **₹3,196,271,063.06**.

---

## Q04 — Top 10 products by revenue and profit

**Rows returned:** 10

### Results

| product_id | product_name | revenue | profit |
| ---: | --- | ---: | ---: |
| 57 | Essential GlowCare Product 57 | 8,693,417.86 | 3,850,186.72 |
| 648 | Basic FreshMart Product 648 | 8,679,169.81 | 1,276,327.12 |
| 941 | Advanced HomeMax Product 941 | 8,322,280.52 | 2,802,560.72 |
| 980 | Professional TechPro Product 980 | 8,172,369.96 | 1,722,007.12 |
| 295 | Ultra NextGen Product 295 | 7,991,017.62 | 724,386.54 |
| 577 | Advanced NextGen Product 577 | 7,820,956.36 | 2,467,014.77 |
| 646 | Classic NextGen Product 646 | 7,812,925.32 | 1,487,899.30 |
| 202 | Smart DailyNeeds Product 202 | 7,569,458.86 | 1,869,093.28 |
| 362 | Ultra UrbanStyle Product 362 | 7,429,985.59 | 1,762,221.19 |
| 213 | Advanced TechPro Product 213 | 7,429,766.01 | 2,531,948.91 |

### Business Insights

- Highest **revenue**: **₹8,693,417.86**.
- Lowest **revenue**: **₹7,429,766.01**.
- Highest value is associated with **Essential GlowCare Product 57**.
- Highest profit: **₹3,850,186.72**.
- Highest-profit item/group: **Essential GlowCare Product 57**.

---

## Q05 — Top 3 products in each category

**Rows returned:** 30

### Results

_Showing first 10 of 30 rows._

| category_name | product_id | product_name | revenue | rank_in_category |
| --- | ---: | --- | ---: | ---: |
| Accessories | 826 | Classic Nova Product 826 | 7,403,167.62 | 1 |
| Accessories | 93 | Advanced GlowCare Product 93 | 6,216,121.04 | 2 |
| Accessories | 847 | Professional FitLife Product 847 | 6,133,699.43 | 3 |
| Beauty | 486 | Smart GlowCare Product 486 | 7,180,687.72 | 1 |
| Beauty | 537 | Ultra FreshMart Product 537 | 6,940,038.96 | 2 |
| Beauty | 434 | Ultra NextGen Product 434 | 6,707,218.03 | 3 |
| Books | 489 | Premium FreshMart Product 489 | 6,765,106.69 | 1 |
| Books | 719 | Advanced KidZone Product 719 | 6,566,100.80 | 2 |
| Books | 896 | Essential NextGen Product 896 | 6,542,632.85 | 3 |
| Electronics | 646 | Classic NextGen Product 646 | 7,812,925.32 | 1 |

### Business Insights

- Highest **revenue**: **₹8,693,417.86**.
- Lowest **revenue**: **₹6,133,699.43**.
- Highest value is associated with **Essential GlowCare Product 57**.

---

## Q06 — Categories below company average margin

**Rows returned:** 4

### Results

| category_name | revenue | profit | margin_pct |
| --- | ---: | ---: | ---: |
| Home & Kitchen | 303,564,645.67 | 69,085,300.92 | 22.76 |
| Fashion | 366,891,144.85 | 86,874,021.85 | 23.68 |
| Grocery | 308,489,980.04 | 73,644,713.78 | 23.87 |
| Footwear | 352,939,332.11 | 85,209,221.50 | 24.14 |

### Business Insights

- Highest **revenue**: **₹366,891,144.85**.
- Lowest **revenue**: **₹303,564,645.67**.
- Highest value is associated with **Fashion**.
- Highest profit: **₹86,874,021.85**.
- Highest-profit item/group: **Fashion**.
- Average **margin_pct**: **23.61**.
- Maximum **margin_pct**: **24.14**.

---

## Q07 — Brand share of total revenue

**Rows returned:** 12

### Results

_Showing first 10 of 12 rows._

| brand | revenue | revenue_share_pct |
| --- | ---: | ---: |
| GlowCare | 315,907,376.11 | 9.88 |
| TechPro | 286,624,107.77 | 8.96 |
| UrbanStyle | 281,889,242.06 | 8.81 |
| FreshMart | 277,195,960.27 | 8.67 |
| KidZone | 271,705,823.85 | 8.50 |
| HomeMax | 267,916,564.25 | 8.38 |
| PrimeChoice | 258,013,539.50 | 8.07 |
| NextGen | 257,145,300.25 | 8.04 |
| FitLife | 250,596,104.45 | 7.84 |
| StyleHub | 246,376,985.46 | 7.70 |

### Business Insights

- Highest **revenue**: **₹315,907,376.11**.
- Lowest **revenue**: **₹242,310,863.31**.
- Highest value is associated with **GlowCare**.
- Average **revenue_share_pct**: **8.33**.
- Maximum **revenue_share_pct**: **9.88**.

---

## Q08 — Aov by customer segment

**Rows returned:** 3

### Results

| customer_segment | customers | total_revenue | average_order_value |
| --- | ---: | ---: | ---: |
| Loyal | 2434 | 1,362,426,725.49 | 96,128.32 |
| Repeat | 6051 | 1,728,447,687.77 | 95,987.54 |
| One-Time | 1156 | 107,238,398.21 | 92,766.78 |

### Business Insights

- Highest **total_revenue**: **₹1,728,447,687.77**.
- Lowest **total_revenue**: **₹107,238,398.21**.
- Total customers represented: **9,641**.
- Average AOV: **₹94,960.88**.

---

## Q09 — Repeat purchase rate

**Rows returned:** 1

### Results

| total_customers | repeat_customers | repeat_purchase_rate_pct |
| ---: | ---: | ---: |
| 9642 | 8491 | 88.06 |

### Business Insights

- Total customers represented: **9,642**.
- Average **repeat_purchase_rate_pct**: **88.06**.
- Maximum **repeat_purchase_rate_pct**: **88.06**.

---

## Q10 — Revenue share from top 10% customers

**Rows returned:** 1

### Results

| top_10_pct_revenue_share |
| ---: |
| 23.56 |

### Business Insights

- Average **top_10_pct_revenue_share**: **23.56**.
- Maximum **top_10_pct_revenue_share**: **23.56**.

---

## Q11 — Churn-risk customers

**Rows returned:** 5,316

### Results

_Showing first 10 of 5,316 rows._

| customer_id | email | total_orders | last_order_date | days_since_last_order |
| ---: | --- | ---: | --- | ---: |
| 5458 | chakradev76@example.com | 3 | 2024-03-18 | 972 |
| 9127 | ekansh85@example.org | 4 | 2024-03-21 | 969 |
| 2962 | lavanyaprasad@example.org | 3 | 2024-04-03 | 956 |
| 9192 | osunder@example.com | 3 | 2024-04-18 | 941 |
| 396 | sbansal@example.org | 3 | 2024-05-31 | 898 |
| 8508 | qchhabra@example.com | 4 | 2024-06-13 | 885 |
| 8595 | birarya@example.net | 3 | 2024-06-21 | 877 |
| 6125 | damyanti33@example.net | 3 | 2024-06-23 | 875 |
| 1046 | xparmer@example.com | 3 | 2024-06-26 | 872 |
| 1241 | patelojasvi@example.com | 3 | 2024-06-27 | 871 |

### Business Insights

- Total orders represented: **22,711**.

---

## Q12 — Cohort retention

**Rows returned:** 561

### Results

_Showing first 10 of 561 rows._

| cohort_month | activity_month | month_number | active_customers |
| --- | --- | ---: | ---: |
| 2024-01-01 | 2024-01-01 | 0 | 973 |
| 2024-01-01 | 2024-02-01 | 1 | 85 |
| 2024-01-01 | 2024-03-01 | 2 | 86 |
| 2024-01-01 | 2024-04-01 | 3 | 82 |
| 2024-01-01 | 2024-05-01 | 4 | 89 |
| 2024-01-01 | 2024-06-01 | 5 | 96 |
| 2024-01-01 | 2024-07-01 | 6 | 82 |
| 2024-01-01 | 2024-08-01 | 7 | 90 |
| 2024-01-01 | 2024-09-01 | 8 | 99 |
| 2024-01-01 | 2024-10-01 | 9 | 112 |

### Business Insights

- Detailed results are available in the table above.

---

## Q13 — Region and state revenue ranking

**Rows returned:** 140

### Results

_Showing first 10 of 140 rows._

| region | state | revenue | revenue_rank |
| --- | --- | ---: | ---: |
| East | Himachal Pradesh | 28,292,175.17 | 1 |
| North | Uttarakhand | 28,206,499.66 | 2 |
| East | Tamil Nadu | 27,985,859.07 | 3 |
| West | West Bengal | 27,347,948.46 | 4 |
| West | Rajasthan | 27,339,704.56 | 5 |
| West | Odisha | 27,099,274.82 | 6 |
| North | Tamil Nadu | 27,080,509.34 | 7 |
| West | Madhya Pradesh | 26,624,854.62 | 8 |
| North | Andhra Pradesh | 26,428,154.18 | 9 |
| North | Uttar Pradesh | 26,257,024.49 | 10 |

### Business Insights

- Highest **revenue**: **₹28,292,175.17**.
- Lowest **revenue**: **₹17,974,832.51**.
- Highest value is associated with **Himachal Pradesh**.

---

## Q14 — Units and margin by discount band

**Rows returned:** 5

### Results

| discount_band | units_sold | revenue | profit |
| --- | ---: | ---: | ---: |
| 0% | 12 | 385,515.23 | 138,894.91 |
| 1-10% | 44713 | 1,062,695,061.50 | 361,421,204.59 |
| 11-20% | 45025 | 953,684,291.88 | 254,262,462.62 |
| 21-30% | 43509 | 812,721,411.28 | 137,046,431.32 |
| 30%+ | 21822 | 368,626,531.58 | 27,077,361.28 |

### Business Insights

- Highest **revenue**: **₹1,062,695,061.50**.
- Lowest **revenue**: **₹385,515.23**.
- Highest profit: **₹361,421,204.59**.

---

## Q15 — Products with return rate above 2x average

**Rows returned:** 16

### Results

_Showing first 10 of 16 rows._

| product_id | product_name | return_rate_pct |
| ---: | --- | ---: |
| 732 | Premium Nova Product 732 | 9.18 |
| 763 | Essential Nova Product 763 | 8.80 |
| 337 | Professional UrbanStyle Product 337 | 8.65 |
| 455 | Smart UrbanStyle Product 455 | 8.42 |
| 334 | Essential NextGen Product 334 | 8.28 |
| 329 | Ultra KidZone Product 329 | 8.13 |
| 415 | Ultra Nova Product 415 | 7.91 |
| 953 | Smart TechPro Product 953 | 7.79 |
| 342 | Basic DailyNeeds Product 342 | 7.77 |
| 189 | Professional StyleHub Product 189 | 7.69 |

### Business Insights

- Average **return_rate_pct**: **7.98**.
- Maximum **return_rate_pct**: **9.18**.

---

## Q16 — Return reasons by category

**Rows returned:** 60

### Results

_Showing first 10 of 60 rows._

| category_name | reason | return_count | refund_value |
| --- | --- | ---: | ---: |
| Accessories | Wrong Product | 96 | 955,808.58 |
| Accessories | Quality Issue | 96 | 986,914.08 |
| Accessories | Size Issue | 91 | 980,979.80 |
| Accessories | Late Delivery | 89 | 840,733.88 |
| Accessories | Damaged | 83 | 923,089.52 |
| Accessories | Changed Mind | 83 | 973,960.37 |
| Beauty | Size Issue | 118 | 1,183,595.41 |
| Beauty | Late Delivery | 106 | 1,066,845.64 |
| Beauty | Damaged | 102 | 1,080,213.32 |
| Beauty | Wrong Product | 99 | 1,004,693.72 |

### Business Insights

- Highest return value/rate: **129.00**.
- Highest-return group: **Footwear**.

---

## Q17 — Payment method mix and failed payment rate

**Rows returned:** 6

### Results

| method | total_payments | failed_payments | failed_payment_rate_pct | total_payment_amount |
| --- | ---: | ---: | ---: | ---: |
| Wallet | 8408 | 1428 | 16.98 | 802,738,771.71 |
| Net Banking | 8381 | 1357 | 16.19 | 798,307,358.68 |
| Credit Card | 8335 | 1391 | 16.69 | 790,096,987.98 |
| Debit Card | 8334 | 1420 | 17.04 | 806,420,252.75 |
| UPI | 8273 | 1366 | 16.51 | 789,163,606.64 |
| Cash on Delivery | 8269 | 1398 | 16.91 | 783,631,945.97 |

### Business Insights

- Average **failed_payment_rate_pct**: **16.72**.
- Maximum **failed_payment_rate_pct**: **17.04**.

---

## Q18 — Campaign revenue vs budget

**Rows returned:** 200

### Results

_Showing first 10 of 200 rows._

| campaign_id | name | channel | budget | revenue | revenue_minus_budget | revenue_to_budget_ratio |
| ---: | --- | --- | ---: | ---: | ---: | ---: |
| 131 | Campaign 131 | Social Media | 6,138.29 | 15,304,738.33 | 15,298,600.04 | 2,493.32 |
| 183 | Campaign 183 | Affiliate | 7,571.79 | 14,971,854.29 | 14,964,282.50 | 1,977.32 |
| 35 | Campaign 35 | Google Ads | 7,013.22 | 13,401,706.02 | 13,394,692.80 | 1,910.92 |
| 146 | Campaign 146 | Display | 8,050.85 | 14,726,899.54 | 14,718,848.69 | 1,829.24 |
| 12 | Campaign 12 | Influencer | 8,432.13 | 15,139,743.83 | 15,131,311.70 | 1,795.48 |
| 145 | Campaign 145 | Email | 9,014.40 | 14,821,114.71 | 14,812,100.31 | 1,644.16 |
| 20 | Campaign 20 | Google Ads | 10,074.70 | 15,322,414.51 | 15,312,339.81 | 1,520.88 |
| 18 | Campaign 18 | Google Ads | 9,365.04 | 14,105,889.19 | 14,096,524.15 | 1,506.23 |
| 87 | Campaign 87 | Display | 9,825.16 | 14,193,736.69 | 14,183,911.53 | 1,444.63 |
| 85 | Campaign 85 | Affiliate | 13,746.05 | 15,362,981.95 | 15,349,235.90 | 1,117.63 |

### Business Insights

- Highest **revenue**: **₹18,017,582.39**.
- Lowest **revenue**: **₹10,797,852.94**.

---

## Q19 — Days between first and second order

**Rows returned:** 8,491

### Results

_Showing first 10 of 8,491 rows._

| customer_id | first_order_date | second_order_date | days_between_orders |
| ---: | --- | --- | ---: |
| 6503 | 2024-04-25 | 2024-04-25 | 0 |
| 4464 | 2024-02-12 | 2024-02-12 | 0 |
| 8674 | 2024-04-30 | 2024-04-30 | 0 |
| 5289 | 2024-07-14 | 2024-07-14 | 0 |
| 6731 | 2024-04-06 | 2024-04-06 | 0 |
| 9153 | 2025-09-13 | 2025-09-13 | 0 |
| 2314 | 2024-03-11 | 2024-03-11 | 0 |
| 1652 | 2024-01-07 | 2024-01-07 | 0 |
| 8235 | 2024-01-13 | 2024-01-13 | 0 |
| 4393 | 2024-12-29 | 2024-12-29 | 0 |

### Business Insights

- Detailed results are available in the table above.

---

## Q20 — Revenue anomalies

**Rows returned:** 44

### Results

_Showing first 10 of 44 rows._

| date | revenue | average_revenue | standard_deviation | anomaly_flag |
| --- | ---: | ---: | ---: | --- |
| 2024-01-04 | 4,655,639.62 | 3,182,201.80 | 696,138.47 | Anomaly |
| 2024-02-19 | 1,524,284.24 | 3,182,201.80 | 696,138.47 | Anomaly |
| 2024-02-23 | 1,759,827.43 | 3,182,201.80 | 696,138.47 | Anomaly |
| 2024-03-16 | 4,630,060.08 | 3,182,201.80 | 696,138.47 | Anomaly |
| 2024-03-20 | 1,296,429.32 | 3,182,201.80 | 696,138.47 | Anomaly |
| 2024-03-21 | 4,686,367.45 | 3,182,201.80 | 696,138.47 | Anomaly |
| 2024-03-26 | 5,501,051.13 | 3,182,201.80 | 696,138.47 | Anomaly |
| 2024-04-17 | 1,615,247.38 | 3,182,201.80 | 696,138.47 | Anomaly |
| 2024-07-03 | 5,425,889.73 | 3,182,201.80 | 696,138.47 | Anomaly |
| 2024-08-25 | 1,464,453.68 | 3,182,201.80 | 696,138.47 | Anomaly |

### Business Insights

- Highest **revenue**: **₹5,715,443.09**.
- Lowest **revenue**: **₹1,091,061.00**.

---

# Next Development Steps

Completed analytics stages:

1. RFM Customer Segmentation — done
2. Cohort Retention Analysis — done
3. Time Series Analysis — done
4. Revenue Anomaly Detection — done

Next stages:

5. Power BI Dashboard
6. AI Business Insights
7. Resend Email Alerts

SQL and Python remain responsible for calculating business metrics. AI should explain pre-computed results rather than independently calculating KPIs.
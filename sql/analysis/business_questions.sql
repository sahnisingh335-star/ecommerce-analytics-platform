-- =========================================================
-- E-COMMERCE INTELLIGENCE & ANALYTICS
-- SQL BUSINESS QUESTIONS
-- =========================================================


-- Q1. Revenue, Orders and Customers per Year
SELECT
    EXTRACT(YEAR FROM o.order_date) AS year,
    ROUND(SUM(oi.quantity * oi.unit_price *
        (1 - oi.discount_pct / 100)), 2) AS revenue,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT o.customer_id) AS total_customers
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'Completed'
GROUP BY 1
ORDER BY 1;


-- Q2. Monthly Revenue and MoM Growth
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', o.order_date) AS month,
        SUM(oi.quantity * oi.unit_price *
            (1 - oi.discount_pct / 100)) AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status = 'Completed'
      AND o.order_date < (
        -- Only complete months: drop the last month if the data
        -- ends before that month's last day (e.g. only 1 Oct 2026).
        SELECT CASE
            WHEN MAX(order_date) >= (DATE_TRUNC('month', MAX(order_date))
                 + INTERVAL '1 month - 1 day')::date
            THEN (DATE_TRUNC('month', MAX(order_date)) + INTERVAL '1 month')::date
            ELSE DATE_TRUNC('month', MAX(order_date))::date
        END
        FROM orders
    )
    GROUP BY 1
)
SELECT
    month,
    ROUND(revenue, 2) AS revenue,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY month))
        / NULLIF(LAG(revenue) OVER (ORDER BY month), 0) * 100,
        2
    ) AS mom_growth_pct
FROM monthly_revenue
ORDER BY month;


-- Q3. Running Total of Revenue
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', o.order_date) AS month,
        SUM(oi.quantity * oi.unit_price *
            (1 - oi.discount_pct / 100)) AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status = 'Completed'
      AND o.order_date < (
        -- Only complete months: drop the last month if the data
        -- ends before that month's last day (e.g. only 1 Oct 2026).
        SELECT CASE
            WHEN MAX(order_date) >= (DATE_TRUNC('month', MAX(order_date))
                 + INTERVAL '1 month - 1 day')::date
            THEN (DATE_TRUNC('month', MAX(order_date)) + INTERVAL '1 month')::date
            ELSE DATE_TRUNC('month', MAX(order_date))::date
        END
        FROM orders
    )
    GROUP BY 1
)
SELECT
    month,
    ROUND(revenue, 2) AS monthly_revenue,
    ROUND(
        SUM(revenue) OVER (ORDER BY month), 2
    ) AS running_revenue
FROM monthly_revenue
ORDER BY month;


-- Q4. Top 10 Products by Revenue and Profit
SELECT
    p.product_id,
    p.product_name,
    ROUND(SUM(
        oi.quantity * oi.unit_price *
        (1 - oi.discount_pct / 100)
    ), 2) AS revenue,
    ROUND(SUM(
        oi.quantity * oi.unit_price *
        (1 - oi.discount_pct / 100)
        - oi.quantity * oi.unit_cost
    ), 2) AS profit
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.status = 'Completed'
GROUP BY p.product_id, p.product_name
ORDER BY revenue DESC
LIMIT 10;


-- Q5. Top 3 Products in Each Category
WITH product_sales AS (
    SELECT
        cat.category_name,
        p.product_id,
        p.product_name,
        SUM(oi.quantity * oi.unit_price *
            (1 - oi.discount_pct / 100)) AS revenue
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    JOIN products p ON oi.product_id = p.product_id
    JOIN categories cat ON p.category_id = cat.category_id
    WHERE o.status = 'Completed'
    GROUP BY cat.category_name, p.product_id, p.product_name
),
ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY category_name
            ORDER BY revenue DESC
        ) AS rank_in_category
    FROM product_sales
)
SELECT
    category_name,
    product_id,
    product_name,
    ROUND(revenue, 2) AS revenue,
    rank_in_category
FROM ranked
WHERE rank_in_category <= 3
ORDER BY category_name, rank_in_category;


-- Q6. Categories Below Company Average Margin
WITH category_margin AS (
    SELECT
        cat.category_name,
        SUM(oi.quantity * oi.unit_price *
            (1 - oi.discount_pct / 100)) AS revenue,
        SUM(oi.quantity * oi.unit_cost) AS cogs
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    JOIN products p ON oi.product_id = p.product_id
    JOIN categories cat ON p.category_id = cat.category_id
    WHERE o.status = 'Completed'
    GROUP BY cat.category_name
),
margin_calc AS (
    SELECT
        category_name,
        revenue,
        revenue - cogs AS profit,
        (revenue - cogs) / NULLIF(revenue, 0) * 100 AS margin_pct
    FROM category_margin
)
SELECT
    category_name,
    ROUND(revenue, 2) AS revenue,
    ROUND(profit, 2) AS profit,
    ROUND(margin_pct, 2) AS margin_pct
FROM margin_calc
WHERE margin_pct < (SELECT AVG(margin_pct) FROM margin_calc)
ORDER BY margin_pct;


-- Q7. Brand Share of Total Revenue
WITH brand_revenue AS (
    SELECT
        p.brand,
        SUM(oi.quantity * oi.unit_price *
            (1 - oi.discount_pct / 100)) AS revenue
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.status = 'Completed'
    GROUP BY p.brand
)
SELECT
    brand,
    ROUND(revenue, 2) AS revenue,
    ROUND(revenue / SUM(revenue) OVER () * 100, 2)
        AS revenue_share_pct
FROM brand_revenue
ORDER BY revenue DESC;


-- Q8. AOV by Customer Segment
WITH customer_orders AS (
    SELECT
        o.customer_id,
        COUNT(DISTINCT o.order_id) AS order_count,
        SUM(oi.quantity * oi.unit_price *
            (1 - oi.discount_pct / 100)) AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status = 'Completed'
    GROUP BY o.customer_id
),
segmented AS (
    SELECT *,
        CASE
            WHEN order_count = 1 THEN 'One-Time'
            WHEN order_count BETWEEN 2 AND 4 THEN 'Repeat'
            ELSE 'Loyal'
        END AS customer_segment
    FROM customer_orders
)
SELECT
    customer_segment,
    COUNT(*) AS customers,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(
        SUM(revenue) / NULLIF(SUM(order_count), 0), 2
    ) AS average_order_value
FROM segmented
GROUP BY customer_segment
ORDER BY average_order_value DESC;


-- Q9. Repeat Purchase Rate
WITH customer_orders AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS order_count
    FROM orders
    WHERE status = 'Completed'
    GROUP BY customer_id
)
SELECT
    COUNT(*) AS total_customers,
    COUNT(*) FILTER (WHERE order_count >= 2)
        AS repeat_customers,
    ROUND(
        COUNT(*) FILTER (WHERE order_count >= 2)
        / COUNT(*)::NUMERIC * 100, 2
    ) AS repeat_purchase_rate_pct
FROM customer_orders;


-- Q10. Revenue Share from Top 10% Customers
WITH customer_revenue AS (
    SELECT
        o.customer_id,
        SUM(oi.quantity * oi.unit_price *
            (1 - oi.discount_pct / 100)) AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status = 'Completed'
    GROUP BY o.customer_id
),
ranked AS (
    SELECT *,
        NTILE(10) OVER (ORDER BY revenue DESC) AS customer_decile
    FROM customer_revenue
)
SELECT
    ROUND(
        SUM(CASE WHEN customer_decile = 1 THEN revenue ELSE 0 END)
        / SUM(revenue) * 100, 2
    ) AS top_10_pct_revenue_share
FROM ranked;


-- Q11. Churn-Risk Customers
SELECT
    c.customer_id,
    c.email,
    COUNT(DISTINCT o.order_id) AS total_orders,
    MAX(o.order_date) AS last_order_date,
    CURRENT_DATE - MAX(o.order_date) AS days_since_last_order
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'Completed'
GROUP BY c.customer_id, c.email
HAVING COUNT(DISTINCT o.order_id) >= 3
   AND MAX(o.order_date) < CURRENT_DATE - INTERVAL '90 days'
ORDER BY days_since_last_order DESC;


-- Q12. Cohort Retention
WITH first_purchase AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', MIN(order_date)) AS cohort_month
    FROM orders
    WHERE status = 'Completed'
      AND order_date < (
        -- Only complete months: drop the last month if the data
        -- ends before that month's last day (e.g. only 1 Oct 2026).
        SELECT CASE
            WHEN MAX(order_date) >= (DATE_TRUNC('month', MAX(order_date))
                 + INTERVAL '1 month - 1 day')::date
            THEN (DATE_TRUNC('month', MAX(order_date)) + INTERVAL '1 month')::date
            ELSE DATE_TRUNC('month', MAX(order_date))::date
        END
        FROM orders
    )
    GROUP BY customer_id
),
activity AS (
    SELECT DISTINCT
        o.customer_id,
        f.cohort_month,
        DATE_TRUNC('month', o.order_date) AS activity_month
    FROM orders o
    JOIN first_purchase f ON o.customer_id = f.customer_id
    WHERE o.status = 'Completed'
      AND o.order_date < (
        -- Only complete months: drop the last month if the data
        -- ends before that month's last day (e.g. only 1 Oct 2026).
        SELECT CASE
            WHEN MAX(order_date) >= (DATE_TRUNC('month', MAX(order_date))
                 + INTERVAL '1 month - 1 day')::date
            THEN (DATE_TRUNC('month', MAX(order_date)) + INTERVAL '1 month')::date
            ELSE DATE_TRUNC('month', MAX(order_date))::date
        END
        FROM orders
    )
)
SELECT
    cohort_month,
    activity_month,
    (
        EXTRACT(YEAR FROM activity_month)
        - EXTRACT(YEAR FROM cohort_month)
    ) * 12
    +
    (
        EXTRACT(MONTH FROM activity_month)
        - EXTRACT(MONTH FROM cohort_month)
    ) AS month_number,
    COUNT(DISTINCT customer_id) AS active_customers
FROM activity
GROUP BY cohort_month, activity_month
ORDER BY cohort_month, activity_month;


-- Q13. Region and State Revenue Ranking
SELECT
    o.ship_region AS region,
    c.state,
    ROUND(SUM(
        oi.quantity * oi.unit_price *
        (1 - oi.discount_pct / 100)
    ), 2) AS revenue,
    DENSE_RANK() OVER (
        ORDER BY SUM(
            oi.quantity * oi.unit_price *
            (1 - oi.discount_pct / 100)
        ) DESC
    ) AS revenue_rank
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'Completed'
GROUP BY o.ship_region, c.state
ORDER BY revenue_rank;


-- Q14. Units and Margin by Discount Band
SELECT
    CASE
        WHEN oi.discount_pct = 0 THEN '0%'
        WHEN oi.discount_pct <= 10 THEN '1-10%'
        WHEN oi.discount_pct <= 20 THEN '11-20%'
        WHEN oi.discount_pct <= 30 THEN '21-30%'
        ELSE '30%+'
    END AS discount_band,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(
        oi.quantity * oi.unit_price *
        (1 - oi.discount_pct / 100)
    ), 2) AS revenue,
    ROUND(SUM(
        oi.quantity * oi.unit_price *
        (1 - oi.discount_pct / 100)
        - oi.quantity * oi.unit_cost
    ), 2) AS profit
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status = 'Completed'
GROUP BY discount_band
ORDER BY MIN(oi.discount_pct);


-- Q15. Products with Return Rate Above 2x Average
WITH product_sales AS (
    SELECT
        oi.product_id,
        SUM(oi.quantity) AS units_sold
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.status = 'Completed'
    GROUP BY oi.product_id
),
product_returns AS (
    SELECT
        oi.product_id,
        COUNT(DISTINCT r.return_id) AS returns
    FROM returns r
    JOIN order_items oi ON r.order_item_id = oi.order_item_id
    GROUP BY oi.product_id
),
return_rates AS (
    SELECT
        ps.product_id,
        ps.units_sold,
        COALESCE(pr.returns, 0) AS returns,
        COALESCE(pr.returns, 0)::NUMERIC
        / NULLIF(ps.units_sold, 0) * 100 AS return_rate
    FROM product_sales ps
    LEFT JOIN product_returns pr ON ps.product_id = pr.product_id
)
SELECT
    p.product_id,
    p.product_name,
    ROUND(rr.return_rate, 2) AS return_rate_pct
FROM return_rates rr
JOIN products p ON rr.product_id = p.product_id
WHERE rr.return_rate > (
    SELECT AVG(return_rate) * 2 FROM return_rates
)
ORDER BY return_rate_pct DESC;


-- Q16. Return Reasons by Category
SELECT
    cat.category_name,
    r.reason,
    COUNT(*) AS return_count,
    ROUND(SUM(r.refund_amount), 2) AS refund_value
FROM returns r
JOIN order_items oi ON r.order_item_id = oi.order_item_id
JOIN products p ON oi.product_id = p.product_id
JOIN categories cat ON p.category_id = cat.category_id
GROUP BY cat.category_name, r.reason
ORDER BY cat.category_name, return_count DESC;


-- Q17. Payment Method Mix and Failed Payment Rate
SELECT
    method,
    COUNT(*) AS total_payments,
    COUNT(*) FILTER (WHERE status = 'Failed') AS failed_payments,
    ROUND(
        COUNT(*) FILTER (WHERE status = 'Failed')
        / COUNT(*)::NUMERIC * 100, 2
    ) AS failed_payment_rate_pct,
    ROUND(SUM(amount), 2) AS total_payment_amount
FROM payments
GROUP BY method
ORDER BY total_payments DESC;


-- Q18. Campaign Revenue vs Budget
WITH campaign_revenue AS (
    SELECT
        o.campaign_id,
        SUM(oi.quantity * oi.unit_price *
            (1 - oi.discount_pct / 100)) AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status = 'Completed'
      AND o.campaign_id IS NOT NULL
    GROUP BY o.campaign_id
)
SELECT
    mc.campaign_id,
    mc.name,
    mc.channel,
    ROUND(mc.budget, 2) AS budget,
    ROUND(COALESCE(cr.revenue, 0), 2) AS revenue,
    ROUND(COALESCE(cr.revenue, 0) - mc.budget, 2)
        AS revenue_minus_budget,
    ROUND(
        COALESCE(cr.revenue, 0) / NULLIF(mc.budget, 0), 2
    ) AS revenue_to_budget_ratio
FROM marketing_campaigns mc
LEFT JOIN campaign_revenue cr
    ON mc.campaign_id = cr.campaign_id
ORDER BY revenue_to_budget_ratio DESC;


-- Q19. Days Between First and Second Order
WITH customer_orders AS (
    SELECT
        customer_id,
        order_date,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY order_date
        ) AS order_number
    FROM orders
    WHERE status = 'Completed'
),
first_second AS (
    SELECT
        customer_id,
        MAX(CASE WHEN order_number = 1 THEN order_date END)
            AS first_order_date,
        MAX(CASE WHEN order_number = 2 THEN order_date END)
            AS second_order_date
    FROM customer_orders
    GROUP BY customer_id
)
SELECT
    customer_id,
    first_order_date,
    second_order_date,
    second_order_date - first_order_date
        AS days_between_orders
FROM first_second
WHERE second_order_date IS NOT NULL
ORDER BY days_between_orders;


-- Q20. Revenue Anomalies
WITH daily_revenue AS (
    SELECT
        o.order_date AS date,
        SUM(oi.quantity * oi.unit_price *
            (1 - oi.discount_pct / 100)) AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status = 'Completed'
    GROUP BY o.order_date
),
stats AS (
    SELECT
        *,
        AVG(revenue) OVER () AS avg_revenue,
        STDDEV(revenue) OVER () AS stddev_revenue
    FROM daily_revenue
)
SELECT
    date,
    ROUND(revenue, 2) AS revenue,
    ROUND(avg_revenue, 2) AS average_revenue,
    ROUND(stddev_revenue, 2) AS standard_deviation,
    CASE
        WHEN ABS(revenue - avg_revenue) > 2 * stddev_revenue
        THEN 'Anomaly'
        ELSE 'Normal'
    END AS anomaly_flag
FROM stats
WHERE ABS(revenue - avg_revenue) > 2 * stddev_revenue
ORDER BY date;
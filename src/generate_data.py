from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker


# ============================================================
# PROJECT SETUP
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42

rng = np.random.default_rng(SEED)

fake = Faker("en_IN")
fake.seed_instance(SEED)


# ============================================================
# DATASET SIZE
# ============================================================

N_CUSTOMERS = 10_000
N_PRODUCTS = 1_000
N_CAMPAIGNS = 200
N_ORDERS = 50_000


# ============================================================
# HELPER FUNCTION
# ============================================================

def random_dates(start_date, end_date, size):
    """
    Generate random dates between start_date and end_date.
    """
    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)

    days = (end - start).days

    random_days = rng.integers(0, days + 1, size=size)

    return start + pd.to_timedelta(random_days, unit="D")


# ============================================================
# 1. DATE DIMENSION
# ============================================================

print("Generating date_dimension.csv...")

date_range = pd.date_range(
    start="2024-01-01",
    end="2026-12-31",
    freq="D"
)

date_dimension = pd.DataFrame({
    "date_id": date_range,
})

date_dimension["year"] = date_dimension["date_id"].dt.year
date_dimension["quarter"] = date_dimension["date_id"].dt.quarter
date_dimension["month"] = date_dimension["date_id"].dt.month
date_dimension["month_name"] = date_dimension["date_id"].dt.month_name()
date_dimension["week"] = date_dimension["date_id"].dt.isocalendar().week.astype(int)
date_dimension["day_of_week"] = date_dimension["date_id"].dt.dayofweek + 1
date_dimension["is_weekend"] = date_dimension["date_id"].dt.dayofweek >= 5

# Simple holiday-season flag
date_dimension["is_holiday_season"] = (
    date_dimension["date_id"].dt.month.isin([10, 11, 12])
)

date_dimension.to_csv(
    RAW_DATA_DIR / "date_dimension.csv",
    index=False
)

print(f"Created date_dimension.csv: {len(date_dimension):,} rows")


# ============================================================
# 2. CATEGORIES
# ============================================================

print("Generating categories.csv...")

category_data = [
    (1, "Electronics", "Technology"),
    (2, "Fashion", "Lifestyle"),
    (3, "Home & Kitchen", "Home"),
    (4, "Beauty", "Lifestyle"),
    (5, "Sports", "Lifestyle"),
    (6, "Books", "Education"),
    (7, "Grocery", "Food"),
    (8, "Toys", "Kids"),
    (9, "Accessories", "Fashion"),
    (10, "Footwear", "Fashion"),
]

categories = pd.DataFrame(
    category_data,
    columns=[
        "category_id",
        "category_name",
        "parent_category"
    ]
)

categories.to_csv(
    RAW_DATA_DIR / "categories.csv",
    index=False
)

print(f"Created categories.csv: {len(categories):,} rows")


# ============================================================
# 3. PRODUCTS
# ============================================================

print("Generating products.csv...")

brands = [
    "Nova", "UrbanStyle", "TechPro", "HomeMax",
    "FitLife", "GlowCare", "FreshMart", "KidZone",
    "StyleHub", "PrimeChoice", "NextGen", "DailyNeeds"
]

product_prefixes = [
    "Premium",
    "Classic",
    "Smart",
    "Advanced",
    "Essential",
    "Professional",
    "Ultra",
    "Basic"
]

product_names = [
    f"{rng.choice(product_prefixes)} {rng.choice(brands)} Product {i}"
    for i in range(1, N_PRODUCTS + 1)
]

product_category_ids = rng.integers(
    1,
    len(categories) + 1,
    size=N_PRODUCTS
)

list_prices = np.round(
    rng.uniform(100, 50_000, N_PRODUCTS),
    2
)

unit_costs = np.round(
    list_prices * rng.uniform(0.45, 0.80, N_PRODUCTS),
    2
)

products = pd.DataFrame({
    "product_id": np.arange(1, N_PRODUCTS + 1),
    "category_id": product_category_ids,
    "brand": rng.choice(brands, N_PRODUCTS),
    "product_name": product_names,
    "list_price": list_prices,
    "unit_cost": unit_costs,
    "launch_date": random_dates(
        "2023-01-01",
        "2026-06-30",
        N_PRODUCTS
    )
})

# Intentional data-quality issue:
# inconsistent category spelling
bad_category_rows = rng.choice(
    products.index,
    size=int(N_PRODUCTS * 0.01),
    replace=False
)

# We cannot change category_id because it is a foreign key.
# Instead, product names receive an inconsistent suffix.
products.loc[
    bad_category_rows,
    "product_name"
] = (
    products.loc[bad_category_rows, "product_name"]
    + " - new"
)

products.to_csv(
    RAW_DATA_DIR / "products.csv",
    index=False
)

print(f"Created products.csv: {len(products):,} rows")


# ============================================================
# 4. CUSTOMERS
# ============================================================

print("Generating customers.csv...")

genders = ["Male", "Female", "Other"]

acquisition_channels = [
    "Organic Search",
    "Social Media",
    "Email",
    "Paid Search",
    "Referral",
    "Direct"
]

regions = [
    "North",
    "South",
    "East",
    "West",
    "Central"
]

customers = pd.DataFrame({
    "customer_id": np.arange(1, N_CUSTOMERS + 1),

    "email": [
        fake.unique.email()
        for _ in range(N_CUSTOMERS)
    ],

    "signup_date": random_dates(
        "2023-01-01",
        "2026-06-30",
        N_CUSTOMERS
    ),

    "city": [
        fake.city()
        for _ in range(N_CUSTOMERS)
    ],

    "state": [
        fake.state()
        for _ in range(N_CUSTOMERS)
    ],

    "region": rng.choice(
        regions,
        N_CUSTOMERS
    ),

    "acquisition_channel": rng.choice(
        acquisition_channels,
        N_CUSTOMERS
    ),

    "gender": rng.choice(
        genders,
        N_CUSTOMERS
    )
})

# Intentional missing values
missing_email_rows = rng.choice(
    customers.index,
    size=int(N_CUSTOMERS * 0.01),
    replace=False
)

customers.loc[
    missing_email_rows,
    "email"
] = np.nan

customers.to_csv(
    RAW_DATA_DIR / "customers.csv",
    index=False
)

print(f"Created customers.csv: {len(customers):,} rows")


# ============================================================
# 5. MARKETING CAMPAIGNS
# ============================================================

print("Generating marketing_campaigns.csv...")

campaign_channels = [
    "Email",
    "Social Media",
    "Google Ads",
    "Affiliate",
    "Influencer",
    "Display"
]

campaign_start_dates = random_dates(
    "2024-01-01",
    "2026-10-01",
    N_CAMPAIGNS
)

campaign_durations = rng.integers(
    7,
    61,
    size=N_CAMPAIGNS
)

campaign_end_dates = (
    campaign_start_dates
    + pd.to_timedelta(campaign_durations, unit="D")
)

marketing_campaigns = pd.DataFrame({
    "campaign_id": np.arange(1, N_CAMPAIGNS + 1),

    "name": [
        f"Campaign {i}"
        for i in range(1, N_CAMPAIGNS + 1)
    ],

    "channel": rng.choice(
        campaign_channels,
        N_CAMPAIGNS
    ),

    "start_date": campaign_start_dates,

    "end_date": campaign_end_dates,

    "budget": np.round(
        rng.uniform(5_000, 500_000, N_CAMPAIGNS),
        2
    ),

    "discount_pct": np.round(
        rng.uniform(0, 40, N_CAMPAIGNS),
        2
    ),

    "target_category_id": rng.integers(
        1,
        len(categories) + 1,
        N_CAMPAIGNS
    )
})

marketing_campaigns.to_csv(
    RAW_DATA_DIR / "marketing_campaigns.csv",
    index=False
)

print(
    f"Created marketing_campaigns.csv: "
    f"{len(marketing_campaigns):,} rows"
)


# ============================================================
# 6. ORDERS
# ============================================================

print("Generating orders.csv...")

order_dates = random_dates(
    "2024-01-01",
    "2026-10-01",
    N_ORDERS
)

order_statuses = [
    "Completed",
    "Completed",
    "Completed",
    "Completed",
    "Cancelled",
    "Pending"
]

sales_channels = [
    "Website",
    "Mobile App",
    "Marketplace"
]

orders = pd.DataFrame({
    "order_id": np.arange(1, N_ORDERS + 1),

    "customer_id": rng.integers(
        1,
        N_CUSTOMERS + 1,
        N_ORDERS
    ),

    "campaign_id": rng.choice(
        np.append(
            marketing_campaigns["campaign_id"].values,
            [np.nan] * 30
        ),
        N_ORDERS
    ),

    "order_date": order_dates,

    "status": rng.choice(
        order_statuses,
        N_ORDERS
    ),

    "sales_channel": rng.choice(
        sales_channels,
        N_ORDERS
    ),

    "ship_region": rng.choice(
        regions,
        N_ORDERS
    )
})

delivery_days = rng.integers(
    2,
    11,
    N_ORDERS
)

orders["delivery_date"] = (
    orders["order_date"]
    + pd.to_timedelta(delivery_days, unit="D")
)

# Intentional future delivery-date issues
future_delivery_rows = rng.choice(
    orders.index,
    size=int(N_ORDERS * 0.005),
    replace=False
)

orders.loc[
    future_delivery_rows,
    "delivery_date"
] = (
    orders.loc[future_delivery_rows, "order_date"]
    - pd.to_timedelta(
        rng.integers(1, 5, len(future_delivery_rows)),
        unit="D"
    )
)

orders.to_csv(
    RAW_DATA_DIR / "orders.csv",
    index=False
)

print(f"Created orders.csv: {len(orders):,} rows")


# ============================================================
# 7. ORDER ITEMS
# ============================================================

print("Generating order_items.csv...")

items_per_order = rng.choice(
    [1, 2, 3, 4],
    size=N_ORDERS,
    p=[0.45, 0.30, 0.18, 0.07]
)

order_item_records = []

order_item_id = 1

for order_id, item_count in zip(
    orders["order_id"],
    items_per_order
):

    selected_products = rng.choice(
        products["product_id"].values,
        size=item_count,
        replace=False
    )

    for product_id in selected_products:

        product = products.loc[
            products["product_id"] == product_id
        ].iloc[0]

        quantity = int(
            rng.integers(1, 5)
        )

        discount_pct = round(
            float(rng.uniform(0, 35)),
            2
        )

        order_item_records.append({
            "order_item_id": order_item_id,
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": float(product["list_price"]),
            "discount_pct": discount_pct,
            "unit_cost": float(product["unit_cost"])
        })

        order_item_id += 1


order_items = pd.DataFrame(order_item_records)

# Intentional invalid quantity issues
invalid_quantity_rows = rng.choice(
    order_items.index,
    size=max(1, int(len(order_items) * 0.002)),
    replace=False
)

order_items.loc[
    invalid_quantity_rows,
    "quantity"
] = rng.choice(
    [0, -1],
    size=len(invalid_quantity_rows)
)

# Intentional abnormal discount issues
invalid_discount_rows = rng.choice(
    order_items.index,
    size=max(1, int(len(order_items) * 0.002)),
    replace=False
)

order_items.loc[
    invalid_discount_rows,
    "discount_pct"
] = rng.uniform(
    101,
    150,
    len(invalid_discount_rows)
).round(2)

# Intentional missing unit price
missing_price_rows = rng.choice(
    order_items.index,
    size=max(1, int(len(order_items) * 0.005)),
    replace=False
)

order_items.loc[
    missing_price_rows,
    "unit_price"
] = np.nan

order_items.to_csv(
    RAW_DATA_DIR / "order_items.csv",
    index=False
)

print(
    f"Created order_items.csv: "
    f"{len(order_items):,} rows"
)


# ============================================================
# 8. PAYMENTS
# ============================================================

print("Generating payments.csv...")

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Cash on Delivery",
    "Wallet"
]

payment_records = []

for _, order in orders.iterrows():

    order_items_for_order = order_items[
        order_items["order_id"] == order["order_id"]
    ]

    valid_items = order_items_for_order.dropna(
        subset=["unit_price"]
    )

    if len(valid_items) == 0:
        amount = 0
    else:
        amount = (
            valid_items["quantity"]
            .clip(lower=0)
            * valid_items["unit_price"]
            * (
                1
                - valid_items["discount_pct"].clip(
                    lower=0,
                    upper=100
                ) / 100
            )
        ).sum()

    payment_records.append({
        "payment_id": int(order["order_id"]),
        "order_id": int(order["order_id"]),
        "method": rng.choice(payment_methods),
        "status": (
            "Failed"
            if order["status"] == "Cancelled"
            else rng.choice(
                ["Paid", "Paid", "Paid", "Pending"]
            )
        ),
        "amount": round(float(amount), 2),
        "payment_date": order["order_date"]
    })

payments = pd.DataFrame(payment_records)

payments.to_csv(
    RAW_DATA_DIR / "payments.csv",
    index=False
)

print(
    f"Created payments.csv: "
    f"{len(payments):,} rows"
)


# ============================================================
# 9. RETURNS
# ============================================================

print("Generating returns.csv...")

return_count = int(
    len(order_items) * 0.06
)

return_indices = rng.choice(
    order_items.index,
    size=return_count,
    replace=False
)

return_items = order_items.loc[
    return_indices
].copy()

return_reasons = [
    "Damaged",
    "Wrong Product",
    "Size Issue",
    "Quality Issue",
    "Changed Mind",
    "Late Delivery"
]

returns = pd.DataFrame({
    "return_id": np.arange(
        1,
        len(return_items) + 1
    ),

    "order_item_id": return_items[
        "order_item_id"
    ].values,

    "return_date": random_dates(
        "2024-01-05",
        "2026-10-31",
        len(return_items)
    ),

    "reason": rng.choice(
        return_reasons,
        len(return_items)
    ),

    "refund_amount": np.round(
        rng.uniform(
            100,
            20_000,
            len(return_items)
        ),
        2
    )
})

returns.to_csv(
    RAW_DATA_DIR / "returns.csv",
    index=False
)

print(
    f"Created returns.csv: "
    f"{len(returns):,} rows"
)


# ============================================================
# 10. INVENTORY
# ============================================================

print("Generating inventory.csv...")

inventory_dates = pd.date_range(
    start="2024-01-01",
    end="2026-12-01",
    freq="MS"
)

inventory_records = []

inventory_id = 1

for snapshot_date in inventory_dates:

    # One snapshot for every product
    stock_values = rng.integers(
        0,
        2_000,
        N_PRODUCTS
    )

    reorder_values = rng.integers(
        50,
        300,
        N_PRODUCTS
    )

    for product_id, stock, reorder_level in zip(
        products["product_id"],
        stock_values,
        reorder_values
    ):

        inventory_records.append({
            "inventory_id": inventory_id,
            "product_id": int(product_id),
            "snapshot_date": snapshot_date,
            "stock_on_hand": int(stock),
            "reorder_level": int(reorder_level)
        })

        inventory_id += 1


inventory = pd.DataFrame(inventory_records)

inventory.to_csv(
    RAW_DATA_DIR / "inventory.csv",
    index=False
)

print(
    f"Created inventory.csv: "
    f"{len(inventory):,} rows"
)


# ============================================================
# 11. CREATE PROBLEM MANIFEST
# ============================================================

print("Creating problem_manifest.csv...")

problem_manifest = pd.DataFrame([
    {
        "table_name": "customers",
        "issue_type": "Missing values",
        "description": "Some customer email values are missing."
    },
    {
        "table_name": "products",
        "issue_type": "Inconsistent values",
        "description": "Some product names contain inconsistent naming patterns."
    },
    {
        "table_name": "orders",
        "issue_type": "Invalid dates",
        "description": "Some delivery dates occur before the order date."
    },
    {
        "table_name": "order_items",
        "issue_type": "Invalid quantity",
        "description": "Some order items contain zero or negative quantities."
    },
    {
        "table_name": "order_items",
        "issue_type": "Abnormal discount",
        "description": "Some order items contain discounts above 100 percent."
    },
    {
        "table_name": "order_items",
        "issue_type": "Missing values",
        "description": "Some unit prices are missing."
    }
])

problem_manifest.to_csv(
    RAW_DATA_DIR / "problem_manifest.csv",
    index=False
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("DATA GENERATION COMPLETED")
print("=" * 60)

print(f"Raw data location: {RAW_DATA_DIR}")

print("\nGenerated files:")

for file in sorted(RAW_DATA_DIR.glob("*.csv")):
    print(f"  - {file.name}")

print("\nDataset generation finished successfully.")
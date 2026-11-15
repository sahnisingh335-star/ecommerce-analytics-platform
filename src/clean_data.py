from pathlib import Path
import pandas as pd

# Paths work no matter which folder the script is run from
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
CLEAN_DIR = BASE_DIR / "data" / "cleaned"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)


# =========================================================
# 1. ORDER ITEMS CLEANING
# =========================================================

order_items = pd.read_csv(RAW_DIR / "order_items.csv")

print("\n========== ORDER ITEMS CLEANING ==========")
print("Original rows:", len(order_items))

# Remove invalid quantity
invalid_quantity = order_items["quantity"] <= 0
print("Invalid quantity:", invalid_quantity.sum())

order_items = order_items[~invalid_quantity].copy()

# Remove discount above 100%
invalid_discount = (
    (order_items["discount_pct"] < 0)
    | (order_items["discount_pct"] > 100)
)

print("Invalid discount:", invalid_discount.sum())

order_items = order_items[~invalid_discount].copy()

# Fill missing unit_price using product list_price
products = pd.read_csv(RAW_DIR / "products.csv")

order_items = order_items.merge(
    products[["product_id", "list_price"]],
    on="product_id",
    how="left"
)

missing_price = order_items["unit_price"].isna()
print("Missing unit_price:", missing_price.sum())

order_items.loc[missing_price, "unit_price"] = (
    order_items.loc[missing_price, "list_price"]
)

order_items.drop(columns=["list_price"], inplace=True)

print("Remaining missing unit_price:",
      order_items["unit_price"].isna().sum())

print("Final order_items rows:", len(order_items))

order_items.to_csv(
    CLEAN_DIR / "order_items.csv",
    index=False
)


# =========================================================
# 2. CUSTOMERS CLEANING
# =========================================================

customers = pd.read_csv(RAW_DIR / "customers.csv")

print("\n========== CUSTOMERS CLEANING ==========")

# Keep missing emails as missing.
# We do NOT invent fake customer emails.
customers.to_csv(
    CLEAN_DIR / "customers.csv",
    index=False
)

print("Customers saved:", len(customers))


# =========================================================
# 3. ORDERS CLEANING
# =========================================================

orders = pd.read_csv(RAW_DIR / "orders.csv")

print("\n========== ORDERS CLEANING ==========")

orders["order_date"] = pd.to_datetime(orders["order_date"])
orders["delivery_date"] = pd.to_datetime(orders["delivery_date"])

invalid_delivery = orders["delivery_date"] < orders["order_date"]

print("Invalid delivery dates:", invalid_delivery.sum())

# Set logically impossible delivery dates to missing
orders.loc[invalid_delivery, "delivery_date"] = pd.NaT

orders.to_csv(
    CLEAN_DIR / "orders.csv",
    index=False
)

print("Orders saved:", len(orders))


# =========================================================
# 4. PRODUCTS
# =========================================================

products = pd.read_csv(RAW_DIR / "products.csv")

print("\n========== PRODUCTS CLEANING ==========")

# Product-name standardization
# Rule: names follow "<Tier> <Brand> Product <id>".
# Some names carry an extra " - new" suffix -> remove it
# and collapse repeated spaces.
products["product_name"] = (
    products["product_name"]
    .astype(str)
    .str.strip()
)

bad_suffix = products["product_name"].str.contains(
    r"\s*-\s*new$", case=False, regex=True
)
print("Product names with ' - new' suffix:", bad_suffix.sum())

products["product_name"] = (
    products["product_name"]
    .str.replace(r"\s*-\s*new$", "", case=False, regex=True)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

products.to_csv(
    CLEAN_DIR / "products.csv",
    index=False
)

print("\nProducts saved:", len(products))


# =========================================================
# 5. PAYMENTS
# =========================================================

payments = pd.read_csv(RAW_DIR / "payments.csv")

print("\n========== PAYMENTS ==========")

invalid_payment = payments["amount"] <= 0

print("Invalid payment amounts:", invalid_payment.sum())

# Rule: a valid payment amount equals the order total
# (sum of quantity * unit_price * (1 - discount_pct / 100)
# over the cleaned order items). For invalid (<= 0) amounts
# we derive the amount from that order total.
# If the order has no valid order items left, the amount
# cannot be derived, so it is set to missing (NaN) instead
# of inventing a value.
order_totals = (
    order_items.assign(
        item_total=lambda d: d["quantity"]
        * d["unit_price"]
        * (1 - d["discount_pct"] / 100)
    )
    .groupby("order_id")["item_total"]
    .sum()
    .round(2)
)

derived_amount = payments.loc[invalid_payment, "order_id"].map(order_totals)

payments.loc[invalid_payment, "amount"] = derived_amount

print("Payment amounts derived from order total:",
      derived_amount.notna().sum())
print("Payment amounts set to missing (no valid items):",
      derived_amount.isna().sum())

payments.to_csv(
    CLEAN_DIR / "payments.csv",
    index=False
)

print("Payments saved:", len(payments))


# =========================================================
# 6. RETURNS
# =========================================================

returns = pd.read_csv(RAW_DIR / "returns.csv")

print("\n========== RETURNS ==========")

# Rule: a return must point to an order item that still
# exists after order-item cleaning.
orphan_returns = ~returns["order_item_id"].isin(
    order_items["order_item_id"]
)

print("Returns linked to removed order items:",
      orphan_returns.sum())

returns = returns[~orphan_returns].copy()

returns.to_csv(
    CLEAN_DIR / "returns.csv",
    index=False
)

print("Returns saved:", len(returns))


print("\n========================================")
print("DATA CLEANING COMPLETED")
print("========================================")
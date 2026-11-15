"""
Apply the new cleaning rules to the existing Supabase tables.

Run this ONCE after `python src/clean_data.py`.

What it changes (targeted UPDATEs only, no tables are dropped):
  1. products.product_name  -> removes the " - new" suffix (10 rows)
  2. payments.amount        -> replaces zero amounts with the order total
                               (104 rows). For 85 orders with no valid
                               items the amount is set to NULL - or left
                               at 0 if the column does not allow NULL.

Everything runs in one transaction: if any step fails, nothing changes.
Safe to run more than once. The password is never printed.
"""

import os
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

db_url = os.getenv("SUPABASE_DB_URL")

if not db_url:
    raise ValueError("SUPABASE_DB_URL is missing in .env")

BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_DIR = BASE_DIR / "data" / "cleaned"
RAW_DIR = BASE_DIR / "data" / "raw"


# --------------------------------------------------------------
# 1. Rows that need to change (raw vs cleaned)
# --------------------------------------------------------------

raw_products = pd.read_csv(RAW_DIR / "products.csv")
clean_products = pd.read_csv(CLEAN_DIR / "products.csv")

products_to_fix = clean_products.merge(
    raw_products[["product_id", "product_name"]],
    on="product_id",
    suffixes=("", "_raw"),
)
products_to_fix = products_to_fix[
    products_to_fix["product_name"] != products_to_fix["product_name_raw"]
]

raw_payments = pd.read_csv(RAW_DIR / "payments.csv")
clean_payments = pd.read_csv(CLEAN_DIR / "payments.csv")

payment_ids = raw_payments.loc[raw_payments["amount"] <= 0, "payment_id"]
payments_to_fix = clean_payments[
    clean_payments["payment_id"].isin(payment_ids)
]

print("=" * 60)
print("APPLY CLEANING FIXES TO SUPABASE")
print("=" * 60)
print(f"Product names to update:   {len(products_to_fix)}")
print(f"Payment amounts to update: {len(payments_to_fix)}")
sys.stdout.flush()


def column_info(connection, table, column):
    """Return (data_type, is_nullable) of a column, or None."""

    return connection.execute(
        text(
            "SELECT data_type, is_nullable "
            "FROM information_schema.columns "
            "WHERE table_schema = 'public' "
            "AND table_name = :t AND column_name = :c"
        ),
        {"t": table, "c": column},
    ).fetchone()


def id_value(value, data_type):
    """Pass IDs as text if the column was imported as text."""

    if data_type in ("text", "character varying"):
        return str(int(value))

    return int(value)


engine = create_engine(
    db_url,
    connect_args={"connect_timeout": 15, "sslmode": "require"},
)

try:

    with engine.begin() as connection:

        # Stop with an error instead of waiting forever on a locked row
        connection.execute(text("SET LOCAL statement_timeout = '60s'"))

        # ----------------------------------------------------------
        # 2. Check the table columns first
        # ----------------------------------------------------------

        product_id_info = column_info(connection, "products", "product_id")
        payment_id_info = column_info(connection, "payments", "payment_id")
        amount_info = column_info(connection, "payments", "amount")

        for name, info in [
            ("products.product_id", product_id_info),
            ("payments.payment_id", payment_id_info),
            ("payments.amount", amount_info),
        ]:
            if info is None:
                raise RuntimeError(
                    f"Column {name} not found in the public schema. "
                    "Check the table and column names in Supabase."
                )
            print(f"{name}: type={info[0]}, nullable={info[1]}")

        amount_allows_null = amount_info[1] == "YES"

        # ----------------------------------------------------------
        # 3. Product names
        # ----------------------------------------------------------

        print("\nUpdating product names...")
        sys.stdout.flush()

        connection.execute(
            text(
                "UPDATE products SET product_name = :name "
                "WHERE product_id = :pid"
            ),
            [
                {
                    "name": row.product_name,
                    "pid": id_value(row.product_id, product_id_info[0]),
                }
                for row in products_to_fix.itertuples(index=False)
            ],
        )

        print("Product names updated.")

        # ----------------------------------------------------------
        # 4. Payment amounts
        # ----------------------------------------------------------

        derived = payments_to_fix[payments_to_fix["amount"].notna()]
        unknown = payments_to_fix[payments_to_fix["amount"].isna()]

        print("\nUpdating payment amounts...")
        sys.stdout.flush()

        if len(derived):
            connection.execute(
                text(
                    "UPDATE payments SET amount = :amount "
                    "WHERE payment_id = :pid"
                ),
                [
                    {
                        "amount": float(row.amount),
                        "pid": id_value(row.payment_id, payment_id_info[0]),
                    }
                    for row in derived.itertuples(index=False)
                ],
            )

        print(f"Amounts set from order total: {len(derived)}")

        if len(unknown):

            if amount_allows_null:

                connection.execute(
                    text(
                        "UPDATE payments SET amount = NULL "
                        "WHERE payment_id = :pid"
                    ),
                    [
                        {"pid": id_value(row.payment_id, payment_id_info[0])}
                        for row in unknown.itertuples(index=False)
                    ],
                )

                print(f"Amounts set to NULL (no valid items): {len(unknown)}")

            else:

                print(
                    f"Amounts left at 0 (no valid items): {len(unknown)} "
                    "- the amount column does not allow NULL."
                )

        # ----------------------------------------------------------
        # 5. Check
        # ----------------------------------------------------------

        remaining_bad = connection.execute(
            text("SELECT COUNT(*) FROM payments WHERE amount <= 0")
        ).scalar()

        remaining_new = connection.execute(
            text(
                "SELECT COUNT(*) FROM products "
                "WHERE product_name ILIKE '%- new'"
            )
        ).scalar()

except Exception as error:

    # Database error messages do not contain the password.
    print("\nFAILED - nothing was changed (transaction rolled back).")
    print(f"Error type: {type(error).__name__}")
    print(f"Error: {str(error).splitlines()[0]}")
    sys.exit(1)

print()
print(f"Payments with amount <= 0 now: {remaining_bad}")
print(f"Products ending with '- new' now: {remaining_new}")
print("SUCCESS: database updated.")

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import make_url

load_dotenv()

db_url = os.getenv("SUPABASE_DB_URL")

if not db_url:
    raise ValueError("SUPABASE_DB_URL is missing in .env")

# Show where we are connecting (password is NOT printed)
url = make_url(db_url)
print(f"Connecting to host: {url.host}, port: {url.port}, user: {url.username}")

engine = create_engine(
    db_url,
    connect_args={"connect_timeout": 10, "sslmode": "require"},
)

with engine.connect() as connection:
    result = connection.execute(text("SELECT version();"))

    print("Database connection successful!")
    print(result.fetchone()[0])

    inspector = inspect(engine)
    for table in inspector.get_table_names(schema="public"):
        count = connection.execute(text(f'SELECT COUNT(*) FROM "{table}"')).scalar()
        print(f"Table: {table} | Rows: {count}")
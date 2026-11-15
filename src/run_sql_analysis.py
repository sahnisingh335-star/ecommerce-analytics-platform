import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load .env
load_dotenv()

db_url = os.getenv("SUPABASE_DB_URL")

if not db_url:
    raise ValueError("SUPABASE_DB_URL is missing in .env")

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

SQL_FILE = BASE_DIR / "sql" / "analysis" / "business_questions.sql"
OUTPUT_DIR = BASE_DIR / "reports" / "sql_results"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Database connection
engine = create_engine(db_url)

# Read SQL file
sql_text = SQL_FILE.read_text(encoding="utf-8")

# Split queries using -- Q comments
queries = []

current_title = None
current_query = []

for line in sql_text.splitlines():

    stripped = line.strip()

    if stripped.startswith("-- Q"):

        if current_title and current_query:
            queries.append(
                (
                    current_title,
                    "\n".join(current_query).strip()
                )
            )

        current_title = stripped.replace("-- ", "")
        current_query = []

    else:
        current_query.append(line)

# Add final query
if current_title and current_query:
    queries.append(
        (
            current_title,
            "\n".join(current_query).strip()
        )
    )

print("=" * 60)
print("SQL BUSINESS ANALYSIS")
print("=" * 60)
print(f"Total queries found: {len(queries)}")

successful = 0
failed = 0

with engine.connect() as connection:

    for index, (title, query) in enumerate(queries, start=1):

        print()
        print("-" * 60)
        print(f"Running Q{index}: {title}")
        print("-" * 60)

        try:
            query = query.rstrip().rstrip(";")

            result = connection.execute(text(query))

            rows = result.fetchall()
            columns = result.keys()

            df = pd.DataFrame(rows, columns=columns)

            safe_title = (
                title.lower()
                .replace(" ", "_")
                .replace("/", "_")
                .replace("&", "and")
                .replace(":", "")
            )

            output_file = (
                OUTPUT_DIR /
                f"q{index:02d}_{safe_title}.csv"
            )

            df.to_csv(output_file, index=False)

            print(f"Rows returned: {len(df)}")
            print(f"Saved: {output_file}")

            successful += 1

        except Exception as error:

            print(f"ERROR in Q{index}")
            print(error)

            failed += 1

print()
print("=" * 60)
print("ANALYSIS COMPLETED")
print("=" * 60)

print(f"Successful queries: {successful}")
print(f"Failed queries:     {failed}")
print(f"Results folder:     {OUTPUT_DIR}")

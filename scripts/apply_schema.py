import os
from pathlib import Path
from dotenv import load_dotenv
import psycopg

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
schema = (ROOT / "sql" / "schema.sql").read_text()

with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
    conn.execute(schema)
    conn.commit()
    print("Tabelle:", conn.execute("SHOW TABLES").fetchall())
    for idx in conn.execute("SHOW INDEXES FROM detections").fetchall():
        print(idx)

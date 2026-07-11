import os, sys
from pathlib import Path
from dotenv import load_dotenv
import psycopg

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
sql = (ROOT / "sql" / sys.argv[1]).read_text()

with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
    conn.execute(sql)
    conn.commit()
    cols = conn.execute("SHOW COLUMNS FROM detections").fetchall()
    for c in cols:
        print(c[0], c[1])

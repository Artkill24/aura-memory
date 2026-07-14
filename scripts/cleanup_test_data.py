import os
from pathlib import Path
from dotenv import load_dotenv
import psycopg

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
    n = conn.execute("DELETE FROM detections WHERE media_hash = 'test_hash_001'").rowcount
    conn.commit()
    print(f"Rimosse {n} righe di test")
    print("Rimaste:", conn.execute("SELECT count(*) FROM detections").fetchone()[0])

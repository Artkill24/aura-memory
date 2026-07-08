import os, random
from pathlib import Path
from dotenv import load_dotenv
import psycopg

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
vec = str([round(random.random(), 4) for _ in range(1024)])

with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
    conn.execute("""
        INSERT INTO detections (media_hash, media_type, verdict, confidence, embedding)
        VALUES ('test_hash_001', 'image', 'deepfake', 0.9731, %s)
    """, (vec,))
    conn.commit()
    row = conn.execute("""
        SELECT detection_id, verdict, confidence, embedding <=> %s AS distance
        FROM detections
        ORDER BY embedding <=> %s
        LIMIT 3
    """, (vec, vec)).fetchone()
    print("Match più vicino:", row)

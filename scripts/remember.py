"""AURA Memory core loop: embed -> recall -> store."""
import hashlib
import os
import sys
from pathlib import Path

import psycopg
from dotenv import load_dotenv

from embed import embed_image

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

def remember(image_path: str, verdict: str = "unknown", confidence: float = 0.0):
    emb = str(embed_image(image_path))
    media_hash = hashlib.sha256(open(image_path, "rb").read()).hexdigest()

    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        matches = conn.execute("""
            SELECT media_hash, verdict, confidence, embedding <=> %s AS distance
            FROM detections
            WHERE embedding IS NOT NULL
            ORDER BY embedding <=> %s
            LIMIT 3
        """, (emb, emb)).fetchall()

        if matches:
            print("Memoria — media simili già visti:")
            for m in matches:
                print(f"  hash={m[0][:12]}…  verdict={m[1]}  conf={m[2]}  distance={m[3]:.4f}")
        else:
            print("Memoria vuota: primo media di questo tipo.")

        conn.execute("""
            INSERT INTO detections (media_hash, media_type, verdict, confidence, embedding)
            VALUES (%s, 'image', %s, %s, %s)
        """, (media_hash, verdict, confidence, emb))
        conn.commit()
        print(f"Memorizzato: {media_hash[:12]}…")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Uso: python3 scripts/remember.py <immagine> [verdict] [confidence]")
    remember(
        sys.argv[1],
        sys.argv[2] if len(sys.argv) > 2 else "unknown",
        float(sys.argv[3]) if len(sys.argv) > 3 else 0.0,
    )

"""AURA Memory — S3-triggered Lambda: embed -> recall -> store."""
import base64
import hashlib
import json
import os
import urllib.parse

import boto3
import psycopg

s3 = boto3.client("s3")
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

MODEL_ID = "amazon.titan-embed-image-v1"


def embed_image(path: str) -> list[float]:
    with open(path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()
    resp = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps({"inputImage": image_b64}),
    )
    return json.loads(resp["body"].read())["embedding"]


def lambda_handler(event, context):
    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])

    local = f"/tmp/{os.path.basename(key)}"
    s3.download_file(bucket, key, local)

    emb = str(embed_image(local))
    media_hash = hashlib.sha256(open(local, "rb").read()).hexdigest()
    s3_uri = f"s3://{bucket}/{key}"

    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        matches = conn.execute("""
            SELECT media_hash, verdict, confidence, embedding <=> %s AS distance
            FROM detections
            WHERE embedding IS NOT NULL
            ORDER BY embedding <=> %s
            LIMIT 3
        """, (emb, emb)).fetchall()

        conn.execute("""
            INSERT INTO detections (media_hash, media_type, s3_uri, verdict, confidence, embedding)
            VALUES (%s, 'image', %s, 'unknown', 0.0, %s)
        """, (media_hash, s3_uri, emb))
        conn.commit()

    result = {
        "stored": media_hash[:12],
        "s3_uri": s3_uri,
        "similar": [
            {"hash": m[0][:12], "verdict": m[1], "distance": round(float(m[3]), 4)}
            for m in matches
        ],
    }
    print(json.dumps(result))
    return result

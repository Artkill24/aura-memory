"""Generate a 1024-dim embedding for an image via Amazon Titan Multimodal."""
import base64
import json
import sys

import boto3

MODEL_ID = "amazon.titan-embed-image-v1"

def embed_image(image_path: str) -> list[float]:
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    response = client.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps({"inputImage": image_b64}),
    )
    return json.loads(response["body"].read())["embedding"]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Uso: python3 scripts/embed.py <immagine>")
    emb = embed_image(sys.argv[1])
    print(f"Embedding: {len(emb)} dimensioni")
    print(f"Prime 5: {emb[:5]}")

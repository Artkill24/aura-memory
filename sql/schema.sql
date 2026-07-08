-- AURA Memory — Forensic detection memory layer
-- CockroachDB with distributed vector indexing

CREATE TABLE IF NOT EXISTS detections (
  detection_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  media_hash STRING NOT NULL,
  media_type STRING NOT NULL,
  s3_uri STRING,
  verdict STRING NOT NULL,
  confidence DECIMAL(5,4),
  layer_scores JSONB,
  embedding VECTOR(1024),
  suspected_generator STRING,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_det_hash ON detections (media_hash);
CREATE VECTOR INDEX IF NOT EXISTS idx_det_embedding ON detections (embedding);

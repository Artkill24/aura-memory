-- Job state + real verdict fields on the forensic memory table
ALTER TABLE detections ADD COLUMN IF NOT EXISTS status STRING NOT NULL DEFAULT 'done';
ALTER TABLE detections ADD COLUMN IF NOT EXISTS composite_score DECIMAL(5,4);
ALTER TABLE detections ADD COLUMN IF NOT EXISTS pdf_url STRING;
ALTER TABLE detections ADD COLUMN IF NOT EXISTS filename STRING;
ALTER TABLE detections ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT now();
CREATE INDEX IF NOT EXISTS idx_det_status ON detections (status);

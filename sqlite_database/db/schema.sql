CREATE TABLE IF NOT EXISTS detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT NOT NULL,
    img_raw BLOB NOT NULL,
    img_detect BLOB NOT NULL,
    defect TEXT,
    barcode TEXT
);
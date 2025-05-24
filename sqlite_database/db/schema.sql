CREATE TABLE IF NOT EXISTS detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT,
    img_raw BLOB,
    img_detect BLOB,,
    defect TEXT,
    barcode TEXT
);
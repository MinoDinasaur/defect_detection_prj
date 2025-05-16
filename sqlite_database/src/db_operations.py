import sqlite3
from datetime import datetime
from sqlite3 import Error
import os
import cv2
import sys
from datetime import datetime

def save_detection_to_db(db_path, img_raw, img_detect, defect):
    """
    Save detection data to the SQLite database.

    Args:
        db_path (str): Path to the SQLite database file.
        img_raw (bytes): Raw image data (binary).
        img_detect (bytes): Detected image data (binary).
        defect (str): Detected defect description.
    """
    # Get the current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert data into the detections table
    query = """
    INSERT INTO detections (time, img_raw, img_detect, defect, barcode)
    VALUES (?, ?, ?, ?, NULL);
    """
    cursor.execute(query, (current_time, img_raw, img_detect, defect))

    # Commit and close the connection
    conn.commit()
    conn.close()

def save_to_db(img_raw_path, img_with_boxes, result_obj):
    """
    Save the raw image, detected image, and defect information to the database.

    Args:
        img_raw_path (str): Path to the raw image file.
        img_with_boxes (numpy.ndarray): Image with bounding boxes drawn.
        result_obj (object): Detection result object containing defect information.
    """
    try:
        # Save the detected image to a file
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        detected_path = f"/home/ducanh/Desktop/DATN/DB/images_origin_detect/detected/{timestamp}_detected.png"
        cv2.imwrite(detected_path, img_with_boxes)

        # Read raw and detected images as binary data
        with open(img_raw_path, "rb") as raw_file:
            img_raw = raw_file.read()
        with open(detected_path, "rb") as detected_file:
            img_detect = detected_file.read()

        # Extract defect information
        classes = result_obj.names
        boxes = result_obj.boxes
        labels = boxes.cls.cpu().tolist() if boxes is not None else []
        confidences = boxes.conf.cpu().tolist() if boxes is not None else []

        # Filter out OK class
        defect_indices = [(i, cls_id) for i, cls_id in enumerate(labels) if classes[int(cls_id)].lower() != "ok"]

        # Save each defect to the database
        for i, cls_id in defect_indices:
            defect_name = classes[int(cls_id)]
            confidence = confidences[i] * 100
            defect_info = f"{defect_name} ({confidence:.2f}%)"

            save_detection_to_db(
                db_path="sqlite_database/db/detections.db",
                img_raw=img_raw,
                img_detect=img_detect,
                defect=defect_info
            )

        print("Data saved to database successfully.")

    except Exception as e:
        print(f"Error saving to database: {e}")
    
def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    import sqlite3
    from sqlite3 import Error

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_table(conn):
    """Create the table in the database."""
    sql_create_table = """CREATE TABLE IF NOT EXISTS records (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            time TEXT NOT NULL,
                            img_raw BLOB NOT NULL,
                            img_detect BLOB NOT NULL,
                            defect TEXT,
                            barcode TEXT
                        );"""
    try:
        c = conn.cursor()
        c.execute(sql_create_table)
    except Error as e:
        print(e)


def insert_record(conn, record):
    """Insert a new record into the records table."""
    sql_insert_record = '''INSERT INTO records(time, img_raw, img_detect, defect, barcode)
                           VALUES(?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql_insert_record, record)
    conn.commit()
    return cur.lastrowid


def query_records(conn):
    """Query all rows in the records table."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM records")

    rows = cur.fetchall()
    return rows


def update_record(conn, record):
    """Update a record in the records table."""
    sql_update_record = '''UPDATE records
                           SET time = ?,
                               img_raw = ?,
                               img_detect = ?,
                               defect = ?,
                               barcode = ?
                           WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql_update_record, record)
    conn.commit()


def delete_record(conn, id):
    """Delete a record by record id."""
    sql_delete_record = 'DELETE FROM records WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql_delete_record, (id,))
    conn.commit()
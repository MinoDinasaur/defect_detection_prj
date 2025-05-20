import sqlite3
from datetime import datetime
from sqlite3 import Error
import os
import cv2
import sys
from datetime import datetime

DB_PATH = 'sqlite_database/db/detections.db'

#Helper function
def execute_query(query, params=None, fetch=False):
    """
    Execute a query on the database.

    Args:
        query (str): SQL query to execute.
        params (tuple): Parameters for the query.
        fetch (bool): Whether to fetch results.

    Returns:
        list: Query results if fetch is True, otherwise None.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        if fetch:
            results = cursor.fetchall()
            conn.close()
            return results
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database query error: {e}")
    return None

def save_detection_to_db(img_raw, img_detect, defect):
    """
    Save detection data to the SQLite database.

    Args:
        img_raw (bytes): Raw image data (binary).
        img_detect (bytes): Detected image data (binary).
        defect (str): Detected defect description.
    """
    # Get the current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert data into the detections table
    query = """
    INSERT INTO detections (time, img_raw, img_detect, defect, barcode)
    VALUES (?, ?, ?, ?, NULL);
    """
    execute_query(query, (current_time, img_raw, img_detect, defect))

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

            save_detection_to_db(img_raw, img_detect, defect_info)

        print("Data saved to database successfully.")

    except Exception as e:
        print(f"Error saving to database: {e}")

def create_database():
    """Check if the database exists; if not, create it and initialize tables."""
    # Ensure the directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # Check if the database file exists
    if not os.path.exists(DB_PATH):
        try:
            query = '''
                CREATE TABLE IF NOT EXISTS detections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    time TEXT NOT NULL,
                    img_raw BLOB NOT NULL,
                    img_detect BLOB NOT NULL,
                    defect TEXT,
                    barcode TEXT
                )
            '''
            execute_query(query)
            print(f"Database created at {DB_PATH}")
        except Exception as e:
            print(f"Error creating database: {str(e)}")
    else:
        print(f"Database already exists at {DB_PATH}")

def create_connection():
    """Create a database connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except Error as e:
        print(e)
    return None

def get_defect_types():
    """Fetch distinct defect types from the database."""
    query = "SELECT DISTINCT defect FROM detections"
    return execute_query(query, fetch=True)

def get_detections(date_from, date_to, defect_filter=None):
    """
    Fetch detection records based on filters.

    Args:
        date_from (str): Start date in 'YYYY-MM-DD' format.
        date_to (str): End date in 'YYYY-MM-DD' format.
        defect_filter (str): Filter for defect type (optional).

    Returns:
        list: List of detection records.
    """
    query = "SELECT rowid, time, img_raw, img_detect, defect, barcode FROM detections WHERE time BETWEEN ? AND ?"
    params = [date_from, date_to]

    if defect_filter and defect_filter != "All":
        if defect_filter == "No defects":
            query += " AND defect = ?"
            params.append("No defects")
        else:
            query += " AND defect LIKE ?"
            params.append(f"%{defect_filter}%")

    query += " ORDER BY time DESC"
    return execute_query(query, params, fetch=True)

def get_image_data(row_id, image_type):
    """
    Fetch image data (raw or detection) for a specific row ID.

    Args:
        row_id (int): The ID of the detection record.
        image_type (str): The column name ('img_raw' or 'img_detect').

    Returns:
        bytes: Image data as binary.
    """
    query = f"SELECT {image_type} FROM detections WHERE rowid = ?"
    result = execute_query(query, (row_id,), fetch=True)
    return result[0][0] if result and result[0][0] else None

def delete_detection_from_db(row_id):
    """
    Delete a detection record from the database by its row ID.

    Args:
        row_id (int): The ID of the detection record to delete.
    """
    try:
        query = "DELETE FROM detections WHERE rowid = ?"
        execute_query(query, (row_id,))
        print(f"Detection #{row_id} deleted successfully.")
    except Exception as e:
        print(f"Error deleting detection #{row_id}: {str(e)}")

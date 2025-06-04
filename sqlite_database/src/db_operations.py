import sqlite3
from datetime import datetime
from sqlite3 import Error
import os
import cv2
import sys
from datetime import datetime

DB_PATH = 'sqlite_database/db/detections.db'

# Global variable to store scanned barcode temporarily
scanned_barcode = None

def set_scanned_barcode(barcode):
    """
    Set the scanned barcode value.
    
    Args:
        barcode (str): The scanned barcode value
    """
    global scanned_barcode
    scanned_barcode = barcode
    print(f"Barcode set: {barcode}")

def get_scanned_barcode():
    """
    Get the current scanned barcode value.
    
    Returns:
        str: The current scanned barcode or None
    """
    global scanned_barcode
    return scanned_barcode

def reset_scanned_barcode():
    """
    Reset the scanned barcode to None.
    """
    global scanned_barcode
    scanned_barcode = None
    print("Barcode reset")

#Helper function
def execute_query(query, params=None, fetch=False):
    conn = None
    cursor = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        if fetch:
            results = cursor.fetchall()
            return results
        else:
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()  # Rollback transaction
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def save_detection_to_db(img_raw, img_detect, defect, barcode=None):
    """
    Save detection data to the SQLite database.

    Args:
        img_raw (bytes): Raw image data (binary).
        img_detect (bytes): Detected image data (binary).
        defect (str): Detected defect description.
        barcode (str): Barcode information (optional).

    Returns:
        int: The row_id of the inserted record.
    """
    global scanned_barcode
    try:
        # Use provided barcode or fall back to scanned_barcode
        final_barcode = barcode if barcode is not None else scanned_barcode
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = """
        INSERT INTO detections (time, img_raw, img_detect, defect, barcode)
        VALUES (?, ?, ?, ?, ?);
        """
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query, (current_time, img_raw, img_detect, defect, final_barcode))
        conn.commit()
        row_id = cursor.lastrowid
        conn.close()
        
        print(f"Detection saved to database with barcode: {final_barcode}")
        return row_id
    except Exception as e:
        print(f"Error saving detection to database: {e}")
        return None

def save_to_db(img_raw_path, img_with_boxes, result_obj):
    """
    Save the raw image, detected image, and defect information to the database.

    Args:
        img_raw_path (str): Path to the raw image file.
        img_with_boxes (numpy.ndarray): Image with bounding boxes drawn.
        result_obj (object): Detection result object containing defect information.
    """
    global scanned_barcode
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

        # Extract defect information - CHỈ LẤY TÊN, KHÔNG CÓ CONFIDENCE
        classes = result_obj.names
        boxes = result_obj.boxes
        labels = boxes.cls.cpu().tolist() if boxes is not None else []

        # Filter out OK class
        defect_indices = [cls_id for cls_id in labels if classes[int(cls_id)].lower() != "ok"]

        if defect_indices:
            # Get unique defect names only (no confidence scores)
            defect_names = [classes[int(cls_id)] for cls_id in defect_indices]
            unique_defects = list(set(defect_names))  # Remove duplicates
            defect_info = ", ".join(sorted(unique_defects))  # Sort for consistency
        else:
            defect_info = "No defects"

        # Save to database
        save_detection_to_db(img_raw, img_detect, defect_info, barcode=scanned_barcode)

        print("Data saved to database successfully.")
        
        # Reset the barcode after saving to database
        reset_scanned_barcode()

    except Exception as e:
        print(f"Error saving to database: {e}")

def update_detection_in_db(row_id, img_with_boxes, result_obj):
    """
    Update detection data in the SQLite database.

    Args:
        row_id (int): The row ID of the record to update.
        img_with_boxes (numpy.ndarray): Image with bounding boxes drawn.
        result_obj (object): Detection result object containing defect information.
    """
    try:
        # Save the detected image to a file
        detected_path = f"/home/ducanh/Desktop/defect_detection_prj/storage/detected_images/{row_id}_detected.png"
        cv2.imwrite(detected_path, img_with_boxes)

        # Read detected image as binary data
        with open(detected_path, "rb") as detected_file:
            img_detect = detected_file.read()

        # Extract defect information
        classes = result_obj.names
        boxes = result_obj.boxes
        labels = boxes.cls.cpu().tolist() if boxes is not None else []

        # Filter out OK class
        defect_indices = [cls_id for cls_id in labels if classes[int(cls_id)].lower() != "ok"]
        
        if defect_indices:
            # Get unique defect names only (no confidence scores)
            defect_names = [classes[int(cls_id)] for cls_id in defect_indices]
            unique_defects = list(set(defect_names))  # Remove duplicates
            defect_info = ", ".join(sorted(unique_defects))  # Sort for consistency
        else:
            defect_info = "No defects"

        # Update the database record
        query = """
        UPDATE detections
        SET img_detect = ?, defect = ?
        WHERE rowid = ?;
        """
        execute_query(query, (img_detect, defect_info, row_id))
        print(f"Detection record {row_id} updated successfully.")
    except Exception as e:
        print(f"Error updating detection in database: {e}")

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
                    time TEXT,
                    img_raw BLOB,
                    img_detect BLOB,
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

def get_detections_paginated(date_from, date_to, defect_filter=None, page=1, page_size=10):
    """
    Fetch detection records with pagination.
    
    Args:
        date_from (str): Start date in 'YYYY-MM-DD' format.
        date_to (str): End date in 'YYYY-MM-DD' format.
        defect_filter (str): Filter for defect type (optional).
        page (int): Page number (1-based).
        page_size (int): Number of records per page.
    
    Returns:
        tuple: (records, total_count)
    """
    # Base query
    base_query = "SELECT rowid, time, img_raw, img_detect, defect, barcode FROM detections WHERE time BETWEEN ? AND ?"
    count_query = "SELECT COUNT(*) FROM detections WHERE time BETWEEN ? AND ?"
    
    params = [date_from, date_to]
    
    # Add defect filter if specified
    if defect_filter and defect_filter != "All":
        filter_condition = ""
        if defect_filter == "No defects":
            filter_condition = " AND defect = ?"
            params.append("No defects")
        else:
            filter_condition = " AND defect LIKE ?"
            params.append(f"%{defect_filter}%")
        
        base_query += filter_condition
        count_query += filter_condition
    
    # Get total count
    total_result = execute_query(count_query, params, fetch=True)
    total_count = total_result[0][0] if total_result else 0
    
    # Add pagination to main query
    base_query += " ORDER BY time DESC LIMIT ? OFFSET ?"
    offset = (page - 1) * page_size
    params.extend([page_size, offset])
    
    # Get paginated records
    records = execute_query(base_query, params, fetch=True) or []
    
    return records, total_count

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

def get_detection_for_export(row_id):
    """
    Get detection data for export by row ID.
    
    Args:
        row_id (int): The row ID of the detection record.
    
    Returns:
        tuple: (time_str, img_raw, img_detect, defect, barcode) or None if not found
    """
    query = "SELECT time, img_raw, img_detect, defect, barcode FROM detections WHERE rowid = ?"
    result = execute_query(query, (row_id,), fetch=True)
    
    if result and len(result) > 0:
        return result[0]  # Return the first (and should be only) result
    return None

def get_detection_summary(row_id):
    """
    Get detection summary data (without large binary data) for display.
    
    Args:
        row_id (int): The row ID of the detection record.
    
    Returns:
        tuple: (time_str, defect, barcode) or None if not found
    """
    query = "SELECT time, defect, barcode FROM detections WHERE rowid = ?"
    result = execute_query(query, (row_id,), fetch=True)
    
    if result and len(result) > 0:
        return result[0]
    return None

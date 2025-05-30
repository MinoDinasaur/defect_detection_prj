import os
import cv2
from ultralytics import YOLO
from sqlite_database.src.db_operations import get_image_data 
import numpy as np

# Load YOLO model
model = YOLO("./models/v8/bestv8.pt")

def detect_image(row_id):
    """
    Phát hiện lỗi trên ảnh được load từ cơ sở dữ liệu.

    Args:
        row_id (int): ID của bản ghi trong cơ sở dữ liệu.

    Returns:
        results: Kết quả phát hiện từ model YOLO.
    """
    # Lấy dữ liệu ảnh từ cơ sở dữ liệu
    img_raw_data = get_image_data(row_id, "img_raw")
    if img_raw_data is None:
        print(f"[!] Không tìm thấy dữ liệu ảnh với row_id={row_id}")
        return None

    # Chuyển dữ liệu nhị phân thành numpy array
    img_array = cv2.imdecode(np.frombuffer(img_raw_data, np.uint8), cv2.IMREAD_COLOR)
    if img_array is None:
        print(f"[!] Không thể giải mã dữ liệu ảnh từ row_id={row_id}")
        return None

    # Phát hiện lỗi bằng YOLO
    results = model(img_array)
    return results

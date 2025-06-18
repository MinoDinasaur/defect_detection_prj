import os
import cv2
from ultralytics import YOLO
from sqlite_database.src.db_operations import get_image_data 
import numpy as np

# Load YOLO model
model = YOLO("./models/v8/bestv8.onnx")

def plot_results_without_confidence(results, img_array):
    """
    Vẽ bounding boxes KHÔNG CÓ confidence score với màu sắc mới
    
    Args:
        results: YOLO detection results
        img_array: Original image array
        
    Returns:
        img_with_boxes: Image với bounding boxes (no confidence)
    """
    if not results or len(results) == 0:
        return img_array
        
    result = results[0]
    img_with_boxes = img_array.copy()
    
    if result.boxes is not None:
        boxes = result.boxes.xyxy.cpu().numpy()  # Bounding box coordinates
        classes = result.boxes.cls.cpu().numpy()  # Class IDs
        names = result.names  # Class names
        
        # MÀU SẮC MỚI - DỄ NHÌN VÀ TƯƠNG PHẢN TỐT
        colors = [
            (255, 69, 0),     # Red Orange - Cam đỏ
            (255, 20, 147),   # Deep Pink - Hồng đậm  
            (255, 215, 0),    # Gold - Vàng
            (138, 43, 226),   # Blue Violet - Tím xanh
            (0, 255, 127),    # Spring Green - Xanh lá sáng
            (255, 105, 180),  # Hot Pink - Hồng nóng
            (64, 224, 208),   # Turquoise - Xanh ngọc
            (255, 140, 0),    # Dark Orange - Cam đậm
        ]
        
        for i, (box, cls_id) in enumerate(zip(boxes, classes)):
            x1, y1, x2, y2 = map(int, box)
            class_name = names[int(cls_id)]
            
            # Skip "OK" class
            if class_name.lower() == "ok":
                continue
                
            # Get color for this class - CHỌN MÀU THEO CLASS ID
            color = colors[int(cls_id) % len(colors)]
            
            # Draw bounding box với độ dày lớn hơn để nổi bật
            cv2.rectangle(img_with_boxes, (x1, y1), (x2, y2), color, 4)  # Tăng từ 3 lên 4
            
            # Draw label (ONLY CLASS NAME - NO CONFIDENCE)
            label = f"{class_name}"
            
            # Calculate label size với font lớn hơn
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1.0  # Tăng từ 0.8 lên 1.0
            font_thickness = 2
            (label_width, label_height), baseline = cv2.getTextSize(
                label, font, font_scale, font_thickness
            )
            
            # Draw label background với padding lớn hơn
            cv2.rectangle(
                img_with_boxes,
                (x1, y1 - label_height - baseline - 15),  # Tăng padding từ 10 lên 15
                (x1 + label_width + 15, y1),  # Tăng padding từ 10 lên 15
                color,
                -1
            )
            
            # Draw label text
            cv2.putText(
                img_with_boxes,
                label,
                (x1 + 7, y1 - baseline - 7),  # Adjust position
                font,
                font_scale,
                (255, 255, 255),  # White text
                font_thickness
            )
    
    return img_with_boxes

def detect_image_with_custom_plot(row_id):
    """
    Phát hiện lỗi và vẽ bounding boxes KHÔNG CÓ confidence score
    
    Args:
        row_id (int): ID của bản ghi trong cơ sở dữ liệu.
        
    Returns:
        tuple: (img_with_boxes, results) hoặc (None, None) nếu lỗi
    """
    # Lấy dữ liệu ảnh từ cơ sở dữ liệu
    img_raw_data = get_image_data(row_id, "img_raw")
    if img_raw_data is None:
        print(f"[!] Không tìm thấy dữ liệu ảnh với row_id={row_id}")
        return None, None

    # Chuyển dữ liệu nhị phân thành numpy array
    img_array = cv2.imdecode(np.frombuffer(img_raw_data, np.uint8), cv2.IMREAD_COLOR)
    if img_array is None:
        print(f"[!] Không thể giải mã dữ liệu ảnh từ row_id={row_id}")
        return None, None

    # Phát hiện lỗi bằng YOLO
    results = model(img_array)
    
    if results and len(results) > 0:
        # Vẽ bounding boxes WITHOUT confidence
        img_with_boxes = plot_results_without_confidence(results, img_array)
        return img_with_boxes, results[0]
    
    return img_array, None

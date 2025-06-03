# from ultralytics import YOLO
# import cv2
# import os

# model = YOLO("models/v5/best.pt")

# # Các class lỗi cần hiển thị
# VISIBLE_CLASSES = {"miss", "bridge", "lifted"}

# def detect_image(img_path, save_dir="storage/detected_images"):
#     img = cv2.imread(img_path)
#     if img is None:
#         print(f"[!] Không đọc được ảnh từ {img_path}")
#         return None

#     results = model(img)[0]
#     names = model.names  # ví dụ: {0: 'ok', 1: 'miss', 2: 'bridge', 3: 'lifted'}

#     # Vẽ lại bbox cho các class lỗi
#     for box in results.boxes:
#         cls_id = int(box.cls[0])
#         label = names[cls_id]

#         if label not in VISIBLE_CLASSES:
#             continue  # Bỏ qua class 'ok'

#         # Lấy toạ độ bbox
#         x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)

#         # Vẽ khung bbox
#         cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 255), 2)

#         # Ghi tên lỗi lên ảnh
#         cv2.putText(img, label, (x1, y1 - 8),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

#     # Lưu ảnh sau khi vẽ
#     os.makedirs(save_dir, exist_ok=True)
#     out_path = os.path.join(save_dir, "filtered_detected_" + os.path.basename(img_path))
#     cv2.imwrite(out_path, img)
#     print(f"[✓] Ảnh detect đã lưu tại: {out_path}")

#     # Hiển thị ảnh sau detect
#     cv2.imshow("Detected Errors Only", img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#     return out_path

import os
import cv2
from ultralytics import YOLO
from yolov5 import YOLOv5
model = YOLO("/home/ducanh/Desktop/defect_detection_prj/models/v5/best.pt")

def detect_image(image_path):
    if not os.path.exists(image_path):
        return None, None
    img = cv2.imread(image_path)
    results = model(img)
    return results

if __name__ == "__main__":
    image_path = "/home/ducanh/Desktop/defect_detection_prj/storage/captured_images/captured_image_20250514_114209.png"  # Thay đổi đường dẫn ảnh
    results = detect_image(image_path)
    print (results)

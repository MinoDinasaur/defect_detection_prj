# camera/basler_camera.py

from pypylon import pylon
import cv2
import os
from datetime import datetime

def capture_image(save_dir="storage/captured_images"):
    os.makedirs(save_dir, exist_ok=True)

    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

    try:
        camera.Open()
        camera.StartGrabbingMax(1)

        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        grab_result = camera.RetrieveResult(2000, pylon.TimeoutHandling_ThrowException)

        image_path = None
        if grab_result.GrabSucceeded():
            image = converter.Convert(grab_result)
            img = image.GetArray()

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = os.path.join(save_dir, f"captured_image_{timestamp}.png")
            cv2.imwrite(image_path, img)

            print(f"[✓] Ảnh đã được lưu tại: {image_path}")
        else:
            print("[!] Grab thất bại")

        grab_result.Release()
        return image_path

    except Exception as e:
        print(f"[!] Lỗi khi chụp ảnh: {e}")
        return None

    finally:
        if camera.IsGrabbing():
            camera.StopGrabbing()
        if camera.IsOpen():
            camera.Close()

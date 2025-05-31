import os
import cv2
from pypylon import pylon

import os
import cv2
from pypylon import pylon
from sqlite_database.src.db_operations import save_detection_to_db  # Import the database function

class PylonCamera:
    def __init__(self, save_dir="/home/ducanh/Desktop/defect_detection_prj"):
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

        # Initialize the camera but do not open it yet
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

    def capture_image(self, timeout=1000):
        """
        Capture an image and save it directly to the database.

        Args:
            timeout (int): Timeout for capturing the image.

        Returns:
            int: The row_id of the saved image in the database, or None if failed.
        """
        try:
            # Open the camera
            self.camera.Open()

            # Capture an image with a timeout
            grab_result = self.camera.GrabOne(timeout)

            if grab_result.GrabSucceeded():
                # Get the image as a numpy array (OpenCV format)
                img = grab_result.Array

                # Encode the image as binary data
                _, img_encoded = cv2.imencode('.png', img)
                img_binary = img_encoded.tobytes()

                # Save the image to the database (only raw image)
                row_id = save_detection_to_db(img_binary, None, None)
                return row_id
            else:
                return None
        except Exception as e:
            print(f"Error capturing image: {e}")
            return None
        finally:
            # Close the camera to release resources
            self.camera.Close()

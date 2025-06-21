import os
import cv2
from pypylon import pylon
from sqlite_database.src.db_operations import save_detection_to_db  # Import the database function

class PylonCamera:
    def __init__(self):
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
            print(f"Error capturing image")
            return None
        finally:
            # Close the camera to release resources
            self.camera.Close()

    # def capture_image_from_file(self, file_path = "./storage/captured_images/captured_image_20250514_115546.png"):
    #     """
    #     Load an image from file and save it to the database (for testing purposes).

    #     Args:
    #         file_path (str): Path to the image file to load.

    #     Returns:
    #         int: The row_id of the saved image in the database, or None if failed.
    #     """
    #     try:
    #         # Check if file exists
    #         if not os.path.exists(file_path):
    #             print(f"Error: File not found: {file_path}")
    #             return None
            
    #         # Load the image from file
    #         img = cv2.imread(file_path)
            
    #         if img is None:
    #             print(f"Error: Could not load image from {file_path}")
    #             return None
            
    #         # Encode the image as binary data
    #         _, img_encoded = cv2.imencode('.png', img)
    #         img_binary = img_encoded.tobytes()

    #         # Save the image to the database (only raw image)
    #         row_id = save_detection_to_db(img_binary, None, None)
    #         print(f"Test image loaded from {file_path} and saved to database with row_id: {row_id}")
    #         return row_id
            
    #     except Exception as e:
    #         print(f"Error loading image from file: {e}")
    #         return None
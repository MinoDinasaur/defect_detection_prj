# from PySide6.QtWidgets import QApplication
# import sys
# from app.ui.main_window import DefectDetectionApp  

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     win = DefectDetectionApp()
#     win.show()
#     sys.exit(app.exec())

# import sys
# from PySide6.QtWidgets import QApplication
# from PySide6.QtGui import QFont
# from app.ui.main_window import DefectDetectionApp

# # Main entry point of the application
# if __name__ == "__main__":
#     # Initialize the application
#     app = QApplication(sys.argv)
    
#     # Set application-wide style and font
#     app.setStyle("Fusion")
#     font = QFont("Segoe UI", 10)
#     app.setFont(font)
    
#     # Create and display the main window
#     main_window = DefectDetectionApp()
#     main_window.show()
    
#     # Execute the application event loop
#     sys.exit(app.exec())

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from app.ui.main_window import DefectDetectionApp  # Import the main application class

def main():
    """Main entry point of the application."""
    # Initialize the application
    app = QApplication(sys.argv)
    
    # Set application-wide style and font
    app.setStyle("Fusion")
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Create and display the main window
    main_window = DefectDetectionApp()
    main_window.show()
    
    # Execute the application event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
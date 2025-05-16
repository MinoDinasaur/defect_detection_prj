from PySide6.QtWidgets import QApplication
import sys
from app.ui.main_window import DefectDetectionApp  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = DefectDetectionApp()
    win.show()
    sys.exit(app.exec())


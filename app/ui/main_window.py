import os
import cv2
from datetime import datetime
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton, QListWidget, QListWidgetItem,
    QVBoxLayout, QHBoxLayout, QGroupBox, QTabWidget, QGridLayout, QStatusBar,
    QFrame, QSplitter, QSizePolicy, QToolBar
)
from PySide6.QtGui import QImage, QPixmap, QFont, QColor
from PySide6.QtCore import Qt, QTimer, Signal, Slot, QThread

from app.model.detector import detect_and_annotate
from app.camera.basler_camera import capture_image  # Giả định hàm này đã có

class ImageThread(QThread):
    image_loaded = Signal(object, str)

    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path

    def run(self):
        result_path = detect_and_annotate(self.image_path)
        result_img = cv2.imread(result_path)
        self.image_loaded.emit(result_img, result_path)

class DefectDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.last_captured_path = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("🔍 Defect Detection System")
        self.setMinimumSize(1200, 800)
        self.showMaximized()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.lblImage = QLabel("Captured image will appear here")
        self.lblImage.setAlignment(Qt.AlignCenter)
        self.lblImage.setMinimumSize(600, 500)
        self.lblImage.setStyleSheet("font-size: 16px; background-color: #f9f9f9;")

        self.image_info = QLabel("No image loaded")

        image_box = QVBoxLayout()
        image_box.addWidget(self.lblImage)
        image_box.addWidget(self.image_info)

        image_widget = QWidget()
        image_widget.setLayout(image_box)

        self.lstResult = QListWidget()
        self.total_defects_label = QLabel("Total Defects: 0")
        self.defect_types_label = QLabel("Defect Types: 0")
        self.status_label = QLabel("Status: Waiting for image")
        self.result_indicator = QLabel()
        self.result_indicator.setMinimumHeight(40)
        self.result_indicator.setAlignment(Qt.AlignCenter)

        result_box = QVBoxLayout()
        result_box.addWidget(self.lstResult)
        result_box.addWidget(self.total_defects_label)
        result_box.addWidget(self.defect_types_label)
        result_box.addWidget(self.status_label)
        result_box.addWidget(self.result_indicator)

        result_widget = QWidget()
        result_widget.setLayout(result_box)

        splitter.addWidget(image_widget)
        splitter.addWidget(result_widget)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter)

        self.btnCapture = QPushButton("📸 Capture Image")
        self.btnCapture.clicked.connect(self.on_capture)

        self.btnClear = QPushButton("🧹 Clear")
        self.btnClear.clicked.connect(self.clear_results)

        self.btnExit = QPushButton("🚪 Exit")
        self.btnExit.clicked.connect(self.close)

        controls = QHBoxLayout()
        controls.addWidget(self.btnCapture)
        controls.addWidget(self.btnClear)
        controls.addWidget(self.btnExit)

        main_layout.addLayout(controls)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.status_message = QLabel("Ready")
        self.statusBar.addPermanentWidget(self.status_message)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status_bar)
        self.timer.start(1000)

    def update_status_bar(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status_message.setText(f"Ready | {now}")

    def on_capture(self):
        try:
            self.set_processing_state(True)
            image_path = capture_image()
            if not image_path:
                raise Exception("Không thể lấy ảnh từ camera")
            self.last_captured_path = image_path
            self.image_thread = ImageThread(image_path)
            self.image_thread.image_loaded.connect(self.on_image_processed)
            self.image_thread.start()
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
            self.set_processing_state(False)

    @Slot(object, str)
    def on_image_processed(self, img_with_boxes, result_path):
        rgb = cv2.cvtColor(img_with_boxes, cv2.COLOR_BGR2RGB)
        h, w, _ = rgb.shape
        qimg = QImage(rgb.data, w, h, 3 * w, QImage.Format_RGB888)
        self.lblImage.setPixmap(QPixmap.fromImage(qimg).scaled(
            self.lblImage.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.image_info.setText(f"Detected Image: {os.path.basename(result_path)}")

        # Dummy results (vì bạn xử lý detect bên trong detect_and_annotate)
        self.lstResult.clear()
        self.lstResult.addItem(QListWidgetItem("✅ Detection complete. Check image above."))
        self.total_defects_label.setText("--")
        self.defect_types_label.setText("--")
        self.status_label.setText("Status: --")
        self.result_indicator.setText("Check image for defects.")

        self.set_processing_state(False)

    def clear_results(self):
        self.lblImage.clear()
        self.lblImage.setText("Captured image will appear here")
        self.lstResult.clear()
        self.image_info.setText("No image loaded")
        self.result_indicator.clear()
        self.total_defects_label.setText("Total Defects: 0")
        self.defect_types_label.setText("Defect Types: 0")
        self.status_label.setText("Status: Waiting for image")

    def set_processing_state(self, state):
        self.btnCapture.setEnabled(not state)
        self.btnClear.setEnabled(not state)

    def show_error(self, msg):
        self.statusBar.showMessage(msg, 5000)
        self.result_indicator.setText(f"⚠️ ERROR: {msg}")

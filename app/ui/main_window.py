# import os
# import cv2
# from datetime import datetime
# from PySide6.QtWidgets import (
#     QMainWindow, QWidget, QLabel, QPushButton, QListWidget, QListWidgetItem,
#     QVBoxLayout, QHBoxLayout, QGroupBox, QTabWidget, QGridLayout, QStatusBar,
#     QFrame, QSplitter, QSizePolicy, QToolBar
# )
# from PySide6.QtGui import QImage, QPixmap, QFont, QColor
# from PySide6.QtCore import Qt, QTimer, Signal, Slot, QThread

# from app.model.detector import detect_and_annotate
# from app.camera.basler_camera import capture_image  # Giả định hàm này đã có

# class ImageThread(QThread):
#     image_loaded = Signal(object, str)

#     def __init__(self, image_path):
#         super().__init__()
#         self.image_path = image_path

#     def run(self):
#         result_path = detect_and_annotate(self.image_path)
#         result_img = cv2.imread(result_path)
#         self.image_loaded.emit(result_img, result_path)

# class DefectDetectionApp(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.last_captured_path = None
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle("🔍 Defect Detection System")
#         self.setMinimumSize(1200, 800)
#         self.showMaximized()

#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
#         main_layout = QVBoxLayout(central_widget)

#         splitter = QSplitter(Qt.Horizontal)
#         splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

#         self.lblImage = QLabel("Captured image will appear here")
#         self.lblImage.setAlignment(Qt.AlignCenter)
#         self.lblImage.setMinimumSize(600, 500)
#         self.lblImage.setStyleSheet("font-size: 16px; background-color: #f9f9f9;")

#         self.image_info = QLabel("No image loaded")

#         image_box = QVBoxLayout()
#         image_box.addWidget(self.lblImage)
#         image_box.addWidget(self.image_info)

#         image_widget = QWidget()
#         image_widget.setLayout(image_box)

#         self.lstResult = QListWidget()
#         self.total_defects_label = QLabel("Total Defects: 0")
#         self.defect_types_label = QLabel("Defect Types: 0")
#         self.status_label = QLabel("Status: Waiting for image")
#         self.result_indicator = QLabel()
#         self.result_indicator.setMinimumHeight(40)
#         self.result_indicator.setAlignment(Qt.AlignCenter)

#         result_box = QVBoxLayout()
#         result_box.addWidget(self.lstResult)
#         result_box.addWidget(self.total_defects_label)
#         result_box.addWidget(self.defect_types_label)
#         result_box.addWidget(self.status_label)
#         result_box.addWidget(self.result_indicator)

#         result_widget = QWidget()
#         result_widget.setLayout(result_box)

#         splitter.addWidget(image_widget)
#         splitter.addWidget(result_widget)
#         splitter.setStretchFactor(0, 2)
#         splitter.setStretchFactor(1, 1)

#         main_layout.addWidget(splitter)

#         self.btnCapture = QPushButton("📸 Capture Image")
#         self.btnCapture.clicked.connect(self.on_capture)

#         self.btnClear = QPushButton("🧹 Clear")
#         self.btnClear.clicked.connect(self.clear_results)

#         self.btnExit = QPushButton("🚪 Exit")
#         self.btnExit.clicked.connect(self.close)

#         controls = QHBoxLayout()
#         controls.addWidget(self.btnCapture)
#         controls.addWidget(self.btnClear)
#         controls.addWidget(self.btnExit)

#         main_layout.addLayout(controls)

#         self.statusBar = QStatusBar()
#         self.setStatusBar(self.statusBar)
#         self.status_message = QLabel("Ready")
#         self.statusBar.addPermanentWidget(self.status_message)

#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.update_status_bar)
#         self.timer.start(1000)

#     def update_status_bar(self):
#         now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         self.status_message.setText(f"Ready | {now}")

#     def on_capture(self):
#         try:
#             self.set_processing_state(True)
#             image_path = capture_image()
#             if not image_path:
#                 raise Exception("Không thể lấy ảnh từ camera")
#             self.last_captured_path = image_path
#             self.image_thread = ImageThread(image_path)
#             self.image_thread.image_loaded.connect(self.on_image_processed)
#             self.image_thread.start()
#         except Exception as e:
#             self.show_error(f"Error: {str(e)}")
#             self.set_processing_state(False)

#     @Slot(object, str)
#     def on_image_processed(self, img_with_boxes, result_path):
#         rgb = cv2.cvtColor(img_with_boxes, cv2.COLOR_BGR2RGB)
#         h, w, _ = rgb.shape
#         qimg = QImage(rgb.data, w, h, 3 * w, QImage.Format_RGB888)
#         self.lblImage.setPixmap(QPixmap.fromImage(qimg).scaled(
#             self.lblImage.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

#         self.image_info.setText(f"Detected Image: {os.path.basename(result_path)}")

#         # Dummy results (vì bạn xử lý detect bên trong detect_and_annotate)
#         self.lstResult.clear()
#         self.lstResult.addItem(QListWidgetItem("✅ Detection complete. Check image above."))
#         self.total_defects_label.setText("--")
#         self.defect_types_label.setText("--")
#         self.status_label.setText("Status: --")
#         self.result_indicator.setText("Check image for defects.")

#         self.set_processing_state(False)

#     def clear_results(self):
#         self.lblImage.clear()
#         self.lblImage.setText("Captured image will appear here")
#         self.lstResult.clear()
#         self.image_info.setText("No image loaded")
#         self.result_indicator.clear()
#         self.total_defects_label.setText("Total Defects: 0")
#         self.defect_types_label.setText("Defect Types: 0")
#         self.status_label.setText("Status: Waiting for image")

#     def set_processing_state(self, state):
#         self.btnCapture.setEnabled(not state)
#         self.btnClear.setEnabled(not state)

#     def show_error(self, msg):
#         self.statusBar.showMessage(msg, 5000)
#         self.result_indicator.setText(f"⚠️ ERROR: {msg}")


from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
    QFrame, QListWidget, QListWidgetItem, QWidget, QSplitter, QSizePolicy,
    QStatusBar, QToolBar, QTabWidget, QGridLayout, QGroupBox
)
from PySide6.QtCore import Qt, QSize, QTimer, Signal, Slot, QThread
from PySide6.QtGui import QImage, QPixmap, QIcon, QFont, QColor, QPalette
from app.model.detector import detect_image
import cv2
from datetime import datetime
from sqlite_database.src.db_operations import save_to_db

class ImageThread(QThread):
    """Thread for loading and processing images"""
    image_loaded = Signal(object, object)
    
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        
    def run(self):
        # Process image in background thread
        results = detect_image(self.image_path)
        result_obj = results[0]
        img_with_boxes = result_obj.plot()
        
        # Emit the processed image and results
        self.image_loaded.emit(img_with_boxes, result_obj)

class DefectDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize attributes early
        self.last_captured_path = None
        
        self.initUI()
        # Start with test image if available
        self.test_img_path = "/home/ducanh/Desktop/defect_detection_prj/storage/captured_images/captured_image_20250514_114617.png"
        
    def initUI(self):
        # Window configuration
        self.setWindowTitle("🔍 Defect Detection System")
        self.setMinimumSize(1200, 800)
        self.showMaximized()
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f7f9fc;
            }
            QLabel {
                font-family: 'Segoe UI', Arial;
                color: #333;
            }
            QPushButton {
                background-color: #4a86e8;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #3a76d8;
            }
            QPushButton:pressed {
                background-color: #2a66c8;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ddd;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Create horizontal splitter for image and results
        splitter = QSplitter(Qt.Horizontal)
        splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # ===== Left side: Image area =====
        self.image_container = QWidget()
        image_layout = QVBoxLayout(self.image_container)
        
        # Image preview group
        image_group = QGroupBox("Image Preview")
        image_group_layout = QVBoxLayout(image_group)
        
        # Image display
        self.image_frame = QFrame()
        self.image_frame.setFrameShape(QFrame.StyledPanel)
        self.image_frame.setStyleSheet("""
            background-color: #ffffff;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
        """)
        image_frame_layout = QVBoxLayout(self.image_frame)
        
        self.lblImage = QLabel("Captured image will appear here")
        self.lblImage.setAlignment(Qt.AlignCenter)
        self.lblImage.setMinimumSize(600, 500)
        self.lblImage.setStyleSheet("""
            font-size: 16px;
            color: #888;
            background-color: #f9f9f9;
        """)
        image_frame_layout.addWidget(self.lblImage)
        
        image_group_layout.addWidget(self.image_frame)
        
        # Image statistics
        self.image_info = QLabel("No image loaded")
        self.image_info.setStyleSheet("font-size: 12px; color: #666; padding: 5px;")
        image_group_layout.addWidget(self.image_info)
        
        image_layout.addWidget(image_group)
        
        # ===== Right side: Results area =====
        self.results_container = QWidget()
        results_layout = QVBoxLayout(self.results_container)
        
        # Results group
        results_group = QGroupBox("Detection Results")
        results_group_layout = QVBoxLayout(results_group)
        
        # Tab widget for different result views
        self.results_tabs = QTabWidget()
        self.results_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 12px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 1px solid white;
            }
        """)
        
        # Results list
        self.lstResult = QListWidget()
        self.lstResult.setStyleSheet("""
            QListWidget {
                background-color: #ffffff;
                padding: 10px;
                font-family: 'Segoe UI';
                font-size: 14px;
                border: none;
            }
            QListWidget::item {
                padding: 8px;
                margin: 2px 0;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #e0e8f8;
                color: #333;
            }
        """)
        self.results_tabs.addTab(self.lstResult, "Defects List")
        
        # Statistics tab
        self.stats_widget = QWidget()
        stats_layout = QGridLayout(self.stats_widget)
        
        self.total_defects_label = QLabel("Total Defects: 0")
        self.defect_types_label = QLabel("Defect Types: 0")
        self.status_label = QLabel("Status: Waiting for image")
        
        for label in [self.total_defects_label, self.defect_types_label, self.status_label]:
            label.setStyleSheet("font-size: 14px; padding: 10px;")
        
        stats_layout.addWidget(self.total_defects_label, 0, 0)
        stats_layout.addWidget(self.defect_types_label, 1, 0)
        stats_layout.addWidget(self.status_label, 2, 0)
        stats_layout.setRowStretch(3, 1)  # Add stretch to bottom
        
        self.results_tabs.addTab(self.stats_widget, "Statistics")
        
        results_group_layout.addWidget(self.results_tabs)
        
        # Result status indicator
        self.result_indicator = QLabel()
        self.result_indicator.setAlignment(Qt.AlignCenter)
        self.result_indicator.setMinimumHeight(40)
        self.result_indicator.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            border-radius: 5px;
            padding: 5px;
            background-color: #f0f0f0;
        """)
        results_group_layout.addWidget(self.result_indicator)
        
        results_layout.addWidget(results_group)
        
        # Add both containers to splitter
        splitter.addWidget(self.image_container)
        splitter.addWidget(self.results_container)
        splitter.setStretchFactor(0, 2)  # Image gets more space
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
        
        # Bottom controls
        controls_layout = QHBoxLayout()
        
        # Create a button group
        button_group = QGroupBox("Controls")
        button_group.setStyleSheet("""
            QGroupBox { 
                border: 1px solid #ddd;
                border-radius: 6px;
                margin-top: 12px;
                background-color: #f9f9f9;
            }
        """)
        button_layout = QHBoxLayout(button_group)
        
        # Camera button
        self.btnCapture = QPushButton("📸 Capture Image")
        self.btnCapture.setIcon(QIcon.fromTheme("camera-photo"))
        self.btnCapture.setMinimumWidth(150)
        self.btnCapture.clicked.connect(self.on_capture)
        
        # Clear results button
        self.btnClear = QPushButton("🧹 Clear")
        self.btnClear.setIcon(QIcon.fromTheme("edit-clear"))
        self.btnClear.setMinimumWidth(120)
        self.btnClear.clicked.connect(self.clear_results)
        
        # Exit button
        self.btnExit = QPushButton("🚪 Exit")
        self.btnExit.setIcon(QIcon.fromTheme("application-exit"))
        self.btnExit.setMinimumWidth(120)
        self.btnExit.clicked.connect(self.close)
        
        # Add buttons to layout
        button_layout.addWidget(self.btnCapture)
        button_layout.addWidget(self.btnClear)
        button_layout.addStretch()
        button_layout.addWidget(self.btnExit)
        
        controls_layout.addWidget(button_group)
        main_layout.addLayout(controls_layout)
        
        # Create status bar
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet("""
            QStatusBar {
                background-color: #f0f0f0;
                border-top: 1px solid #ddd;
            }
        """)
        self.setStatusBar(self.statusBar)
        
        self.status_message = QLabel("Ready")
        self.statusBar.addPermanentWidget(self.status_message)
        
        # Create a timer for updating the status bar time
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status_bar)
        self.timer.start(1000)  # Update every second
        
        # Initial status update
        self.update_status_bar()

    def update_status_bar(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status_message.setText(f"Ready | {current_time}")

    def on_capture(self):
        """Capture image from camera"""
        try:
            self.statusBar.showMessage("Capturing image...", 2000)
            self.set_processing_state(True)
            
            # camera = PylonCamera()                             #Uncomment dòng này để chụp ảnh từ camera
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{timestamp}.png"
            
            # captured_img_path = camera.capture_image(filename) #Uncomment dòng này để chụp ảnh từ camera
            
            # For testing, we'll use the test image
            captured_img_path = self.test_img_path              #Comment dòng này để chụp ảnh từ camera
            self.last_captured_path = captured_img_path
            
            # Process image in background thread
            self.image_thread = ImageThread(captured_img_path)
            self.image_thread.image_loaded.connect(self.on_image_processed)
            self.image_thread.start()
            
        except Exception as e:
            self.show_error(f"Error capturing image: {str(e)}")
            self.set_processing_state(False)

    @Slot(object, object)
    def on_image_processed(self, img_with_boxes, result_obj):
        """Handle processed image from thread"""
        try:
            # Save detected image
            save_to_db(self.last_captured_path, img_with_boxes, result_obj)
            
            # Display image
            pixmap = cv2.cvtColor(img_with_boxes, cv2.COLOR_BGR2RGB)
            height, width, channel = pixmap.shape
            bytes_per_line = 3 * width
            qimg = QImage(pixmap.data, width, height, bytes_per_line, QImage.Format_RGB888)
            
            # Scale to fit the label while maintaining aspect ratio
            self.lblImage.setPixmap(QPixmap.fromImage(qimg).scaled(
                self.lblImage.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            
            # Update image info
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.image_info.setText(f"Image size: {width}x{height} | Captured: {timestamp}")
            
            # Get defect information
            classes = result_obj.names
            boxes = result_obj.boxes
            labels = boxes.cls.cpu().tolist() if boxes is not None else []
            confidences = boxes.conf.cpu().tolist() if boxes is not None else []
            
            # Filter out OK class
            defect_indices = [(i, cls_id) for i, cls_id in enumerate(labels) if classes[int(cls_id)].lower() != "ok"]
            
            # Show results in list
            self.lstResult.clear()
            
            if defect_indices:
                defect_count = len(defect_indices)
                defect_types = set(classes[int(cls_id)] for _, cls_id in defect_indices)
                
                # Update statistics
                self.total_defects_label.setText(f"Total Defects: {defect_count}")
                self.defect_types_label.setText(f"Defect Types: {len(defect_types)}")
                self.status_label.setText(f"Status: Defects Detected")
                
                # Header item
                header_item = QListWidgetItem("🛠️ Product has the following defects:")
                header_item.setFont(QFont("Segoe UI", 14, QFont.Bold))
                self.lstResult.addItem(header_item)
                
                # Add each defect with confidence score
                for idx, (i, cls_id) in enumerate(defect_indices):
                    defect_name = classes[int(cls_id)]
                    confidence = confidences[i] * 100
                    
                    item = QListWidgetItem(f"🔴 Defect #{idx+1}: {defect_name}")
                    
                    # Set background color based on confidence
                    if confidence > 90:
                        item.setBackground(QColor(255, 200, 200))  # Strong red for high confidence
                    elif confidence > 75:
                        item.setBackground(QColor(255, 225, 225))  # Medium red
                    else:
                        item.setBackground(QColor(255, 240, 240))  # Light red
                        
                    self.lstResult.addItem(item)
                
                # Update indicator
                self.result_indicator.setText(f"❌ FAILED: {defect_count} defects detected")
                self.result_indicator.setStyleSheet("""
                    background-color: #ffebee;
                    color: #d32f2f;
                    border: 2px solid #ffcdd2;
                    border-radius: 5px;
                    padding: 8px;
                    font-size: 16px;
                    font-weight: bold;
                """)
                
            else:
                # Update statistics
                self.total_defects_label.setText("Total Defects: 0")
                self.defect_types_label.setText("Defect Types: 0")
                self.status_label.setText("Status: No Defects")
                
                # Add success message
                success_item = QListWidgetItem("✅ Product passed quality control - No defects detected.")
                success_item.setFont(QFont("Segoe UI", 14))
                success_item.setBackground(QColor(230, 250, 230))
                self.lstResult.addItem(success_item)
                
                # Update indicator
                self.result_indicator.setText("✅ PASSED: No defects detected")
                self.result_indicator.setStyleSheet("""
                    background-color: #e8f5e9;
                    color: #2e7d32;
                    border: 2px solid #c8e6c9;
                    border-radius: 5px;
                    padding: 8px;
                    font-size: 16px;
                    font-weight: bold;
                """)
                
            # Switch to results tab
            self.results_tabs.setCurrentIndex(0)
            self.set_processing_state(False)
            
        except Exception as e:
            self.show_error(f"Error processing results: {str(e)}")
            self.set_processing_state(False)

    def clear_results(self):
        """Clear all results and reset UI"""
        self.lblImage.clear()
        self.lblImage.setText("Captured image will appear here")
        self.lstResult.clear()
        self.image_info.setText("No image loaded")
        self.last_captured_path = None
        
        # Reset statistics
        self.total_defects_label.setText("Total Defects: 0")
        self.defect_types_label.setText("Defect Types: 0")
        self.status_label.setText("Status: Waiting for image")
        
        # Reset indicator
        self.result_indicator.setText("")
        self.result_indicator.setStyleSheet("background-color: #f0f0f0;")
        
        self.statusBar.showMessage("Results cleared", 2000)

    def set_processing_state(self, is_processing):
        """Update UI elements based on processing state"""
        self.btnCapture.setEnabled(not is_processing)
        # self.btnLoadTest.setEnabled(not is_processing)
        self.btnClear.setEnabled(not is_processing)
        
        if is_processing:
            self.setCursor(Qt.WaitCursor)
            self.statusBar.showMessage("Processing image...")
        else:
            self.setCursor(Qt.ArrowCursor)
            self.statusBar.showMessage("Processing complete", 2000)

    def show_error(self, message):
        """Display error message"""
        self.statusBar.showMessage(f"Error: {message}", 5000)
        self.result_indicator.setText(f"⚠️ ERROR: {message}")
        self.result_indicator.setStyleSheet("""
            background-color: #fff3e0;
            color: #e65100;
            border: 2px solid #ffe0b2;
            border-radius: 5px;
            padding: 8px;
        """)

    def resizeEvent(self, event):
        """Handle window resize"""
        super().resizeEvent(event)
        # If we have an image loaded, rescale it
        if self.last_captured_path and not self.lblImage.text():
            pixmap = self.lblImage.pixmap()
            if pixmap:
                self.lblImage.setPixmap(pixmap.scaled(
                    self.lblImage.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

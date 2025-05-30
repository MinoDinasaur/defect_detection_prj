from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
    QFrame, QListWidget, QListWidgetItem, QWidget, QSplitter, QSizePolicy,
    QStatusBar, QToolBar, QTabWidget, QGridLayout, QGroupBox, QMessageBox, QLineEdit,
    QProgressBar, QScrollArea, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QSize, QTimer, Signal, Slot, QThread, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QImage, QPixmap, QIcon, QFont, QColor, QPalette, QPainter, QLinearGradient
from app.model.detector import detect_image
import cv2
from datetime import datetime
from app.camera.basler_camera import PylonCamera
from app.ui.detection_history_tab import DetectionHistoryTab
from sqlite_database.src.db_operations import update_detection_in_db, create_database, create_connection

class ImageThread(QThread):
    """Thread for loading and processing images"""
    image_loaded = Signal(object, object)
    progress_updated = Signal(int)
    
    def __init__(self, row_id):
        super().__init__()
        self.row_id = row_id 
        
    def run(self):
        # Emit progress updates
        self.progress_updated.emit(25)
        
        # Process image in background thread
        results = detect_image(self.row_id)  
        
        self.progress_updated.emit(75)
        
        if results:
            result_obj = results[0]
            img_with_boxes = result_obj.plot()
            # Emit the processed image and results
            self.image_loaded.emit(img_with_boxes, result_obj)
            
        self.progress_updated.emit(100)

class AnimatedButton(QPushButton):
    """Custom button with hover animations"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a86e8, stop:1 #3a76d8);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-weight: bold;
                font-size: 14px;
                min-height: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a96f8, stop:1 #4a86e8);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2a66c8, stop:1 #1a56b8);
                transform: translateY(1px);
            }
            QPushButton:disabled {
                background: #cccccc;
                color: #666666;
            }
        """)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)

class StatusCard(QFrame):
    """Custom status card widget"""
    def __init__(self, title, value, color="#4a86e8", parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)
        self.setStyleSheet(f"""
            QFrame {{
                background: white;
                border: 1px solid #e0e6ed;
                border-radius: 12px;
                padding: 16px;
            }}
        """)
        
        # Add shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: #666;
                font-size: 14px;
                font-weight: 500;
                margin: 0;
            }}
        """)
        layout.addWidget(title_label)
        
        # Value
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 28px;
                font-weight: bold;
                margin: 0;
            }}
        """)
        layout.addWidget(self.value_label)
        
    def update_value(self, value, color=None):
        self.value_label.setText(str(value))
        if color:
            self.value_label.setStyleSheet(f"""
                QLabel {{
                    color: {color};
                    font-size: 28px;
                    font-weight: bold;
                    margin: 0;
                }}
            """)

class DefectDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize attributes early
        self.last_captured_path = None
        self.current_raw_image = None
        self.history_needs_refresh = False
        self.history_loaded = False 
        self.processing_timer = QTimer()
        
        # Initialize database
        create_database()
        create_connection()
        
        self.init_UI()
        # Start with test image if available
        self.test_img_path = "storage/captured_images/captured_image_20250514_114617.png"
        
    def init_UI(self):
        # Window configuration
        self.setWindowTitle("🔍 Defect Detection System v2.0")
        self.setMinimumSize(1400, 900)
        self.showMaximized()
        
        # Modern application style
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
            QLabel {
                font-family: 'Segoe UI', 'San Francisco', Arial;
                color: #2c3e50;
            }
            QGroupBox {
                font-weight: 600;
                font-size: 16px;
                color: #2c3e50;
                border: 2px solid #e0e6ed;
                border-radius: 12px;
                margin-top: 20px;
                padding-top: 20px;
                background: rgba(255, 255, 255, 0.9);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 8px 16px;
                background: white;
                border-radius: 6px;
                margin-left: 10px;
            }
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                border-radius: 12px;
                background: white;
                margin-top: 5px;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border: 1px solid #dee2e6;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 12px 24px;
                margin-right: 4px;
                font-weight: 500;
                font-size: 14px;
                color: #495057;
                min-width: 120px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 2px solid #4a86e8;
                color: #4a86e8;
                font-weight: 600;
            }
            QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
            QListWidget {
                background: white;
                border: 1px solid #e0e6ed;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 12px;
                margin: 4px 0;
                border-radius: 6px;
                border: 1px solid transparent;
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e3f2fd, stop:1 #bbdefb);
                border: 1px solid #4a86e8;
                color: #1976d2;
            }
            QListWidget::item:hover {
                background: #f5f5f5;
            }
        """)
        
        # Create main tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.setCentralWidget(self.tab_widget)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        # Live detection tab
        self.live_detection_tab = QWidget()
        self.tab_widget.addTab(self.live_detection_tab, "📹 Live Detection")
        
        # Setup live detection UI
        self.setup_live_detection_tab()
        
        # History tab
        self.history_tab = DetectionHistoryTab(self)
        self.tab_widget.addTab(self.history_tab, "📊 Detection History")
        
        # Create modern status bar
        self.setup_status_bar()
        
        # Create a timer for updating the status bar time
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status_bar)
        self.timer.start(1000)  # Update every second
        
        # Initial status update
        self.update_status_bar()
    
    def setup_status_bar(self):
        """Setup modern status bar"""
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet("""
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border-top: 1px solid #dee2e6;
                padding: 8px;
                font-size: 13px;
                color: #495057;
            }
        """)
        self.setStatusBar(self.statusBar)
        
        # Status message with icon
        self.status_message = QLabel("🟢 Ready")
        self.status_message.setStyleSheet("font-weight: 500;")
        self.statusBar.addWidget(self.status_message)
        
        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #dee2e6;
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
                background: #f8f9fa;
                height: 20px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a86e8, stop:1 #3a76d8);
                border-radius: 7px;
            }
        """)
        self.statusBar.addPermanentWidget(self.progress_bar)
        
        # Connection status
        self.connection_status = QLabel("🔗 Database Connected")
        self.connection_status.setStyleSheet("color: #28a745; font-weight: 500;")
        self.statusBar.addPermanentWidget(self.connection_status)
    
    def on_tab_changed(self, index):
        """Load history tab data only once."""
        if self.tab_widget.tabText(index) == "📊 Detection History" and not self.history_loaded:
            self.history_tab.refresh_data()
            self.history_loaded = True  # Mark as loaded

    def setup_live_detection_tab(self):
        """Setup the enhanced UI for live detection tab"""
        # Main scroll area
        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        main_layout = QVBoxLayout(scroll_widget)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)
        
        # === Header Section ===
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 16px;
                padding: 20px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        
        # Title and subtitle
        title_layout = QVBoxLayout()
        title_label = QLabel("Quality Control Station")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                margin: 0;
            }
        """)
        
        subtitle_label = QLabel("Real-time defect detection and analysis")
        subtitle_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 16px;
                margin: 0;
            }
        """)
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        main_layout.addWidget(header_frame)
        
        # === Stats Cards Section ===
        stats_frame = QFrame()
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.setSpacing(16)
        
        self.total_defects_card = StatusCard("Total Defects", "0", "#e74c3c")
        self.defect_types_card = StatusCard("Defect Types", "0", "#f39c12")
        self.status_card = StatusCard("Status", "Ready", "#27ae60")
        
        stats_layout.addWidget(self.total_defects_card)
        stats_layout.addWidget(self.defect_types_card)
        stats_layout.addWidget(self.status_card)
        
        main_layout.addWidget(stats_frame)
        
        # === Main Content Splitter ===
        splitter = QSplitter(Qt.Horizontal)
        splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # === Left side: Image area ===
        self.image_container = QWidget()
        image_layout = QVBoxLayout(self.image_container)
        
        # Enhanced image preview group
        image_group = QGroupBox("📷 Live Camera Feed")
        image_group.setStyleSheet("""
            QGroupBox {
                font-size: 18px;
                font-weight: 600;
                color: #2c3e50;
                border: 2px solid #3498db;
            }
            QGroupBox::title {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                padding: 8px 20px;
                border-radius: 8px;
            }
        """)
        image_group_layout = QVBoxLayout(image_group)
        
        # Enhanced image display
        self.image_frame = QFrame()
        self.image_frame.setFrameShape(QFrame.StyledPanel)
        self.image_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border: 3px dashed #bdc3c7;
                border-radius: 16px;
                min-height: 400px;
            }
        """)
        image_frame_layout = QVBoxLayout(self.image_frame)
        
        self.lblImage = QLabel("🎯 Captured image will appear here\n\nClick 'Capture Image' to start quality inspection")
        self.lblImage.setAlignment(Qt.AlignCenter)
        self.lblImage.setMinimumSize(700, 500)
        self.lblImage.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #7f8c8d;
                background: transparent;
                padding: 40px;
                line-height: 1.6;
            }
        """)
        image_frame_layout.addWidget(self.lblImage)
        
        image_group_layout.addWidget(self.image_frame)
        
        # Enhanced image info
        self.image_info = QLabel("📊 No image loaded")
        self.image_info.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #34495e;
                background: rgba(52, 152, 219, 0.1);
                padding: 12px;
                border-radius: 8px;
                font-weight: 500;
            }
        """)
        image_group_layout.addWidget(self.image_info)
        
        image_layout.addWidget(image_group)
        
        # === Right side: Enhanced Results area ===
        self.results_container = QWidget()
        results_layout = QVBoxLayout(self.results_container)
        
        # Enhanced results group
        results_group = QGroupBox("🔍 Analysis Results")
        results_group.setStyleSheet("""
            QGroupBox {
                font-size: 18px;
                font-weight: 600;
                color: #2c3e50;
                border: 2px solid #e74c3c;
            }
            QGroupBox::title {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                padding: 8px 20px;
                border-radius: 8px;
            }
        """)
        results_group_layout = QVBoxLayout(results_group)
        
        # Enhanced results list
        self.lstResult = QListWidget()
        self.lstResult.setStyleSheet("""
            QListWidget {
                background: white;
                border: 2px solid #ecf0f1;
                border-radius: 12px;
                padding: 16px;
                font-size: 15px;
                min-height: 300px;
            }
            QListWidget::item {
                padding: 16px;
                margin: 6px 0;
                border-radius: 8px;
                border-left: 4px solid transparent;
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e8f4fd, stop:1 #d4edda);
                border-left: 4px solid #3498db;
                color: #2c3e50;
            }
        """)
        results_group_layout.addWidget(self.lstResult)
        
        # Enhanced result indicator
        self.result_indicator = QLabel("⏳ Waiting for analysis...")
        self.result_indicator.setAlignment(Qt.AlignCenter)
        self.result_indicator.setWordWrap(True)
        self.result_indicator.setMinimumHeight(60)
        self.result_indicator.setMaximumHeight(120)
        self.result_indicator.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                border-radius: 12px;
                padding: 16px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border: 2px solid #dee2e6;
                color: #6c757d;
                max-height: 120px;
            }
        """)
        results_group_layout.addWidget(self.result_indicator)
        
        results_layout.addWidget(results_group)
        
        # Add containers to splitter
        splitter.addWidget(self.image_container)
        splitter.addWidget(self.results_container)
        splitter.setStretchFactor(0, 3)  # Image gets more space
        splitter.setStretchFactor(1, 2)
        
        main_layout.addWidget(splitter)
        
        # === Enhanced Controls Section ===
        controls_frame = QFrame()
        controls_frame.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #e0e6ed;
                border-radius: 16px;
                padding: 20px;
            }
        """)
        
        # Add shadow to controls
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 20))
        controls_frame.setGraphicsEffect(shadow)
        
        controls_layout = QHBoxLayout(controls_frame)
        
        # Enhanced buttons
        self.btnCapture = AnimatedButton("📸 Capture & Analyze")
        self.btnCapture.setMinimumSize(200, 50)
        self.btnCapture.clicked.connect(self.on_capture)
        
        self.btnClear = AnimatedButton("🧹 Clear Results")
        self.btnClear.setMinimumSize(150, 50)
        self.btnClear.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #95a5a6, stop:1 #7f8c8d);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a5b5b6, stop:1 #8f9c9d);
            }
        """)
        self.btnClear.clicked.connect(self.clear_results)
        
        controls_layout.addWidget(self.btnCapture)
        controls_layout.addWidget(self.btnClear)
        controls_layout.addStretch()
        
        main_layout.addWidget(controls_frame)
        
        # Set the scroll area as the tab's main widget
        tab_layout = QVBoxLayout(self.live_detection_tab)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll)

    def update_status_bar(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status_message.setText(f"🟢 Ready | {current_time}")

    def on_capture(self):
        """Enhanced capture with progress indication"""
        try:
            self.status_message.setText("📸 Capturing image...")
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.set_processing_state(True)
            
            camera = PylonCamera() 
            row_id = camera.capture_image()
            if row_id is None:
                raise Exception("Failed to capture image.")    
                
            # Process image in background thread
            self.image_thread = ImageThread(row_id)
            self.image_thread.image_loaded.connect(self.on_image_processed)
            self.image_thread.progress_updated.connect(self.update_progress)
            self.image_thread.start()
            
        except Exception as e:
            self.show_error(f"Error capturing image: {str(e)}")
            self.set_processing_state(False)
            self.progress_bar.setVisible(False)

    @Slot(int)
    def update_progress(self, value):
        """Update progress bar"""
        self.progress_bar.setValue(value)
        if value == 100:
            QTimer.singleShot(1000, lambda: self.progress_bar.setVisible(False))

    @Slot(object, object)
    def on_image_processed(self, img_with_boxes, result_obj):
        """Handle processed image with enhanced UI updates"""
        try:
            # Save to database
            update_detection_in_db(self.image_thread.row_id, img_with_boxes, result_obj)

            # Mark history as needing refresh
            self.history_loaded = False
            self.history_needs_refresh = True
            
            # Display image with enhanced styling
            pixmap = cv2.cvtColor(img_with_boxes, cv2.COLOR_BGR2RGB)
            height, width, channel = pixmap.shape
            bytes_per_line = 3 * width
            qimg = QImage(pixmap.data, width, height, bytes_per_line, QImage.Format_RGB888)
            
            # Scale to fit with smooth transformation
            scaled_pixmap = QPixmap.fromImage(qimg).scaled(
                self.lblImage.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.lblImage.setPixmap(scaled_pixmap)
            
            # Update image info with enhanced formatting
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.image_info.setText(f"📊 Image: {width}x{height}px | 📅 Captured: {timestamp} | 🔍 Analysis Complete")
            
            # Process results
            classes = result_obj.names
            boxes = result_obj.boxes
            labels = boxes.cls.cpu().tolist() if boxes is not None else []
            confidences = boxes.conf.cpu().tolist() if boxes is not None else []
            
            # Filter out OK class
            defect_indices = [(i, cls_id) for i, cls_id in enumerate(labels) if classes[int(cls_id)].lower() != "ok"]
            
            # Clear results list
            self.lstResult.clear()
             
            if defect_indices:
                defect_count = len(defect_indices)
                defect_types = set(classes[int(cls_id)] for _, cls_id in defect_indices)
                
                # Update status cards with animations
                self.total_defects_card.update_value(defect_count, "#e74c3c")
                self.defect_types_card.update_value(len(defect_types), "#f39c12")
                self.status_card.update_value("FAILED", "#e74c3c")
                
                # Enhanced defect list
                header_item = QListWidgetItem("🚨 QUALITY ALERT: Defects Detected")
                header_item.setFont(QFont("Segoe UI", 16, QFont.Bold))
                header_item.setBackground(QColor(255, 240, 240))
                self.lstResult.addItem(header_item)
                
                for idx, (i, cls_id) in enumerate(defect_indices):
                    defect_name = classes[int(cls_id)]
                    confidence = confidences[i] * 100
                    
                    item_text = f"🔴 Defect #{idx+1}: {defect_name}\n   Confidence: {confidence:.1f}%"
                    item = QListWidgetItem(item_text)
                    item.setFont(QFont("Segoe UI", 13))
                    
                    # Enhanced color coding
                    if confidence > 90:
                        item.setBackground(QColor(255, 182, 193))  # Light pink
                    elif confidence > 75:
                        item.setBackground(QColor(255, 218, 185))  # Peach
                    else:
                        item.setBackground(QColor(255, 235, 205))  # Light yellow
                        
                    self.lstResult.addItem(item)
                
                # Enhanced fail indicator
                self.result_indicator.setText(f"❌ QUALITY FAILED\n{defect_count} defects detected")
                self.result_indicator.setStyleSheet("""
                    QLabel {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                            stop:0 #ffebee, stop:1 #ffcdd2);
                        color: #c62828;
                        border: 3px solid #ef5350;
                        border-radius: 12px;
                        padding: 16px;
                        font-size: 18px;
                        font-weight: bold;
                    }
                """)
                
            else:
                # Update status cards for pass
                self.total_defects_card.update_value("0", "#27ae60")
                self.defect_types_card.update_value("0", "#27ae60") 
                self.status_card.update_value("PASSED", "#27ae60")
                
                # Enhanced pass message
                success_item = QListWidgetItem("✅ QUALITY PASSED\n\nProduct meets all quality standards\nNo defects detected in inspection")
                success_item.setFont(QFont("Segoe UI", 16))
                success_item.setBackground(QColor(232, 245, 233))
                self.lstResult.addItem(success_item)
                
                # Enhanced pass indicator
                self.result_indicator.setText("✅ QUALITY PASSED\nNo defects detected")
                self.result_indicator.setStyleSheet("""
                    QLabel {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                            stop:0 #e8f5e9, stop:1 #c8e6c9);
                        color: #2e7d32;
                        border: 3px solid #66bb6a;
                        border-radius: 12px;
                        padding: 16px;
                        font-size: 18px;
                        font-weight: bold;
                    }
                """)
            
            self.set_processing_state(False)
            self.status_message.setText("🟢 Analysis complete")
            
        except Exception as e:
            self.show_error(f"Error processing results: {str(e)}")
            self.set_processing_state(False)

    def clear_results(self):
        """Enhanced clear function with animations"""
        self.lblImage.clear()
        self.lblImage.setText("🎯 Captured image will appear here\n\nClick 'Capture Image' to start quality inspection")
        self.lstResult.clear()
        self.image_info.setText("📊 No image loaded")
        self.last_captured_path = None
        self.current_raw_image = None
        
        # Reset status cards
        self.total_defects_card.update_value("0", "#6c757d")
        self.defect_types_card.update_value("0", "#6c757d")
        self.status_card.update_value("Ready", "#6c757d")
        
        # Reset indicator with proper sizing
        self.result_indicator.setText("⏳ Waiting for analysis...")
        self.result_indicator.setWordWrap(True)
        self.result_indicator.setMaximumHeight(120)
        self.result_indicator.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                border-radius: 12px;
                padding: 16px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border: 2px solid #dee2e6;
                color: #6c757d;
                max-height: 120px;
            }
        """)
        
        self.status_message.setText("🧹 Results cleared")

    def set_processing_state(self, is_processing):
        """Enhanced processing state with visual feedback"""
        self.btnCapture.setEnabled(not is_processing)
        self.btnClear.setEnabled(not is_processing)
        
        if is_processing:
            self.setCursor(Qt.WaitCursor)
            self.status_message.setText("⚙️ Processing image...")
            
            # Update status card to show processing
            self.status_card.update_value("Processing...", "#f39c12")
            
            # Animate result indicator with proper sizing
            self.result_indicator.setText("⚙️ ANALYZING...\nPlease wait")
            self.result_indicator.setWordWrap(True)
            self.result_indicator.setMaximumHeight(120)
            self.result_indicator.setStyleSheet("""
                QLabel {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #fff3cd, stop:1 #ffeaa7);
                    color: #856404;
                    border: 3px solid #ffc107;
                    border-radius: 12px;
                    padding: 16px;
                    font-size: 14px;
                    font-weight: bold;
                    max-height: 120px;
                }
            """)
        else:
            self.setCursor(Qt.ArrowCursor)

    def show_error(self, message):
        """Enhanced error display with proper text wrapping"""
        self.status_message.setText(f"❌ Error: {message}")
        
        # Update status card
        self.status_card.update_value("Error", "#e74c3c")
        
        # Truncate long error messages for display
        display_message = message if len(message) <= 50 else message[:47] + "..."
        
        # Enhanced error indicator with word wrap and size constraints
        self.result_indicator.setText(f"⚠️ ERROR\n{display_message}")
        self.result_indicator.setWordWrap(True)
        self.result_indicator.setMaximumHeight(120)
        self.result_indicator.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #fff3e0, stop:1 #ffe0b2);
                color: #e65100;
                border: 3px solid #ff9800;
                border-radius: 12px;
                padding: 16px;
                font-size: 14px;
                font-weight: bold;
                max-height: 120px;
            }
        """)

    def show_history_tab(self):
        """Switch to history tab and refresh data"""
        self.tab_widget.setCurrentWidget(self.history_tab)
        self.history_tab.refresh_data()

    def resizeEvent(self, event):
        """Handle window resize"""
        super().resizeEvent(event)
        # If we have an image loaded, rescale it
        if self.last_captured_path and not self.lblImage.text():
            pixmap = self.lblImage.pixmap()
            if pixmap:
                self.lblImage.setPixmap(pixmap.scaled(
                    self.lblImage.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
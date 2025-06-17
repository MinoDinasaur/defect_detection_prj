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
from sqlite_database.src.db_operations import update_detection_in_db, create_database, create_connection, get_scanned_barcode
# Import barcode detector
from app.barcode.detector import read_from_scanner_pynput
import threading
from app.ui.styles import AppStyles

class BarcodeThread(QThread):
    """Thread for running barcode scanner in background"""
    barcode_scanned = Signal(str)
    
    def __init__(self):
        super().__init__()
        # Connect to the detector's signal
        from app.barcode.detector import barcode_scanner
        barcode_scanner.barcode_detected.connect(self.barcode_scanned.emit)
    
    def run(self):
        """Run barcode scanner in background thread"""
        try:
            read_from_scanner_pynput()
        except Exception as e:
            print(f"Barcode scanner error: {e}")

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
        self.setStyleSheet(AppStyles.get_button_style())
        
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
        self.setStyleSheet(AppStyles.get_status_card_style())
        
        # Add shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setXOffset(0)
        shadow.setYOffset(1)
        shadow.setColor(QColor(0, 0, 0, 15))
        self.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(2)  # Giảm spacing
        layout.setContentsMargins(4, 4, 4, 4)  # Giảm margins
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(AppStyles.get_status_card_title_style())
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True)
        layout.addWidget(title_label)
        
        # Value
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(AppStyles.get_status_card_value_style(color))
        self.value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.value_label)
        
    def update_value(self, value, color=None):
        self.value_label.setText(str(value))
        if color:
            self.value_label.setStyleSheet(AppStyles.get_status_card_value_style(color))

class MiniStatusCard(QFrame):
    """Compact status card widget"""
    def __init__(self, title, value, color="#4a86e8", parent=None):
        super().__init__(parent)
        # self.setFixedSize(100, 95) 
        self.setStyleSheet(AppStyles.get_status_card_style())
        
        # Layout chính
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 8, 6, 6)  # Tăng padding top từ 6 lên 8
        layout.setSpacing(6)  
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(AppStyles.get_status_card_title_style())
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Value
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(AppStyles.get_status_card_value_style(color))
        self.value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.value_label)
        
    def update_value(self, value, color=None):
        """Update the value and optionally the color"""
        self.value_label.setText(str(value))
        if color:
            self.value_label.setStyleSheet(AppStyles.get_status_card_value_style(color))

class DefectDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Remove default title bar
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.history_needs_refresh = False
        self.history_loaded = False 
        self.processing_timer = QTimer()
        
        # Initialize database
        create_database()
        create_connection()
        
        # Initialize and start barcode scanner thread
        self.init_barcode_scanner()
        
        self.init_UI()

    def init_UI(self):
        """Initialize the main UI with custom title bar"""
        # Window configuration
        self.setWindowTitle("Defect Detection System")
        self.setMinimumSize(1400, 900)
        
        # THAY ĐỔI TỪ showMaximized() SANG showFullScreen()
        self.showFullScreen()  # Chế độ toàn màn hình
        
        # Apply main window style
        self.setStyleSheet(AppStyles.get_main_window_style())
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ADD CUSTOM TITLE BAR
        self.setup_custom_title_bar(main_layout)
        
        # Setup status bar
        self.setup_status_bar()
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(AppStyles.get_main_window_style())
        
        # Create tabs
        self.live_detection_tab = QWidget()
        self.history_tab = DetectionHistoryTab()
        
        # Add tabs
        self.tab_widget.addTab(self.live_detection_tab, "Live Detection")
        self.tab_widget.addTab(self.history_tab, "Detection History")
        
        # Setup tabs
        self.setup_live_detection_tab()
        
        # Add tab widget to main layout
        main_layout.addWidget(self.tab_widget)
        
        # Setup timer for status updates
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status_bar)
        self.status_timer.start(1000)  # Update every second
        
        # Initial status update
        self.update_status_bar()
    
    def setup_status_bar(self):
        """Setup modern status bar"""
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet(AppStyles.get_status_bar_style())
        self.setStatusBar(self.statusBar)
        
        # Status message
        self.status_message = QLabel("Ready")
        self.status_message.setStyleSheet("padding: 4px 8px; font-weight: 500; font-size: 19px; color: #6c757d;")
        self.statusBar.addWidget(self.status_message)
        
        # Add stretch
        self.statusBar.addWidget(QLabel(), 1)
        
        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet(AppStyles.get_progress_bar_style())
        self.progress_bar.setMaximumWidth(200)
        self.statusBar.addPermanentWidget(self.progress_bar)
        
        # Version info
        version_label = QLabel("Đại học Bách Khoa Hà Nội - 2025")
        version_label.setStyleSheet("color: #6c757d; font-size: 19px; padding: 4px 8px;")
        self.statusBar.addPermanentWidget(version_label)

    def init_barcode_scanner(self):
        """Initialize barcode scanner in background thread"""
        self.barcode_thread = BarcodeThread()
        self.barcode_thread.barcode_scanned.connect(self.on_barcode_scanned)
        self.barcode_thread.start()
        print("Barcode scanner started in background")
        
    @Slot(str)
    def on_barcode_scanned(self, barcode):
        """Handle barcode scanned event"""
        print(f"Barcode scanned: {barcode}")
        # Update status bar to show scanned barcode
        self.status_message.setText(f"📦 Barcode: {barcode}")
        
        # You can add visual feedback here
        self.show_barcode_notification(barcode)
        
    def show_barcode_notification(self, barcode):
        """Show visual notification when barcode is scanned"""
        # Create a temporary status message
        original_style = self.status_message.styleSheet()
        self.status_message.setStyleSheet(AppStyles.get_barcode_notification_style())
        
        # Reset style after 3 seconds
        QTimer.singleShot(3000, lambda: self.status_message.setStyleSheet(original_style))

    def setup_live_detection_tab(self):
        """Setup the enhanced UI for live detection tab"""
        main_layout = QVBoxLayout(self.live_detection_tab)
        main_layout.setContentsMargins(24, 4, 24, 4)
        main_layout.setSpacing(2)
        
        # === Header Section ===
        header_frame = QFrame()
        header_frame.setStyleSheet(AppStyles.get_header_frame_style())
        header_layout = QHBoxLayout(header_frame)
        
        # Title and subtitle
        title_layout = QVBoxLayout()
        title_label = QLabel("Quality Control Station")
        title_label.setStyleSheet(AppStyles.get_header_title_style())
        
        title_layout.addWidget(title_label)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        main_layout.addWidget(header_frame)
        
        # === Main Content Splitter ===
        splitter = QSplitter(Qt.Horizontal)
        splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # === Left side: Image area ONLY ===
        self.image_container = QWidget()
        image_layout = QVBoxLayout(self.image_container)
        
        # Enhanced image preview group
        image_group = QGroupBox("▣ Live Camera Feed")
        image_group.setStyleSheet(AppStyles.get_image_group_style())
        image_group_layout = QVBoxLayout(image_group)
        
        # Enhanced image display
        self.image_frame = QFrame()
        self.image_frame.setFrameShape(QFrame.StyledPanel)
        self.image_frame.setStyleSheet(AppStyles.get_image_frame_style())
        image_frame_layout = QVBoxLayout(self.image_frame)
        
        self.lblImage = QLabel("Captured image will appear here\n\nClick 'Capture Image' to start quality inspection")
        self.lblImage.setAlignment(Qt.AlignCenter)
        self.lblImage.setMinimumSize(700, 500)
        self.lblImage.setStyleSheet(AppStyles.get_image_label_style())
        image_frame_layout.addWidget(self.lblImage)
        
        image_group_layout.addWidget(self.image_frame)
        image_layout.addWidget(image_group)
        
        # Image info
        self.image_info = QLabel("No image loaded")
        self.image_info.setStyleSheet(AppStyles.get_image_info_style())
        self.image_info.setAlignment(Qt.AlignCenter)
        self.image_info.setMinimumHeight(20) 
        self.image_info.setMaximumHeight(30)
        image_layout.addWidget(self.image_info)
        
        # === Right side: Status Cards + Results + Controls ===
        self.results_container = QWidget()
        results_layout = QVBoxLayout(self.results_container)
        results_layout.setSpacing(12)  # Space between sections
        
        # === MOVE STATS CARDS HERE (top of right side) ===
        stats_frame = QFrame()
        stats_frame.setStyleSheet(AppStyles.get_stats_frame_style())  # ← Use style from AppStyles
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.setContentsMargins(8, 8, 8, 8)
        stats_layout.setSpacing(8)
        
        # ADD STRETCH BEFORE CARDS TO CENTER THEM
        stats_layout.addStretch()  # Left stretch
        
        # Create cards with adjusted size for right panel
        self.total_defects_card = MiniStatusCard("Defects", "0", "#dc3545")
        self.defect_types_card = MiniStatusCard("Types", "0", "#fd7e14")
        self.status_card = MiniStatusCard("Status", "Ready", "#28a745")
        
        # Add cards to stats layout
        stats_layout.addWidget(self.total_defects_card)
        stats_layout.addWidget(self.defect_types_card)
        stats_layout.addWidget(self.status_card)
        
        # ADD STRETCH AFTER CARDS TO CENTER THEM
        stats_layout.addStretch()  # Right stretch

        # Add stats frame to results container (top)
        results_layout.addWidget(stats_frame)
        
        # === Results Section ===
        results_group = QGroupBox("▦ Analysis Results")
        results_group.setStyleSheet(AppStyles.get_results_group_style())
        results_group_layout = QVBoxLayout(results_group)
        
        # Enhanced results list
        self.lstResult = QListWidget()
        self.lstResult.setStyleSheet(AppStyles.get_results_list_style())
        results_group_layout.addWidget(self.lstResult)
        
        # Enhanced result indicator
        self.result_indicator = QLabel("○ Waiting for analysis...")
        self.result_indicator.setAlignment(Qt.AlignCenter)
        self.result_indicator.setWordWrap(True)
        self.result_indicator.setMinimumHeight(80)
        self.result_indicator.setMaximumHeight(120)
        self.result_indicator.setStyleSheet(AppStyles.get_result_indicator_styles()['waiting'])
        results_group_layout.addWidget(self.result_indicator)
        
        results_layout.addWidget(results_group)
        
        # === Controls Section (bottom of right side) ===
        controls_frame = QFrame()
        controls_frame.setStyleSheet(AppStyles.get_controls_frame_style())
        
        # Add shadow to controls
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 20))
        controls_frame.setGraphicsEffect(shadow)
        
        controls_layout = QVBoxLayout(controls_frame)
        controls_layout.setSpacing(12)
        controls_layout.setContentsMargins(16, 16, 16, 16)
        
        # Enhanced buttons
        self.btnCapture = AnimatedButton("▶ Capture & Analyze")
        self.btnCapture.setMinimumSize(200, 50)
        self.btnCapture.clicked.connect(self.on_capture)
        
        self.btnClear = AnimatedButton("⌫ Clear Results")
        self.btnClear.setMinimumSize(200, 50)
        self.btnClear.setStyleSheet(AppStyles.get_clear_button_style())
        self.btnClear.clicked.connect(self.clear_results)
        
        controls_layout.addWidget(self.btnCapture)
        controls_layout.addWidget(self.btnClear)
        controls_layout.addStretch()  # Push buttons to top
        
        # Add controls to results container (bottom)
        results_layout.addWidget(controls_frame)
        
        # === Add containers to splitter ===
        splitter.addWidget(self.image_container)
        splitter.addWidget(self.results_container)
        
        # Adjust splitter ratios - left side (image) gets more space
        splitter.setStretchFactor(0, 3)  # Image area
        splitter.setStretchFactor(1, 2)  # Results + Status + Controls area
        
        main_layout.addWidget(splitter)
        
        # BỎ CONTROLS FRAME CŨ Ở DƯỚI CÙNG
        # Không cần đoạn code controls ở dưới main_layout nữa

    def setup_custom_title_bar(self, main_layout):
        """Setup custom title bar với 3 nút cùng kích thước - FULLSCREEN MODE"""
        title_bar = QFrame()
        title_bar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2c3e50, stop:1 #34495e);
                border: none;
                max-height: 30px;
                min-height: 30px;
            }
        """)
        
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 5, 0)
        title_layout.setSpacing(15)
        
        # App title
        title_label = QLabel("Defect Detection System")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 2px 2px;
            }
        """)
        title_label.setAlignment(Qt.AlignVCenter)
        title_layout.addWidget(title_label)
        
        title_layout.addStretch()
        
        # 3 NÚT với chức năng fullscreen
        
        # Minimize button - XÁM
        self.minimize_btn = QPushButton("−")
        self.minimize_btn.clicked.connect(self.showMinimized)
        self.minimize_btn.setStyleSheet(AppStyles.get_title_button_style())
        title_layout.addWidget(self.minimize_btn)
        
        # Fullscreen toggle button - XÁM  
        self.fullscreen_btn = QPushButton("□")
        self.fullscreen_btn.clicked.connect(self.toggle_fullscreen)
        self.fullscreen_btn.setStyleSheet(AppStyles.get_title_button_style())
        title_layout.addWidget(self.fullscreen_btn)
        
        # Close button - ĐỎ
        self.close_btn = QPushButton("✕")
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setStyleSheet(AppStyles.get_close_button_style())
        title_layout.addWidget(self.close_btn)
        
        main_layout.addWidget(title_bar)
        
        # Make title bar draggable (chỉ hoạt động khi không fullscreen)
        self.title_bar = title_bar
        self.title_bar.mousePressEvent = self.title_bar_mouse_press
        self.title_bar.mouseMoveEvent = self.title_bar_mouse_move
        self.drag_position = None

    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        if self.isFullScreen():
            self.showNormal()  # Thay đổi từ showMaximized() sang showNormal()
            self.fullscreen_btn.setText("□")
        else:
            self.showFullScreen()  # Chuyển về fullscreen
            self.fullscreen_btn.setText("🗗")

    def title_bar_mouse_press(self, event):
        """Handle mouse press on title bar for dragging - chỉ khi không fullscreen"""
        if not self.isFullScreen() and event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def title_bar_mouse_move(self, event):
        """Handle mouse move on title bar for dragging - chỉ khi không fullscreen"""
        if not self.isFullScreen() and event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPosition().toPoint() - self.drag_position)

    def update_status_bar(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Check if there's a scanned barcode
        current_barcode = get_scanned_barcode()
        if current_barcode:
            self.status_message.setText(f"Ready | {current_time} | Barcode: {current_barcode}")
        else:
            self.status_message.setText(f"Ready | {current_time} | Scanner active")

    def on_capture(self):
        """Enhanced capture with progress indication"""
        try:
            self.status_message.setText("Capturing image...")
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.set_processing_state(True)
            
            camera = PylonCamera() 
            
            # ========================
            # CHUYỂN ĐỔI TEST MODE
            # ========================
            
            # Uncomment một trong những dòng dưới để test:
            
            # 1. Test với file cụ thể:
            # row_id = camera.capture_image_from_file()
            
            # 2. Test với file có tên cụ thể trong storage:
            # row_id = camera.capture_test_image("defect_sample.jpg")
            
            # 3. Dùng camera thật (dòng gốc):
            row_id = camera.capture_image()
            
            if row_id is None:
                raise Exception("Failed to capture image.")    
                
            # Process image in background thread
            self.image_thread = ImageThread(row_id)
            self.image_thread.image_loaded.connect(self.on_image_processed)
            self.image_thread.progress_updated.connect(self.update_progress)
            self.image_thread.start()
            
        except Exception as e:
            self.show_error(f"No device were found.")
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

            # TỰ ĐỘNG REFRESH HISTORY TAB NGAY SAU KHI CHỤP XONG
            if hasattr(self, 'history_tab') and self.history_tab:
                self.history_tab.refresh_data()
                print("History tab auto-refreshed after image processing")
            
            # Mark history as needing refresh (backup)
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
            self.image_info.setText(f"Image: {width}x{height}px | Captured: {timestamp} | Analysis Complete")
            
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
                header_item = QListWidgetItem("⚠ ALERT: Defects Detected")
                header_item.setFont(QFont("Segoe UI", 16, QFont.Bold))
                header_item.setBackground(QColor(255, 240, 240))
                header_item.setForeground(QColor(220, 53, 69))  # Màu đỏ cho text
                self.lstResult.addItem(header_item)
                
                for idx, (i, cls_id) in enumerate(defect_indices):
                    defect_name = classes[int(cls_id)]
                    confidence = confidences[i] * 100
                    
                    # CHỈ HIỂN THỊ TÊN DEFECT, KHÔNG CÓ CONFIDENCE
                    item_text = f"● Defect #{idx+1}: {defect_name}"
                    item = QListWidgetItem(item_text)
                    item.setFont(QFont("Segoe UI", 13))
                    
                    # Enhanced color coding based on confidence (internally - không hiển thị)
                    if confidence > 90:
                        item.setBackground(QColor(255, 182, 193))  # Light pink
                    elif confidence > 75:
                        item.setBackground(QColor(255, 218, 185))  # Peach
                    else:
                        item.setBackground(QColor(255, 235, 205))  # Light yellow
                        
                    self.lstResult.addItem(item)
                
                # Enhanced fail indicator
                self.result_indicator.setText(f"✗ QUALITY FAILED\n{defect_count} defects detected")
                self.result_indicator.setStyleSheet(AppStyles.get_result_indicator_styles()['failed'])
                
            else:
                # Update status cards for pass
                self.total_defects_card.update_value("0", "#27ae60")
                self.defect_types_card.update_value("0", "#27ae60") 
                self.status_card.update_value("PASSED", "#27ae60")
                
                # Enhanced pass message VỚI MÀU XANH LÁ CÂY
                success_item = QListWidgetItem("✓ QUALITY PASSED\n\nProduct meets all quality standards\nNo defects detected in inspection")
                success_item.setFont(QFont("Segoe UI", 16))
                success_item.setBackground(QColor(232, 245, 233))  # Nền xanh nhạt
                success_item.setForeground(QColor(46, 125, 50))   # Chữ xanh lá cây đậm
                self.lstResult.addItem(success_item)
                
                # Enhanced pass indicator
                self.result_indicator.setText("✓ QUALITY PASSED\nNo defects detected")
                self.result_indicator.setStyleSheet(AppStyles.get_result_indicator_styles()['passed'])
            
            self.set_processing_state(False)
            self.status_message.setText("🟢 Analysis complete")
            
        except Exception as e:
            self.show_error(f"Error processing results: {str(e)}")
            self.set_processing_state(False)

    def clear_results(self):
        """Enhanced clear function with animations"""
        self.lblImage.clear()
        self.lblImage.setText("Captured image will appear here\n\nClick 'Capture Image' to start quality inspection")
        self.lstResult.clear()
        self.image_info.setText("No image loaded")
        
        # Reset mini status cards
        self.total_defects_card.update_value("0", "#6c757d")
        self.defect_types_card.update_value("0", "#6c757d") 
        self.status_card.update_value("Ready", "#6c757d")
        
        # Reset indicator with proper sizing
        self.result_indicator.setText("Waiting for analysis...")
        self.result_indicator.setWordWrap(True)
        self.result_indicator.setMaximumHeight(120)
        self.result_indicator.setStyleSheet(AppStyles.get_result_indicator_styles()['waiting'])
        
        self.status_message.setText("Results cleared")

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
            self.result_indicator.setStyleSheet(AppStyles.get_result_indicator_styles()['processing'])
        else:
            self.setCursor(Qt.ArrowCursor)

    def show_error(self, message):
        """Enhanced error display with proper text wrapping"""
        self.status_message.setText(f"Error: {message}")
        
        # Update status card
        self.status_card.update_value("Error", "#e74c3c")
        
        # Enhanced error indicator with word wrap and size constraints
        self.result_indicator.setText(f"ERROR\n{message}")
        self.result_indicator.setWordWrap(True)
        self.result_indicator.setMaximumHeight(120)
        self.result_indicator.setStyleSheet(AppStyles.get_result_indicator_styles()['error'])

    def show_history_tab(self):
        """Switch to history tab and refresh data"""
        self.tab_widget.setCurrentWidget(self.history_tab)
        self.history_tab.refresh_data()

    def resizeEvent(self, event):
        """Handle window resize"""
        super().resizeEvent(event)
    
        # Kiểm tra xem lblImage đã được khởi tạo chưa
        if hasattr(self, 'lblImage'):
            # Resize pixmap if available
            pixmap = self.lblImage.pixmap()
            if pixmap and not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    self.lblImage.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.lblImage.setPixmap(scaled_pixmap)

    def closeEvent(self, event):
        """Handle close event with confirmation dialog"""
        try:
            # TẠO DIALOG XÁC NHẬN THOÁT
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Exit Application")
            msg_box.setIcon(QMessageBox.Question)
            
            # NỘI DUNG DIALOG VỚI FONT LỚN
            msg_box.setText(f"""
            <h2 style='color: #e74c3c; font-size: 24px;'>Exit Defect Detection System</h2>
            <p style='font-size: 25px; margin: 15px 0;'>
            Are you sure you want to <b>exit</b> the application?
            </p>
            <p style='font-size: 20px; background: #fff3cd; padding: 10px; border-left: 4px solid #ffc107;'>
            </p>
            <p style='font-size: 20x; color: #666; margin-top: 15px;'>
            All data has been automatically saved to the database.
            </p>
            """)
            
            # TĂNG KÍCH THƯỚC DIALOG
            msg_box.setMinimumSize(500, 350)
            msg_box.resize(600, 400)
            
            # CUSTOM BUTTONS VỚI FONT LỚN HƠN
            exit_btn = msg_box.addButton("Exit", QMessageBox.YesRole)
            cancel_btn = msg_box.addButton("Cancel", QMessageBox.NoRole)
            
            # SỬ DỤNG STYLES TỪ AppStyles
            exit_btn.setStyleSheet(AppStyles.get_exit_dialog_exit_button_style())
            cancel_btn.setStyleSheet(AppStyles.get_exit_dialog_cancel_button_style())
            
            # HIỂN THỊ DIALOG VÀ XỬ LÝ KẾT QUẢ
            msg_box.exec()
            
            if msg_box.clickedButton() == exit_btn:
                # USER CHỌN EXIT - THỰC HIỆN CLEANUP
                print("User confirmed exit - Starting cleanup...")
                
                # Hiển thị thông báo đang thoát
                self.status_message.setText("Shutting down application...")
                
                # Stop barcode scanner thread
                if hasattr(self, 'barcode_thread') and self.barcode_thread.isRunning():
                    print("Stopping barcode scanner...")
                    
                    # Request thread to stop gracefully
                    self.barcode_thread.requestInterruption()
                    
                    # Wait for thread to finish naturally
                    if not self.barcode_thread.wait(1000):  
                        print("Thread didn't stop gracefully, terminating...")
                        self.barcode_thread.terminate()
                        if not self.barcode_thread.wait(500):  # Wait 0.5 more second
                            print("Force killing thread")        
                    print("Barcode scanner stopped")
                
                # Stop image processing thread
                if hasattr(self, 'image_thread') and self.image_thread.isRunning():
                    print("Stopping image processing thread...")
                    self.image_thread.requestInterruption()
                    if not self.image_thread.wait(1000):
                        self.image_thread.terminate()
                    print("Image processing thread stopped")
                
                # Stop status timer
                if hasattr(self, 'status_timer'):
                    self.status_timer.stop()
                    print("Status timer stopped")
                
                print("Cleanup completed successfully")
                
                # Accept the close event
                event.accept()
                
            else:
                # USER CHỌN CANCEL - HỦY THOÁT
                print("User cancelled exit")
                self.status_message.setText("Exit cancelled - Application continues running")
                
                # Ignore the close event
                event.ignore()
                
        except Exception as e:
            print(f"Error during cleanup: {e}")
            # Nếu có lỗi trong cleanup, vẫn cho phép thoát
            event.accept()
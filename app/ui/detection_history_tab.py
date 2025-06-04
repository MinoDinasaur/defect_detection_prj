from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
    QGroupBox, QLabel, QComboBox, QDateEdit, QHeaderView, QSplitter, QMessageBox,
    QDialog, QFileDialog, QFrame, QSizePolicy, QGridLayout, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QDateTime, QDate, Signal, Slot
from PySide6.QtGui import QPixmap, QImage, QIcon, QFont, QColor
import sqlite3
import cv2
import numpy as np
import os
from sqlite_database.src.db_operations import (
    get_defect_types, delete_detection_from_db,
    get_detections, get_image_data, get_detections_paginated
)
from app.ui.styles import HistoryTabStyles

class ImageViewDialog(QDialog):
    """Enhanced dialog for viewing images in larger size"""
    def __init__(self, image_data, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"🖼️ {title}")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(HistoryTabStyles.get_dialog_style())
        
        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Title section
        title_frame = QFrame()
        title_frame.setStyleSheet(HistoryTabStyles.get_dialog_title_frame_style())
        title_layout = QHBoxLayout(title_frame)
        
        title_label = QLabel(f"📸 {title}")
        title_label.setStyleSheet(HistoryTabStyles.get_dialog_title_style())
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        layout.addWidget(title_frame)
        
        # Image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setStyleSheet(HistoryTabStyles.get_dialog_image_label_style())
        
        # Convert image data to QPixmap
        if isinstance(image_data, bytes):
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width, channel = img.shape
            bytes_per_line = 3 * width
            q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
        elif isinstance(image_data, QPixmap):
            pixmap = image_data
        else:
            self.image_label.setText("Invalid image data")
            layout.addWidget(self.image_label)
            return
            
        # Scale image maintaining aspect ratio
        self.image_label.setPixmap(pixmap.scaled(
            700, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        layout.addWidget(self.image_label)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_button = QPushButton("💾 Save Image")
        save_button.clicked.connect(lambda: self.save_image(pixmap))
        save_button.setStyleSheet(HistoryTabStyles.get_dialog_save_button_style())
        
        close_button = QPushButton("✖️ Close")
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet(HistoryTabStyles.get_dialog_close_button_style())
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)
        
    def save_image(self, pixmap):
        """Save image to file"""
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "PNG Files (*.png);;JPEG Files (*.jpg)"
        )
        
        if file_name:
            pixmap.save(file_name)
            QMessageBox.information(self, "Success", f"Image saved to {file_name}")

class ClickableImageLabel(QLabel):
    """Custom QLabel that emits signals on double-click"""
    double_clicked = Signal(int, str)  # row_id, image_type
    
    def __init__(self, row_id, image_type, parent=None):
        super().__init__(parent)
        self.row_id = row_id
        self.image_type = image_type
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(HistoryTabStyles.get_image_thumbnail_style())
        
        # Set cursor pointer để cho biết có thể click
        self.setCursor(Qt.PointingHandCursor)
        
        # Add tooltip to indicate double-click functionality
        self.setToolTip("Double-click to view full image")
        
    def mouseDoubleClickEvent(self, event):
        """Handle double-click event"""
        if event.button() == Qt.LeftButton:
            self.double_clicked.emit(self.row_id, self.image_type)
        super().mouseDoubleClickEvent(event)

class DetectionHistoryTab(QWidget):
    """Enhanced tab for viewing detection history with pagination"""
    
    refresh_signal = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # Pagination variables
        self.current_page = 1
        self.page_size = 10  # 10 records per page
        self.total_records = 0
        self.total_pages = 0
        
        self.initUI()
        
    def initUI(self):
        """Initialize enhanced UI components with pagination"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)
        
        # === Enhanced Header ===
        header_frame = QFrame()
        header_frame.setStyleSheet(HistoryTabStyles.get_header_frame_style())
        
        header_layout = QHBoxLayout(header_frame)
        
        title_label = QLabel("📊 Detection History & Analytics")
        title_label.setStyleSheet(HistoryTabStyles.get_header_title_style())
        
        subtitle_label = QLabel("View and analyze past quality control results")
        subtitle_label.setStyleSheet(HistoryTabStyles.get_header_subtitle_style())
        
        title_layout = QVBoxLayout()
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        main_layout.addWidget(header_frame)
        
        # === Enhanced Filter Section ===
        filter_group = QGroupBox("🔍 Filter and Search Options")
        filter_group.setStyleSheet(HistoryTabStyles.get_filter_group_style())
        
        filter_layout = QGridLayout(filter_group)
        filter_layout.setSpacing(16)
        
        # Enhanced date controls
        filter_layout.addWidget(QLabel("📅 Date Range:"), 0, 0)
        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate.currentDate().addDays(-7))
        filter_layout.addWidget(self.date_from, 0, 1)
        
        filter_layout.addWidget(QLabel("to"), 0, 2)
        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate())
        filter_layout.addWidget(self.date_to, 0, 3)
        
        # Enhanced defect filter
        filter_layout.addWidget(QLabel("🔧 Defect Type:"), 0, 4)
        self.defect_combo = QComboBox()
        self.defect_combo.addItem("All")
        filter_layout.addWidget(self.defect_combo, 0, 5)
        
        # Quick date buttons
        quick_buttons = [
            ("Today", lambda: self.set_date_range(0)),
            ("Last Week", lambda: self.set_date_range(7)),
            ("Last Month", lambda: self.set_date_range(30))
        ]
        
        for i, (text, func) in enumerate(quick_buttons):
            btn = QPushButton(text)
            btn.clicked.connect(func)
            btn.setStyleSheet(HistoryTabStyles.get_quick_filter_button_style())
            filter_layout.addWidget(btn, 1, i)
        
        # Apply filter button
        self.apply_filter_btn = QPushButton("🔍 Apply Filter")
        self.apply_filter_btn.clicked.connect(self.refresh_data)
        filter_layout.addWidget(self.apply_filter_btn, 1, 3, 1, 2)
        
        main_layout.addWidget(filter_group)
        
        # === MAIN CONTENT: HORIZONTAL SPLITTER ===
        # Thay đổi từ Vertical thành Horizontal splitter
        main_content_splitter = QSplitter(Qt.Horizontal)
        main_content_splitter.setChildrenCollapsible(False)  # Ngăn không cho collapse
        
        # === LEFT SIDE: Table và Pagination (70%) ===
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 10, 0)  # Margin phải để tạo khoảng cách
        left_layout.setSpacing(12)
        
        # Enhanced table styling
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels(["#", "Date/Time", "Raw Image", "Detection Image", "Defects", "Barcode"])
        
        header = self.history_table.horizontalHeader()
        
        # Cột # - cố định nhỏ (40px)
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        self.history_table.setColumnWidth(0, 40)
        
        # Cột Date/Time - giữ nguyên (100px)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        self.history_table.setColumnWidth(1, 100)
        
        # Cột Raw Image - giữ nguyên (100px)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        self.history_table.setColumnWidth(2, 140)
        
        # Cột Detection Image - giữ nguyên (100px)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        self.history_table.setColumnWidth(3, 140)
        
        # Cột Defects - CỐ ĐỊNH 180PX thay vì stretch
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        self.history_table.setColumnWidth(4, 690)
        
        # Cột Barcode - stretch để chiếm phần còn lại
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setMinimumHeight(400)  # Đặt chiều cao tối thiểu
        
        self.history_table.setStyleSheet(HistoryTabStyles.get_table_style())
        
        left_layout.addWidget(self.history_table)
        
        # === PAGINATION CONTROLS (dưới table) ===
        pagination_frame = QFrame()
        pagination_frame.setStyleSheet(HistoryTabStyles.get_pagination_frame_style())
        pagination_layout = QHBoxLayout(pagination_frame)
        pagination_layout.setSpacing(12)
        
        # Records info (left side)
        self.records_info_label = QLabel("Showing 0-0 of 0 records")
        self.records_info_label.setStyleSheet(HistoryTabStyles.get_pagination_records_info_style())
        pagination_layout.addWidget(self.records_info_label)
        
        pagination_layout.addStretch()
        
        # Navigation buttons (center)
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(8)
        
        self.first_page_btn = QPushButton("⏮️ First")
        self.first_page_btn.clicked.connect(self.go_to_first_page)
        
        self.prev_page_btn = QPushButton("⬅️ Prev")
        self.prev_page_btn.clicked.connect(self.go_to_previous_page)
        
        self.page_info_label = QLabel("Page 1 of 1")
        self.page_info_label.setStyleSheet(HistoryTabStyles.get_pagination_page_info_style())
        
        self.next_page_btn = QPushButton("Next ➡️")
        self.next_page_btn.clicked.connect(self.go_to_next_page)
        
        self.last_page_btn = QPushButton("Last ⏭️")
        self.last_page_btn.clicked.connect(self.go_to_last_page)
        
        # Apply pagination button style to all buttons
        pagination_button_style = HistoryTabStyles.get_pagination_button_style()
        for btn in [self.first_page_btn, self.prev_page_btn, self.next_page_btn, self.last_page_btn]:
            btn.setStyleSheet(pagination_button_style)
        
        nav_layout.addWidget(self.first_page_btn)
        nav_layout.addWidget(self.prev_page_btn)
        nav_layout.addWidget(self.page_info_label)
        nav_layout.addWidget(self.next_page_btn)
        nav_layout.addWidget(self.last_page_btn)
        
        pagination_layout.addLayout(nav_layout)
        
        pagination_layout.addStretch()
        
        # Page size selector (right side)
        page_size_layout = QHBoxLayout()
        
        show_label = QLabel("Show:")
        show_label.setStyleSheet(HistoryTabStyles.get_pagination_label_style())
        page_size_layout.addWidget(show_label)
        
        self.page_size_combo = QComboBox()
        self.page_size_combo.addItems(["5", "10", "20", "50"])
        self.page_size_combo.setCurrentText("10")
        self.page_size_combo.currentTextChanged.connect(self.on_page_size_changed)
        self.page_size_combo.setStyleSheet(HistoryTabStyles.get_pagination_combo_style())
        page_size_layout.addWidget(self.page_size_combo)
        
        per_page_label = QLabel("per page")
        per_page_label.setStyleSheet(HistoryTabStyles.get_pagination_label_style())
        page_size_layout.addWidget(per_page_label)
        
        pagination_layout.addLayout(page_size_layout)
        
        left_layout.addWidget(pagination_frame)
        
        # === RIGHT SIDE: Details Panel (30%) ===
        details_container = QWidget()
        details_container.setMaximumWidth(400)  # Giới hạn chiều rộng tối đa
        details_container.setMinimumWidth(300)   # Chiều rộng tối thiểu
        details_layout = QVBoxLayout(details_container)
        details_layout.setContentsMargins(10, 0, 0, 0)  # Margin trái để tạo khoảng cách
        details_layout.setSpacing(16)
        
        # Enhanced details section
        details_frame = QFrame()
        details_frame.setFrameShape(QFrame.StyledPanel)
        details_frame.setStyleSheet(HistoryTabStyles.get_details_frame_style())
        
        details_frame_layout = QVBoxLayout(details_frame)
        details_frame_layout.setContentsMargins(16, 16, 16, 16)
        details_frame_layout.setSpacing(12)
        
        # Enhanced detail labels
        details_title = QLabel("📋 Selected Detection Details")
        details_title.setStyleSheet(HistoryTabStyles.get_details_title_style())
        details_frame_layout.addWidget(details_title)
        
        # Create a grid layout for better organization
        details_grid = QGridLayout()
        details_grid.setSpacing(10)
        details_grid.setContentsMargins(0, 8, 0, 8)
        
        # Defect info - spans full width
        self.details_defect = QLabel("🔧 None selected")
        self.details_defect.setWordWrap(True)
        self.details_defect.setMinimumHeight(40)
        details_grid.addWidget(self.details_defect, 0, 0, 1, 2)
        
        # Time and Barcode in separate rows for better readability
        self.details_time = QLabel("⏰ None selected")
        self.details_time.setWordWrap(True)
        self.details_time.setMinimumHeight(35)
        details_grid.addWidget(self.details_time, 1, 0, 1, 2)
        
        self.details_barcode = QLabel("📦 None selected")
        self.details_barcode.setWordWrap(True)
        self.details_barcode.setMinimumHeight(35)
        details_grid.addWidget(self.details_barcode, 2, 0, 1, 2)
        
        # Apply initial styling
        for label in [self.details_defect, self.details_time, self.details_barcode]:
            label.setStyleSheet(HistoryTabStyles.get_details_label_style())
        
        details_frame_layout.addLayout(details_grid)
        
        # Enhanced action buttons
        actions_layout = QVBoxLayout()  # Vertical layout for better spacing
        actions_layout.setSpacing(8)
        actions_layout.setContentsMargins(0, 16, 0, 0)
        
        button_configs = [
            ("📤 Export Detection", self.export_detection, "#f39c12"),
            ("🗑️ Delete Detection", self.delete_detection, "#e74c3c")
        ]
        
        self.action_buttons = []
        for text, func, color in button_configs:
            btn = QPushButton(text)
            btn.setEnabled(False)
            btn.clicked.connect(func)
            btn.setMinimumHeight(40)  # Tăng chiều cao button
            btn.setStyleSheet(HistoryTabStyles.get_action_button_style(color))
            self.action_buttons.append(btn)
            actions_layout.addWidget(btn)
        
        details_frame_layout.addLayout(actions_layout)
        details_frame_layout.addStretch()  # Push content to top
        
        details_layout.addWidget(details_frame)
        details_layout.addStretch()  # Push content to top
        
        # === ADD TO SPLITTER ===
        main_content_splitter.addWidget(left_container)
        main_content_splitter.addWidget(details_container)
        
        # Set splitter proportions: 70% table, 30% details
        main_content_splitter.setStretchFactor(0, 7)  # Left side (table)
        main_content_splitter.setStretchFactor(1, 3)  # Right side (details)
        main_content_splitter.setSizes([700, 300])  # Initial sizes
        
        # Add splitter to main layout
        main_layout.addWidget(main_content_splitter)
        
        # Connect signals
        self.history_table.itemSelectionChanged.connect(self.on_selection_changed)
        
        # Initialize data
        self.populate_defect_types()
        self.refresh_data()
    
    def refresh_data(self):
        """Refresh data with pagination"""
        try:
            date_from = self.date_from.date().toString("yyyy-MM-dd")
            date_to = self.date_to.date().addDays(1).toString("yyyy-MM-dd")
            defect_filter = self.defect_combo.currentText()
            
            # Get paginated data
            rows, total_count = get_detections_paginated(
                date_from, date_to, defect_filter, 
                self.current_page, self.page_size
            )
            
            # Update pagination info
            self.total_records = total_count
            self.total_pages = (total_count + self.page_size - 1) // self.page_size if total_count > 0 else 1
            
            # Clear table
            self.history_table.setRowCount(0)
            
            # Populate table with serial numbers
            for i, row in enumerate(rows):
                rowid, time_str, img_raw, img_detect, defect, barcode = row
                
                self.history_table.insertRow(i)
                self.history_table.setRowHeight(i, 70)  # Tăng chiều cao row lên 70px để chứa defects dài
                
                # SERIAL NUMBER (hiển thị) - tính từ trang hiện tại
                serial_number = (self.current_page - 1) * self.page_size + i + 1
                serial_item = QTableWidgetItem(str(serial_number))
                serial_item.setTextAlignment(Qt.AlignCenter)
                # LƯU DATABASE ID VÀO DATA ROLE để dùng cho delete
                serial_item.setData(Qt.UserRole, rowid)  # Store real database ID
                self.history_table.setItem(i, 0, serial_item)
                
                # Time - HIỂN THỊ ĐẦY ĐỦ HƠN
                time_parts = time_str.split(' ')
                if len(time_parts) >= 2:
                    time_display = time_parts[1][:8]  # Lấy HH:MM:SS thay vì chỉ HH:MM
                else:
                    time_display = time_str[-8:]  # Lấy 8 ký tự cuối
                
                time_item = QTableWidgetItem(time_display)
                time_item.setTextAlignment(Qt.AlignCenter)
                time_item.setToolTip(time_str)  # Full timestamp trong tooltip
                self.history_table.setItem(i, 1, time_item)
                
                # Images with double-click - TĂNG KÍCH THƯỚC ẢNH
                for col, img_data, img_type in [(2, img_raw, "img_raw"), (3, img_detect, "img_detect")]:
                    if img_data:
                        nparr = np.frombuffer(img_data, np.uint8)
                        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = cv2.resize(img, (90, 60))  # Tăng từ (70, 50) lên (90, 60) để fit 100px column
                        height, width, channel = img.shape
                        bytes_per_line = 3 * width
                        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
                        pixmap = QPixmap.fromImage(q_img)
                        
                        lbl = ClickableImageLabel(rowid, img_type)  # Vẫn dùng database ID
                        lbl.setPixmap(pixmap)
                        lbl.double_clicked.connect(self.on_image_double_clicked)
                        
                        self.history_table.setCellWidget(i, col, lbl)
                    else:
                        self.history_table.setItem(i, col, QTableWidgetItem("No image"))
                
                # Defects - HIỂN THỊ ĐẦY ĐỦ, KHÔNG CẮT
                defect_display = defect if defect else "No defects"
                
                # BỎ LOGIC CẮT TEXT - hiển thị đầy đủ trong 690px column
                # Không cần: if len(defect_display) > 25: defect_display = defect_display[:22] + "..."
                
                defect_item = QTableWidgetItem(defect_display)
                defect_item.setToolTip(defect if defect else "No defects")  # Vẫn giữ tooltip
                defect_item.setToolTip(defect if defect else "No defects")  # Full text trong tooltip
                
                if defect and defect.lower() != "no defects":
                    defect_item.setBackground(QColor(255, 235, 238))
                    defect_item.setForeground(QColor(183, 28, 28))
                else:
                    defect_item.setBackground(QColor(232, 245, 233))
                    defect_item.setForeground(QColor(46, 125, 50))
                
                self.history_table.setItem(i, 4, defect_item)
                
                # Barcode - HIỂN THỊ ĐẦY ĐỦ HƠN VÌ CÓ STRETCH
                barcode_display = barcode if barcode else "N/A"
                barcode_item = QTableWidgetItem(barcode_display)
                barcode_item.setTextAlignment(Qt.AlignCenter)
                barcode_item.setToolTip(barcode if barcode else "No barcode")
                self.history_table.setItem(i, 5, barcode_item)
            
            # Update pagination controls
            self.update_pagination_controls();
            
            # Update parent status
            if hasattr(self.parent, 'status_message'):
                start_record = (self.current_page - 1) * self.page_size + 1 if self.total_records > 0 else 0
                end_record = min(self.current_page * self.page_size, self.total_records)
                self.parent.status_message.setText(
                    f"📊 Showing {start_record}-{end_record} of {self.total_records} records (Page {self.current_page}/{self.total_pages})"
                )
            
            self.reset_details()
            self.populate_defect_types()
            
        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"Error loading detection history: {str(e)}")
    
    def update_pagination_controls(self):
        """Update pagination button states and labels"""
        # Update page info
        self.page_info_label.setText(f"Page {self.current_page} of {self.total_pages}")
        
        # Update records info
        start_record = (self.current_page - 1) * self.page_size + 1 if self.total_records > 0 else 0
        end_record = min(self.current_page * self.page_size, self.total_records)
        self.records_info_label.setText(f"Showing {start_record}-{end_record} of {self.total_records} records")
        
        # Update button states
        self.first_page_btn.setEnabled(self.current_page > 1)
        self.prev_page_btn.setEnabled(self.current_page > 1)
        self.next_page_btn.setEnabled(self.current_page < self.total_pages)
        self.last_page_btn.setEnabled(self.current_page < self.total_pages)
    
    # Pagination navigation methods
    def go_to_first_page(self):
        """Go to first page"""
        if self.current_page != 1:
            self.current_page = 1
            self.refresh_data()
    
    def go_to_previous_page(self):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_data()
    
    def go_to_next_page(self):
        """Go to next page"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.refresh_data()
    
    def go_to_last_page(self):
        """Go to last page"""
        if self.current_page != self.total_pages:
            self.current_page = self.total_pages
            self.refresh_data()
    
    @Slot(str)
    def on_page_size_changed(self, new_size):
        """Handle page size change"""
        self.page_size = int(new_size)
        self.current_page = 1  # Reset to first page
        self.refresh_data()
    
    def set_date_range(self, days_back):
        """Set date range for quick filters"""
        today = QDate.currentDate()
        self.date_to.setDate(today)
        self.date_from.setDate(today.addDays(-days_back))
        self.current_page = 1  # Reset to first page when filter changes
        self.refresh_data()
    
    def delete_detection(self):
        """Delete selected detection from database and refresh current page"""
        database_id = self.get_selected_row_id()
        if database_id is None:
            return
        
        # Get serial number for display
        selected_items = self.history_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            serial_number = self.history_table.item(row, 0).text()
        else:
            serial_number = "Unknown"
            
        reply = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete detection #{serial_number}?\n\n(Database ID: {database_id})",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                delete_detection_from_db(database_id)  # Use real database ID
                
                if hasattr(self.parent, 'status_message'):
                    self.parent.status_message.setText(f"🗑️ Detection #{serial_number} deleted (DB ID: {database_id})")
                
                # Check if current page becomes empty after deletion
                if self.history_table.rowCount() == 1 and self.current_page > 1:
                    self.current_page -= 1  # Go to previous page if current page becomes empty
                
                self.refresh_data()
            except Exception as e:
                QMessageBox.warning(self, "Delete Error", f"Error deleting detection: {str(e)}")
    
    def reset_details(self):
        """Reset detail view when no row is selected"""
        self.details_defect.setText("🔧 None selected")
        self.details_time.setText("⏰ None selected")
        self.details_barcode.setText("📦 None selected")
        
        defect_styles = HistoryTabStyles.get_defect_status_styles()
        for label in [self.details_defect, self.details_time, self.details_barcode]:
            label.setStyleSheet(defect_styles['none_selected'])
        
        for btn in self.action_buttons:
            btn.setEnabled(False)
    
    def get_selected_row_id(self):
        """Get the real database ID from selected row (stored in UserRole)"""
        selected_items = self.history_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            # Lấy database ID từ UserRole của cột đầu tiên
            id_item = self.history_table.item(row, 0)
            if id_item:
                return id_item.data(Qt.UserRole)  # Returns real database rowid
        return None
    
    def get_image_data(self, row_id, image_type):
        """Get image data from database."""
        try:
            return get_image_data(row_id, image_type)
        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"Error retrieving image: {str(e)}")
            return None
    
    def export_detection(self):
        """Export detection data to files"""
        database_id = self.get_selected_row_id()
        if database_id is None:
            return
        
        # Get serial number for display
        selected_items = self.history_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            serial_number = self.history_table.item(row, 0).text()
        else:
            serial_number = "Unknown"
            
        try:
            conn = sqlite3.connect('sqlite_database/db/detections.db')
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT time, img_raw, img_detect, defect, barcode FROM detections WHERE rowid = ?", 
                (database_id,)  # Use real database ID
            )
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                QMessageBox.warning(self, "Error", f"Detection record not found (DB ID: {database_id})")
                return
                
            time_str, img_raw, img_detect, defect, barcode = result
            
            export_dir = QFileDialog.getExistingDirectory(
                self, "Select Directory for Export", "",
                QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
            )
            
            if not export_dir:
                return
                
            safe_time = time_str.replace(":", "-").replace(" ", "_")
            filename_base = f"detection_serial_{serial_number}_db_{database_id}_{safe_time}"
            
            if img_raw:
                self.save_image_data(img_raw, os.path.join(export_dir, f"{filename_base}_raw.png"))
                
            if img_detect:
                self.save_image_data(img_detect, os.path.join(export_dir, f"{filename_base}_detect.png"))
                
            with open(os.path.join(export_dir, f"{filename_base}_info.txt"), 'w') as f:
                f.write(f"Serial Number: #{serial_number}\n")
                f.write(f"Database ID: {database_id}\n")
                f.write(f"Time: {time_str}\n")
                f.write(f"Defects: {defect}\n")
                f.write(f"Barcode: {barcode}\n")
            
            QMessageBox.information(
                self, "Export Complete", 
                f"Detection #{serial_number} exported successfully to {export_dir}"
            )
            
        except Exception as e:
            QMessageBox.warning(self, "Export Error", f"Error exporting detection: {str(e)}")
    
    def save_image_data(self, img_data, filepath):
        """Save image data to file"""
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imwrite(filepath, img)
    
    def on_selection_changed(self):
        """Handle table selection change"""
        selected_items = self.history_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            
            # Get data from selected row
            id_item = self.history_table.item(row, 0)
            serial_number = id_item.text()  # Serial number for display
            database_id = id_item.data(Qt.UserRole)  # Real database ID
            
            time_str = self.history_table.item(row, 1).toolTip()  # Full timestamp from tooltip
            defect_item = self.history_table.item(row, 4)
            defect = defect_item.toolTip() if defect_item else "No defects"
            barcode_item = self.history_table.item(row, 5)
            barcode = barcode_item.toolTip() if barcode_item else "No barcode"
            
            # Update detail labels với serial number
            self.details_defect.setText(f"🔧 Defect: {defect}")
            self.details_time.setText(f"⏰ Time: {time_str}")
            self.details_barcode.setText(f"📦 Barcode: {barcode} | Serial: #{serial_number}")
            
            # Style based on defect status
            defect_styles = HistoryTabStyles.get_defect_status_styles()
            if defect and defect.lower() != "no defects":
                for label in [self.details_defect, self.details_time, self.details_barcode]:
                    label.setStyleSheet(defect_styles['failed'])
            else:
                for label in [self.details_defect, self.details_time, self.details_barcode]:
                    label.setStyleSheet(defect_styles['passed'])
            
            # Enable action buttons
            for btn in self.action_buttons:
                btn.setEnabled(True)
        else:
            self.reset_details()
    
    def on_image_double_clicked(self, row_id, image_type):
        """Handle image double-click to show full view"""
        try:
            image_data = self.get_image_data(row_id, image_type)
            if image_data:
                title = f"Detection #{row_id} - {'Raw Image' if image_type == 'img_raw' else 'Detection Result'}"
                dialog = ImageViewDialog(image_data, title, self)
                dialog.exec()
            else:
                QMessageBox.warning(self, "No Image", "No image data available for this record.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error loading image: {str(e)}")
    
    def populate_defect_types(self):
        """Populate defect type combo box"""
        try:
            current_selection = self.defect_combo.currentText()
            self.defect_combo.clear()
            self.defect_combo.addItem("All")
            
            defect_types = get_defect_types()
            unique_defects = set()
            
            for row in defect_types:
                defect = row[0]
                if defect and defect.strip():
                    # Split multiple defects and add each
                    for single_defect in defect.split(','):
                        single_defect = single_defect.strip()
                        if single_defect and single_defect not in unique_defects:
                            unique_defects.add(single_defect)
            
            # Add sorted unique defects
            for defect in sorted(unique_defects):
                self.defect_combo.addItem(defect)
            
            # Restore previous selection if it exists
            index = self.defect_combo.findText(current_selection)
            if index >= 0:
                self.defect_combo.setCurrentIndex(index)
                
        except Exception as e:
            print(f"Error populating defect types: {e}")
    
    def delete_detection(self):
        """Delete selected detection from database and refresh current page"""
        database_id = self.get_selected_row_id()
        if database_id is None:
            return
        
        # Get serial number for display
        selected_items = self.history_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            serial_number = self.history_table.item(row, 0).text()
        else:
            serial_number = "Unknown"
            
        reply = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete detection #{serial_number}?\n\n(Database ID: {database_id})",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                delete_detection_from_db(database_id)  # Use real database ID
                
                if hasattr(self.parent, 'status_message'):
                    self.parent.status_message.setText(f"🗑️ Detection #{serial_number} deleted (DB ID: {database_id})")
                
                # Check if current page becomes empty after deletion
                if self.history_table.rowCount() == 1 and self.current_page > 1:
                    self.current_page -= 1  # Go to previous page if current page becomes empty
                
                self.refresh_data()
            except Exception as e:
                QMessageBox.warning(self, "Delete Error", f"Error deleting detection: {str(e)}")
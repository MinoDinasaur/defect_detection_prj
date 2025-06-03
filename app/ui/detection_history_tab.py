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
from sqlite_database.src.db_operations import (
    get_defect_types, delete_detection_from_db,
    get_detections, get_image_data
)
import os
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
    """Enhanced tab for viewing detection history"""
    
    refresh_signal = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()
        
    def initUI(self):
        """Initialize enhanced UI components"""
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
        
        # === Enhanced Results Table ===
        results_splitter = QSplitter(Qt.Vertical)
        
        # Enhanced table styling
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels(["ID", "Date/Time", "Raw Image", "Detection Image", "Defects", "Barcode"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.history_table.setAlternatingRowColors(True)
        
        self.history_table.setStyleSheet(HistoryTabStyles.get_table_style())
        
        results_splitter.addWidget(self.history_table)
        
        # Enhanced details section
        details_frame = QFrame()
        details_frame.setFrameShape(QFrame.StyledPanel)
        details_frame.setMaximumHeight(220)
        details_frame.setStyleSheet(HistoryTabStyles.get_details_frame_style())
        
        details_layout = QVBoxLayout(details_frame)
        
        # Enhanced detail labels
        details_title = QLabel("📋 Selected Detection Details")
        details_title.setStyleSheet(HistoryTabStyles.get_details_title_style())
        details_layout.addWidget(details_title)
        
        self.details_defect = QLabel("🔧 Defect: None selected")
        self.details_time = QLabel("⏰ Time: None selected") 
        self.details_barcode = QLabel("📦 Barcode: None selected")
        
        for label in [self.details_defect, self.details_time, self.details_barcode]:
            label.setStyleSheet(HistoryTabStyles.get_details_label_style())
            details_layout.addWidget(label)
        
        # Enhanced action buttons - CHỈ GIỮ LẠI 2 NÚT
        actions_layout = QHBoxLayout()
        
        button_configs = [
            ("📤 Export", self.export_detection, "#f39c12"),
            ("🗑️ Delete", self.delete_detection, "#e74c3c")
        ]
        
        self.action_buttons = []
        for text, func, color in button_configs:
            btn = QPushButton(text)
            btn.setEnabled(False)
            btn.clicked.connect(func)
            btn.setStyleSheet(HistoryTabStyles.get_action_button_style(color))
            self.action_buttons.append(btn)
            actions_layout.addWidget(btn)
        
        # Add stretch to center the buttons
        actions_layout.addStretch()
        
        details_layout.addLayout(actions_layout)
        details_layout.addStretch()
        
        results_splitter.addWidget(details_frame)
        results_splitter.setSizes([600, 220])
        
        main_layout.addWidget(results_splitter)
        
        # Connect signals
        self.history_table.itemSelectionChanged.connect(self.on_selection_changed)
        
        # Initialize data
        self.populate_defect_types()
        self.refresh_data()
    
    def set_date_range(self, days_back):
        """Set date range for quick filters"""
        today = QDate.currentDate()
        self.date_to.setDate(today)
        self.date_from.setDate(today.addDays(-days_back))
        self.refresh_data()
    
    def populate_defect_types(self):
        """Populate defect type combobox from database"""
        try:
            defect_types = get_defect_types()       
            current_selection = self.defect_combo.currentText()
            
            self.defect_combo.clear()
            self.defect_combo.addItem("All")
            
            for defect_type in defect_types:
                if defect_type[0]:
                    for defect in defect_type[0].split(','):
                        defect = defect.strip()
                        if defect and defect != "No defects" and defect not in [self.defect_combo.itemText(i) for i in range(self.defect_combo.count())]:
                            self.defect_combo.addItem(defect)
            
            self.defect_combo.addItem("No defects")
            
            index = self.defect_combo.findText(current_selection)
            if index >= 0:
                self.defect_combo.setCurrentIndex(index)          
        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"Error loading defect types: {str(e)}")
    
    def refresh_data(self):
        """Refresh data in the history table based on filters"""
        try:
            date_from = self.date_from.date().toString("yyyy-MM-dd")
            date_to = self.date_to.date().addDays(1).toString("yyyy-MM-dd")
            
            defect_filter = self.defect_combo.currentText()
            rows = get_detections(date_from, date_to, defect_filter)
            
            self.history_table.setRowCount(0)
            
            for i, row in enumerate(rows):
                rowid, time_str, img_raw, img_detect, defect, barcode = row
                
                self.history_table.insertRow(i)
                self.history_table.setRowHeight(i, 50)  # Compact row height
                
                # ID
                id_item = QTableWidgetItem(str(rowid))
                id_item.setTextAlignment(Qt.AlignCenter)
                self.history_table.setItem(i, 0, id_item)
                
                # Time (shortened format)
                time_item = QTableWidgetItem(time_str.split(' ')[1] if ' ' in time_str else time_str)  # Show only time
                time_item.setTextAlignment(Qt.AlignCenter)
                time_item.setToolTip(time_str)  # Full datetime in tooltip
                self.history_table.setItem(i, 1, time_item)
                
                # Compact image thumbnails with double-click functionality
                for col, img_data, img_type in [(2, img_raw, "img_raw"), (3, img_detect, "img_detect")]:
                    if img_data:
                        nparr = np.frombuffer(img_data, np.uint8)
                        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        
                        # Smaller thumbnails
                        img = cv2.resize(img, (50, 38))
                        height, width, channel = img.shape
                        bytes_per_line = 3 * width
                        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
                        pixmap = QPixmap.fromImage(q_img)
                        
                        # Create clickable image label
                        lbl = ClickableImageLabel(rowid, img_type)
                        lbl.setPixmap(pixmap)
                        
                        # Connect double-click signal
                        lbl.double_clicked.connect(self.on_image_double_clicked)
                        
                        self.history_table.setCellWidget(i, col, lbl)
                    else:
                        self.history_table.setItem(i, col, QTableWidgetItem("No image"))
                
                # Defect status with better formatting
                defect_display = defect if defect else "None"
                if len(defect_display) > 20:
                    defect_display = defect_display[:17] + "..."
                
                defect_item = QTableWidgetItem(defect_display)
                defect_item.setToolTip(defect if defect else "No defects")
                
                if defect and defect.lower() != "no defects":
                    defect_item.setBackground(QColor(255, 235, 238))  # Light red
                    defect_item.setForeground(QColor(183, 28, 28))
                else:
                    defect_item.setBackground(QColor(232, 245, 233))  # Light green
                    defect_item.setForeground(QColor(46, 125, 50))
                    
                self.history_table.setItem(i, 4, defect_item)
                
                # Barcode
                barcode_display = (barcode[:8] + "...") if barcode and len(barcode) > 8 else (barcode or "N/A")
                barcode_item = QTableWidgetItem(barcode_display)
                barcode_item.setToolTip(barcode if barcode else "No barcode")
                self.history_table.setItem(i, 5, barcode_item)
            
            # Update parent status
            if hasattr(self.parent, 'status_message'):
                self.parent.status_message.setText(f"📊 Loaded {len(rows)} records")
            
            self.reset_details()
            self.populate_defect_types()
            
        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"Error loading detection history: {str(e)}")
    
    @Slot(int, str)
    def on_image_double_clicked(self, row_id, image_type):
        """Handle double-click on image thumbnail"""
        try:
            img_data = self.get_image_data(row_id, image_type)
            if img_data:
                # Determine title based on image type
                title = "Raw Image" if image_type == "img_raw" else "Detection Image"
                dialog = ImageViewDialog(img_data, title, self)
                dialog.exec_()
            else:
                QMessageBox.warning(self, "Error", "Could not load image data")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error viewing image: {str(e)}")

    def on_selection_changed(self):
        """Handle selection change in the table"""
        selected_rows = self.history_table.selectedItems()
        
        if selected_rows:
            row = selected_rows[0].row()
            
            row_id = self.history_table.item(row, 0).text()
            time_str = self.history_table.item(row, 1).toolTip() or self.history_table.item(row, 1).text()
            defect = self.history_table.item(row, 4).toolTip() or self.history_table.item(row, 4).text()
            barcode = self.history_table.item(row, 5).toolTip() or self.history_table.item(row, 5).text()
            
            # Update compact details
            self.details_defect.setText(f"🔧 {defect[:15] + '...' if len(defect) > 15 else defect}")
            self.details_time.setText(f"⏰ {time_str.split(' ')[0] if ' ' in time_str else time_str}")
            self.details_barcode.setText(f"📦 {barcode[:8] + '...' if len(barcode) > 8 else barcode}")
            
            # Enable buttons
            for btn in self.action_buttons:
                btn.setEnabled(True)
            
            # Color coding for defect status
            defect_styles = HistoryTabStyles.get_defect_status_styles()
            if defect.lower() != "no defects" and defect.lower() != "none":
                self.details_defect.setStyleSheet(defect_styles['failed'])
            else:
                self.details_defect.setStyleSheet(defect_styles['passed'])
        else:
            self.reset_details()
    
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
        """Get the database ID from selected row"""
        selected_items = self.history_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            return int(self.history_table.item(row, 0).text())
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
        row_id = self.get_selected_row_id()
        if row_id is None:
            return
            
        try:
            conn = sqlite3.connect('sqlite_database/db/detections.db')
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT time, img_raw, img_detect, defect, barcode FROM detections WHERE rowid = ?", 
                (row_id,)
            )
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                QMessageBox.warning(self, "Error", "Detection record not found")
                return
                
            time_str, img_raw, img_detect, defect, barcode = result
            
            export_dir = QFileDialog.getExistingDirectory(
                self, "Select Directory for Export", "",
                QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
            )
            
            if not export_dir:
                return
                
            safe_time = time_str.replace(":", "-").replace(" ", "_")
            filename_base = f"detection_{row_id}_{safe_time}"
            
            if img_raw:
                self.save_image_data(img_raw, os.path.join(export_dir, f"{filename_base}_raw.png"))
                
            if img_detect:
                self.save_image_data(img_detect, os.path.join(export_dir, f"{filename_base}_detect.png"))
                
            with open(os.path.join(export_dir, f"{filename_base}_info.txt"), 'w') as f:
                f.write(f"Detection ID: {row_id}\n")
                f.write(f"Time: {time_str}\n")
                f.write(f"Defects: {defect}\n")
                f.write(f"Barcode: {barcode}\n")
            
            QMessageBox.information(
                self, "Export Complete", 
                f"Detection data exported successfully to {export_dir}"
            )
            
        except Exception as e:
            QMessageBox.warning(self, "Export Error", f"Error exporting detection: {str(e)}")
    
    def save_image_data(self, img_data, filepath):
        """Save image data to file"""
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imwrite(filepath, img)
    
    def delete_detection(self):
        """Delete selected detection from database"""
        row_id = self.get_selected_row_id()
        if row_id is None:
            return
            
        reply = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete detection #{row_id}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                delete_detection_from_db(row_id)
                
                if hasattr(self.parent, 'status_message'):
                    self.parent.status_message.setText(f"🗑️ Detection #{row_id} deleted")
                
                self.refresh_data()
            except Exception as e:
                QMessageBox.warning(self, "Delete Error", f"Error deleting detection: {str(e)}")
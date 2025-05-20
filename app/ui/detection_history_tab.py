from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
    QGroupBox, QLabel, QComboBox, QDateEdit, QHeaderView, QSplitter, QMessageBox,
    QDialog, QFileDialog, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, QDateTime, QDate, Signal, Slot
from PySide6.QtGui import QPixmap, QImage, QIcon, QFont, QColor
import sqlite3
import cv2
import numpy as np
from sqlite_database.src.db_operations import (
    get_defect_types, execute_query, 
    delete_detection_from_db,
    get_detections, get_image_data
    )
import os

class ImageViewDialog(QDialog):
    """Dialog for viewing images in larger size"""
    def __init__(self, image_data, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(800, 600)
        
        # Layout
        layout = QVBoxLayout(self)
        
        # Image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Convert image data to QPixmap
        if isinstance(image_data, bytes):
            # Convert bytes to numpy array
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            # Convert BGR to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # Create QImage
            height, width, channel = img.shape
            bytes_per_line = 3 * width
            q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
        elif isinstance(image_data, QPixmap):
            pixmap = image_data
        else:
            # If not bytes or QPixmap, show error
            self.image_label.setText("Invalid image data")
            layout.addWidget(self.image_label)
            return
            
        # Scale image maintaining aspect ratio
        self.image_label.setPixmap(pixmap.scaled(
            800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        # Add to layout
        layout.addWidget(self.image_label)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #4a86e8;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a76d8;
            }
        """)
        
        # Save image button
        save_button = QPushButton("Save Image")
        save_button.clicked.connect(lambda: self.save_image(pixmap))
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        # Button layout
        button_layout = QHBoxLayout()
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

class DetectionHistoryTab(QWidget):
    """Tab for viewing detection history"""
    
    refresh_signal = Signal()  # Signal to refresh data from parent
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()
        
    def initUI(self):
        """Initialize UI components"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # ===== Filter controls =====
        filter_group = QGroupBox("Filter Options")
        filter_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ddd;
                border-radius: 6px;
                margin-top: 12px;
                background-color: #f9f9f9;
            }
        """)
        filter_layout = QHBoxLayout(filter_group)
        
        # Date range
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Date Range:"))
        
        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate.currentDate().addDays(-7))  # Default to last week
        date_layout.addWidget(self.date_from)
        
        date_layout.addWidget(QLabel("to"))
        
        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate())  # Default to today
        date_layout.addWidget(self.date_to)
        
        filter_layout.addLayout(date_layout)
        
        # Defect type filter
        defect_layout = QHBoxLayout()
        defect_layout.addWidget(QLabel("Defect Type:"))
        
        self.defect_combo = QComboBox()
        self.defect_combo.addItem("All")
        defect_layout.addWidget(self.defect_combo)
        
        filter_layout.addLayout(defect_layout)
        
        # Quick date buttons
        quick_date_layout = QHBoxLayout()
        
        today_btn = QPushButton("Today")
        today_btn.clicked.connect(lambda: self.set_date_range(0))
        
        week_btn = QPushButton("Last Week")
        week_btn.clicked.connect(lambda: self.set_date_range(7))
        
        month_btn = QPushButton("Last Month")
        month_btn.clicked.connect(lambda: self.set_date_range(30))
        
        for btn in [today_btn, week_btn, month_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    padding: 4px 8px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
            quick_date_layout.addWidget(btn)
        
        filter_layout.addLayout(quick_date_layout)
        
        # Apply filter button
        self.apply_filter_btn = QPushButton("Apply Filter")
        self.apply_filter_btn.clicked.connect(self.refresh_data)
        self.apply_filter_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a86e8;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a76d8;
            }
        """)
        filter_layout.addWidget(self.apply_filter_btn)
        
        main_layout.addWidget(filter_group)
        
        # ===== Results area =====
        results_splitter = QSplitter(Qt.Vertical)
        
        # Table for detection history
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels(["ID", "Date/Time", "Raw Image", "Detection Image", "Defects", "Barcode"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.history_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                gridline-color: #f0f0f0;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                padding: 6px;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 4px;
            }
            QTableWidget::item:selected {
                background-color: #e0e8f8;
                color: #333;
            }
        """)
        results_splitter.addWidget(self.history_table)
        
        # Details frame
        details_frame = QFrame()
        details_frame.setFrameShape(QFrame.StyledPanel)
        details_frame.setMaximumHeight(200)  # Limit height
        details_layout = QVBoxLayout(details_frame)
        
        # Detail labels
        details_layout.addWidget(QLabel("Selected Detection Details:"))
        
        self.details_defect = QLabel("Defect: None selected")
        self.details_defect.setStyleSheet("font-weight: bold;")
        details_layout.addWidget(self.details_defect)
        
        self.details_time = QLabel("Time: None selected")
        details_layout.addWidget(self.details_time)
        
        self.details_barcode = QLabel("Barcode: None selected")  
        details_layout.addWidget(self.details_barcode)
        
        # Actions layout
        actions_layout = QHBoxLayout()
        
        self.view_raw_btn = QPushButton("View Raw Image")
        self.view_raw_btn.setEnabled(False)
        self.view_raw_btn.clicked.connect(self.view_raw_image)
        
        self.view_detect_btn = QPushButton("View Detection Image")
        self.view_detect_btn.setEnabled(False)
        self.view_detect_btn.clicked.connect(self.view_detection_image)
        
        self.export_btn = QPushButton("Export")
        self.export_btn.setEnabled(False)
        self.export_btn.clicked.connect(self.export_detection)
        
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.delete_detection)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
            QPushButton:disabled {
                background-color: #ffcdd2;
                color: #b71c1c;
            }
        """)
        
        for btn in [self.view_raw_btn, self.view_detect_btn, self.export_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a86e8;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 6px 12px;
                }
                QPushButton:hover {
                    background-color: #3a76d8;
                }
                QPushButton:disabled {
                    background-color: #cccccc;
                    color: #666666;
                }
            """)
            actions_layout.addWidget(btn)
        
        actions_layout.addWidget(self.delete_btn)
        details_layout.addLayout(actions_layout)
        
        # Add stretch to push everything up
        details_layout.addStretch()
        
        results_splitter.addWidget(details_frame)
        
        # Set ratio between table and details
        results_splitter.setSizes([700, 200])
        
        main_layout.addWidget(results_splitter)
        
        # Connect signals
        self.history_table.itemSelectionChanged.connect(self.on_selection_changed)
        
        # Refresh data initially
        self.populate_defect_types()
        self.refresh_data()
    
    def set_date_range(self, days_back):
        """Set date range for quick filters"""
        today = QDate.currentDate()
        self.date_to.setDate(today)
        self.date_from.setDate(today.addDays(-days_back))
        
        # Auto-apply filter
        self.refresh_data()
    
    def populate_defect_types(self):
        """Populate defect type combobox from database"""
        try:
            defect_types = get_defect_types()       
            # Current combobox selection
            current_selection = self.defect_combo.currentText()
            
            # Clear and repopulate
            self.defect_combo.clear()
            self.defect_combo.addItem("All")
            
            for defect_type in defect_types:
                if defect_type[0]:  # Skip empty
                    # Split multiple defects
                    for defect in defect_type[0].split(','):
                        defect = defect.strip()
                        if defect and defect != "No defects" and defect not in [self.defect_combo.itemText(i) for i in range(self.defect_combo.count())]:
                            self.defect_combo.addItem(defect)
            
            # Add "No defects" as an option
            self.defect_combo.addItem("No defects")
            
            # Try to restore previous selection
            index = self.defect_combo.findText(current_selection)
            if index >= 0:
                self.defect_combo.setCurrentIndex(index)          
        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"Error loading defect types: {str(e)}")
    
    def refresh_data(self):
        """Refresh data in the history table based on filters"""
        try:
            # Build query with date filter
            date_from = self.date_from.date().toString("yyyy-MM-dd")
            date_to = self.date_to.date().addDays(1).toString("yyyy-MM-dd")  # Add 1 day to include end date
            
            # Get defect filter
            defect_filter = self.defect_combo.currentText()
            # Fetch data from database
            rows = get_detections(date_from, date_to, defect_filter)
            
            # Clear table
            self.history_table.setRowCount(0)
            
            # Populate table with data
            for i, row in enumerate(rows):
                rowid, time_str, img_raw, img_detect, defect, barcode = row
                
                # Insert row
                self.history_table.insertRow(i)
                
                # ID
                id_item = QTableWidgetItem(str(rowid))
                id_item.setTextAlignment(Qt.AlignCenter)
                self.history_table.setItem(i, 0, id_item)
                
                # Time
                time_item = QTableWidgetItem(time_str)
                time_item.setTextAlignment(Qt.AlignCenter)
                self.history_table.setItem(i, 1, time_item)
                
                # Images - show placeholders
                for col, img_data in [(2, img_raw), (3, img_detect)]:
                    # Convert image blob to thumbnail
                    if img_data:
                        nparr = np.frombuffer(img_data, np.uint8)
                        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        
                        # Create small thumbnail
                        img = cv2.resize(img, (80, 60))
                        height, width, channel = img.shape
                        bytes_per_line = 3 * width
                        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
                        pixmap = QPixmap.fromImage(q_img)
                        
                        # Create label with thumbnail
                        lbl = QLabel()
                        lbl.setPixmap(pixmap)
                        lbl.setAlignment(Qt.AlignCenter)
                        self.history_table.setCellWidget(i, col, lbl)
                    else:
                        self.history_table.setItem(i, col, QTableWidgetItem("No image"))
                
                # Defect types
                defect_item = QTableWidgetItem(defect if defect else "None")
                
                # Set color based on defect status
                if defect and defect.lower() != "no defects":
                    defect_item.setBackground(QColor(255, 200, 200))  # Light red
                else:
                    defect_item.setBackground(QColor(200, 255, 200))  # Light green
                    
                self.history_table.setItem(i, 4, defect_item)
                
                # Barcode
                barcode_item = QTableWidgetItem(barcode if barcode else "N/A")
                self.history_table.setItem(i, 5, barcode_item)
            
            # Update status message
            if hasattr(self.parent, 'statusBar') and self.parent.statusBar is not None:
                if hasattr(self.parent.statusBar, 'showMessage'):
                    self.parent.statusBar.showMessage(f"Loaded {len(rows)} detection records", 3000)
                elif hasattr(self.parent, 'status_message'):
                    self.parent.status_message.setText(f"Loaded {len(rows)} detection records")
            
            # Reset selection
            self.reset_details()
            
            # Re-populate defect types for any new data
            self.populate_defect_types()
            
        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"Error loading detection history: {str(e)}")
    
    def on_selection_changed(self):
        """Handle selection change in the table"""
        selected_rows = self.history_table.selectedItems()
        
        if selected_rows:
            row = selected_rows[0].row()
            
            # Get row ID from first column
            row_id = self.history_table.item(row, 0).text()
            time_str = self.history_table.item(row, 1).text()
            defect = self.history_table.item(row, 4).text()
            barcode = self.history_table.item(row, 5).text()
            
            # Update details
            self.details_defect.setText(f"Defect: {defect}")
            self.details_time.setText(f"Time: {time_str}")
            self.details_barcode.setText(f"Barcode: {barcode}")
            
            # Enable buttons
            self.view_raw_btn.setEnabled(True)
            self.view_detect_btn.setEnabled(True)
            self.export_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
            
            # Set different styles based on detection result
            if defect.lower() != "no defects" and defect.lower() != "none":
                self.details_defect.setStyleSheet("font-weight: bold; color: #d32f2f;")
            else:
                self.details_defect.setStyleSheet("font-weight: bold; color: #2e7d32;")
        else:
            self.reset_details()
    
    def reset_details(self):
        """Reset detail view when no row is selected"""
        self.details_defect.setText("Defect: None selected")
        self.details_defect.setStyleSheet("font-weight: bold;")
        self.details_time.setText("Time: None selected")
        self.details_barcode.setText("Barcode: None selected")
        
        # Disable buttons
        self.view_raw_btn.setEnabled(False)
        self.view_detect_btn.setEnabled(False)
        self.export_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
    
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
            return get_image_data(row_id, image_type)  # Fetch image data from db_operations
        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"Error retrieving image: {str(e)}")
            return None
    
    def view_raw_image(self):
        """View raw image in popup dialog"""
        row_id = self.get_selected_row_id()
        if row_id is not None:
            img_data = self.get_image_data(row_id, "img_raw")
            if img_data:
                dialog = ImageViewDialog(img_data, "Raw Image", self)
                dialog.exec_()
    
    def view_detection_image(self):
        """View detection image in popup dialog"""
        row_id = self.get_selected_row_id()
        if row_id is not None:
            img_data = self.get_image_data(row_id, "img_detect")
            if img_data:
                dialog = ImageViewDialog(img_data, "Detection Image", self)
                dialog.exec_()
    
    def export_detection(self):
        """Export detection data to files"""
        row_id = self.get_selected_row_id()
        if row_id is None:
            return
            
        try:
            # Get data from database
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
            
            # Ask for directory to save files
            export_dir = QFileDialog.getExistingDirectory(
                self, "Select Directory for Export", "",
                QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
            )
            
            if not export_dir:
                return
                
            # Create filename base
            safe_time = time_str.replace(":", "-").replace(" ", "_")
            filename_base = f"detection_{row_id}_{safe_time}"
            
            # Save images
            if img_raw:
                self.save_image_data(img_raw, os.path.join(export_dir, f"{filename_base}_raw.png"))
                
            if img_detect:
                self.save_image_data(img_detect, os.path.join(export_dir, f"{filename_base}_detect.png"))
                
            # Save metadata
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
            
        # Confirm deletion
        reply = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete detection #{row_id}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                delete_detection_from_db(row_id)
                
                if hasattr(self.parent, 'statusBar') and self.parent.statusBar is not None:
                    if hasattr(self.parent.statusBar, 'showMessage'):
                        self.parent.statusBar.showMessage(f"Detection #{row_id} deleted", 3000)
                    elif hasattr(self.parent, 'status_message'):
                        self.parent.status_message.setText(f"Detection #{row_id} deleted")
                
                self.refresh_data()
            except Exception as e:
                QMessageBox.warning(self, "Delete Error", f"Error deleting detection: {str(e)}")
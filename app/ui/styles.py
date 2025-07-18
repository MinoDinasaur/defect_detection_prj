class AppStyles:
    @staticmethod
    def get_main_window_style():
        return """
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
                border-radius: 8px;
                background: white;
                margin-top: 0px;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border: 1px solid #dee2e6;
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                padding: 4px 12px;
                margin-right: 1px;
                font-weight: 500;
                font-size: 13px;
                color: #495057;
                min-width: 80px;
                max-width: 160px;
                height: 24px;
                max-height: 24px;
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
            QTabBar {
                qproperty-drawBase: 0;
                max-height: 26px;
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
        """
    
    @staticmethod
    def get_button_style():
        return """
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
        """
    
    @staticmethod
    def get_clear_button_style():
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #95a5a6, stop:1 #7f8c8d);
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
                    stop:0 #a5b5b6, stop:1 #8f9c9d);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #75858e, stop:1 #6f7c7d);
                transform: translateY(1px);
            }
            QPushButton:disabled {
                background: #cccccc;
                color: #666666;
            }
        """
    
    @staticmethod
    def get_status_bar_style():
        return """
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border-top: 1px solid #dee2e6;
                padding: 8px;
                font-size: 13px;
                color: #495057;
            }
        """
    
    @staticmethod
    def get_progress_bar_style():
        return """
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
        """
    
    @staticmethod
    def get_status_card_style():
        return """
            QFrame {
                background: white;
                border: 1px solid #e1e5e9;
                border-radius: 8px;
                padding: 6px;
                margin: 2px;
            }
        """
    
    @staticmethod
    def get_status_card_title_style():
        return """
            QLabel {
                color: #2c3e50;
                font-size: 12px;
                font-weight: 600;
                margin: 0;
                padding: 1px 0;
            }
        """
    
    @staticmethod
    def get_status_card_value_style(color="#4a86e8"):
        return f"""
            QLabel {{
                color: {color};
                font-size: 17px;
                font-weight: 700;
                margin: 0;
                padding: 8px 0;
                min-height: 30px;
            }}
        """
    
    @staticmethod
    def get_barcode_notification_style():
        return """
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #d4edda, stop:1 #c3e6cb);
                color: #155724;
                border: 1px solid #c3e6cb;
                border-radius: 4px;
                padding: 4px 8px;
                font-weight: bold;
            }
        """
    
    @staticmethod
    def get_header_frame_style():
        return """
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 8px;
                padding: 12px 16px;
            }
        """
    
    @staticmethod
    def get_header_title_style():
        return """
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                margin: 0;
            }
        """
    
    @staticmethod
    def get_header_subtitle_style():
        return """
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 13px;
                margin: 0;
            }
        """
    
    @staticmethod
    def get_image_group_style():
        return """
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
        """
    
    @staticmethod
    def get_image_frame_style():
        return """
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border: 3px dashed #bdc3c7;
                border-radius: 16px;
                min-height: 400px;
            }
        """
    
    @staticmethod
    def get_image_label_style():
        return """
            QLabel {
                font-size: 18px;
                color: #7f8c8d;
                background: transparent;
                padding: 40px;
                line-height: 1.6;
            }
        """
    
    @staticmethod
    def get_image_info_style():
        return """
            QLabel {
                font-size: 14px;
                color: #34495e;
                background: rgba(52, 152, 219, 0.1);
                padding: 12px;
                border-radius: 8px;
                font-weight: 500;
            }
        """
    
    @staticmethod
    def get_results_group_style():
        return """
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
        """
    
    @staticmethod
    def get_results_list_style():
        return """
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
        """
    
    @staticmethod
    def get_controls_frame_style():
        return """
            QFrame {
                background: white;
                border: 1px solid #e0e6ed;
                border-radius: 16px;
                padding: 20px;
            }
        """
    
    @staticmethod
    def get_result_indicator_styles():
        return {
            'waiting': """
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
            """,
            'processing': """
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
            """,
            'passed': """
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
            """,
            'failed': """
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
            """,
            'error': """
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
            """
        }


class HistoryTabStyles:
    """Styles specifically for Detection History Tab"""
    
    @staticmethod
    def get_dialog_style():
        return """
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
        """
    
    @staticmethod
    def get_dialog_title_frame_style():
        return """
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a86e8, stop:1 #3a76d8);
                border-radius: 8px;
                padding: 12px;
            }
        """
    
    @staticmethod
    def get_dialog_title_style():
        return """
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                margin: 0;
            }
        """
    
    @staticmethod
    def get_dialog_image_label_style():
        return """
            QLabel {
                background: white;
                border: 2px solid #e0e6ed;
                border-radius: 8px;
                padding: 8px;
            }
        """
    
    @staticmethod
    def get_dialog_save_button_style():
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #28a745, stop:1 #218838);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
                min-width: 100px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #34ce57, stop:1 #28a745);
            }
        """
    
    @staticmethod
    def get_dialog_close_button_style():
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6c757d, stop:1 #5a6268);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
                min-width: 80px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7c868d, stop:1 #6c757d);
            }
        """
    
    @staticmethod
    def get_header_frame_style():
        return """
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 8px;
                padding: 12px 16px;
            }
        """
    
    @staticmethod
    def get_header_title_style():
        return """
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                margin: 0;
            }
        """
    
    @staticmethod
    def get_header_subtitle_style():
        return """
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 13px;
                margin: 0;
            }
        """
    
    @staticmethod
    def get_filter_group_style():
        return """
            QGroupBox {
                font-weight: 600;
                font-size: 16px;
                color: #2c3e50;
                border: 2px solid #3498db;
                border-radius: 12px;
                margin-top: 10px;
                padding: 10px;
                background: rgba(255, 255, 255, 0.95);
            }
            QGroupBox::title {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                padding: 6px 16px;
                border-radius: 8px;
                margin-left: 10px;
            }
            QDateEdit, QComboBox {
                padding: 6px 10px;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                font-size: 13px;
                background: white;
                min-width: 100px;
                max-height: 32px;
            }
            QDateEdit:focus, QComboBox:focus {
                border: 2px solid #3498db;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                font-weight: 600;
                min-width: 80px;
                max-height: 32px;
                font-size: 13px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4ea8eb, stop:1 #3990c9);
            }
            QLabel {
                font-size: 13px;
                font-weight: 500;
                color: #2c3e50;
                padding: 2px;
            }
        """
    
    @staticmethod
    def get_quick_filter_button_style():
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #95a5a6, stop:1 #7f8c8d);
                min-width: 70px;
                max-height: 32px;
                font-size: 12px;
                padding: 6px 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a5b5b6, stop:1 #8f9c8d);
            }
        """
    
    @staticmethod
    def get_table_style():
        return """
            QTableWidget {
                border: 2px solid #bdc3c7;
                border-radius: 12px;
                background-color: white;
                gridline-color: #ecf0f1;
                font-size: 13px;
                selection-background-color: #e8f4fd;
                outline: none;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #34495e, stop:1 #2c3e50);
                color: white;
                border: 1px solid #2c3e50;
                padding: 10px 8px;
                font-weight: bold;
                font-size: 12px;
                text-align: center;
            }
            QHeaderView::section:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3d566e, stop:1 #34495e);
            }
            QTableWidget::item {
                padding: 8px 6px;
                border-bottom: 1px solid #ecf0f1;
                border-right: 1px solid #f8f9fa;
                word-wrap: break-word;
            }
            QTableWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e8f4fd, stop:1 #d4edda);
                color: #2c3e50;
                border: 1px solid #4a86e8;
            }
            QTableWidget::item:hover {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
            }
            QScrollBar:vertical {
                background: #f8f9fa;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #dee2e6;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #adb5bd;
            }
        """
    
    @staticmethod
    def get_details_frame_style():
        return """
            QFrame {
                background: white;
                border: 2px solid #e0e6ed;
                border-radius: 12px;
                padding: 8px;
                margin: 4px;
            }
        """
    
    @staticmethod
    def get_details_title_style():
        return """
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 8px;
                padding: 4px 0;
                border-bottom: 1px solid #e9ecef;
            }
        """
    
    @staticmethod
    def get_details_label_style():
        return """
            QLabel {
                font-size: 13px;
                color: #34495e;
                padding: 8px 12px;
                background: #f8f9fa;
                border-radius: 6px;
                margin: 2px 0;
                border-left: 3px solid #dee2e6;
                line-height: 1.4;
            }
        """
    
    @staticmethod
    def get_action_button_style(color):
        """Get action button style with dynamic colors"""
        color_map = {
            "#3498db": {"dark": "#2980b9", "light": "#5dade2"},
            "#2ecc71": {"dark": "#27ae60", "light": "#58d68d"},
            "#f39c12": {"dark": "#e67e22", "light": "#f8c471"},
            "#e74c3c": {"dark": "#c0392b", "light": "#ec7063"}
        }
        
        colors = color_map.get(color, {"dark": color, "light": color})
        
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {color}, stop:1 {colors['dark']});
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 16px;
                font-weight: 600;
                font-size: 13px;
                min-width: 100%;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {colors['light']}, stop:1 {color});
                transform: translateY(-1px);
            }}
            QPushButton:pressed {{
                transform: translateY(1px);
            }}
            QPushButton:disabled {{
                background: #bdc3c7;
                color: #7f8c8d;
                transform: none;
            }}
        """
    
    @staticmethod
    def get_image_thumbnail_style():
        return """
            QLabel {
                border: 1px solid #dee2e6; 
                border-radius: 3px;
            }
            QLabel:hover {
                border: 2px solid #4a86e8;
                background-color: rgba(74, 134, 232, 0.1);
            }
        """
    
    @staticmethod
    def get_defect_status_styles():
        return {
            'failed': """
                QLabel {
                    font-size: 13px;
                    color: #721c24;
                    padding: 8px 12px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #f8d7da, stop:1 #f5c6cb);
                    border-radius: 6px;
                    margin: 2px 0;
                    border-left: 3px solid #dc3545;
                    font-weight: 600;
                    line-height: 1.4;
                }
            """,
            'passed': """
                QLabel {
                    font-size: 13px;
                    color: #155724;
                    padding: 8px 12px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #d4edda, stop:1 #c3e6cb);
                    border-radius: 6px;
                    margin: 2px 0;
                    border-left: 3px solid #28a745;
                    font-weight: 600;
                    line-height: 1.4;
                }
            """,
            'none_selected': """
                QLabel {
                    font-size: 13px;
                    color: #495057;
                    padding: 8px 12px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #f8f9fa, stop:1 #e9ecef);
                    border-radius: 6px;
                    margin: 2px 0;
                    border-left: 3px solid #dee2e6;
                    line-height: 1.4;
                }
            """
        }
    
    @staticmethod
    def get_pagination_frame_style():
        return """
            QFrame {
                background: white;
                border: 1px solid #e0e6ed;
                border-radius: 8px;
                padding: 12px;
                margin: 4px;
            }
        """
    
    @staticmethod
    def get_pagination_records_info_style():
        return """
            QLabel {
                color: #6c757d;
                font-size: 13px;
                font-weight: 500;
                padding: 4px;
            }
        """
    
    @staticmethod
    def get_pagination_page_info_style():
        return """
            QLabel {
                font-weight: 600;
                color: #2c3e50;
                padding: 0 16px;
                font-size: 14px;
                min-width: 100px;
                text-align: center;
            }
        """
    
    @staticmethod
    def get_pagination_button_style():
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
                font-weight: 500;
                min-width: 70px;
                max-height: 36px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e9ecef, stop:1 #dee2e6);
                border: 1px solid #adb5bd;
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #dee2e6, stop:1 #ced4da);
                transform: translateY(1px);
            }
            QPushButton:disabled {
                background: #f8f9fa;
                color: #6c757d;
                border: 1px solid #dee2e6;
            }
        """
    
    @staticmethod
    def get_pagination_combo_style():
        return """
            QComboBox {
                padding: 4px 8px;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                font-size: 12px;
                min-width: 50px;
                max-height: 28px;
                background: white;
            }
            QComboBox:hover {
                border: 1px solid #adb5bd;
            }
            QComboBox:focus {
                border: 2px solid #4a86e8;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #6c757d;
                margin-right: 6px;
            }
        """
    
    @staticmethod
    def get_pagination_label_style():
        return """
            QLabel {
                color: #495057;
                font-size: 12px;
                font-weight: 500;
                padding: 2px 4px;
            }
        """
    
    @staticmethod
    def get_compact_header_frame_style():
        """Compact header style for history tab"""
        return """
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 8px;
                padding: 8px 12px;
                max-height: 60px;
            }
        """
    
    @staticmethod
    def get_compact_header_title_style():
        """Compact header title style"""
        return """
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                margin: 0;
            }
        """
    
    @staticmethod
    def get_compact_filter_group_style():
        """Compact filter group style with single row layout"""
        return """
            QGroupBox {
                font-weight: 600;
                font-size: 14px;
                color: #2c3e50;
                border: 1px solid #3498db;
                border-radius: 8px;
                margin-top: 6px;
                padding: 6px;
                background: rgba(255, 255, 255, 0.95);
                max-height: 80px;
            }
            QGroupBox::title {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                padding: 4px 12px;
                border-radius: 6px;
                margin-left: 8px;
            }
            QDateEdit, QComboBox {
                padding: 4px 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                font-size: 12px;
                background: white;
                min-width: 80px;
                max-height: 28px;
            }
            QDateEdit:focus, QComboBox:focus {
                border: 2px solid #3498db;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 10px;
                font-weight: 600;
                min-width: 60px;
                max-height: 28px;
                font-size: 11px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4ea8eb, stop:1 #3990c9);
            }
            QLabel {
                font-size: 11px;
                font-weight: 500;
                color: #2c3e50;
                padding: 1px;
            }
        """
    
    @staticmethod
    def get_compact_quick_filter_button_style():
        """Compact quick filter button style"""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #95a5a6, stop:1 #7f8c8d);
                min-width: 50px;
                max-height: 28px;
                font-size: 10px;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a5b5b6, stop:1 #8f9c8d);
            }
        """
    
    @staticmethod
    def get_compact_pagination_frame_style():
        """Compact pagination frame style"""
        return """
            QFrame {
                background: white;
                border: 1px solid #e0e6ed;
                border-radius: 6px;
                padding: 8px;
                margin: 2px;
                max-height: 50px;
            }
        """
    
    @staticmethod
    def get_compact_pagination_records_info_style():
        """Compact records info style"""
        return """
            QLabel {
                color: #6c757d;
                font-size: 11px;
                font-weight: 500;
                padding: 2px;
            }
        """
    
    @staticmethod
    def get_compact_pagination_page_info_style():
        """Compact page info style"""
        return """
            QLabel {
                font-weight: 600;
                color: #2c3e50;
                padding: 0 12px;
                font-size: 12px;
                min-width: 80px;
                text-align: center;
            }
        """
    
    @staticmethod
    def get_compact_pagination_button_style():
        """Compact pagination button style with icons only"""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 14px;
                font-weight: 500;
                min-width: 30px;
                max-height: 32px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e9ecef, stop:1 #dee2e6);
                border: 1px solid #adb5bd;
            }
            QPushButton:disabled {
                background: #f8f9fa;
                color: #6c757d;
                border: 1px solid #dee2e6;
            }
        """
    
    @staticmethod
    def get_compact_pagination_combo_style():
        """Compact pagination combo style"""
        return """
            QComboBox {
                padding: 2px 6px;
                border: 1px solid #dee2e6;
                border-radius: 3px;
                font-size: 11px;
                min-width: 40px;
                max-height: 24px;
                background: white;
            }
        """
    
    @staticmethod
    def get_compact_pagination_label_style():
        """Compact pagination label style"""
        return """
            QLabel {
                color: #495057;
                font-size: 11px;
                font-weight: 500;
                padding: 2px;
            }
        """
    
    @staticmethod
    def get_expanded_table_style():
        """Table style with more vertical space"""
        return """
            QTableWidget {
                border: 2px solid #bdc3c7;
                border-radius: 12px;
                background-color: white;
                gridline-color: #ecf0f1;
                font-size: 13px;
                selection-background-color: #e8f4fd;
                outline: none;
                min-height: 500px;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #34495e, stop:1 #2c3e50);
                color: white;
                border: 1px solid #2c3e50;
                padding: 10px 8px;
                font-weight: bold;
                font-size: 12px;
                text-align: center;
            }
            QHeaderView::section:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3d566e, stop:1 #34495e);
            }
            QTableWidget::item {
                padding: 8px 6px;
                border-bottom: 1px solid #ecf0f1;
                border-right: 1px solid #f8f9fa;
                word-wrap: break-word;
            }
            QTableWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e8f4fd, stop:1 #d4edda);
                color: #2c3e50;
                border: 1px solid #4a86e8;
            }
            QTableWidget::item:hover {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
            }
            QScrollBar:vertical {
                background: #f8f9fa;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #dee2e6;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #adb5bd;
            }
        """
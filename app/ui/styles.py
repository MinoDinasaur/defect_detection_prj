from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QRect

class AppStyles:
    @staticmethod
    def get_screen_info():
        """Get current screen information for responsive scaling"""
        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        dpi = screen.logicalDotsPerInch()
        
        # Base design: 1920x1080 at 96 DPI
        base_width = 1920
        base_height = 1080
        base_dpi = 96
        
        width_scale = screen_rect.width() / base_width
        height_scale = screen_rect.height() / base_height
        dpi_scale = dpi / base_dpi
        
        # Use average scale factor
        scale_factor = min(width_scale, height_scale) * dpi_scale
        scale_factor = max(0.7, min(2.0, scale_factor))  # Clamp between 0.7x and 2.0x
        
        return {
            'scale_factor': scale_factor,
            'screen_width': screen_rect.width(),
            'screen_height': screen_rect.height(),
            'dpi': dpi
        }
    
    @staticmethod
    def get_close_button_style():
        """Style for LARGE close button"""
        return """
            QPushButton {
                background: #e74c3c;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 20px;
                font-weight: bold;
                min-width: 25px;
                max-width: 25px;
                min-height: 25px;
                max-height: 25px;
                margin: 5px 5px;
            }
            QPushButton:hover {
                background: #c0392b;
                transform: scale(1.15);
                box-shadow: 0 4px 8px rgba(231, 76, 60, 0.3);
            }
            QPushButton:pressed {
                transform: scale(0.9);
                background: #a93226;
            }
    
        """
    @staticmethod
    def get_title_button_style():
        """Style for minimize/maximize buttons - cùng kích thước với close button"""
        return f"""
            QPushButton {{
                background: #95a5a6;  /* Màu xám thống nhất */
                color: white;
                border: none;
                border-radius: 6px;  /* Giống close button */
                font-size: 20px;     /* Giống close button */
                font-weight: bold;
                min-width: 25px;     /* Giống close button */
                max-width: 25px;
                min-height: 25px;    /* Giống close button */
                max-height: 25px;
                margin: 3px 1px;     /* Giống close button */
            }}
            QPushButton:hover {{
                background: #7f8c8d;  /* Màu xám đậm hơn khi hover */
                transform: scale(1.15);  /* Giống close button */
                box-shadow: 0 4px 8px rgba(127, 140, 141, 0.3);
            }}
            QPushButton:pressed {{
                transform: scale(0.9);   /* Giống close button */
                background: #6c757d;     /* Màu xám đậm nhất khi pressed */
            }}
        """
    
    @staticmethod
    def scale_size(base_size):
        """Scale size based on screen"""
        info = AppStyles.get_screen_info()
        return int(base_size * info['scale_factor'])
    
    @staticmethod
    def scale_font_size(base_size):
        """Scale font size based on screen"""
        info = AppStyles.get_screen_info()
        return max(10, int(base_size * info['scale_factor']))
    
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
                padding: 8px 16px;
                margin-right: 1px;
                font-weight: 500;
                font-size: 20px;
                color: #495057;
                min-width: 100px;
                max-width: 180px;
                height: 32px;
                max-height: 32px;
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
                max-height: 34px;
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
        """
    
    @staticmethod
    def get_button_style():
        """Enhanced button style with bigger size"""
        font_size = AppStyles.scale_font_size(30)  # Increased from 14
        
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a86e8, stop:1 #3a76d8);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 16px 28px;
                font-weight: bold;
                font-size: {font_size}px;
                min-height: 48px;
                min-width: 140px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a96f8, stop:1 #4a86e8);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(74, 134, 232, 0.3);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2a66c8, stop:1 #1a56b8);
                transform: translateY(1px);
            }}
            QPushButton:disabled {{
                background: #cccccc;
                color: #666666;
                transform: none;
            }}
        """
    
    @staticmethod
    def get_clear_button_style():
        """Enhanced clear button style with bigger size"""
        font_size = AppStyles.scale_font_size(30)  # Increased from 14
        
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #95a5a6, stop:1 #7f8c8d);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 16px 28px;
                font-weight: bold;
                font-size: {font_size}px;
                min-height: 48px;
                min-width: 140px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a5b5b6, stop:1 #8f9c9d);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(149, 165, 166, 0.3);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #75858e, stop:1 #6f7c7d);
                transform: translateY(1px);
            }}
            QPushButton:disabled {{
                background: #cccccc;
                color: #666666;
                transform: none;
            }}
        """
    
    @staticmethod
    def get_status_bar_style():
        return """
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border-top: 1px solid #dee2e6;
                padding: 10px;
                font-size: 19px;
                color: #495057;
                min-height: 24px;
            }
        """
    @staticmethod
    def get_stats_frame_style():
        """Style for the status cards container frame"""
        return """
            QFrame {
                background: rgba(255, 255, 255, 0.9);
                border: 1px solid #e0e6ed;
                border-radius: 12px;
                padding: 8px;
                margin: 4px 0;
            }
        """
    
    @staticmethod
    def get_progress_bar_style():
        return """
            QProgressBar {
                border: 1px solid #dee2e6;
                border-radius: 10px;
                text-align: center;
                font-weight: bold;
                background: #f8f9fa;
                height: 24px;
                min-height: 24px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a86e8, stop:1 #3a76d8);
                border-radius: 9px;
            }
        """
    
    @staticmethod
    def get_status_card_style():
        return """
            QFrame {
                background: white;
                border: 1px solid #e1e5e9;
                border-radius: 10px;
                padding: 2px;
                margin: 0px;
            }
        """
    
    @staticmethod
    def get_status_card_title_style():
        font_size = AppStyles.scale_font_size(20)  # Increased from 12
        
        return f"""
            QLabel {{
                color: #2c3e50;
                font-size: {font_size}px;
                font-weight: 600;
                margin: 0;
                padding: 2px 0;
            }}
        """
    
    @staticmethod
    def get_status_card_value_style(color="#4a86e8"):
        font_size = AppStyles.scale_font_size(18)  # Increased from 17
        scale_factor = AppStyles.get_screen_info()['scale_factor']
        min_height = int(12 * scale_factor)  # Increased from 30
        
        return f"""
            QLabel {{
                color: {color};
                font-size: {font_size}px;
                font-weight: 600;
                margin: 0;
                padding: 3px 0;
                min-height: {min_height}px;
                qproperty-alignment: AlignCenter;
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
                border-radius: 6px;
                padding: 6px 10px;
                font-weight: bold;
                font-size: 14px;
            }
        """
    
    @staticmethod
    # def get_header_frame_style():
    #     return """
    #         QFrame {
    #             background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    #                 stop:0 #667eea, stop:1 #764ba2);
    #             border-radius: 12px;
    #             padding: 16px 20px;
    #             margin: 4px;
    #         }
    #     """

    @staticmethod
    def get_header_frame_style():
        return """
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 10px;
                padding: 10px 10px;
            }
        """
    
    @staticmethod
    def get_header_title_style():
        font_size = AppStyles.scale_font_size(30)  # Increased from 20
        
        return f"""
            QLabel {{
                color: white;
                font-size: {font_size}px;
                font-weight: bold;
                margin: 0;
            }}
        """
    
    # @staticmethod
    # def get_header_subtitle_style():
    #     font_size = AppStyles.scale_font_size(14)  # Increased from 13
        
    #     return f"""
    #         QLabel {{
    #             color: rgba(255, 255, 255, 0.8);
    #             font-size: {font_size}px;
    #             margin: 0;
    #         }}
    #     """
    
    @staticmethod
    def get_image_group_style():
        font_size = AppStyles.scale_font_size(27) 
        
        return f"""
            QGroupBox {{
                font-size: {font_size}px;
                font-weight: 600;
                color: #2c3e50;
                border: 0px solid #3498db;
                padding-top: 0px;
                margin-top: px;
                margin-bottom: 0px
            }}
            # QGroupBox::title {{
            #     background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            #         stop:0 #3498db, stop:1 #2980b9);
            #     color: white;
            #     padding: 2px 12px;
            #     border-radius: 10px;
            # }}
        """
    
    @staticmethod
    def get_image_frame_style():
        return """
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border: 2px dashed #bdc3c7;
                border-radius: 16px;
                min-height: 300px;
                margin-top: 0px;
                margin-bottom: 0px
            }
        """
    
    @staticmethod
    def get_image_label_style():
        font_size = AppStyles.scale_font_size(22)  # Increased from 18
        
        return f"""
            QLabel {{
                font-size: {font_size}px;
                color: #7f8c8d;
                background: transparent;
                padding: 0px;
                line-height:0;
            }}
        """
    
    @staticmethod
    def get_image_info_style():
        font_size = AppStyles.scale_font_size(18)  # Increased from 14
        
        return f"""
            QLabel {{
                font-size: {font_size}px;
                color: #34495e;
                background: rgba(52, 152, 219, 0.1);
                padding: 0px;
                border-radius: 10px;
                font-weight: 500;
                margin: 0px;
            }}
        """
    
    @staticmethod
    def get_results_group_style():
        font_size = AppStyles.scale_font_size(27)  # Increased from 18
        
        return f"""
            QGroupBox {{
                font-size: {font_size}px;
                font-weight: 600;
                color: #2c3e50;
                border: 2px solid #e74c3c;
                padding-top: 8px;
                margin-top: 50px;
            }}
            QGroupBox::title {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                padding: 10px 24px;
                border-radius: 10px;
                subcontrol-origin: margin;
                subcontrol-position: top center;  /* CENTER THE TITLE */
                margin-left: 0px;  /* Remove left margin for centering */
            }}
        """
    
    @staticmethod
    def get_results_list_style():
        font_size = AppStyles.scale_font_size(16)  # Increased from 15
        
        return f"""
            QListWidget {{
                background: white;
                border: 2px solid #ecf0f1;
                border-radius: 12px;
                padding: 18px;
                font-size: {font_size}px;
                min-height: 320px;
                margin: 4px;
            }}
            QListWidget::item {{
                padding: 18px;
                margin: 8px 0;
                border-radius: 10px;
                border-left: 4px solid transparent;
            }}
            QListWidget::item:selected {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e8f4fd, stop:1 #d4edda);
                border-left: 4px solid #3498db;
                color: #2c3e50;
            }}
        """
    
    @staticmethod
    def get_controls_frame_style():
        return """
            QFrame {
                background: white;
                border: 1px solid #e0e6ed;
                border-radius: 16px;
                padding: 2px;
                margin: 8px 4px 4px 4px;
            }
        """
    
    @staticmethod
    def get_result_indicator_styles():
        font_size_normal = AppStyles.scale_font_size(23)  # Increased from 14
        font_size_large = AppStyles.scale_font_size(25)   # Increased from 18
        
        return {
            'waiting': f"""
                QLabel {{
                    font-size: {font_size_normal}px;
                    font-weight: bold;
                    border-radius: 12px;
                    padding: 10px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #f8f9fa, stop:1 #e9ecef);
                    border: 2px solid #dee2e6;
                    color: #6c757d;
                    max-height: 140px;
                    min-height: 10px;
                    qproperty-alignment: AlignCenter;
                }}
            """,
            'processing': f"""
                QLabel {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #fff3cd, stop:1 #ffeaa7);
                    color: #856404;
                    border: 3px solid #ffc107;
                    border-radius: 12px;
                    padding: 10px;
                    font-size: {font_size_normal}px;
                    font-weight: bold;
                    max-height: 140px;
                    min-height: 10px;
                    qproperty-alignment: AlignCenter;
                }}
            """,
            'passed': f"""
                QLabel {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #e8f5e9, stop:1 #c8e6c9);
                    color: #2e7d32;
                    border: 3px solid #66bb6a;
                    border-radius: 12px;
                    padding: 10px;
                    font-size: {font_size_large}px;
                    font-weight: bold;
                    min-height: 20px;
                    qproperty-alignment: AlignCenter;
                }}
            """,
            'failed': f"""
                QLabel {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #ffebee, stop:1 #ffcdd2);
                    color: #c62828;
                    border: 3px solid #ef5350;
                    border-radius: 12px;
                    padding: 10px;
                    font-size: {font_size_large}px;
                    font-weight: bold;
                    min-height: 10px;
                    qproperty-alignment: AlignCenter;
                }}
            """,
            'error': f"""
                QLabel {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #fff3e0, stop:1 #ffe0b2);
                    color: #e65100;
                    border: 3px solid #ff9800;
                    border-radius: 12px;
                    padding: 10px;
                    font-size: {font_size_normal}px;
                    font-weight: bold;
                    max-height: 140px;
                    min-height: 10px;
                    qproperty-alignment: AlignCenter;
                }}
            """
        }
      
    @staticmethod
    def get_exit_dialog_exit_button_style():
        """Style for exit button in exit confirmation dialog"""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 25px;
                font-weight: bold;
                min-width: 120px;
                min-height: 45px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c0392b, stop:1 #a93226);
                transform: scale(1.05);
            }
            QPushButton:pressed {
                transform: scale(0.95);
            }
        """
    
    @staticmethod
    def get_exit_dialog_cancel_button_style():
        """Style for cancel button in exit confirmation dialog"""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #95a5a6, stop:1 #7f8c8d);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 25px;
                font-weight: bold;
                min-width: 120px;
                min-height: 45px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a5b5b6, stop:1 #8f9c9d);
                transform: scale(1.05);
            }
            QPushButton:pressed {
                transform: scale(0.95);
            }
        """


class HistoryTabStyles:
    """Styles specifically for Detection History Tab with bigger buttons"""
    
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
                border-radius: 10px;
                padding: 14px;
            }
        """
    
    @staticmethod
    def get_dialog_title_style():
        font_size = AppStyles.scale_font_size(19)  # Increased from 18
        
        return f"""
            QLabel {{
                color: white;
                font-size: {font_size}px;
                font-weight: bold;
                margin: 0;
            }}
        """
    
    @staticmethod
    def get_dialog_image_label_style():
        return """
            QLabel {
                background: white;
                border: 2px solid #e0e6ed;
                border-radius: 10px;
                padding: 10px;
            }
        """
    
    @staticmethod
    def get_dialog_save_button_style():
        font_size = AppStyles.scale_font_size(20)  # Increased from 14
        
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #28a745, stop:1 #218838);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-weight: 600;
                font-size: {font_size}px;
                min-width: 120px;
                min-height: 40px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #34ce57, stop:1 #28a745);
                transform: translateY(-1px);
            }}
        """
    
    @staticmethod
    def get_dialog_close_button_style():
        font_size = AppStyles.scale_font_size(20)  # Increased from 14
        
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6c757d, stop:1 #5a6268);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-weight: 600;
                font-size: {font_size}px;
                min-width: 100px;
                min-height: 40px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7c868d, stop:1 #6c757d);
                transform: translateY(-1px);
            }}
        """
    
    @staticmethod
    def get_header_frame_style():
        return """
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 10px;
                padding: 10px 10px;
            }
        """
    
    @staticmethod
    def get_header_title_style():
        font_size = AppStyles.scale_font_size(30)  # Increased from 20
        
        return f"""
            QLabel {{
                color: white;
                font-size: {font_size}px;
                font-weight: bold;
                margin: 0;
            }}
        """
    
    # @staticmethod
    # def get_header_subtitle_style():
    #     font_size = AppStyles.scale_font_size(14)  # Increased from 13
        
    #     return f"""
    #         QLabel {{
    #             color: rgba(255, 255, 255, 0.8);
    #             font-size: {font_size}px;
    #             margin: 0;
    #         }}
    #     """
    
    @staticmethod
    def get_filter_group_style():
        font_size = AppStyles.scale_font_size(19)  # Increased from 16
        input_font_size = AppStyles.scale_font_size(19)  # Increased from 13
        button_font_size = AppStyles.scale_font_size(19)  # Increased from 13
        
        return f"""
            QGroupBox {{
                font-weight: 600;
                font-size: {font_size}px;
                color: #2c3e50;
                border: 2px solid #3498db;
                border-radius: 12px;
                margin-top: 12px;
                padding: 12px;
                background: rgba(255, 255, 255, 0.95);
            }}
            QGroupBox::title {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                padding: 8px 18px;
                border-radius: 8px;
                margin-left: 10px;
            }}
            QDateEdit, QComboBox {{
                padding: 8px 12px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                font-size: {input_font_size}px;
                background: white;
                min-width: 120px;
                min-height: 36px;
                max-height: 36px;
            }}
            QDateEdit:focus, QComboBox:focus {{
                border: 2px solid #3498db;
            }}
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: 600;
                min-width: 90px;
                min-height: 36px;
                max-height: 36px;
                font-size: {button_font_size}px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4ea8eb, stop:1 #3990c9);
                transform: translateY(-1px);
            }}
            QLabel {{
                font-size: {button_font_size}px;
                font-weight: 500;
                color: #2c3e50;
                padding: 3px;
            }}
        """
    
    @staticmethod
    def get_quick_filter_button_style():
        font_size = AppStyles.scale_font_size(19)  # Increased from 12
        
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #95a5a6, stop:1 #7f8c8d);
                min-width: 80px;
                min-height: 36px;
                max-height: 36px;
                font-size: {font_size}px;
                padding: 8px 12px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a5b5b6, stop:1 #8f9c8d);
                transform: translateY(-1px);
            }}
        """
    
    @staticmethod
    def get_table_style():
        font_size = AppStyles.scale_font_size(20)  # Increased from 13
        header_font_size = AppStyles.scale_font_size(27)  # Increased from 12
        
        return f"""
            QTableWidget {{
                border: 2px solid #bdc3c7;
                border-radius: 12px;
                background-color: white;
                gridline-color: #ecf0f1;
                font-size: {font_size}px;
                selection-background-color: #e8f4fd;
                outline: none;
            }}
            QHeaderView::section {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #34495e, stop:1 #2c3e50);
                color: white;
                border: 1px solid #2c3e50;
                padding: 12px 10px;
                font-weight: bold;
                font-size: {header_font_size}px;
                text-align: center;
                min-height: 20px;
            }}
            QHeaderView::section:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3d566e, stop:1 #34495e);
            }}
            QTableWidget::item {{
                padding: 10px 8px;
                border-bottom: 1px solid #ecf0f1;
                border-right: 1px solid #f8f9fa;
                word-wrap: break-word;
            }}
            QTableWidget::item:selected {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e8f4fd, stop:1 #d4edda);
                color: #2c3e50;
                border: 1px solid #4a86e8;
            }}
            QTableWidget::item:hover {{
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
            }}
            QScrollBar:vertical {{
                background: #f8f9fa;
                width: 14px;
                border-radius: 7px;
            }}
            QScrollBar::handle:vertical {{
                background: #dee2e6;
                border-radius: 7px;
                min-height: 24px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: #adb5bd;
            }}
        """
    
    @staticmethod
    def get_details_frame_style():
        return """
            QFrame {
                background: white;
                border: 2px solid #e0e6ed;
                border-radius: 12px;
                padding: 10px;
                margin: 4px;
            }
        """
    
    @staticmethod
    def get_details_title_style():
        font_size = AppStyles.scale_font_size(20)  # Increased from 16
        
        return f"""
            QLabel {{
                font-size: {font_size}px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 10px;
                padding: 6px 0;
                border-bottom: 1px solid #e9ecef;
            }}
        """
    
    @staticmethod
    def get_details_label_style():
        font_size = AppStyles.scale_font_size(20)  # Increased from 13
        
        return f"""
            QLabel {{
                font-size: {font_size}px;
                color: #34495e;
                padding: 10px 14px;
                background: #f8f9fa;
                border-radius: 8px;
                margin: 3px 0;
                border-left: 3px solid #dee2e6;
                line-height: 1.4;
            }}
        """
    
    @staticmethod
    def get_action_button_style(color):
        """Get action button style with dynamic colors and bigger size"""
        font_size = AppStyles.scale_font_size(30)  # Increased from 13
        
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
                border-radius: 10px;
                padding: 14px 18px;
                font-weight: 600;
                font-size: {font_size}px;
                min-width: 100%;
                min-height: 44px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {colors['light']}, stop:1 {color});
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
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
                border-radius: 4px;
                padding: 2px;
            }
            QLabel:hover {
                border: 2px solid #4a86e8;
                background-color: rgba(74, 134, 232, 0.1);
                transform: scale(1.02);
            }
        """
    
    @staticmethod
    def get_defect_status_styles():
        font_size = AppStyles.scale_font_size(20)  # Increased from 13
        
        return {
            'failed': f"""
                QLabel {{
                    font-size: {font_size}px;
                    color: #721c24;
                    padding: 10px 14px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #f8d7da, stop:1 #f5c6cb);
                    border-radius: 8px;
                    margin: 3px 0;
                    border-left: 3px solid #dc3545;
                    font-weight: 600;
                    line-height: 1.4;
                }}
            """,
            'passed': f"""
                QLabel {{
                    font-size: {font_size}px;
                    color: #155724;
                    padding: 10px 14px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #d4edda, stop:1 #c3e6cb);
                    border-radius: 8px;
                    margin: 3px 0;
                    border-left: 3px solid #28a745;
                    font-weight: 600;
                    line-height: 1.4;
                }}
            """,
            'none_selected': f"""
                QLabel {{
                    font-size: {font_size}px;
                    color: #495057;
                    padding: 10px 14px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #f8f9fa, stop:1 #e9ecef);
                    border-radius: 8px;
                    margin: 3px 0;
                    border-left: 3px solid #dee2e6;
                    line-height: 1.4;
                }}
            """
        }
    
    @staticmethod
    def get_pagination_frame_style():
        return """
            QFrame {
                background: white;
                border: 1px solid #e0e6ed;
                border-radius: 10px;
                padding: 14px;
                margin: 4px;
                min-height: 20px;
            }
        """
    
    @staticmethod
    def get_pagination_records_info_style():
        font_size = AppStyles.scale_font_size(20)  # Increased from 13
        
        return f"""
            QLabel {{
                color: #6c757d;
                font-size: {font_size}px;
                font-weight: 500;
                padding: 6px;
            }}
        """
    
    @staticmethod
    def get_pagination_page_info_style():
        font_size = AppStyles.scale_font_size(20)  # Increased from 14
        
        return f"""
            QLabel {{
                font-weight: 600;
                color: #2c3e50;
                padding: 0 18px;
                font-size: {font_size}px;
                min-width: 120px;
                text-align: center;
            }}
        """
    
    @staticmethod
    def get_pagination_button_style():
        font_size = AppStyles.scale_font_size(20)  # Increased from 12
        
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 10px 16px;
                font-size: {font_size}px;
                font-weight: 500;
                min-width: 80px;
                min-height: 40px;
                max-height: 40px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e9ecef, stop:1 #dee2e6);
                border: 1px solid #adb5bd;
                transform: translateY(-1px);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #dee2e6, stop:1 #ced4da);
                transform: translateY(1px);
            }}
            QPushButton:disabled {{
                background: #f8f9fa;
                color: #6c757d;
                border: 1px solid #dee2e6;
                transform: none;
            }}
        """
    
    @staticmethod
    def get_pagination_combo_style():
        font_size = AppStyles.scale_font_size(20)  # Increased from 12
        
        return f"""
            QComboBox {{
                padding: 6px 10px;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                font-size: {font_size}px;
                min-width: 60px;
                min-height: 32px;
                max-height: 32px;
                background: white;
            }}
            QComboBox:hover {{
                border: 1px solid #adb5bd;
            }}
            QComboBox:focus {{
                border: 2px solid #4a86e8;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 24px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #6c757d;
                margin-right: 8px;
            }}
        """
    
    @staticmethod
    def get_compact_header_frame_style():
        """Compact header style for history tab"""
        return """
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 10px;
                padding: 10px 10px;
                max-height: 70px;
            }
        """
    
    @staticmethod
    def get_compact_header_title_style():
        """Compact header title style"""
        font_size = AppStyles.scale_font_size(30)  # Increased from 18
        
        return f"""
            QLabel {{
                color: white;
                font-size: {font_size}px;
                font-weight: bold;
                margin: 0;
            }}
        """
    
    @staticmethod
    def get_compact_filter_group_style():
        """Compact filter group style with single row layout - CHỈ CALENDAR POPUP LỚN HƠN"""
        font_size = AppStyles.scale_font_size(20)  # Giữ nguyên
        input_font_size = AppStyles.scale_font_size(20)  # Giữ nguyên
        button_font_size = AppStyles.scale_font_size(30)  # Giữ nguyên
        
        return f"""
            QGroupBox {{
                font-weight: 600;
                font-size: {font_size}px;
                color: #2c3e50;
                border: 1px solid #3498db;
                border-radius: 10px;
                margin-top: 8px;
                padding: 8px;
                background: rgba(255, 255, 255, 0.95);
                max-height: 90px;
            }}
            QGroupBox::title {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                padding: 6px 14px;
                border-radius: 6px;
                margin-left: 8px;
            }}
            QDateEdit, QComboBox {{
                padding: 6px 10px;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                font-size: {input_font_size}px;
                background: white;
                min-width: 90px;
                min-height: 32px;
                max-height: 32px;
            }}
            QDateEdit:focus, QComboBox:focus {{
                border: 2px solid #3498db;
            }}
            QDateEdit::drop-down, QComboBox::drop-down {{
                border: none;
                width: 24px;
                background: transparent;
            }}
            QDateEdit::down-arrow, QComboBox::down-arrow {{
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #6c757d;
                margin-right: 8px;
            }}
            
            /* CHỈ STYLE CHO CALENDAR POPUP - TO HƠN NHIỀU */
            QCalendarWidget {{
                background-color: white;
                border: 3px solid #4a86e8;
                border-radius: 15px;
                min-width: 500px;  /* Lớn hơn nhiều */
                min-height: 400px; /* Lớn hơn nhiều */
                font-size: 18px;   /* Font lớn hơn */
            }}
            
            /* Header của calendar (tháng/năm) */
            QCalendarWidget QWidget#qt_calendar_navigationbar {{
                background-color: #4a86e8;
                border-radius: 10px;
                min-height: 50px;  /* Header cao hơn */
            }}
            
            /* Navigation buttons (prev/next month) */
            QCalendarWidget QToolButton {{
                background-color: #3a76d8;
                color: white;
                border: none;
                border-radius: 8px;
                min-width: 45px;   /* Buttons lớn hơn */
                min-height: 45px;
                font-size: 20px;   /* Font lớn hơn */
                font-weight: bold;
                margin: 3px;
            }}
            QCalendarWidget QToolButton:hover {{
                background-color: #5a96f8;
                transform: scale(1.1);
            }}
            QCalendarWidget QToolButton:pressed {{
                background-color: #2a66c8;
            }}
            
            /* Month/Year labels trong header */
            QCalendarWidget QLabel {{
                color: white;
                font-size: 18px;
                font-weight: bold;
            }}
            
            /* Month/Year dropdown menu */
            QCalendarWidget QMenu {{
                background-color: white;
                border: 2px solid #4a86e8;
                border-radius: 8px;
                font-size: 16px;
                min-width: 150px;
            }}
            QCalendarWidget QMenu::item {{
                padding: 8px 12px;
                font-size: 16px;
            }}
            QCalendarWidget QMenu::item:selected {{
                background-color: #4a86e8;
                color: white;
            }}
            
            /* Days of week header (Mon, Tue, Wed...) */
            QCalendarWidget QAbstractItemView:enabled {{
                font-size: 16px;
                font-weight: 700;
                color: #2c3e50;
                background-color: #f8f9fa;
                selection-background-color: #4a86e8;
                selection-color: white;
            }}
            
            /* Day cells grid */
            QCalendarWidget QTableView {{
                gridline-color: #dee2e6;
                font-size: 16px;
                font-weight: 600;
                background-color: white;
            }}
            
            /* Individual day cells */
            QCalendarWidget QTableView::item {{
                padding: 10px;  /* Cells lớn hơn */
                margin: 1px;
                border-radius: 6px;
                min-height: 30px;  /* Cells cao hơn */
                min-width: 30px;   /* Cells rộng hơn */
            }}
            
            /* Selected date */
            QCalendarWidget QTableView::item:selected {{
                background-color: #4a86e8;
                color: white;
                border-radius: 8px;
                font-weight: bold;
                font-size: 18px;
            }}
            
            /* Hover effect on dates */
            QCalendarWidget QTableView::item:hover {{
                background-color: #e8f4fd;
                border-radius: 6px;
                font-weight: bold;
            }}
            
            /* Today's date highlight */
            QCalendarWidget QTableView::item:focus {{
                background-color: #ffc107;
                color: #212529;
                border: 2px solid #e67e22;
                font-weight: bold;
                border-radius: 6px;
            }}
            
            /* Days from other months (grayed out) */
            QCalendarWidget QTableView::item:!enabled {{
                color: #adb5bd;
                background-color: transparent;
            }}
            
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                font-weight: 600;
                min-width: 70px;
                min-height: 32px;
                max-height: 32px;
                font-size: {button_font_size}px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4ea8eb, stop:1 #3990c9);
                transform: translateY(-1px);
            }}
            QLabel {{
                font-size: {button_font_size}px;
                font-weight: 500;
                color: #2c3e50;
                padding: 2px;
            }}
        """
    
    @staticmethod
    def get_compact_quick_filter_button_style():
        """Style for compact quick filter buttons"""
        font_size = AppStyles.scale_font_size(30)  # Giữ nguyên kích thước font
        
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #95a5a6, stop:1 #7f8c8d);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                font-weight: 600;
                min-width: 70px;
                min-height: 32px;
                max-height: 32px;
                font-size: {font_size}px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a5b5b6, stop:1 #8f9c8d);
                transform: translateY(-1px);
            }}
            QPushButton:pressed {{
                transform: translateY(1px);
            }}
        """

    @staticmethod
    def get_compact_pagination_frame_style():
        """Style for compact pagination frame"""
        return """
            QFrame {
                background: white;
                border: 1px solid #e0e6ed;
                border-radius: 8px;
                padding: 8px;
                margin: 4px;
                min-height: 16px;
            }
        """

    @staticmethod
    def get_compact_pagination_records_info_style():
        """Style for compact pagination records info"""
        font_size = AppStyles.scale_font_size(20)
        
        return f"""
            QLabel {{
                color: #6c757d;
                font-size: {font_size}px;
                font-weight: 500;
                padding: 4px;
            }}
        """

    @staticmethod
    def get_compact_pagination_page_info_style():
        """Style for compact pagination page info"""
        font_size = AppStyles.scale_font_size(20)
        
        return f"""
            QLabel {{
                font-weight: 600;
                color: #2c3e50;
                padding: 0 12px;
                font-size: {font_size}px;
                min-width: 100px;
                text-align: center;
            }}
        """

    @staticmethod
    def get_compact_pagination_button_style():
        """Style for compact pagination buttons"""
        font_size = AppStyles.scale_font_size(20)
        
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: {font_size}px;
                font-weight: 500;
                min-width: 60px;
                min-height: 32px;
                max-height: 32px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e9ecef, stop:1 #dee2e6);
                border: 1px solid #adb5bd;
                transform: translateY(-1px);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #dee2e6, stop:1 #ced4da);
                transform: translateY(1px);
            }}
            QPushButton:disabled {{
                background: #f8f9fa;
                color: #6c757d;
                border: 1px solid #dee2e6;
                transform: none;
            }}
        """

    @staticmethod
    def get_expanded_table_style():
        """Style for expanded table with more height"""
        font_size = AppStyles.scale_font_size(20)
        header_font_size = AppStyles.scale_font_size(27)
        
        return f"""
            QTableWidget {{
                border: 2px solid #bdc3c7;
                border-radius: 12px;
                background-color: white;
                gridline-color: #ecf0f1;
                font-size: {font_size}px;
                selection-background-color: #e8f4fd;
                outline: none;
            }}
            QHeaderView::section {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #34495e, stop:1 #2c3e50);
                color: white;
                border: 1px solid #2c3e50;
                padding: 12px 10px;
                font-weight: bold;
                font-size: {header_font_size}px;
                text-align: center;
                min-height: 20px;
            }}
            QHeaderView::section:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3d566e, stop:1 #34495e);
            }}
            QTableWidget::item {{
                padding: 10px 8px;
                border-bottom: 1px solid #ecf0f1;
                border-right: 1px solid #f8f9fa;
                word-wrap: break-word;
            }}
            QTableWidget::item:selected {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e8f4fd, stop:1 #d4edda);
                color: #2c3e50;
                border: 1px solid #4a86e8;
            }}
            QTableWidget::item:hover {{
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
            }}
            QScrollBar:vertical {{
                background: #f8f9fa;
                width: 14px;
                border-radius: 7px;
            }}
            QScrollBar::handle:vertical {{
                background: #dee2e6;
                border-radius: 7px;
                min-height: 24px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: #adb5bd;
            }}
        """

    @staticmethod
    def get_image_view_dialog_style():
        """Style for ImageViewDialog"""
        return """
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
        """

    @staticmethod
    def get_image_view_title_frame_style():
        """Style for ImageViewDialog title frame"""
        return """
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a86e8, stop:1 #3a76d8);
                border-radius: 12px;
                padding: 20px;
                min-height: 70px;
            }
        """

    @staticmethod
    def get_image_view_title_label_style():
        """Style for ImageViewDialog title label"""
        return """
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                margin: 0;
                padding: 10px 0;
            }
        """

    @staticmethod
    def get_image_view_image_label_style():
        """Style for ImageViewDialog image label"""
        return """
            QLabel {
                background: white;
                border: 3px solid #e0e6ed;
                border-radius: 15px;
                padding: 20px;
                min-height: 700px;
                min-width: 1000px;
            }
        """

    @staticmethod
    def get_image_view_invalid_image_style():
        """Style for invalid image in ImageViewDialog"""
        return """
            QLabel {
                font-size: 24px;
                color: #e74c3c;
                background: #f8f9fa;
                border: 2px dashed #dee2e6;
                border-radius: 10px;
                padding: 50px;
            }
        """

    @staticmethod
    def get_image_view_save_button_style():
        """Style for save button in ImageViewDialog"""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #28a745, stop:1 #218838);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 18px 30px;
                font-weight: 600;
                font-size: 22px;
                min-width: 180px;
                min-height: 60px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #34ce57, stop:1 #28a745);
                transform: translateY(-3px);
                box-shadow: 0 6px 15px rgba(40, 167, 69, 0.3);
            }
            QPushButton:pressed {
                transform: translateY(1px);
            }
        """

    @staticmethod
    def get_image_view_close_button_style():
        """Style for close button in ImageViewDialog"""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6c757d, stop:1 #5a6268);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 18px 30px;
                font-weight: 600;
                font-size: 22px;
                min-width: 150px;
                min-height: 60px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7c868d, stop:1 #6c757d);
                transform: translateY(-3px);
                box-shadow: 0 6px 15px rgba(108, 117, 125, 0.3);
            }
            QPushButton:pressed {
                transform: translateY(1px);
            }
        """

    @staticmethod
    def get_delete_dialog_delete_button_style():
        """Style for delete button in delete confirmation dialog"""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 25px;
                font-weight: bold;
                min-width: 120px;
                min-height: 45px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c0392b, stop:1 #a93226);
                transform: scale(1.05);
            }
            QPushButton:pressed {
                transform: scale(0.95);
            }
        """

    @staticmethod
    def get_delete_dialog_cancel_button_style():
        """Style for cancel button in delete confirmation dialog"""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #95a5a6, stop:1 #7f8c8d);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 25px;
                font-weight: bold;
                min-width: 120px;
                min-height: 45px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a5b5b6, stop:1 #8f9c9d);
                transform: scale(1.05);
            }
            QPushButton:pressed {
                transform: scale(0.95);
            }
        """
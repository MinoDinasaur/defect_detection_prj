from PySide6.QtWidgets import QSplashScreen, QLabel, QVBoxLayout, QWidget, QProgressBar
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPixmap, QFont, QPainter, QColor, QLinearGradient
import os

class SplashScreen(QSplashScreen):
    def __init__(self):
        # Tạo background pixmap
        pixmap = QPixmap(600, 400)
        super().__init__(pixmap)
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup splash screen UI"""
        # Load app icon
        self.icon_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'app_icon.png')
        
        if os.path.exists(self.icon_path):
            self.icon_pixmap = QPixmap(self.icon_path)
            # Scale icon to reasonable size
            self.icon_pixmap = self.icon_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            print(f"✅ Splash icon loaded: {self.icon_path}")
        else:
            self.icon_pixmap = None
            print(f"❌ Splash icon not found: {self.icon_path}")
        
        # Initialize progress
        self.progress_value = 0
        self.status_text = "Initializing..."
        
    def paintEvent(self, event):
        """Custom paint event for gradient background and content"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create gradient background
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(102, 126, 234))  # #667eea
        gradient.setColorAt(1, QColor(118, 75, 162))   # #764ba2
        
        painter.fillRect(self.rect(), gradient)
        
        # Draw icon if available
        if self.icon_pixmap:
            icon_x = (self.width() - self.icon_pixmap.width()) // 2
            icon_y = 80
            painter.drawPixmap(icon_x, icon_y, self.icon_pixmap)
        else:
            # Draw emoji icon as fallback
            painter.setPen(QColor(255, 255, 255))
            painter.setFont(QFont("Arial", 60))
            painter.drawText(self.rect().adjusted(0, 60, 0, -200), Qt.AlignCenter, "🔍")
        
        # Draw title
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Arial", 24, QFont.Bold))
        title_rect = self.rect().adjusted(20, 200, -20, -150)
        painter.drawText(title_rect, Qt.AlignCenter, "Defect Detection System")
        
        # Draw subtitle
        painter.setPen(QColor(255, 255, 255, 200))
        painter.setFont(QFont("Arial", 14))
        subtitle_rect = self.rect().adjusted(20, 240, -20, -110)
        painter.drawText(subtitle_rect, Qt.AlignCenter, "Quality Control & Analysis")
        
        # Draw progress bar
        progress_rect_bg = self.rect().adjusted(50, 280, -50, -80)
        painter.setPen(QColor(255, 255, 255, 100))
        painter.setBrush(QColor(255, 255, 255, 50))
        painter.drawRoundedRect(progress_rect_bg, 10, 10)
        
        # Draw progress fill
        if self.progress_value > 0:
            progress_width = int((progress_rect_bg.width() - 4) * self.progress_value / 100)
            progress_rect_fill = progress_rect_bg.adjusted(2, 2, -progress_rect_bg.width() + progress_width + 2, -2)
            
            progress_gradient = QLinearGradient(0, 0, progress_width, 0)
            progress_gradient.setColorAt(0, QColor(74, 134, 232))
            progress_gradient.setColorAt(1, QColor(58, 118, 216))
            
            painter.setBrush(progress_gradient)
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(progress_rect_fill, 8, 8)
        
        # Draw status text
        painter.setPen(QColor(255, 255, 255, 220))
        painter.setFont(QFont("Arial", 12))
        status_rect = self.rect().adjusted(20, 320, -20, -40)
        painter.drawText(status_rect, Qt.AlignCenter, self.status_text)
        
        # Draw university info
        painter.setPen(QColor(255, 255, 255, 150))
        painter.setFont(QFont("Arial", 10))
        uni_rect = self.rect().adjusted(20, 360, -20, -10)
        painter.drawText(uni_rect, Qt.AlignCenter, "Hanoi University of Science and Technology - 2025")
    
    def showMessage(self, message, progress=None):
        """Update status message and progress"""
        self.status_text = message
        if progress is not None:
            self.progress_value = progress
        
        # Trigger repaint
        self.update()
        
        # Process events to update UI
        from PySide6.QtWidgets import QApplication
        QApplication.processEvents()
    
    def start_animations(self):
        """Start animations - simplified"""
        # Simple fade in animation for whole splash screen
        self.setWindowOpacity(0.0)
        
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(800)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_animation.start()
import sys
import time
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont
from app.ui.main_window import DefectDetectionApp

def main():
    """Main entry point of the application."""
    try:
        # Initialize the application
        app = QApplication(sys.argv)
        
        # Set application properties
        app.setApplicationName("Defect Detection System")
        app.setApplicationDisplayName("Defect Detection System")
        app.setApplicationVersion("1.0")
        app.setOrganizationName("Hanoi University of Science and Technology")
        
        # Set application-wide style and font
        app.setStyle("Fusion")
        font = QFont("Segoe UI", 10)
        app.setFont(font)
        
        # Try to create splash screen
        splash = None
        try:
            from app.ui.splash_screen import SplashScreen
            splash = SplashScreen()
            splash.show()
            splash.start_animations()
            
            # Simulate loading process
            loading_steps = [
                ("Loading modules...", 10),
                ("Initializing database...", 25),
                ("Setting up camera...", 40),
                ("Loading AI models...", 60),
                ("Initializing barcode scanner...", 80),
                ("Finalizing setup...", 95),
                ("Ready!", 100)
            ]
            
            # Show loading progress
            for message, progress in loading_steps:
                splash.showMessage(message, progress)
                time.sleep(0.3)  # Reduced time for faster startup
                
        except Exception as e:
            print(f"Splash screen error: {e}")
            print("Starting without splash screen...")
            if splash:
                splash.close()
            splash = None
        
        # Create main window
        if splash:
            splash.showMessage("Loading main interface...", 100)
            
        main_window = DefectDetectionApp()
        
        # Show main window and close splash
        main_window.show()
        
        if splash:
            splash.finish(main_window)
        
        print("Application started successfully")
        
        # Execute the application event loop
        return app.exec()
        
    except Exception as e:
        print(f"Fatal error: {e}")
        try:
            QMessageBox.critical(None, "Application Error", f"Failed to start application:\n{str(e)}")
        except:
            pass
        return 1

if __name__ == "__main__":
    sys.exit(main())
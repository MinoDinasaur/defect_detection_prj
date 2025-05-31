from pynput import keyboard
from PySide6.QtCore import QObject, Signal
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from sqlite_database.src.db_operations import set_scanned_barcode

barcode_buffer = []

# Qt object for signal emission
class BarcodeScanner(QObject):
    barcode_detected = Signal(str)

barcode_scanner = BarcodeScanner()

def on_press(key):
    global barcode_buffer
    try:
        # Try to append the character of the key
        barcode_buffer.append(key.char)
    except AttributeError:
        # Special key (e.g., shift, ctrl, enter, space)
        if key == keyboard.Key.enter:
            # Barcode scanners often send 'enter' after the data
            scanned_data = "".join(filter(None, barcode_buffer)) # filter(None,...) handles if key.char was None
            if scanned_data:
                print(f"\nData Scanned (pynput): {scanned_data}")
                # --- Call your interaction logic here ---
                interact_with_barcode_data(scanned_data)
                # Emit signal for Qt integration
                barcode_scanner.barcode_detected.emit(scanned_data)
                # ----------------------------------------
            barcode_buffer = [] # Reset buffer for next scan
        elif key == keyboard.Key.space:
            barcode_buffer.append(' ') # Handle space explicitly if needed

def on_release(key):
    if key == keyboard.Key.esc: # Use Esc key to stop the listener
        print("Listener stopped by Esc key.")
        return False # Stop listener

def read_from_scanner_pynput():
    print("Global scanner listener started (pynput). Press ESC to stop.")
    print("You can now scan barcodes, focus can be on any window.")
    # Collect events until released
    try:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except Exception as e:
        print(f"Barcode scanner error: {e}")

def interact_with_barcode_data(data):
    """Function to handle scanned barcode data."""
    print(f"Interacting with: {data}")
    # Set the scanned barcode in the database module
    set_scanned_barcode(data)

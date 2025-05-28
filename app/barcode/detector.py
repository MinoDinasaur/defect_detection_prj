
from pynput import keyboard

barcode_buffer = []

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
                # ----------------------------------------
            barcode_buffer = [] # Reset buffer for next scan
        elif key == keyboard.Key.space:
            barcode_buffer.append(' ') # Handle space explicitly if needed
        # else:
            # You can handle other special keys if necessary
            # print(f'Special key {key} pressed')
            pass


def on_release(key):
    # print(f'Key {key} released')
    if key == keyboard.Key.esc: # Use Esc key to stop the listener
        print("Listener stopped by Esc key.")
        return False # Stop listener

def read_from_scanner_pynput():
    print("Global scanner listener started (pynput). Press ESC to stop.")
    print("You can now scan barcodes, focus can be on any window.")
    # Collect events until released
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def interact_with_barcode_data(data): # Same function as before
    """Placeholder function for your application logic."""
    print(f"Interacting with: {data}")
    if "PYTHON-DS22" in data:
        print("This seems to be one of our special product codes!")
    # Add more logic: database lookup, API call, file update, etc.

# --- Example Usage ---
if __name__ == "__main__":
    # To generate and then try to read:
    # my_data = "TEST-SCAN-PYNPUT-002"
    # generate_barcode_image(my_data, "test_scan_pynput_barcode")
    # print("\n--- Now switch to reading mode (pynput) ---")

    # Choose which method to run:
    # read_from_scanner_simple()
    read_from_scanner_pynput() # This will run the pynput listener
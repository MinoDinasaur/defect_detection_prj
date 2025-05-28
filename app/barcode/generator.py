from barcode import Code128 # A common barcode type
from barcode.writer import ImageWriter
from PIL import Image # To display the image (optional)

def generate_barcode_image(data_to_encode, filename="barcode_generated", image_format="PNG"):
    """
    Generates a barcode image and saves it.

    Args:
        data_to_encode (str): The string data to encode in the barcode.
        filename (str): The base name for the output file (without extension).
        image_format (str): "PNG" or "SVG".
    """
    try:
        # Select barcode type (Code128 is versatile)
        # Other options: EAN13, EAN8, UPC, ISBN13, Code39, etc.
        barcode_class = Code128

        # Create barcode object with ImageWriter
        # The writer determines how the barcode is rendered (e.g., as a PNG image)
        barcode_instance = barcode_class(data_to_encode, writer=ImageWriter())

        # Save the barcode image
        # The extension will be added automatically by the writer based on format options
        # For PNG, it will be .png
        # For SVG, it will be .svg
        options = {'format': image_format.upper()}
        full_filename = barcode_instance.save(filename, options=options)
        print(f"Barcode generated and saved as: {full_filename}")

        # Optional: Display the generated barcode (if Pillow is installed and you're in a GUI env)
        if image_format.upper() == "PNG":
            try:
                img = Image.open(full_filename)
                img.show()
            except Exception as e:
                print(f"Could not display image (Pillow might need a display server): {e}")
        return full_filename
    except Exception as e:
        print(f"Error generating barcode: {e}")
        return None

# --- Example Usage ---
if __name__ == "__main__":
    my_data = "PYTHON-DS22-12345"
    generate_barcode_imưq2age(my_data, "my_product_code")

    my_data_2 = "https://www.python.org"
    generate_barcode_image(my_data_2, "python_website_qr", image_format="PNG") # Code128 is not for URLs primarily, QR better
                                                                            # For QR codes, use 'qrcode' library: pip install qrcode[pil]
                                                                            # Example for QR:
                                                                            # import qrcode
                                                                            # img = qrcode.make(my_data_2)
                                                                            # img.save("python_website_qr.png")
                                                                            # print("QR Code generated as python_website_qr.png")


from barcode import Code128 # A common barcode type
from barcode.writer import ImageWriter
from PIL import Image # To display the image (optional)
import random
import os

def generate_barcode_image(data_to_encode, filename="barcode_generated", image_format="PNG"):
    """
    Generates a barcode image and saves it.

    Args:
        data_to_encode (str): The string data to encode in the barcode.
        filename (str): The base name for the output file (without extension).
        image_format (str): "PNG" or "SVG".
    """
    try:
        # Create storage directory if it doesn't exist
        storage_dir = "./storage/barcode"
        os.makedirs(storage_dir, exist_ok=True)
        
        # Full path with storage directory
        full_path = os.path.join(storage_dir, filename)
        
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
        full_filename = barcode_instance.save(full_path, options=options)
        print(f"Barcode generated and saved as: {full_filename}")
        return full_filename
    except Exception as e:
        print(f"Error generating barcode: {e}")
        return None

def generate_random_da_code(num_digits=8):
    """
    Generates a random code in format: DucAnh-{random numeric codes}
    
    Args:
        num_digits (int): Number of random digits to generate (default: 8)
    
    Returns:
        str: Random code in format "DucAnh-XXXXXXXX"
    """
    random_numbers = ''.join([str(random.randint(0, 9)) for _ in range(num_digits)])
    return f"DA-{random_numbers}"

def generate_random_da_barcode(num_digits=8, filename=None):
    """
    Generates a random barcode.
    
    Args:
        num_digits (int): Number of random digits (default: 8)
        filename (str): Optional filename, if None uses the generated code
    
    Returns:
        tuple: (generated_code, barcode_filename)
    """
    # Generate random code
    random_code = generate_random_da_code(num_digits)
    
    # Use the code as filename if none provided
    if filename is None:
        filename = f"barcode_{random_code.replace('-', '_')}"
    
    # Generate the barcode
    barcode_file = generate_barcode_image(random_code, filename)
    
    return random_code, barcode_file

# --- Example Usage ---
if __name__ == "__main__":
    # Generate single random barcode
    print("Generating random barcode...")
    code, file = generate_random_da_barcode()
    print(f"Generated code: {code}")
    print(f"Saved as: {file}")
    
    print("\n" + "="*50)
    
    # Generate multiple random barcodes
    print("Generating 5 random barcodes:")
    for i in range(100):
        code, file = generate_random_da_barcode(6)  # 6 digits
        print(f"  {i+1}. {code} -> {file}")

import os
import pytesseract
from PIL import Image

# Set Tesseract OCR executable path if not in the system PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def process_image(image_path):
    # Open the image using PIL
    img = Image.open(image_path)
    # Use Tesseract to do OCR on the image
    text = pytesseract.image_to_string(img, lang='hin')  # 'hin' is the language code for Hindi (Devanagari script)
    return text

def main():
    # Directory containing scanned images
    scanned_images_dir = 'scanned_images'
    if not os.path.exists(scanned_images_dir):
        print(f"Directory {scanned_images_dir} does not exist. Please create it and add images.")
        return
    
    for filename in os.listdir(scanned_images_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff')):
            image_path = os.path.join(scanned_images_dir, filename)
            print(f"\nProcessing {filename}:")
            print("-" * 30)
            try:
                text_content = process_image(image_path)
                print("Recognized text:")
                print(text_content.strip())
            except pytesseract.TesseractError as e:
                print(f"An error occurred while processing {filename}: {e}")
            print("-" * 30)

if __name__ == "__main__":
    main()

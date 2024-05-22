import os
import cv2
import numpy as np
import pytesseract
from PIL import Image

# Set Tesseract OCR executable path if not in the system PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def deskew(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Threshold the image
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours and the bounding box
    coords = np.column_stack(np.where(binary > 0))
    angle = cv2.minAreaRect(coords)[-1]

    # Adjust the angle
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # Rotate the image to deskew
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated

def enhance_text(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Deskew the image
    deskewed_image = deskew(image)

    # Convert the image to grayscale
    gray = cv2.cvtColor(deskewed_image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to binarize the image
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Use morphological operations to enhance text regions
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # Convert the binary image to BGR format for bitwise operations
    binary_bgr = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

    # Apply the inverted binary mask to the original image
    enhanced_image = cv2.bitwise_and(deskewed_image, binary_bgr)

    # Convert all other regions to white
    enhanced_image[binary == 0] = [255, 255, 255]

    return enhanced_image

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
                # Enhance the text in the image
                enhanced_image = enhance_text(image_path)
                enhanced_image_path = os.path.join(scanned_images_dir, f"enhanced_{filename}")
                cv2.imwrite(enhanced_image_path, enhanced_image)

                # Perform OCR on the enhanced image
                text_content = process_image(enhanced_image_path)
                print("Recognized text:")
                print(text_content.strip())
            except pytesseract.TesseractError as e:
                print(f"An error occurred while processing {filename}: {e}")
            print("-" * 30)

if __name__ == "__main__":
    main()

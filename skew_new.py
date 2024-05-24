import os
import cv2
import numpy as np
import pytesseract
from PIL import Image

# Setting path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

def rotate(image):
    # Converting  to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Thresholding the image
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Finding contours and the bounding box
    coords = np.column_stack(np.where(binary > 0))
    angle = cv2.minAreaRect(coords)[-1]

    # Adjusting the angle
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # Rotating the image
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated



def enhance_text(image):

    deskewed_image = rotate(image)

    gray = cv2.cvtColor(deskewed_image, cv2.COLOR_BGR2GRAY)

    # Applying thresholding to binarize the image
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Using morphological operations to enhance text regions
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # Converting the binary image to BGR format for bitwise operations
    binary_bgr = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

    # Applying the inverted binary mask to the original image
    enhanced_image = cv2.bitwise_and(deskewed_image, binary_bgr)

    # Converting all other regions to white
    enhanced_image[binary == 0] = [255, 255, 255]

    # Converting the enhanced image to PIL format
    enhanced_image_pil = Image.fromarray(cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2RGB))

    return enhanced_image_pil

def process_image(image_pil):
    # Useing Tesseract to do OCR on the PIL image
    text = pytesseract.image_to_string(image_pil, lang='hin')  # 'hin' is the language code for Hindi (Devanagari script)
    return text


def main():
    
    scanned_images_dir = 'scanned_images'
    if not os.path.exists(scanned_images_dir):
        print(f"Directory {scanned_images_dir} does not exist. Please create it and add images.")
        return
    

    results_dir = 'ocr_results'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        
        
    for filename in os.listdir(scanned_images_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff')):
            image_path = os.path.join(scanned_images_dir, filename)
            print(f"\nProcessing {filename}:")
            print("-" * 30)
            try:
                image = cv2.imread(image_path)

                enhanced_image_pil = enhance_text(image)

                text_content = process_image(enhanced_image_pil)
                print("Recognized text:")
                print(text_content.strip())


                text_file_path = os.path.join(results_dir, f"{os.path.splitext(filename)[0]}.txt")
                with open(text_file_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(text_content.strip())

            except pytesseract.TesseractError as e:
                print(f"An error occurred while processing {filename}: {e}")
            print("-" * 30)

if __name__ == "__main__":
    main()

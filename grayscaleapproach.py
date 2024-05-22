import cv2
import numpy as np

def enhance_text(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to binarize the image
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Use morphological operations to enhance text regions
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # Convert the binary image to BGR format for bitwise operations
    binary_bgr = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

    # Apply the inverted binary mask to the original image
    enhanced_image = cv2.bitwise_and(image, binary_bgr)

    # Convert all other regions to white
    enhanced_image[binary == 0] = [255, 255, 255]

    return enhanced_image

# Example usage
input_image_path = 'citizenship front.jpg'
enhanced_image = enhance_text(input_image_path)
cv2.imwrite('enhanced_citizenship_certificate.jpg', enhanced_image)

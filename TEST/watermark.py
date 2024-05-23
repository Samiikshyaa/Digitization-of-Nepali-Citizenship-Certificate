import cv2
import numpy as np

def remove_watermark(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range of yellow color in HSV
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    # Create a mask to extract yellow regions
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Inpaint the masked region
    result = cv2.inpaint(image, mask, inpaintRadius=5, flags=cv2.INPAINT_TELEA)

    return result

# Example usage
input_image_path = r'C:\Users\Asus\Documents\python\scanned_images\Screenshot 2024-05-22 150639.png'
output_image = remove_watermark(input_image_path)
cv2.imwrite('output_image.jpg', output_image)

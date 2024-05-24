# Digitization Of Nepali Citizenship Certificate Using OCR

### Project Overview 
This project uses Tesseract OCR Engine for recognition of Nepali Citizenship Certificate. 

As Nepali citizenship follows Devanagari scripts, I have used Tesseract with "Hindi" language.  


### Requirement
1. pip install pytesseract Pillow
2. Install Tesseract OCR engine form this link:  https://github.com/UB-Mannheim/tesseract/wiki
3. Make sure "hin.traineddata" is inside the directory: "C:\Program Files\Tesseract-OCR\tessdata" . Else, download it: https://github.com/tesseract-ocr/tessdata


4. Make sure you have made the directories: "scanned_images" and "ocr_results"
5. Also make sure your certificate image is inside the directory "scanned_images"

   Finally, the result can be dislayed in the console and also in the generated txt file inside "ocr_results"

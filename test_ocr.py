import pytesseract
from PIL import Image

from scam_detector import analyze_message


# Tesseract installation path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# Open screenshot
image = Image.open(
    r"C:\Users\HP\OneDrive\Desktop\AI-ScamGuard\test_screenshot.png"
)


# Extract text
extracted_text = pytesseract.image_to_string(image)


print("===== EXTRACTED TEXT =====")
print(extracted_text)


# Analyze extracted text
result = analyze_message(extracted_text)


print("\n===== SCAM DETECTION RESULT =====")
print("Risk Score:", result["score"])
print("Risk Level:", result["risk_level"])
print("Detected:", result["detected"])
print("ML Prediction:", result["ml_prediction"])
print("ML Probability:", result["ml_probability"], "%")
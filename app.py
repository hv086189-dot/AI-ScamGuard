from flask import Flask, render_template, request, jsonify
import pytesseract
from PIL import Image

from scam_detector import analyze_message


app = Flask(__name__)


# Tesseract installation path
import os
import shutil

tesseract_path = shutil.which("tesseract")

if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )


@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------
# Analyze normal text
# --------------------------------

@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "error": "Please enter a message."
        }), 400

    result = analyze_message(message)

    return jsonify(result)


# --------------------------------
# Analyze screenshot
# --------------------------------

@app.route("/scan-screenshot", methods=["POST"])
def scan_screenshot():

    if "image" not in request.files:
        return jsonify({
            "error": "No image uploaded."
        }), 400

    image_file = request.files["image"]

    if image_file.filename == "":
        return jsonify({
            "error": "Please select an image."
        }), 400

    try:

        # Open uploaded image
        image = Image.open(image_file.stream)

        # Extract text using OCR
        extracted_text = pytesseract.image_to_string(image)

        if not extracted_text.strip():
            return jsonify({
                "error": "No readable text found in the image."
            }), 400

        # Analyze OCR text
        result = analyze_message(extracted_text)

        # Add extracted text to result
        result["extracted_text"] = extracted_text

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "error": f"Could not process image: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
# AI-ScamGuard 🛡️

AI-ScamGuard is an AI-powered scam detection system designed to analyze suspicious messages, emails, URLs, and screenshots.

The system combines rule-based detection, machine learning, URL analysis, and OCR to identify common scam indicators.

## Features

- 🔍 Analyze suspicious messages and emails
- 🤖 Machine learning based spam/ham classification
- 🔗 Suspicious URL detection
- 📸 Screenshot scanning using OCR
- ⚠️ Risk score from 0–100
- 🚨 Low, Medium, and High Risk classification
- 🔐 Detect credential requests such as OTP, PIN, password, and CVV
- 💰 Detect financial scam indicators
- ⏰ Detect urgency and account-threat language
- 🌐 Web-based dashboard using Flask

## Technologies Used

- Python
- Flask
- Scikit-learn
- Pandas
- Joblib
- Tesseract OCR
- Pytesseract
- Pillow
- HTML
- CSS
- JavaScript

## Machine Learning

The project uses the UCI SMS Spam Collection dataset to train a TF-IDF + Logistic Regression model.

The trained model classifies messages as:

- HAM
- SPAM

The machine learning component is combined with rule-based scam indicators to produce an overall risk score.

## OCR Screenshot Detection

Users can upload a screenshot containing a suspicious message.

AI-ScamGuard:

1. Extracts text from the screenshot using OCR.
2. Analyzes the extracted text.
3. Detects suspicious indicators.
4. Performs machine learning classification.
5. Generates a risk score.
6. Displays the detected information on the dashboard.

## Risk Classification

| Score | Risk Level |
|------:|------------|
| 0–39 | Low Risk |
| 40–69 | Medium Risk |
| 70–100 | High Risk |

## Project Structure

```text
AI-ScamGuard/
│
├── app.py
├── scam_detector.py
├── url_analyzer.py
├── train_model.py
├── test_detector.py
├── test_ml_model.py
├── test_ocr.py
├── inspect_dataset.py
│
├── spam_model.pkl
├── tfidf_vectorizer.pkl
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
├── static/
├── templates/
└── venv/

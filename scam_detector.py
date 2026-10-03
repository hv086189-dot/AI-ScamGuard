import re
import joblib

from url_analyzer import analyze_url


# Load trained ML model
model = joblib.load("spam_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")


# Scam-related indicators
SCAM_INDICATORS = {
    "urgency": [
        "urgent",
        "immediately",
        "act now",
        "right now",
        "last chance",
        "within 24 hours"
    ],

    "account_threat": [
        "account blocked",
        "account will be blocked",
        "account suspended",
        "account deactivated",
        "account will be closed"
    ],

    "financial": [
        "you won",
        "winner",
        "prize",
        "cashback",
        "lottery",
        "money",
        "payment",
        "refund"
    ],

    "credential_request": [
        "otp",
        "password",
        "pin",
        "cvv",
        "verification code"
    ],

    "link_request": [
        "click here",
        "click the link",
        "open this link",
        "visit this link"
    ]
}


# Rule-based scores
RULE_SCORES = {
    "urgency": 10,
    "account_threat": 20,
    "financial": 10,
    "credential_request": 25,
    "link_request": 10,
    "suspicious_url": 15
}


def analyze_message(message):

    original_message = message
    message = message.lower()

    rule_score = 0
    detected = []

    # --------------------------------
    # 1. Scam keyword analysis
    # --------------------------------

    for category, phrases in SCAM_INDICATORS.items():

        for phrase in phrases:

            if phrase in message:

                rule_score += RULE_SCORES[category]

                detected.append(category)

                break


    # --------------------------------
    # 2. URL analysis
    # --------------------------------

    url_pattern = r"https?://\S+|www\.\S+"

    urls = re.findall(url_pattern, original_message)

    url_score = 0

    for url in urls:

        url_result = analyze_url(url)

        url_score += min(url_result["score"], 20)

        for indicator in url_result["indicators"]:

            detected.append("url_" + indicator)


    # --------------------------------
    # 3. Machine Learning analysis
    # --------------------------------

    message_tfidf = vectorizer.transform([original_message])

    prediction = model.predict(message_tfidf)[0]

    probabilities = model.predict_proba(message_tfidf)[0]

    spam_probability = float(probabilities[1])

    ml_score = round(spam_probability * 20)


    # --------------------------------
    # 4. Combine scores
    # --------------------------------

    score = rule_score + ml_score + url_score

    score = min(score, 100)


    # --------------------------------
    # 5. ML detection indicator
    # --------------------------------

    if prediction == 1:

        detected.append("ml_spam_detection")


    # Remove duplicate indicators

    detected = list(set(detected))


    # --------------------------------
    # 6. Risk level
    # --------------------------------

    if score >= 70:

        risk_level = "HIGH RISK"

    elif score >= 40:

        risk_level = "MEDIUM RISK"

    else:

        risk_level = "LOW RISK"


    # --------------------------------
    # 7. Return result
    # --------------------------------

    return {
        "score": score,
        "risk_level": risk_level,
        "detected": detected,
        "ml_prediction": "SPAM" if prediction == 1 else "HAM",
        "ml_probability": round(spam_probability * 100, 2)
    }
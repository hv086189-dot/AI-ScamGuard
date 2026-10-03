from scam_detector import analyze_message


message = """
URGENT! Your bank account will be blocked today.
Click this link immediately:
https://bit.ly/claim-refund
Send your OTP to receive your refund.
"""


result = analyze_message(message)


print("===== SCAM DETECTION TEST =====")
print("Risk Score:", result["score"])
print("Risk Level:", result["risk_level"])
print("Detected:", result["detected"])
print("ML Prediction:", result["ml_prediction"])
print("ML Probability:", result["ml_probability"], "%")
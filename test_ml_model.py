import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# 1. Load dataset
file_path = "data/SMSSpamCollection"

df = pd.read_csv(
    file_path,
    sep="\t",
    header=None,
    names=["label", "message"]
)


# 2. Convert labels into numbers
df["label"] = df["label"].map({
    "ham": 0,
    "spam": 1
})


# 3. Separate messages and labels
X = df["message"]
y = df["label"]


# 4. Convert text into TF-IDF
vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english"
)

X_tfidf = vectorizer.fit_transform(X)


# 5. Train the model
model = LogisticRegression(
    max_iter=1000
)

model.fit(X_tfidf, y)


# 6. Our own test messages
test_messages = [
    "URGENT! Your bank account will be blocked. Send your OTP immediately.",
    "Hey bro, are you coming to college tomorrow?",
    "Congratulations! You won a cash prize. Click here to claim your reward.",
    "Can you send me the notes from today's class?"
]


# 7. Convert test messages to TF-IDF
test_tfidf = vectorizer.transform(test_messages)


# 8. Predict
predictions = model.predict(test_tfidf)
probabilities = model.predict_proba(test_tfidf)


# 9. Display results
print("\n===== CUSTOM MESSAGE TEST =====")

for message, prediction, probability in zip(
    test_messages,
    predictions,
    probabilities
):

    if prediction == 1:
        result = "SPAM"
    else:
        result = "HAM"

    confidence = probability[prediction] * 100

    print("\nMessage:")
    print(message)

    print("Prediction:", result)
    print("Confidence: {:.2f}%".format(confidence))
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

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


# 4. Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


print("Total messages:", len(df))
print("Training messages:", len(X_train))
print("Testing messages:", len(X_test))


# 5. Convert text into TF-IDF numbers
vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english"
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)


print("Training TF-IDF shape:", X_train_tfidf.shape)
print("Testing TF-IDF shape:", X_test_tfidf.shape)


# 6. Create the machine learning model
model = LogisticRegression(
    max_iter=1000
)


# 7. Train the model
model.fit(X_train_tfidf, y_train)


print("Model training completed!")

# 8. Make predictions on test data
y_pred = model.predict(X_test_tfidf)


# 9. Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\n===== MODEL EVALUATION =====")
print("Accuracy:", accuracy)


# 10. Detailed classification report
print("\n===== CLASSIFICATION REPORT =====")
print(classification_report(
    y_test,
    y_pred,
    target_names=["ham", "spam"]
))


# 11. Confusion matrix
print("\n===== CONFUSION MATRIX =====")
print(confusion_matrix(y_test, y_pred))

# 12. Save the trained model and vectorizer
joblib.dump(model, "spam_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

print("\nModel saved successfully!")
print("Saved: spam_model.pkl")
print("Saved: tfidf_vectorizer.pkl")
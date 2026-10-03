import pandas as pd


file_path = "data/SMSSpamCollection"


df = pd.read_csv(
    file_path,
    sep="\t",
    header=None,
    names=["label", "message"]
)


print("\n===== DATASET SHAPE =====")
print(df.shape)


print("\n===== FIRST 10 MESSAGES =====")
print(df.head(10))


print("\n===== LABEL COUNTS =====")
print(df["label"].value_counts())


print("\n===== MISSING VALUES =====")
print(df.isnull().sum())


print("\n===== DATASET INFORMATION =====")
print(df.info())
import pandas as pd
import matplotlib.pyplot as plt

print("Loading data...")

data = pd.read_csv("output.csv")

print("Data loaded!")

sentiment_counts = data["Sentiment"].value_counts()

print(sentiment_counts)

plt.figure(figsize=(6,4))

sentiment_counts.plot(kind="bar")

plt.title("Employee Review Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Count")

print("Displaying graph...")

plt.show()

print("Done")
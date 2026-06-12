import pandas as pd
from sentiment_analysis import analyze_sentiment
from preprocessing import preprocess_text

INPUT_FILE = "dataset/employee_reviews.csv"
OUTPUT_FILE = "output.csv"

CHUNK_SIZE = 50000

first_chunk = True

for chunk_num, chunk in enumerate(
    pd.read_csv(
        INPUT_FILE,
        usecols=["pros"],
        dtype=str,
        chunksize=CHUNK_SIZE
    ),
    start=1
):

    print(f"Processing chunk {chunk_num}...")

    # Fill missing values
    chunk["pros"] = chunk["pros"].fillna("")

    # Clean text
    chunk["Cleaned_Review"] = chunk["pros"].apply(preprocess_text)

    # Sentiment analysis
    chunk["Sentiment"] = chunk["Cleaned_Review"].apply(analyze_sentiment)

    # Save incrementally
    chunk.to_csv(
        OUTPUT_FILE,
        mode="w" if first_chunk else "a",
        header=first_chunk,
        index=False
    )

    first_chunk = False

    print(f"Chunk {chunk_num} completed")

print("All reviews processed successfully!")
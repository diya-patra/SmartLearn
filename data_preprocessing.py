
import pandas as pd
import os
import re


# File paths
INPUT_FILE = "dataset/udemy_courses.csv"
OUTPUT_FILE = "dataset/cleaned_courses.csv"


def clean_text(text):
    """Clean text safely without converting missing values into 'nan'."""

    if pd.isna(text):
        return ""

    text = str(text).strip()

    if text.lower() in ["nan", "none", "null"]:
        return ""

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def preprocess_data():

    # Step 1: Load the original dataset
    df = pd.read_csv(INPUT_FILE)

    print("Original dataset shape:", df.shape)

    # Step 2: Remove duplicate courses
    df = df.drop_duplicates(subset=["course_id"])

    # Step 3: Remove rows without essential information
    required_columns = ["course_id", "course_title", "subject", "level"]

    for column in required_columns:
        df[column] = df[column].replace(
            r"^\s*(nan|none|null)?\s*$",
            pd.NA,
            regex=True
        )

    df = df.dropna(subset=required_columns)

    # Step 4: Create cleaned text versions
    # Keep the original course titles readable for display.
    df["clean_title"] = df["course_title"].apply(clean_text)
    df["clean_subject"] = df["subject"].apply(clean_text)
    df["clean_level"] = df["level"].apply(clean_text)

    # Step 5: Combine text for the recommendation model
    df["course_features"] = (
        df["clean_title"] + " " +
        df["clean_subject"] + " " +
        df["clean_level"]
    ).str.strip()

    # Step 6: Remove any rows with empty course features
    df = df[df["course_features"] != ""]

    # Step 7: Save the cleaned dataset
    os.makedirs("dataset", exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print("\nPreprocessing completed successfully!")
    print("Cleaned dataset shape:", df.shape)
    print("Saved file:", OUTPUT_FILE)

    print("\nSample course features:")
    print(
        df[["course_title", "course_features"]]
        .head(5)
        .to_string(index=False)
    )

    return df


if __name__ == "__main__":
    preprocess_data()

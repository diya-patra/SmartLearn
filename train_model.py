
import pandas as pd
import joblib
import os

from sklearn.feature_extraction.text import TfidfVectorizer


# Define file paths
DATASET_FILE = "dataset/cleaned_courses.csv"
MODEL_DIR = "ml_model"


def train_model():

    # Step 1: Load the cleaned dataset
    df = pd.read_csv(DATASET_FILE)

    # Step 2: Extract course features
    course_features = df["course_features"].fillna("")

    # Step 3: Create the TF-IDF vectorizer
    tfidf = TfidfVectorizer(
        stop_words="english",
        max_features=5000
    )

    # Step 4: Convert text into numerical vectors
    course_vectors = tfidf.fit_transform(course_features)

    # Step 5: Create model directory
    os.makedirs(MODEL_DIR, exist_ok=True)

    # Step 6: Save the vectorizer and course vectors
    joblib.dump(
        tfidf,
        os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
    )

    joblib.dump(
        course_vectors,
        os.path.join(MODEL_DIR, "course_vectors.pkl")
    )

    # Step 7: Save course information for recommendations
    df.to_csv(
        os.path.join(MODEL_DIR, "model_courses.csv"),
        index=False
    )

    print("TF-IDF model trained successfully!")
    print("Number of courses:", len(df))
    print("Number of features:", len(tfidf.get_feature_names_out()))
    print("Course vector shape:", course_vectors.shape)


if __name__ == "__main__":
    train_model()

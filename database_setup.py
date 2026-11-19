
from pathlib import Path
import pandas as pd
from pymongo import UpdateOne

from database import get_database


def setup_database():
    db = get_database()
    courses_collection = db["courses"]

    # Find the CSV file in the Downloads folder
    csv_path = (
    Path(__file__).resolve().parent
    / "dataset"
    / "udemy_courses.csv"
    )

    if not csv_path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {csv_path}"
        )

    # Read the actual Udemy dataset
    df = pd.read_csv(csv_path)

    # Remove duplicate course IDs
    df = df.drop_duplicates(
        subset=["course_id"],
        keep="last"
    )

    # Create a unique index for course IDs
    courses_collection.create_index(
        "course_id",
        unique=True
    )

    # Prepare course records
    df = df.where(pd.notna(df), None)
    courses = df.to_dict(orient="records")

    # Insert or update courses without creating duplicates
    operations = [
        UpdateOne(
            {"course_id": course["course_id"]},
            {"$set": course},
            upsert=True
        )
        for course in courses
    ]

    if operations:
        result = courses_collection.bulk_write(operations)

        print("Database setup completed!")
        print(f"Courses processed: {len(courses)}")
        print(f"New courses inserted: {result.upserted_count}")
        print(f"Existing courses updated: {result.modified_count}")


if __name__ == "__main__":
    setup_database()


import pandas as pd
import joblib
import os
from sklearn.metrics.pairwise import cosine_similarity

MODEL_DIR = "ml_model"

VECTORIZER_FILE = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
COURSES_FILE = os.path.join(MODEL_DIR, "model_courses.csv")


def convert_to_text(value):
    """Convert strings or lists into clean text."""

    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip().lower()

    if isinstance(value, list):
        return " ".join(
            str(item).strip().lower()
            for item in value
            if item is not None and str(item).strip()
        )

    return str(value).strip().lower()


def get_level_category(level):
    """Identify the learning level."""

    level = str(level).lower()

    if "beginner" in level:
        return "beginner"
    elif "intermediate" in level:
        return "intermediate"
    elif "expert" in level:
        return "expert"
    elif "all" in level:
        return "all"

    return ""


def calculate_level_score(student_level, course_level):
    """Calculate course level compatibility."""

    student = get_level_category(student_level)
    course = get_level_category(course_level)

    if not student:
        return 0.0

    if course == "all":
        return 0.9

    if student == course:
        return 1.0

    level_scores = {
        "beginner": {
            "intermediate": 0.45,
            "expert": 0.20
        },
        "intermediate": {
            "beginner": 0.75,
            "expert": 0.50
        },
        "expert": {
            "beginner": 0.50,
            "intermediate": 0.75
        }
    }

    return level_scores.get(student, {}).get(course, 0.0)


def recommend_courses(profile, top_n=5):

    # Load trained vectorizer and course dataset.
    tfidf = joblib.load(VECTORIZER_FILE)
    courses = pd.read_csv(COURSES_FILE)

    # Get student profile information.
    interests = convert_to_text(profile.get("interests", ""))
    skills = convert_to_text(profile.get("skills", ""))
    skill_level = convert_to_text(profile.get("skill_level", ""))

    if not interests and not skills and not skill_level:
        print("Student profile does not contain recommendation information.")
        return pd.DataFrame()

    # Prepare course information.
    course_titles = courses["clean_title"].fillna("").astype(str)
    course_subjects = courses["clean_subject"].fillna("").astype(str)

    # ---------------------------------
    # 1. Interest matching
    # ---------------------------------

    if interests:

        # Compare student interests with course titles.
        interest_vector = tfidf.transform([interests])
        title_vectors = tfidf.transform(course_titles)
        subject_vectors = tfidf.transform(course_subjects)

        title_interest_scores = cosine_similarity(
            interest_vector,
            title_vectors
        ).flatten()

        subject_interest_scores = cosine_similarity(
            interest_vector,
            subject_vectors
        ).flatten()

        # Course titles matter more than subject names.
        interest_scores = (
            0.80 * title_interest_scores
            + 0.20 * subject_interest_scores
        )

    else:
        interest_scores = [0.0] * len(courses)

    # ---------------------------------
    # 2. Skill matching
    # ---------------------------------

    if skills:

        skill_vector = tfidf.transform([skills])
        skill_course_vectors = tfidf.transform(course_titles)

        skill_scores = cosine_similarity(
            skill_vector,
            skill_course_vectors
        ).flatten()

    else:
        skill_scores = [0.0] * len(courses)

    # ---------------------------------
    # 3. Learning level matching
    # ---------------------------------

    if skill_level:

        level_scores = courses["level"].apply(
            lambda course_level: calculate_level_score(
                skill_level,
                course_level
            )
        ).tolist()

    else:
        level_scores = [0.0] * len(courses)

    # Store individual scores.
    courses["interest_score"] = interest_scores
    courses["skill_score"] = skill_scores
    courses["level_score"] = level_scores

    # ---------------------------------
    # 4. Final recommendation score
    # ---------------------------------

    weights = {
        "interest_score": 0.40,
        "skill_score": 0.50,
        "level_score": 0.10
    }

    # Use only factors available in the student profile.
    active_weights = {
        column: weight
        for column, weight in weights.items()
        if (
            (column == "interest_score" and interests)
            or (column == "skill_score" and skills)
            or (column == "level_score" and skill_level)
        )
    }

    total_weight = sum(active_weights.values())

    courses["similarity_score"] = sum(
        courses[column] * (weight / total_weight)
        for column, weight in active_weights.items()
    )

    # Rank courses by final score.
    recommended_courses = courses.sort_values(
        by="similarity_score",
        ascending=False
    )

    return recommended_courses.head(top_n).reset_index(drop=True)


if __name__ == "__main__":

    sample_profile = {
        "interests": ["Business Finance"],
        "skills": ["Accounting", "Excel"],
        "skill_level": "Beginner Level"
    }

    results = recommend_courses(sample_profile, top_n=5)

    if not results.empty:

        print("\nRecommended Courses:\n")

        for index, course in results.iterrows():

            print(f"{index + 1}. {course['course_title']}")
            print(f"   Subject: {course['subject']}")
            print(f"   Level: {course['level']}")
            print(f"   Interest Match: {course['interest_score']:.4f}")
            print(f"   Skill Match: {course['skill_score']:.4f}")
            print(f"   Level Match: {course['level_score']:.4f}")
            print(f"   Final Score: {course['similarity_score']:.4f}")
            print()

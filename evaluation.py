
from recommender import recommend_courses


# Different student profiles for testing
test_profiles = {
    "Web Development Student": {
        "interests": ["Web Development"],
        "skills": ["HTML", "CSS"],
        "skill_level": "Beginner Level"
    },

    "Business Finance Student": {
        "interests": ["Business Finance"],
        "skills": ["Accounting", "Finance"],
        "skill_level": "Beginner Level"
    },

    "Musical Instruments Student": {
        "interests": ["Musical Instruments"],
        "skills": ["Guitar", "Music"],
        "skill_level": "Beginner Level"
    },

    "Graphic Design Student": {
        "interests": ["Graphic Design"],
        "skills": ["Photoshop", "Design"],
        "skill_level": "Beginner Level"
    },

    "Cross-Subject Student": {
        "interests": ["Business Finance"],
        "skills": ["Excel", "Python"],
        "skill_level": "Beginner Level"
    }
}


def evaluate_recommendations():

    print("SMARTLEARN RECOMMENDATION EVALUATION")
    print("=" * 50)

    for student, profile in test_profiles.items():

        print(f"\nStudent Profile: {student}")
        print("-" * 50)

        # Show 20 results only for the cross-subject test.
        # Other profiles will continue showing 5 results.
        top_n = 20 if student == "Cross-Subject Student" else 5

        recommendations = recommend_courses(
            profile,
            top_n=top_n
        )

        if recommendations.empty:
            print("No recommendations found.")
            continue

        for index, course in recommendations.iterrows():

            print(f"\n{index + 1}. {course['course_title']}")
            print(f"   Subject: {course['subject']}")
            print(f"   Level: {course['level']}")
            print(f"   Interest Match: {course['interest_score']:.4f}")
            print(f"   Skill Match: {course['skill_score']:.4f}")
            print(f"   Level Match: {course['level_score']:.4f}")
            print(f"   Final Score: {course['similarity_score']:.4f}")

        # Show subject distribution for the cross-subject test.
        if student == "Cross-Subject Student":

            print("\nSUBJECT DISTRIBUTION")
            print("-" * 30)

            subject_counts = recommendations["subject"].value_counts()

            for subject, count in subject_counts.items():
                print(f"{subject}: {count} courses")


if __name__ == "__main__":
    evaluate_recommendations()

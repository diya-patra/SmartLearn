
from pymongo.errors import DuplicateKeyError
from database import get_database


def get_all_courses():
    db = get_database()
    courses = db["courses"]

    return list(courses.find())


def get_course_by_id(course_id):
    db = get_database()
    courses = db["courses"]

    return courses.find_one({"course_id": course_id})


def enroll_student(email, course_id):
    db = get_database()
    enrollments = db["enrollments"]

    email = email.strip().lower()

    enrollments.create_index(
        [("student_email", 1), ("course_id", 1)],
        unique=True
    )

    enrollment = {
        "student_email": email,
        "course_id": course_id,
        "status": "Enrolled",
        "progress": 0
    }

    try:
        enrollments.insert_one(enrollment)
        return True
    except DuplicateKeyError:
        return False


def get_student_enrollments(email):
    db = get_database()
    enrollments = db["enrollments"]

    email = email.strip().lower()

    return list(
        enrollments.find({"student_email": email})
    )


def update_learning_status(email, course_id, status):
    db = get_database()
    enrollments = db["enrollments"]

    email = email.strip().lower()

    result = enrollments.update_one(
        {
            "student_email": email,
            "course_id": course_id
        },
        {
            "$set": {"status": status}
        }
    )

    return result.modified_count > 0

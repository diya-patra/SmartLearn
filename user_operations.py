
from database import get_database


def get_user_profile(email):
    db = get_database()
    users = db["users"]

    email = email.strip().lower()

    user = users.find_one(
        {"email": email},
        {"password_hash": 0}
    )

    return user


def update_user_profile(email, profile_data):
    db = get_database()
    users = db["users"]

    email = email.strip().lower()

    allowed_fields = [
        "name",
        "interests",
        "skills",
        "skill_level"
    ]

    update_data = {
        key: value
        for key, value in profile_data.items()
        if key in allowed_fields
    }

    if not update_data:
        return False

    result = users.update_one(
        {"email": email},
        {"$set": update_data}
    )

    return result.modified_count > 0

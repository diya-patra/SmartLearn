
import bcrypt
from database import get_database


def register_user(name, email, password):
    db = get_database()
    users = db["users"]

    users.create_index("email", unique=True)

    email = email.strip().lower()

    if users.find_one({"email": email}):
        return False

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    user = {
        "name": name,
        "email": email,
        "password_hash": password_hash,
        "interests": [],
        "skills": [],
        "skill_level": "Beginner Level"
    }

    try:
        users.insert_one(user)
        return True
    except Exception:
        return False


def login_user(email, password):
    db = get_database()
    users = db["users"]

    email = email.strip().lower()

    user = users.find_one({"email": email})

    if user is None:
        return None

    if bcrypt.checkpw(
        password.encode("utf-8"),
        user["password_hash"]
    ):
        user.pop("password_hash", None)
        return user

    return None

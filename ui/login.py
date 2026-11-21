
import streamlit as st

from auth import register_user, login_user
from user_operations import get_user_profile, update_user_profile


# --------------------------------------------------
# PROFILE OPTIONS
# --------------------------------------------------

INTEREST_OPTIONS = [
    "Web Development",
    "Business Finance",
    "Musical Instruments",
    "Graphic Design"
]

SKILL_OPTIONS = [
    "HTML",
    "CSS",
    "JavaScript",
    "Java",
    "Python",
    "PHP",
    "C",
    "C++",
    "SQL",
    "MongoDB",
    "MySQL",
    "React",
    "Node.js",
    "Machine Learning",
    "Data Analysis",
    "Git and GitHub"
]

LEVEL_OPTIONS = [
    "Beginner Level",
    "Intermediate Level",
    "Expert Level"
]


# --------------------------------------------------
# SESSION MANAGEMENT
# --------------------------------------------------

def save_user_session(user):

    email = user["email"]

    # Fetch the latest profile from MongoDB
    profile = get_user_profile(email)

    if profile is None:
        profile = user

    st.session_state["logged_in"] = True
    st.session_state["user"] = profile
    st.session_state["user_email"] = email
    st.session_state["student_name"] = profile.get(
        "name", "Student"
    )

    st.session_state["student_profile"] = {
        "interests": profile.get("interests", []),
        "skills": profile.get("skills", []),
        "skill_level": profile.get(
            "skill_level", "Beginner Level"
        )
    }

    st.session_state["profile_skipped"] = False


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------

def logout_user():

    keys = [
        "logged_in",
        "user",
        "user_email",
        "student_name",
        "student_profile",
        "smartlearn_recommendations",
        "profile_skipped"
    ]

    for key in keys:
        st.session_state.pop(key, None)

    st.success("You have been logged out successfully.")
    st.rerun()


# --------------------------------------------------
# LEARNING PROFILE FORM
# --------------------------------------------------

def learning_profile_form():

    email = st.session_state.get("user_email")

    saved_profile = st.session_state.get(
        "student_profile", {}
    )

    with st.form("learning_profile_form"):

        st.subheader("Complete Your Learning Profile")

        st.write(
            "Tell us about your learning interests and existing "
            "skills so SmartLearn can recommend relevant courses."
        )

        interests = st.multiselect(
            "What subjects interest you?",
            options=INTEREST_OPTIONS,
            default=[
                item for item in saved_profile.get("interests", [])
                if item in INTEREST_OPTIONS
            ],
            help="You can select more than one subject."
        )

        skills = st.multiselect(
            "Which skills do you already have?",
            options=SKILL_OPTIONS,
            default=[
                item for item in saved_profile.get("skills", [])
                if item in SKILL_OPTIONS
            ],
            help="Select the skills you already know."
        )

        skill_level = st.selectbox(
            "What is your current skill level?",
            options=LEVEL_OPTIONS,
            index=(
                LEVEL_OPTIONS.index(saved_profile["skill_level"])
                if saved_profile.get("skill_level") in LEVEL_OPTIONS
                else 0
            )
        )

        submitted = st.form_submit_button(
            "Save Learning Profile",
            use_container_width=True
        )

        if submitted:

            if not interests:
                st.warning(
                    "Please select at least one learning interest."
                )

            elif not skills:
                st.warning(
                    "Please select at least one existing skill."
                )

            else:

                profile_data = {
                    "interests": interests,
                    "skills": skills,
                    "skill_level": skill_level
                }

                try:
                    updated = update_user_profile(
                        email,
                        profile_data
                    )

                    # Verify the saved profile, including when
                    # the submitted values were already unchanged.
                    saved = get_user_profile(email)

                    if (
                        saved
                        and saved.get("interests") == interests
                        and saved.get("skills") == skills
                        and saved.get("skill_level") == skill_level
                    ):

                        st.session_state["student_profile"] = profile_data
                        st.session_state["user"] = saved
                        st.session_state["profile_skipped"] = False

                        st.success(
                            "Your learning profile has been saved!"
                        )
                        st.rerun()

                    else:
                        st.error(
                            "Unable to save your learning profile. "
                            "Please try again."
                        )

                except Exception as error:
                    st.error("Unable to update your learning profile.")
                    st.exception(error)


# --------------------------------------------------
# PROFILE SECTION
# --------------------------------------------------

def render_learning_profile():

    profile = st.session_state.get(
        "student_profile", {}
    )

    interests = profile.get("interests", [])
    skills = profile.get("skills", [])

    is_complete = bool(interests and skills)

    if not is_complete:

        if not st.session_state.get("profile_skipped", False):

            st.warning(
                "Your learning profile is incomplete. "
                "Complete it to receive personalised recommendations."
            )

            learning_profile_form()

            if st.button("Skip for now"):
                st.session_state["profile_skipped"] = True
                st.rerun()

        else:

            st.info(
                "You haven't completed your learning profile yet. "
                "Your recommendations may not be personalised."
            )

            with st.expander("Complete your learning profile"):
                learning_profile_form()

    else:

        st.success("Your learning profile is complete.")

        with st.expander("View or edit your learning profile"):
            learning_profile_form()


# --------------------------------------------------
# LOGIN FORM
# --------------------------------------------------

def login_form():

    with st.form("login_form"):

        st.subheader("Welcome Back!")

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        submitted = st.form_submit_button(
            "Login",
            use_container_width=True
        )

        if submitted:

            if not email.strip() or not password:
                st.warning(
                    "Please enter both email and password."
                )

            else:
                try:
                    user = login_user(email, password)

                    if user:
                        save_user_session(user)
                        st.success("Login successful!")
                        st.rerun()

                    else:
                        st.error("Invalid email or password.")

                except Exception:
                    st.error(
                        "Unable to log in. Please check your "
                        "database connection and try again."
                    )


# --------------------------------------------------
# REGISTRATION FORM
# --------------------------------------------------

def registration_form():

    with st.form("registration_form"):

        st.subheader("Create Your Account")

        name = st.text_input(
            "Full Name",
            placeholder="Enter your full name"
        )

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password"
        )

        submitted = st.form_submit_button(
            "Create Account",
            use_container_width=True
        )

        if submitted:

            if not name.strip() or not email.strip() or not password:
                st.warning("Please complete all fields.")

            elif "@" not in email or "." not in email:
                st.warning("Please enter a valid email address.")

            elif password != confirm_password:
                st.error("Passwords do not match.")

            else:
                try:
                    registered = register_user(
                        name.strip(),
                        email.strip(),
                        password
                    )

                    if registered:
                        st.success(
                            "Account created successfully! "
                            "Please log in to complete your learning profile."
                        )

                    else:
                        st.error(
                            "Registration failed. This email may "
                            "already be registered."
                        )

                except Exception:
                    st.error(
                        "Unable to create your account. "
                        "Please check your database connection."
                    )


# --------------------------------------------------
# MAIN LOGIN PAGE
# --------------------------------------------------

def render():

    st.title("SmartLearn")
    st.subheader("Your Learning Journey Starts Here")

    st.write(
        "Sign in to access your learning dashboard, "
        "discover courses and receive intelligent recommendations."
    )

    # Already logged in
    if st.session_state.get("logged_in", False):

        name = st.session_state.get(
            "student_name", "Student"
        )

        st.success(f"Welcome, {name}!")

        render_learning_profile()

        st.divider()

        if st.button("Logout", use_container_width=True):
            logout_user()

        return

    # Login and registration
    login_tab, register_tab = st.tabs(
        ["Login", "Create Account"]
    )

    with login_tab:
        login_form()

    with register_tab:
        registration_form()

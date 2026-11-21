
import streamlit as st
from auth import register_user, login_user


# --------------------------------------------------
# SESSION MANAGEMENT
# --------------------------------------------------

def save_user_session(user):

    st.session_state["logged_in"] = True
    st.session_state["user"] = user
    st.session_state["user_email"] = user["email"]
    st.session_state["student_name"] = user.get("name", "Student")

    # Make the saved profile available to the recommendation page
    st.session_state["student_profile"] = {
        "interests": user.get("interests", []),
        "skills": user.get("skills", []),
        "skill_level": user.get("skill_level", "Beginner Level")
    }


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
        "smartlearn_recommendations"
    ]

    for key in keys:
        st.session_state.pop(key, None)

    st.success("You have been logged out successfully.")
    st.rerun()


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
                st.warning("Please enter both email and password.")

            else:
                try:
                    user = login_user(email, password)

                    if user:
                        save_user_session(user)
                        st.success("Login successful!")
                        st.rerun()

                    else:
                        st.error("Invalid email or password.")

                except Exception as error:
                    st.error(
                        f"Unable to log in. Please check your database connection. Details: {error}"
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
                            "Please go to the Login tab to sign in."
                        )

                    else:
                        st.error(
                            "Registration failed. This email may already "
                            "be registered."
                        )

                except Exception as error:
                    st.error(
                        f"Unable to create account. "
                        f"Please check your database connection. Details: {error}"
                    )


# --------------------------------------------------
# MAIN LOGIN PAGE
# --------------------------------------------------

def render():

    st.title("SmartLearn")
    st.subheader("Your Learning Journey Starts Here")

    st.write(
        "Sign in to access your personalised learning experience, "
        "discover courses and receive intelligent recommendations."
    )

    # If a student is already logged in
    if st.session_state.get("logged_in", False):

        name = st.session_state.get("student_name", "Student")

        st.success(f"Welcome, {name}!")

        st.write("You are currently logged in.")

        if st.button("Logout", use_container_width=True):
            logout_user()

        return

    # Login and registration tabs
    login_tab, register_tab = st.tabs(
        ["Login", "Create Account"]
    )

    with login_tab:
        login_form()

    with register_tab:
        registration_form()

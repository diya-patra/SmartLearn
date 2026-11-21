
import streamlit as st

from user_operations import get_user_profile
from course_operations import (
    get_student_enrollments,
    get_course_by_id,
    update_learning_status
)


def render():
    # Check whether a student is logged in
    if not st.session_state.get("logged_in", False):
        st.title("Student Dashboard")
        st.info("Please log in to access your student dashboard.")
        return

    email = st.session_state.get("user_email")

    if not email:
        st.warning("Your login session could not be identified. Please log in again.")
        return

    st.title("Student Dashboard")
    st.write("View your learning profile and manage your enrolled courses.")

    try:
        # Fetch the latest profile and enrolments from MongoDB
        user = get_user_profile(email)

        if not user:
            st.error("Unable to find your student profile.")
            return

        enrollments = get_student_enrollments(email)

        name = user.get("name", "Student")
        interests = user.get("interests", [])
        skills = user.get("skills", [])
        skill_level = user.get("skill_level", "Not specified")

        st.header(f"Welcome, {name}!")

        # Overview
        total_courses = len(enrollments)
        completed_courses = sum(
            1 for item in enrollments
            if item.get("status") == "Completed"
        )
        in_progress_courses = sum(
            1 for item in enrollments
            if item.get("status") == "In Progress"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Enrolled Courses", total_courses)
        col2.metric("In Progress", in_progress_courses)
        col3.metric("Completed", completed_courses)

        # Learning profile
        st.divider()
        st.subheader("My Learning Profile")

        st.write("**Learning Interests**")
        if interests:
            st.write(", ".join(interests))
        else:
            st.info("No interests added yet.")

        st.write("**Skills**")
        if skills:
            st.write(", ".join(skills))
        else:
            st.info("No skills added yet.")

        st.write("**Skill Level:**", skill_level)

        st.caption("You can update your learning information from the profile section.")

        # Enrolled courses
        st.divider()
        st.subheader("My Enrolled Courses")

        if not enrollments:
            st.info(
                "You haven't enrolled in any courses yet. "
                "Explore the course catalogue to get started."
            )
            return

        for index, enrollment in enumerate(enrollments):
            course_id = enrollment.get("course_id")
            course = get_course_by_id(course_id)

            with st.container(border=True):
                if course:
                    course_name = course.get(
                        "course_title",
                        course.get("title", "Course")
                    )
                    subject = course.get("subject", "General")
                    level = course.get("level", "Not specified")
                else:
                    course_name = f"Course ID: {course_id}"
                    subject = "Course details unavailable"
                    level = "Not specified"

                current_status = enrollment.get("status", "Enrolled")

                st.markdown(f"**{course_name}**")
                st.caption(f"{subject} · {level}")

                status_options = [
                    "Enrolled",
                    "In Progress",
                    "Completed"
                ]

                selected_status = st.selectbox(
                    "Learning Status",
                    status_options,
                    index=(
                        status_options.index(current_status)
                        if current_status in status_options
                        else 0
                    ),
                    key=f"status_{course_id}_{index}"
                )

                if selected_status != current_status:
                    if st.button(
                        "Update Status",
                        key=f"update_{course_id}_{index}"
                    ):
                        updated = update_learning_status(
                            email,
                            course_id,
                            selected_status
                        )

                        if updated:
                            st.success("Learning status updated!")
                            st.rerun()
                        else:
                            st.error("Unable to update the learning status.")

    except Exception as error:
        st.error("Something went wrong while loading your dashboard.")
        st.caption(f"Details: {error}")

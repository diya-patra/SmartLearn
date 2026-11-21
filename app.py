
import streamlit as st
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="SmartLearn | Learn Today, Lead Tomorrow",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
CSS_PATH = BASE_DIR / "assets" / "style.css"


# --------------------------------------------------
# GLOBAL CSS
# --------------------------------------------------

def load_global_css():
    if CSS_PATH.exists():
        css = CSS_PATH.read_text(encoding="utf-8")
        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True
        )


def hide_sidebar():
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }

            [data-testid="collapsedControl"] {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# PAGE ROUTING
# --------------------------------------------------

VALID_PAGES = [
    "Home",
    "Course Catalogue",
    "Recommendations",
    "Student Dashboard",
    "Admin Dashboard",
    "Login",
    "About",
    "Features",
    "Contact",
    "Demo"
]


def get_current_page():
    page = st.query_params.get("page", "Home")

    if page not in VALID_PAGES:
        page = "Home"

    return page


# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------

def render_navigation(current_page):

    pages = [
        "Home",
        "Course Catalogue",
        "Recommendations",
        "Student Dashboard",
        "Admin Dashboard",
        "Login"
    ]

    selected_page = st.radio(
        "Navigation",
        pages,
        index=pages.index(current_page)
        if current_page in pages else 0,
        horizontal=True,
        label_visibility="collapsed",
        key="main_navigation"
    )

    if selected_page != current_page:
        st.query_params["page"] = selected_page
        st.rerun()


# --------------------------------------------------
# RENDER SELECTED PAGE
# --------------------------------------------------

def render_page(page):

    if page == "Home":
        from ui.home import render
        render()

    elif page == "Course Catalogue":
        from ui.course_catalogue import render
        render()

    elif page == "Recommendations":
        from ui.recommendations import render
        render()

    elif page == "Student Dashboard":
        from ui.student_dashboard import render
        render()

    elif page == "Admin Dashboard":
        from ui.admin_dashboard import render
        render()

    elif page == "Login":
        st.title("Student Login")
        st.info("Login and registration will be connected in the next integration step.")

    else:
        st.title(page)
        st.info(f"The {page} page is currently under development.")

        if st.button("Back to Home"):
            st.query_params["page"] = "Home"
            st.rerun()


# --------------------------------------------------
# MAIN APPLICATION
# --------------------------------------------------

def main():

    load_global_css()
    hide_sidebar()

    current_page = get_current_page()

    render_navigation(current_page)

    render_page(current_page)


if __name__ == "__main__":
    main()

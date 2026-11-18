
import streamlit as st
from pathlib import Path
from html import escape

# =====================================================
# PAGE CONFIGURATION
# Must be the first Streamlit command
# =====================================================

st.set_page_config(
    page_title="SmartLearn | Learn Today, Lead Tomorrow",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =====================================================
# PROJECT PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent
CSS_PATH = BASE_DIR / "assets" / "style.css"


# =====================================================
# LOAD GLOBAL CSS
# =====================================================

def load_global_css():

    if not CSS_PATH.exists():
        st.error(f"CSS file not found: {CSS_PATH}")
        st.stop()

    css = CSS_PATH.read_text(encoding="utf-8")

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )


# =====================================================
# HIDE STREAMLIT SIDEBAR
# =====================================================

def hide_sidebar():

    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none !important;
        }

        [data-testid="collapsedControl"] {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)


# =====================================================
# AVAILABLE PAGES
# =====================================================

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


# =====================================================
# GET CURRENT PAGE
# =====================================================

def get_current_page():

    page = st.query_params.get("page", "Home")

    if page not in VALID_PAGES:
        page = "Home"

    st.session_state["smartlearn_page"] = page

    return page


# =====================================================
# PAGE ROUTING
# =====================================================

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

        from ui.login import render
        render()

    else:

        st.html(f"""
            <div class="smartlearn-placeholder">
                <h1>{escape(page)}</h1>
                <p>This section is coming soon.</p>
                <a href="?page=Home">← Back to Home</a>
            </div>
        """)


# =====================================================
# MAIN APPLICATION
# =====================================================

def main():

    # Load global styles
    load_global_css()

    # Hide sidebar
    hide_sidebar()

    # Get selected page
    current_page = get_current_page()

    # Render the SAME Home-style navigation
    from ui.navigation import render_navigation

    render_navigation(current_page)

    # Render selected page
    render_page(current_page)


# =====================================================
# RUN APPLICATION
# =====================================================

if __name__ == "__main__":
    main()

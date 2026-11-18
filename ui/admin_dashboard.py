
import streamlit as st
from pathlib import Path
import base64
import mimetypes


# =====================================================
# 1. PROJECT PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

IMAGE_PATH = BASE_DIR / "assets" / "admin_background.png"


# =====================================================
# 2. LOAD BACKGROUND IMAGE
# =====================================================

def get_background():

    if not IMAGE_PATH.exists():
        return None

    image_data = base64.b64encode(
        IMAGE_PATH.read_bytes()
    ).decode("utf-8")

    mime_type = (
        mimetypes.guess_type(str(IMAGE_PATH))[0]
        or "image/png"
    )

    return f"data:{mime_type};base64,{image_data}"


# =====================================================
# 3. LOAD ADMIN CSS
# =====================================================

def load_admin_css():

    background_image = get_background()

    if background_image:

        background_css = f"""
            linear-gradient(
                90deg,
                rgba(8, 7, 5, 0.76),
                rgba(12, 10, 7, 0.65),
                rgba(8, 7, 5, 0.80)
            ),
            url("{background_image}")
        """

    else:

        background_css = """
            linear-gradient(
                135deg,
                #080706,
                #21180e,
                #080706
            )
        """

        st.warning(
            f"Background image not found: {IMAGE_PATH}"
        )

    st.markdown(
        f"""
        <style>

        /* =========================================
           GLOBAL BACKGROUND
        ========================================= */

        .stApp {{
            background: #080706 !important;
        }}

        [data-testid="stAppViewContainer"] {{

            background-image: {background_css} !important;

            background-size: cover !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        }}

        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"],
        .main {{
            background: transparent !important;
        }}

        header[data-testid="stHeader"] {{
            background: transparent !important;
        }}

        section[data-testid="stSidebar"],
        [data-testid="collapsedControl"] {{
            display: none !important;
        }}


        /* =========================================
           OUTER DASHBOARD PANEL
        ========================================= */

        .st-key-admin_page {{

            background: rgba(22, 16, 11, 0.78) !important;

            border: 1px solid rgba(255, 202, 66, 0.55);
            border-radius: 28px;

            padding: 32px 38px 40px;

            margin: 25px auto 45px;

            width: 94%;

            box-shadow:
                0 15px 50px rgba(0, 0, 0, 0.40),
                0 0 30px rgba(255, 202, 66, 0.07);

            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
        }}


        /* =========================================
           HEADER
        ========================================= */

        .admin-eyebrow {{
            color: #ffca42;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }}

        .admin-heading {{
            color: #ffffff;
            font-size: 38px;
            font-weight: 850;
            margin: 0;
        }}

        .admin-heading span {{
            color: #ffca42;
        }}

        .admin-subtitle {{
            color: #d1c7b9;
            font-size: 14px;
            line-height: 1.7;
            margin-top: 10px;
            margin-bottom: 25px;
        }}


        /* =========================================
           SECTION HEADINGS
        ========================================= */

        .admin-section-heading {{
            color: #ffca42;
            font-size: 22px;
            font-weight: 800;
            margin: 28px 0 16px;
        }}

        .admin-section-description {{
            color: #cfc4b4;
            font-size: 13px;
            line-height: 1.7;
            margin-bottom: 20px;
        }}


        /* =========================================
           STATISTICS CARDS
        ========================================= */

        .admin-card {{

            background: linear-gradient(
                145deg,
                rgba(43, 32, 19, 0.96),
                rgba(20, 17, 13, 0.98)
            );

            border: 1px solid rgba(255, 202, 66, 0.38);
            border-radius: 18px;

            padding: 22px;
            min-height: 145px;

            box-shadow:
                0 8px 25px rgba(0, 0, 0, 0.20);

            transition: all 0.3s ease;
        }}

        .admin-card:hover {{
            border-color: #ffca42;
            transform: translateY(-4px);

            box-shadow:
                0 12px 28px rgba(255, 202, 66, 0.10);
        }}

        .admin-card-label {{
            color: #d1c7b9;
            font-size: 13px;
            font-weight: 600;
        }}

        .admin-card-value {{
            color: #ffca42;
            font-size: 32px;
            font-weight: 850;
            margin-top: 15px;
        }}


        /* =========================================
           MANAGEMENT CARDS
        ========================================= */

        .admin-management-card {{

            background: linear-gradient(
                145deg,
                rgba(43, 32, 19, 0.94),
                rgba(20, 17, 13, 0.98)
            );

            border: 1px solid rgba(255, 202, 66, 0.32);
            border-radius: 18px;

            padding: 23px;
            min-height: 185px;

            box-shadow:
                0 8px 25px rgba(0, 0, 0, 0.18);

            transition: all 0.3s ease;
        }}

        .admin-management-card:hover {{
            border-color: #ffca42;
            transform: translateY(-3px);
        }}

        .admin-management-icon {{
            font-size: 28px;
            margin-bottom: 13px;
        }}

        .admin-management-card h3 {{
            color: #ffca42;
            font-size: 18px;
            margin: 0 0 10px;
        }}

        .admin-management-card p {{
            color: #d0c6b8;
            font-size: 13px;
            line-height: 1.7;
            margin: 0;
        }}


        /* =========================================
           BUTTONS
        ========================================= */

        .st-key-admin_page div[data-testid="stButton"] > button {{

            width: 100%;

            background: linear-gradient(
                135deg,
                #ffca42,
                #e9a91e
            ) !important;

            color: #171009 !important;

            border: 1px solid #ffca42 !important;
            border-radius: 10px !important;

            padding: 11px 18px !important;

            font-weight: 800 !important;

            transition: all 0.25s ease !important;
        }}

        .st-key-admin_page div[data-testid="stButton"] > button:hover {{

            background: #ffffff !important;
            color: #171009 !important;

            border-color: #ffffff !important;

            transform: translateY(-2px);

            box-shadow:
                0 6px 20px rgba(255, 202, 66, 0.25);
        }}

        .st-key-admin_page div[data-testid="stButton"] > button:focus {{
            box-shadow: 0 0 0 2px #ffca42 !important;
        }}


        /* =========================================
           SELECTED MANAGEMENT SECTION
        ========================================= */

        .admin-selected-panel {{

            background: rgba(255, 202, 66, 0.08);

            border: 1px solid rgba(255, 202, 66, 0.45);
            border-radius: 16px;

            padding: 22px;
            margin-top: 25px;
        }}

        .admin-selected-panel h3 {{
            color: #ffca42;
            font-size: 20px;
            margin-bottom: 10px;
        }}

        .admin-selected-panel p {{
            color: #e0d7ca;
            font-size: 14px;
            line-height: 1.7;
        }}


        /* =========================================
           DIVIDER AND FOOTER
        ========================================= */

        .st-key-admin_page hr {{
            border-color: rgba(255, 202, 66, 0.25);
        }}

        .admin-footer {{
            color: #a99e8d;
            font-size: 12px;
            text-align: center;
            padding-top: 20px;
        }}


        /* =========================================
           RESPONSIVE DESIGN
        ========================================= */

        @media screen and (max-width: 768px) {{

            .st-key-admin_page {{
                width: 96%;
                padding: 22px 16px 30px;
                border-radius: 20px;
            }}

            .admin-heading {{
                font-size: 29px;
            }}

            .admin-card {{
                min-height: 120px;
                padding: 17px;
            }}

            .admin-card-value {{
                font-size: 26px;
            }}

            .admin-management-card {{
                min-height: 155px;
                padding: 18px;
            }}

        }}

        </style>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# 4. MANAGEMENT SECTION CONTENT
# =====================================================

def render_selected_section():

    selected_section = st.session_state.get(
        "admin_section"
    )

    section_details = {

        "Student Management": (
            "👨‍🎓",
            "Student Management",
            "This section will allow administrators to view "
            "student profiles, manage student accounts and "
            "monitor learner activity."
        ),

        "Course Management": (
            "📚",
            "Course Management",
            "This section will allow administrators to add, "
            "update, remove and organise learning courses."
        ),

        "Reports & Analytics": (
            "📊",
            "Reports & Analytics",
            "This section will display student performance, "
            "course completion statistics and platform reports."
        ),

        "Platform Settings": (
            "🔧",
            "Platform Settings",
            "This section will contain administrative settings "
            "and platform configuration options."
        )
    }

    if selected_section in section_details:

        icon, title, description = section_details[
            selected_section
        ]

        st.html(f"""
        <div class="admin-selected-panel">

            <h3>{icon} {title}</h3>

            <p>{description}</p>

            <p>
                <strong>Status:</strong>
                Frontend module selected. Database and
                management functionality can be connected next.
            </p>

        </div>
        """)

        if st.button(
            "← Back to Dashboard",
            key="back_to_admin_dashboard"
        ):
            st.session_state.pop("admin_section", None)
            st.rerun()


# =====================================================
# 5. ADMIN DASHBOARD
# =====================================================

def render():

    load_admin_css()

    with st.container(key="admin_page"):

        # =============================================
        # HEADER
        # =============================================

        st.html("""
        <div class="admin-header">

            <div class="admin-eyebrow">
                SMARTLEARN • ADMINISTRATION
            </div>

            <h1 class="admin-heading">
                Admin <span>Dashboard</span> ⚙️
            </h1>

            <p class="admin-subtitle">
                Manage SmartLearn and monitor platform activity
                from one centralised dashboard.
            </p>

        </div>
        """)

        st.markdown("---")

        # =============================================
        # PLATFORM STATISTICS
        # =============================================

        st.html("""
        <div class="admin-section-heading">
            📊 Platform Overview
        </div>
        """)

        statistics = [
            ("Total Students", "0", "👨‍🎓"),
            ("Total Courses", "0", "📚"),
            ("Active Enrollments", "0", "📝"),
            ("Completed Courses", "0", "🏆")
        ]

        columns = st.columns(4)

        for column, (label, value, icon) in zip(
            columns,
            statistics
        ):

            with column:

                st.html(f"""
                <div class="admin-card">

                    <div class="admin-card-label">
                        {icon} {label}
                    </div>

                    <div class="admin-card-value">
                        {value}
                    </div>

                </div>
                """)

        # =============================================
        # PLATFORM MANAGEMENT
        # =============================================

        st.html("""
        <div class="admin-section-heading">
            ⚙️ Platform Management
        </div>

        <p class="admin-section-description">
            Access different management areas of your
            SmartLearn platform.
        </p>
        """)

        # ROW 1

        col1, col2 = st.columns(2)

        with col1:

            st.html("""
            <div class="admin-management-card">

                <div class="admin-management-icon">
                    👨‍🎓
                </div>

                <h3>Student Management</h3>

                <p>
                    Manage student accounts, view learner profiles
                    and monitor learning activity.
                </p>

            </div>
            """)

            if st.button(
                "Manage Students",
                key="manage_students",
                use_container_width=True
            ):

                st.session_state["admin_section"] = (
                    "Student Management"
                )

        with col2:

            st.html("""
            <div class="admin-management-card">

                <div class="admin-management-icon">
                    📚
                </div>

                <h3>Course Management</h3>

                <p>
                    Organise courses, update course information
                    and manage available learning resources.
                </p>

            </div>
            """)

            if st.button(
                "Manage Courses",
                key="manage_courses",
                use_container_width=True
            ):

                st.session_state["admin_section"] = (
                    "Course Management"
                )

        st.markdown("")

        # ROW 2

        col3, col4 = st.columns(2)

        with col3:

            st.html("""
            <div class="admin-management-card">

                <div class="admin-management-icon">
                    📊
                </div>

                <h3>Reports & Analytics</h3>

                <p>
                    Monitor platform performance and review
                    student learning statistics.
                </p>

            </div>
            """)

            if st.button(
                "View Reports",
                key="view_reports",
                use_container_width=True
            ):

                st.session_state["admin_section"] = (
                    "Reports & Analytics"
                )

        with col4:

            st.html("""
            <div class="admin-management-card">

                <div class="admin-management-icon">
                    🔧
                </div>

                <h3>Platform Settings</h3>

                <p>
                    Manage platform configuration and
                    administrative preferences.
                </p>

            </div>
            """)

            if st.button(
                "Settings",
                key="admin_settings",
                use_container_width=True
            ):

                st.session_state["admin_section"] = (
                    "Platform Settings"
                )

        # =============================================
        # SELECTED SECTION
        # =============================================

        render_selected_section()

        # =============================================
        # FOOTER
        # =============================================

        st.markdown("---")

        st.html("""
        <div class="admin-footer">
            SmartLearn Admin Dashboard • Frontend Version
        </div>
        """)


# =====================================================
# 6. DIRECT EXECUTION
# =====================================================

if __name__ == "__main__":

    st.set_page_config(
        page_title="SmartLearn | Admin Dashboard",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    render()

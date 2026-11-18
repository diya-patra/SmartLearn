
import streamlit as st
from pathlib import Path
from textwrap import dedent
from html import escape
import base64


# =========================================================
# 1. PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CSS_PATH = BASE_DIR / "assets" / "style.css"
BACKGROUND_PATH = BASE_DIR / "assets" / "login_background.png"


# =========================================================
# 2. LOAD CSS AND BACKGROUND
# =========================================================

def load_catalogue_css():

    if CSS_PATH.exists():

        css = CSS_PATH.read_text(encoding="utf-8")

        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True
        )

    if BACKGROUND_PATH.exists():

        image_data = base64.b64encode(
            BACKGROUND_PATH.read_bytes()
        ).decode("utf-8")

        background_css = f"""
        <style>

        [data-testid="stAppViewContainer"] {{
            background-image:
                linear-gradient(
                    90deg,
                    rgba(8, 5, 3, 0.88),
                    rgba(20, 10, 5, 0.58),
                    rgba(8, 5, 3, 0.78)
                ),
                url("data:image/png;base64,{image_data}") !important;

            background-size: cover !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;

            min-height: 100vh;
        }}

        [data-testid="stHeader"],
        [data-testid="stMain"] {{
            background: transparent !important;
        }}

        section[data-testid="stSidebar"],
        [data-testid="collapsedControl"] {{
            display: none !important;
        }}

        </style>
        """

        st.markdown(
            background_css,
            unsafe_allow_html=True
        )

    else:

        st.warning(
            f"Background image not found: {BACKGROUND_PATH}"
        )


# =========================================================
# 3. COURSE CATALOGUE STYLES
# =========================================================

def load_catalogue_page_styles():

    st.markdown("""
    <style>

    /* =========================================
       LARGE OUTER CATALOGUE PANEL
    ========================================= */

    .st-key-catalogue_page {

        background: rgba(22, 16, 11, 0.78);

        border: 1px solid rgba(255, 202, 66, 0.55);
        border-radius: 28px;

        padding: 35px 38px 40px 38px;

        margin: 25px auto 45px auto;

        width: 94%;

        box-shadow:
            0 15px 50px rgba(0, 0, 0, 0.40),
            0 0 30px rgba(255, 202, 66, 0.07);

        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
    }


    /* =========================================
       PAGE HEADER
    ========================================= */

    .catalogue-heading {
        color: #ffca42;
        font-size: 40px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 8px;
    }

    .catalogue-subtitle {
        color: #e0d5c5;
        font-size: 15px;
        line-height: 1.7;
        margin-bottom: 25px;
    }


    /* =========================================
       SMALL INNER FILTER PANEL
    ========================================= */

    .st-key-catalogue_filters {

        background: rgba(10, 8, 6, 0.72);

        border: 1px solid rgba(255, 202, 66, 0.30);
        border-radius: 18px;

        padding: 22px 22px 12px 22px;

        margin: 12px 0 25px 0;

        box-shadow:
            inset 0 0 18px rgba(255, 202, 66, 0.025);
    }


    /* =========================================
       SECTION HEADING
    ========================================= */

    .catalogue-section-title {
        color: #ffffff;
        font-size: 25px;
        font-weight: 750;
        margin: 28px 0 20px 0;
    }

    .catalogue-count {
        color: #ffca42;
        font-size: 20px;
    }


    /* =========================================
       COURSE CARDS
    ========================================= */

    .catalogue-card {
        background: linear-gradient(
            145deg,
            rgba(40, 29, 16, 0.97),
            rgba(25, 19, 12, 0.97) 65%,
            rgba(16, 13, 9, 0.98)
        );

        border: 1px solid rgba(255, 202, 66, 0.28);
        border-radius: 18px;

        padding: 24px;
        min-height: 280px;

        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);

        transition: all 0.3s ease;
        margin-bottom: 8px;
    }

    .catalogue-card:hover {
        border-color: #ffca42;
        transform: translateY(-5px);

        box-shadow:
            0 12px 28px rgba(255, 202, 66, 0.13);
    }


    /* =========================================
       COURSE ICON
    ========================================= */

    .catalogue-icon {
        width: 58px;
        height: 58px;

        display: flex;
        align-items: center;
        justify-content: center;

        background: rgba(255, 202, 66, 0.12);
        border: 1px solid rgba(255, 202, 66, 0.25);

        border-radius: 15px;
        font-size: 30px;

        margin-bottom: 20px;
    }


    /* =========================================
       COURSE TITLE
    ========================================= */

    .catalogue-card h3 {
        color: #ffca42;
        font-size: 21px;
        font-weight: 750;

        margin: 0 0 12px 0;
    }


    /* =========================================
       COURSE DESCRIPTION
    ========================================= */

    .catalogue-card p {
        color: #ded6ca;
        font-size: 14px;
        line-height: 1.7;

        min-height: 75px;
        margin: 0 0 20px 0;
    }


    /* =========================================
       COURSE TAGS
    ========================================= */

    .catalogue-tag {
        display: inline-block;

        color: #ffcf55;
        background: rgba(255, 202, 66, 0.10);

        border: 1px solid rgba(255, 202, 66, 0.25);
        border-radius: 20px;

        padding: 7px 11px;

        font-size: 10px;
        font-weight: 750;
        letter-spacing: 0.6px;
    }


    /* =========================================
       SEARCH AND FILTER LABELS
    ========================================= */

    .st-key-catalogue_page label {
        color: #f4e9d5 !important;
        font-weight: 600 !important;
    }


    /* =========================================
       SEARCH INPUT
    ========================================= */

    .st-key-catalogue_page input {
        background-color: #1c1711 !important;
        color: #ffffff !important;

        border: 1px solid #60491f !important;
        border-radius: 10px !important;
    }

    .st-key-catalogue_page input::placeholder {
        color: #a99c88 !important;
    }


    /* =========================================
       DROPDOWN
    ========================================= */

    .st-key-catalogue_page [data-baseweb="select"] > div {
        background-color: #1c1711 !important;
        color: #ffffff !important;

        border: 1px solid #60491f !important;
        border-radius: 10px !important;
    }

    .st-key-catalogue_page [data-baseweb="select"] span {
        color: #ffffff !important;
    }


    /* =========================================
       BUTTONS
    ========================================= */

    .st-key-catalogue_page .stButton > button {
        background: linear-gradient(
            135deg,
            #ffca42,
            #e8a91c
        );

        color: #171008 !important;
        border: none !important;
        border-radius: 10px !important;

        min-height: 43px;
        font-weight: 750;

        transition: all 0.2s ease;
    }

    .st-key-catalogue_page .stButton > button:hover {
        background: #ffdf78 !important;
        color: #100b05 !important;

        box-shadow:
            0 5px 18px rgba(255, 202, 66, 0.18);
    }

    .st-key-catalogue_page .stButton > button:disabled {
        background: #493b22 !important;
        color: #d4bd83 !important;
        opacity: 1 !important;
    }


    /* =========================================
       RECOMMENDATION PANEL
    ========================================= */

    .catalogue-recommendation {
        background: linear-gradient(
            110deg,
            rgba(40, 29, 16, 0.97),
            rgba(23, 18, 12, 0.97)
        );

        border: 1px solid #634a20;
        border-radius: 18px;

        padding: 28px;
        margin-top: 15px;

        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }

    .catalogue-recommendation h3 {
        color: #ffca42;
        font-size: 22px;
        font-weight: 750;
        margin: 0 0 12px 0;
    }

    .catalogue-recommendation p {
        color: #ded6ca;
        font-size: 14px;
        line-height: 1.8;
        margin: 0;
    }


    /* =========================================
       DIVIDER
    ========================================= */

    .st-key-catalogue_page hr {
        border-color: rgba(255, 202, 66, 0.25);
    }


    /* =========================================
       ALERT
    ========================================= */

    .st-key-catalogue_page [data-testid="stAlert"] {
        background: rgba(40, 29, 16, 0.9);
        border: 1px solid rgba(255, 202, 66, 0.3);
        color: #ffffff;
        border-radius: 12px;
    }


    /* =========================================
       RESPONSIVE DESIGN
    ========================================= */

    @media screen and (max-width: 768px) {

        .st-key-catalogue_page {
            width: 96%;
            padding: 22px 16px 30px 16px;
            margin-top: 15px;
            border-radius: 20px;
        }

        .st-key-catalogue_filters {
            padding: 15px 12px 8px 12px;
        }

        .catalogue-heading {
            font-size: 29px;
        }

        .catalogue-subtitle {
            font-size: 14px;
        }

        .catalogue-card {
            min-height: 240px;
        }

        .catalogue-recommendation {
            padding: 20px;
        }

    }

    </style>
    """, unsafe_allow_html=True)


# =========================================================
# 4. COURSE DATA
# =========================================================

courses = [

    {
        "title": "Python Programming",
        "category": "Programming",
        "level": "Beginner",
        "icon": "🐍",
        "description": (
            "Learn Python fundamentals, variables, loops, "
            "functions and build your programming foundation."
        )
    },

    {
        "title": "Machine Learning",
        "category": "Data Science",
        "level": "Intermediate",
        "icon": "🤖",
        "description": (
            "Discover machine learning algorithms, model training "
            "and real-world AI applications."
        )
    },

    {
        "title": "Web Development",
        "category": "Web Development",
        "level": "Beginner",
        "icon": "💻",
        "description": (
            "Master HTML, CSS and JavaScript to design "
            "and develop modern websites."
        )
    },

    {
        "title": "Data Science",
        "category": "Data Science",
        "level": "Advanced",
        "icon": "📊",
        "description": (
            "Explore data analysis, visualization, statistics "
            "and predictive modelling."
        )
    },

    {
        "title": "Business Management",
        "category": "Business",
        "level": "Beginner",
        "icon": "📈",
        "description": (
            "Understand business strategy, leadership "
            "and essential management principles."
        )
    },

    {
        "title": "Advanced Python",
        "category": "Programming",
        "level": "Advanced",
        "icon": "⚙️",
        "description": (
            "Strengthen your Python skills with object-oriented "
            "programming and advanced concepts."
        )
    }

]


# =========================================================
# 5. COURSE CARD HTML
# =========================================================

def create_course_card(course):

    title = escape(str(course["title"]))
    icon = escape(str(course["icon"]))
    description = escape(str(course["description"]))
    category = escape(str(course["category"]).upper())
    level = escape(str(course["level"]).upper())

    return dedent(f"""
        <div class="catalogue-card">

            <div class="catalogue-icon">
                {icon}
            </div>

            <h3>{title}</h3>

            <p>{description}</p>

            <span class="catalogue-tag">
                {category}
                &nbsp; • &nbsp;
                {level}
            </span>

        </div>
    """)


# =========================================================
# 6. MAIN RENDER FUNCTION
# =========================================================

def render():

    load_catalogue_css()
    load_catalogue_page_styles()

    # LARGE OUTER PANEL
    with st.container(key="catalogue_page"):

        # =============================================
        # PAGE HEADER
        # =============================================

        st.html("""
            <div class="catalogue-heading">
                Explore Courses 📚
            </div>

            <div class="catalogue-subtitle">
                Discover courses, develop new skills, and build your future.
            </div>
        """)

        # =============================================
        # SMALL INNER FILTER PANEL
        # =============================================

        with st.container(key="catalogue_filters"):

            search_col, category_col, level_col = st.columns(
                [2.2, 1, 1],
                gap="medium"
            )

            with search_col:

                search = st.text_input(
                    "Search Courses",
                    placeholder="Search by course name...",
                    key="catalogue_search"
                )

            with category_col:

                category = st.selectbox(
                    "Category",
                    [
                        "All Categories",
                        "Programming",
                        "Data Science",
                        "Web Development",
                        "Business"
                    ],
                    key="catalogue_category"
                )

            with level_col:

                level = st.selectbox(
                    "Difficulty",
                    [
                        "All Levels",
                        "Beginner",
                        "Intermediate",
                        "Advanced"
                    ],
                    key="catalogue_level"
                )

        st.markdown("---")

        # =============================================
        # FILTER COURSES
        # =============================================

        filtered_courses = []

        search_text = search.strip().lower()

        for course in courses:

            matches_search = (
                search_text in course["title"].lower()
                or search_text in course["description"].lower()
                or search_text in course["category"].lower()
            )

            matches_category = (
                category == "All Categories"
                or course["category"] == category
            )

            matches_level = (
                level == "All Levels"
                or course["level"] == level
            )

            if (
                matches_search
                and matches_category
                and matches_level
            ):
                filtered_courses.append(course)

        # =============================================
        # COURSE COUNT
        # =============================================

        st.html(f"""
            <div class="catalogue-section-title">
                Available Courses
                <span class="catalogue-count">
                    ({len(filtered_courses)})
                </span>
            </div>
        """)

        # =============================================
        # DISPLAY COURSE CARDS
        # =============================================

        if not filtered_courses:

            st.info(
                "No courses found. Try changing your search or filters."
            )

        else:

            columns = st.columns(3, gap="medium")

            for index, course in enumerate(filtered_courses):

                with columns[index % 3]:

                    st.html(create_course_card(course))

                    st.button(
                        "Explore Course →",
                        key=f"explore_course_{index}",
                        use_container_width=True,
                        disabled=True
                    )

        # =============================================
        # AI RECOMMENDATION SECTION
        # =============================================

        st.markdown("---")

        st.html("""
            <div class="catalogue-recommendation">

                <h3>
                    Need help choosing a course? 🎯
                </h3>

                <p>
                    Discover courses that match your interests, skills
                    and learning level with SmartLearn's AI recommendation
                    system.
                </p>

            </div>
        """)

        st.write("")

        if st.button(
            "View My Recommendations →",
            key="view_recommendations",
            type="primary"
        ):

            st.query_params["page"] = "Recommendations"
            st.rerun()

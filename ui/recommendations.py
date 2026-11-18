
import streamlit as st
from html import escape
from pathlib import Path
import base64
import mimetypes


# =====================================================
# 1. PROJECT PATHS
# =====================================================

ROOT = Path(__file__).resolve().parent.parent

IMAGE_PATH = ROOT / "assets" / "reco.png"


# =====================================================
# 2. LOAD CSS AND BACKGROUND
# =====================================================

def load_recommendation_css():

    # ---------------------------------------------
    # Load background image
    # ---------------------------------------------

    if IMAGE_PATH.is_file():

        image_data = base64.b64encode(
            IMAGE_PATH.read_bytes()
        ).decode("utf-8")

        mime_type = (
            mimetypes.guess_type(str(IMAGE_PATH))[0]
            or "image/png"
        )

        background_css = f"""
            linear-gradient(
                90deg,
                rgba(8, 7, 5, 0.48),
                rgba(12, 10, 7, 0.38),
                rgba(8, 7, 5, 0.52)
            ),
            url("data:{mime_type};base64,{image_data}")
        """

    else:

        background_css = """
            linear-gradient(
                135deg,
                #080706,
                #241a0e,
                #080706
            )
        """

        st.warning(
            f"Recommendation background image not found: {IMAGE_PATH}"
        )

    # ---------------------------------------------
    # Global CSS
    # ---------------------------------------------

    st.markdown(f"""
    <style>

    /* =========================================
       GLOBAL PAGE BACKGROUND
    ========================================= */

    html,
    body {{
        background: #080706 !important;
    }}

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
    [data-testid="stMainBlockContainer"] {{
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
       OUTER GLASS PANEL
    ========================================= */

    .st-key-recommendation_page {{

        background: rgba(22, 16, 11, 0.72) !important;

        border: 1px solid rgba(255, 202, 66, 0.55);
        border-radius: 28px;

        padding: 30px 38px 40px;

        margin: 25px auto 45px;

        width: 94%;

        box-shadow:
            0 15px 50px rgba(0, 0, 0, 0.40),
            0 0 30px rgba(255, 202, 66, 0.07);

        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
    }}


    /* =========================================
       PAGE HEADER
    ========================================= */

    .recommend-header {{
        padding: 15px 5px 22px;
    }}

    .recommend-eyebrow {{
        color: #ffca42;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 10px;
    }}

    .recommend-title {{
        color: #ffffff;
        font-size: 38px;
        font-weight: 800;
        margin: 0;
    }}

    .recommend-description {{
        color: #e0d8cc;
        font-size: 15px;
        margin-top: 10px;
        line-height: 1.7;
    }}


    /* =========================================
       HERO PANEL
    ========================================= */

    .recommend-hero {{

        background: linear-gradient(
            110deg,
            rgba(80, 49, 10, 0.85),
            rgba(32, 23, 12, 0.95)
        );

        border: 1px solid rgba(255, 202, 66, 0.5);
        border-radius: 20px;

        padding: 28px;
        margin: 10px 0 28px;
    }}

    .recommend-hero h2 {{
        color: #ffca42;
        font-size: 27px;
        margin: 0 0 10px;
    }}

    .recommend-hero p {{
        color: #ffffff;
        font-size: 14px;
        line-height: 1.7;
        margin: 0;
    }}


    /* =========================================
       INNER PROFILE PANEL
    ========================================= */

    .st-key-recommendation_preferences {{

        background: rgba(10, 8, 6, 0.72);

        border: 1px solid rgba(255, 202, 66, 0.35);
        border-radius: 20px;

        padding: 22px 25px 25px;

        margin: 10px 0 30px;

        box-shadow:
            inset 0 0 18px rgba(255, 202, 66, 0.025);
    }}


    /* =========================================
       SECTION HEADINGS
    ========================================= */

    .section-heading {{
        color: #ffca42;
        font-size: 21px;
        font-weight: 800;
        margin: 20px 0 15px;
    }}


    /* =========================================
       PROFILE FORM
    ========================================= */

    div[data-testid="stForm"] {{

        background: rgba(25, 19, 12, 0.88);

        border: 1px solid rgba(255, 202, 66, 0.35);
        border-radius: 16px;

        padding: 22px;
    }}

    div[data-testid="stForm"] label {{
        color: #ffffff !important;
    }}

    .st-key-recommendation_page
    div[data-testid="stTextInput"] input,

    .st-key-recommendation_page
    div[data-testid="stSelectbox"]
    div[data-baseweb="select"] > div {{

        background: #1c1711 !important;
        color: #ffffff !important;

        border: 1px solid #76551f !important;
        border-radius: 9px !important;
    }}

    .st-key-recommendation_page
    input::placeholder {{
        color: #a99c88 !important;
    }}


    /* =========================================
       FORM SUBMIT BUTTON
    ========================================= */

    .st-key-recommendation_page
    div[data-testid="stFormSubmitButton"] button {{

        background: linear-gradient(
            135deg,
            #ffca42,
            #e8a91c
        ) !important;

        color: #171008 !important;

        border: none !important;
        border-radius: 10px !important;

        font-weight: 750 !important;
        min-height: 45px;

        transition: all 0.2s ease;
    }}

    .st-key-recommendation_page
    div[data-testid="stFormSubmitButton"] button:hover {{

        background: #ffdf78 !important;

        box-shadow:
            0 5px 18px rgba(255, 202, 66, 0.18);

        transform: translateY(-2px);
    }}


    /* =========================================
       RECOMMENDATION CARDS
    ========================================= */

    .recommend-card {{

        background: linear-gradient(
            145deg,
            rgba(43, 32, 19, 0.96),
            rgba(20, 17, 13, 0.98)
        );

        border: 1px solid rgba(255, 202, 66, 0.38);
        border-radius: 18px;

        padding: 24px;
        margin: 10px 0 18px;

        min-height: 190px;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.20);

        transition: all 0.3s ease;
    }}

    .recommend-card:hover {{

        border-color: #ffca42;

        box-shadow:
            0 12px 28px rgba(255, 202, 66, 0.10);

        transform: translateY(-2px);
    }}

    .recommend-number {{
        color: #ffca42;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 2px;
    }}

    .recommend-card h3 {{
        color: #ffffff;
        font-size: 21px;
        margin: 10px 0;
    }}

    .recommend-subject {{
        color: #ffca42;
        font-size: 12px;
        font-weight: 600;
    }}

    .recommend-level {{

        display: inline-block;

        background: rgba(255, 202, 66, 0.12);
        border: 1px solid rgba(255, 202, 66, 0.35);

        color: #ffdc82;

        padding: 5px 12px;
        border-radius: 20px;

        font-size: 11px;
        margin-top: 10px;
    }}

    .recommend-score {{
        color: #ffca42;
        font-size: 29px;
        font-weight: 800;
        text-align: right;
    }}

    .recommend-score-label {{
        color: #bcb4a7;
        font-size: 11px;
        text-align: right;
    }}


    /* =========================================
       MATCH SCORE BARS
    ========================================= */

    .score-label {{
        color: #ffffff;
        font-size: 12px;
        margin-top: 12px;
    }}

    .score-track {{
        height: 7px;
        background: #40382d;
        border-radius: 20px;
        overflow: hidden;
        margin-top: 6px;
    }}

    .score-fill {{

        height: 7px;

        background: linear-gradient(
            90deg,
            #ff9d24,
            #ffda55
        );

        border-radius: 20px;
    }}


    /* =========================================
       COURSE LINKS
    ========================================= */

    .st-key-recommendation_page
    .stLinkButton a {{

        background: linear-gradient(
            135deg,
            #ffca42,
            #e8a91c
        ) !important;

        color: #171008 !important;

        border: none !important;
        border-radius: 10px !important;

        font-weight: 750;
    }}

    .st-key-recommendation_page
    .stLinkButton a:hover {{
        background: #ffdf78 !important;
    }}


    /* =========================================
       DIVIDERS AND CAPTIONS
    ========================================= */

    .st-key-recommendation_page hr {{
        border-color: rgba(255, 202, 66, 0.25);
    }}

    .st-key-recommendation_page
    [data-testid="stCaptionContainer"] {{
        color: #cfc4b4 !important;
    }}


    /* =========================================
       ALERTS
    ========================================= */

    .st-key-recommendation_page
    [data-testid="stAlert"] {{

        background: rgba(40, 29, 16, 0.9);

        border: 1px solid rgba(255, 202, 66, 0.3);

        color: #ffffff;
        border-radius: 12px;
    }}


    /* =========================================
       RESPONSIVE DESIGN
    ========================================= */

    @media screen and (max-width: 768px) {{

        .st-key-recommendation_page {{
            width: 96%;
            padding: 22px 16px 30px;
            margin-top: 15px;
            border-radius: 20px;
        }}

        .st-key-recommendation_preferences {{
            padding: 15px 12px 18px;
        }}

        .recommend-header {{
            padding: 10px 3px 18px;
        }}

        .recommend-title {{
            font-size: 29px;
        }}

        .recommend-description {{
            font-size: 14px;
        }}

        .recommend-hero {{
            padding: 20px;
        }}

        .recommend-hero h2 {{
            font-size: 22px;
        }}

        .recommend-card {{
            padding: 18px;
        }}

    }}

    </style>
    """, unsafe_allow_html=True)


# =====================================================
# 3. HELPER FUNCTIONS
# =====================================================

def convert_to_list(value):

    if value is None:
        return []

    if isinstance(value, list):

        return [
            str(item).strip()
            for item in value
            if str(item).strip()
        ]

    if isinstance(value, str):

        return [
            item.strip()
            for item in value.split(",")
            if item.strip()
        ]

    return []


def safe_score(value):

    try:

        score = float(value)

        # Support both decimal scores and percentages
        if 0 <= score <= 1:
            score *= 100

        return max(0, min(100, round(score)))

    except (TypeError, ValueError):
        return 0


def get_saved_profile():

    profile = st.session_state.get(
        "student_profile",
        {}
    )

    if not isinstance(profile, dict):
        profile = {}

    return profile


# =====================================================
# 4. RECOMMENDATION CARD
# =====================================================

def display_course(course, index):

    title = escape(
        str(course.get("course_title", "Untitled Course"))
    )

    subject = escape(
        str(course.get("subject", "General"))
    )

    level = escape(
        str(course.get("level", "Not specified"))
    )

    final_score = safe_score(
        course.get("similarity_score", 0)
    )

    interest_score = safe_score(
        course.get("interest_score", 0)
    )

    skill_score = safe_score(
        course.get("skill_score", 0)
    )

    level_score = safe_score(
        course.get("level_score", 0)
    )

    card_html = f"""
    <div class="recommend-card">

        <div class="recommend-number">
            RECOMMENDATION #{index:02d}
        </div>

        <div style="
            display:flex;
            justify-content:space-between;
            gap:15px;
        ">

            <div style="flex:1;">

                <h3>{title}</h3>

                <div class="recommend-subject">
                    {subject}
                </div>

                <span class="recommend-level">
                    {level}
                </span>

            </div>

            <div>

                <div class="recommend-score">
                    {final_score}%
                </div>

                <div class="recommend-score-label">
                    Match score
                </div>

            </div>

        </div>

        <div class="score-label">
            Interest Match — {interest_score}%
        </div>

        <div class="score-track">
            <div class="score-fill"
                 style="width:{interest_score}%">
            </div>
        </div>

        <div class="score-label">
            Skill Match — {skill_score}%
        </div>

        <div class="score-track">
            <div class="score-fill"
                 style="width:{skill_score}%">
            </div>
        </div>

        <div class="score-label">
            Learning Level Match — {level_score}%
        </div>

        <div class="score-track">
            <div class="score-fill"
                 style="width:{level_score}%">
            </div>
        </div>

    </div>
    """

    st.html(card_html)

    # ---------------------------------------------
    # Course URL
    # ---------------------------------------------

    course_url = (
        course.get("course_url")
        or course.get("url")
        or course.get("link")
    )

    if (
        isinstance(course_url, str)
        and course_url.startswith(("https://", "http://"))
    ):

        st.link_button(
            "Explore Course ↗",
            course_url,
            use_container_width=True
        )


# =====================================================
# 5. MAIN RECOMMENDATION PAGE
# =====================================================

def render():

    load_recommendation_css()

    with st.container(key="recommendation_page"):

        # =============================================
        # PAGE HEADER
        # =============================================

        st.html("""
        <div class="recommend-header">

            <div class="recommend-eyebrow">
                SMARTLEARN • INTELLIGENT LEARNING
            </div>

            <h1 class="recommend-title">
                Recommended For You ✨
            </h1>

            <p class="recommend-description">
                Discover courses selected according to your interests,
                existing skills and learning level.
            </p>

        </div>
        """)

        # =============================================
        # HERO PANEL
        # =============================================

        st.html("""
        <div class="recommend-hero">

            <h2>
                Your next learning opportunity starts here.
            </h2>

            <p>
                SmartLearn analyses your learning preferences and
                identifies courses that may suit your goals.
            </p>

        </div>
        """)

        # =============================================
        # GET SAVED PROFILE
        # =============================================

        saved_profile = get_saved_profile()

        saved_interests = convert_to_list(
            saved_profile.get("interests", [])
        )

        saved_skills = convert_to_list(
            saved_profile.get("skills", [])
        )

        saved_level = saved_profile.get(
            "skill_level",
            "Beginner Level"
        )

        # =============================================
        # INNER PROFILE PANEL
        # =============================================

        with st.container(key="recommendation_preferences"):

            st.html("""
            <div class="section-heading">
                🎯 Your Learning Preferences
            </div>
            """)

            # =========================================
            # PROFILE FORM
            # =========================================

            with st.form("recommendation_profile_form"):

                interests = st.text_input(
                    "Your interests",
                    value=", ".join(saved_interests),
                    placeholder=(
                        "Example: Machine Learning, Web Development"
                    )
                )

                skills = st.text_input(
                    "Your existing skills",
                    value=", ".join(saved_skills),
                    placeholder=(
                        "Example: Python, HTML, CSS, Java"
                    )
                )

                levels = [
                    "Beginner Level",
                    "Intermediate Level",
                    "Expert Level"
                ]

                selected_index = (
                    levels.index(saved_level)
                    if saved_level in levels
                    else 0
                )

                skill_level = st.selectbox(
                    "Your learning level",
                    levels,
                    index=selected_index
                )

                generate = st.form_submit_button(
                    "✨ Generate My Recommendations",
                    use_container_width=True
                )

        # =============================================
        # GENERATE RECOMMENDATIONS
        # =============================================

        if generate:

            student_profile = {
                "interests": convert_to_list(interests),
                "skills": convert_to_list(skills),
                "skill_level": skill_level
            }

            if not (
                student_profile["interests"]
                or student_profile["skills"]
            ):

                st.warning(
                    "Please enter at least one interest or skill."
                )

            else:

                st.session_state["student_profile"] = (
                    student_profile
                )

                try:

                    from recommender import recommend_courses

                    with st.spinner(
                        "Analysing your profile and finding suitable courses..."
                    ):

                        recommendations = recommend_courses(
                            student_profile,
                            top_n=8
                        )

                    if (
                        recommendations is None
                        or not hasattr(recommendations, "empty")
                        or recommendations.empty
                    ):

                        st.warning(
                            "No recommendations were found. "
                            "Try adding more interests or skills."
                        )

                        st.session_state.pop(
                            "smartlearn_recommendations",
                            None
                        )

                    else:

                        st.session_state[
                            "smartlearn_recommendations"
                        ] = recommendations

                        st.success(
                            f"{len(recommendations)} recommendations generated!"
                        )

                except FileNotFoundError:

                    st.error(
                        "The trained ML model files could not be found. "
                        "Please check your ml_model folder."
                    )

                except ImportError:

                    st.error(
                        "Could not import recommender.py. "
                        "Make sure it is in your project root folder."
                    )

                except Exception as error:

                    st.error(
                        f"Recommendation error: {error}"
                    )

        # =============================================
        # DISPLAY RECOMMENDATION RESULTS
        # =============================================

        recommendations = st.session_state.get(
            "smartlearn_recommendations"
        )

        if recommendations is not None:

            if (
                hasattr(recommendations, "empty")
                and not recommendations.empty
            ):

                st.html("""
                <div class="section-heading">
                    ⭐ Your Personalised Course Matches
                </div>
                """)

                st.caption(
                    "Courses are ranked using the recommendation "
                    "model's similarity scores."
                )

                for index, (_, course) in enumerate(
                    recommendations.iterrows(),
                    start=1
                ):

                    display_course(
                        course.to_dict(),
                        index
                    )

                st.markdown("---")

                st.caption(
                    "Recommendations are generated by SmartLearn's "
                    "machine learning recommendation system."
                )


# =====================================================
# 6. DIRECT EXECUTION
# =====================================================

if __name__ == "__main__":

    st.set_page_config(
        page_title="SmartLearn | Recommendations",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    render()

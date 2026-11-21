
import streamlit as st
from pathlib import Path
from textwrap import dedent
import base64


# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

CSS_PATH = BASE_DIR / "assets" / "style.css"

BACKGROUND_PATH = BASE_DIR / "assets" / "login_background.png"


# ==========================================
# LOAD CSS
# ==========================================

def load_login_css():

    if CSS_PATH.exists():

        css = CSS_PATH.read_text(encoding="utf-8")

        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True
        )

    else:
        st.error("CSS file not found: assets/style.css")


# ==========================================
# LOAD LOGIN BACKGROUND IMAGE
# ==========================================

def load_login_background():

    if not BACKGROUND_PATH.exists():

        st.error(
            f"Background image not found: {BACKGROUND_PATH}"
        )
        return

    image_data = base64.b64encode(
        BACKGROUND_PATH.read_bytes()
    ).decode("utf-8")

    st.markdown(
        f"""
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

        [data-testid="stHeader"] {{
            background: transparent !important;
        }}

        [data-testid="stMain"] {{
            background: transparent !important;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# LOGIN PAGE
# ==========================================

def render():

    load_login_css()
    load_login_background()

    # --------------------------------------
    # SMARTLEARN BRAND
    # --------------------------------------

    st.html(dedent("""
        <div class="login-brand">
            <div class="login-brand-icon">🎓</div>
            <div>Smart<span>Learn</span></div>
        </div>
    """))

    # --------------------------------------
    # TWO-COLUMN LAYOUT
    # --------------------------------------

    left, right = st.columns(
        [1.25, 1],
        gap="large"
    )

    # ======================================
    # LEFT SIDE - WELCOME SECTION
    # ======================================

    with left:

        st.html(dedent("""
            <div class="login-welcome">

                <h1>
                    Welcome <span>Back!</span>
                </h1>

                <p class="login-subtitle">
                    Continue your learning journey<br>
                    with <strong>SmartLearn.</strong>
                </p>

                <div class="login-line"></div>

                <p class="login-quote">
                    “Learn today,<br>
                    Lead tomorrow.”
                </p>

                <div class="login-features">

                    <div class="login-feature">
                        <span>▤</span>
                        <p>Expert-Led<br>Courses</p>
                    </div>

                    <div class="login-feature">
                        <span>▷</span>
                        <p>Interactive<br>Learning</p>
                    </div>

                    <div class="login-feature">
                        <span>▥</span>
                        <p>Track Your<br>Progress</p>
                    </div>

                </div>

            </div>
        """))

    # ======================================
    # RIGHT SIDE - LOGIN CARD
    # ======================================

    with right:

        st.html(dedent("""
            <div class="login-card-heading">
                <h2>
                    Login to <span>SmartLearn</span>
                </h2>

                <p>Your knowledge. Our mission.</p>
            </div>
        """))

        # ----------------------------------
        # LOGIN FORM
        # ----------------------------------

        with st.form("smartlearn_login_form"):

            email = st.text_input(
                "Email Address",
                placeholder="✉  Email Address",
                label_visibility="collapsed"
            )

            password = st.text_input(
                "Password",
                placeholder="🔒  Password",
                type="password",
                label_visibility="collapsed"
            )

            remember_col, forgot_col = st.columns(
                [1, 1]
            )

            with remember_col:

                remember = st.checkbox(
                    "Remember Me"
                )

            with forgot_col:

                st.html("""
                    <div class="forgot-link">
                        <a href="?page=ForgotPassword">
                            Forgot Password?
                        </a>
                    </div>
                """)

            submitted = st.form_submit_button(
                "Login  →",
                use_container_width=True
            )

            # ----------------------------------
            # FORM VALIDATION
            # ----------------------------------

            if submitted:

                if not email.strip() or not password:

                    st.error(
                        "Please enter your email address "
                        "and password."
                    )

                else:

                    st.info(
                        "Login form submitted. Authentication "
                        "will be connected when the backend "
                        "is integrated."
                    )

        # ----------------------------------
        # OR DIVIDER
        # ----------------------------------

        st.html("""
            <div class="login-divider">
                <span></span>
                OR
                <span></span>
            </div>
        """)

        # ----------------------------------
        # GOOGLE LOGIN
        # ----------------------------------

        if st.button(
            "🌐  Continue with Google",
            key="google_login",
            use_container_width=True
        ):

            st.info(
                "Google authentication will be integrated later."
            )

        # ----------------------------------
        # SIGN UP
        # ----------------------------------

        st.html("""
            <div class="login-signup">
                Don't have an account?
                <a href="?page=SignUp">Sign Up</a>
            </div>
        """)

    # ======================================
    # BACK TO HOME
    # ======================================

    st.html("""
        <div class="login-back">
            <a href="?page=Home">
                ← Back to Home
            </a>
        </div>
    """)


# ==========================================
# RUN LOGIN PAGE DIRECTLY
# ==========================================

if __name__ == "__main__":

    st.set_page_config(
        page_title="Login | SmartLearn",
        page_icon="🎓",
        layout="wide"
    )

    render()


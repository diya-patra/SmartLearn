
import streamlit as st
from pathlib import Path
import base64

# =====================================================
# PROJECT PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_PATH = BASE_DIR / "assets" / "hero_background.png"


# =====================================================
# LOAD HOMEPAGE BACKGROUND
# =====================================================

def get_background_image():

    if not IMAGE_PATH.exists():
        st.error(f"Hero image not found: {IMAGE_PATH}")
        st.stop()

    image_data = base64.b64encode(
        IMAGE_PATH.read_bytes()
    ).decode("utf-8")

    return f"data:image/png;base64,{image_data}"


# =====================================================
# HOMEPAGE
# =====================================================

def render_home():

    background_image = get_background_image()

    html = f"""
    <div class="smartlearn-page">

        <section class="smartlearn-hero"
        style="--hero-image: url('{background_image}');">

            <!-- HERO CONTENT -->

            <main class="smartlearn-content">

                <h1 class="smartlearn-title">
                    Smart<span>Learn</span>
                </h1>

                <h2 class="smartlearn-tagline">
                    Learn Today,<br>
                    Lead <span>Tomorrow.</span>
                </h2>

                <p class="smartlearn-description">
                    Your personalized learning platform<br>
                    for a smarter, brighter future.
                </p>

                <div class="smartlearn-actions">

                    <a href="?page=Course%20Catalogue"
                       class="explore-button">
                        Explore Courses <span>→</span>
                    </a>

                    <a href="?page=Demo"
                       class="demo-button">
                        <span class="play-icon">▶</span>
                        Watch Demo
                    </a>

                </div>

            </main>

            <!-- FEATURES -->

            <div class="smartlearn-features">

                <div class="smartlearn-feature">
                    <div class="feature-icon">♧</div>
                    <div class="feature-text">
                        Expert-Led<br>Courses
                    </div>
                </div>

                <div class="smartlearn-feature">
                    <div class="feature-icon">▣</div>
                    <div class="feature-text">
                        Flexible<br>Learning
                    </div>
                </div>

                <div class="smartlearn-feature">
                    <div class="feature-icon">▥</div>
                    <div class="feature-text">
                        Track Your<br>Progress
                    </div>
                </div>

                <div class="smartlearn-feature">
                    <div class="feature-icon">♜</div>
                    <div class="feature-text">
                        Achieve Your<br>Goals
                    </div>
                </div>

            </div>

        </section>

    </div>
    """

    st.html(html)


# =====================================================
# APP COMPATIBILITY
# =====================================================

def render():
    render_home()


# =====================================================
# DIRECT EXECUTION
# =====================================================

if __name__ == "__main__":

    st.set_page_config(
        page_title="SmartLearn | Learn Today, Lead Tomorrow",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    css_path = BASE_DIR / "assets" / "style.css"

    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True
        )

    from ui.navigation import render_navigation

    render_navigation("Home")
    render_home()

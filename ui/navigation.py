
import streamlit as st


def render_navigation(current_page="Home"):

    pages = [
        ("Home", "Home"),
        ("Courses", "Course Catalogue"),
        ("Recommendations", "Recommendations"),
        ("Student Dashboard", "Student Dashboard"),
        ("Admin Dashboard", "Admin Dashboard"),
        ("Contact", "Contact"),
    ]

    navigation_links = ""

    for label, page in pages:

        active_class = "active" if current_page == page else ""
        page_url = page.replace(" ", "%20")

        navigation_links += f"""
            <a href="?page={page_url}" class="{active_class}">
                {label}
            </a>
        """

    login_active = "active" if current_page == "Login" else ""

    navigation_html = f"""
    <header class="smartlearn-navbar">

        <a href="?page=Home" class="smartlearn-brand">

            <svg class="brand-icon"
                 viewBox="0 0 100 80"
                 fill="none"
                 xmlns="http://www.w3.org/2000/svg">

                <path d="M8 24 L50 5 L92 24 L50 43 Z"
                      fill="#FFCA42"/>

                <path d="M25 35 L25 49
                         C25 49 39 43 50 52
                         C61 43 75 49 75 49
                         L75 35"
                      stroke="#FFCA42"
                      stroke-width="5"
                      stroke-linejoin="round"/>

                <path d="M18 51 L18 62
                         C29 57 40 57 50 68
                         C60 57 71 57 82 62
                         L82 51"
                      stroke="#FFFFFF"
                      stroke-width="4"
                      stroke-linejoin="round"/>

                <path d="M12 70 Q50 78 88 70"
                      stroke="#FFCA42"
                      stroke-width="4"
                      stroke-linecap="round"/>

            </svg>

            <div>Smart<span>Learn</span></div>

        </a>

        <nav class="smartlearn-navlinks">

            {navigation_links}

            <a href="?page=Login"
               class="login-link {login_active}">
                <span>♟</span> Login
            </a>

        </nav>

    </header>
    """

    st.html(navigation_html)

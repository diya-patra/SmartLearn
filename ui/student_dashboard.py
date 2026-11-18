import streamlit as st
import sqlite3
import os

# =========================================================
# DATABASE CONNECTION
# =========================================================

DB_PATH = os.getenv("SMARTLEARN_DB", "smartlearn.db")


def get_db_connection():
    return sqlite3.connect(DB_PATH)


# =========================================================
# GET LOGGED-IN STUDENT
# =========================================================

def get_logged_in_student():

    student_id = (
        st.session_state.get("student_id")
        or st.session_state.get("user_id")
    )

    student_name = (
        st.session_state.get("student_name")
        or st.session_state.get("username")
        or "Student"
    )

    # Check session dictionary
    if "student" in st.session_state:
        student = st.session_state["student"]

        if isinstance(student, dict):
            student_id = student.get("id", student_id)
            student_name = student.get("name", student_name)

    if "logged_in_user" in st.session_state:
        user = st.session_state["logged_in_user"]

        if isinstance(user, dict):
            student_id = user.get("id", student_id)
            student_name = user.get("name", student_name)

    return student_id, student_name


# =========================================================
# LOAD STUDENT DATA
# =========================================================

def load_student_data(student_id):

    data = {
        "courses": [],
        "enrolled_courses": 0,
        "completed_courses": 0,
        "learning_time": "0h 0m",
        "average_score": 0,
        "completion": 0,
        "classes": [],
        "quizzes": 0,
        "assignments": 0,
    }

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        # -------------------------------------------------
        # ENROLLED COURSES
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                courses.course_name,
                enrollments.progress,
                enrollments.status
            FROM enrollments
            JOIN courses
            ON enrollments.course_id = courses.id
            WHERE enrollments.student_id = ?
        """, (student_id,))

        courses = cursor.fetchall()

        data["courses"] = courses
        data["enrolled_courses"] = len(courses)

        completed = 0
        total_progress = 0

        for course in courses:

            course_name = course[0]
            progress = course[1] or 0
            status = course[2] or ""

            total_progress += progress

            if progress >= 100 or status.lower() == "completed":
                completed += 1

        data["completed_courses"] = completed

        if courses:
            data["completion"] = int(
                total_progress / len(courses)
            )

        # -------------------------------------------------
        # AVERAGE QUIZ SCORE
        # -------------------------------------------------

        try:

            cursor.execute("""
                SELECT AVG(score)
                FROM quiz_results
                WHERE student_id = ?
            """, (student_id,))

            result = cursor.fetchone()

            if result and result[0] is not None:
                data["average_score"] = round(result[0])

        except sqlite3.Error:
            pass

        # -------------------------------------------------
        # QUIZ COUNT
        # -------------------------------------------------

        try:

            cursor.execute("""
                SELECT COUNT(*)
                FROM quiz_results
                WHERE student_id = ?
            """, (student_id,))

            data["quizzes"] = cursor.fetchone()[0]

        except sqlite3.Error:
            pass

        # -------------------------------------------------
        # ASSIGNMENT COUNT
        # -------------------------------------------------

        try:

            cursor.execute("""
                SELECT COUNT(*)
                FROM assignments
                WHERE student_id = ?
            """, (student_id,))

            data["assignments"] = cursor.fetchone()[0]

        except sqlite3.Error:
            pass

        # -------------------------------------------------
        # LEARNING TIME
        # -------------------------------------------------

        try:

            cursor.execute("""
                SELECT SUM(minutes)
                FROM learning_sessions
                WHERE student_id = ?
            """, (student_id,))

            result = cursor.fetchone()

            if result and result[0]:

                total_minutes = int(result[0])

                hours = total_minutes // 60
                minutes = total_minutes % 60

                data["learning_time"] = (
                    f"{hours}h {minutes}m"
                )

        except sqlite3.Error:
            pass

        # -------------------------------------------------
        # UPCOMING CLASSES
        # -------------------------------------------------

        try:

            cursor.execute("""
                SELECT course_name, class_date, start_time, end_time
                FROM classes
                WHERE student_id = ?
                ORDER BY class_date
                LIMIT 5
            """, (student_id,))

            data["classes"] = cursor.fetchall()

        except sqlite3.Error:
            pass

        conn.close()

    except sqlite3.Error as error:

        st.warning(
            f"Database connection issue: {error}"
        )

    return data


# =========================================================
# DASHBOARD CSS
# =========================================================

def dashboard_css():

    st.markdown("""
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
        radial-gradient(
            circle at 20% 80%,
            #291906 0%,
            #100c07 45%,
            #080706 100%
        );

        color: white;
    }

    [data-testid="stSidebar"] {
        background:
        linear-gradient(
            180deg,
            #17120b,
            #241707
        );

        border-right: 1px solid #735017;
    }

    [data-testid="stSidebar"] * {
        color: #f5e7bd;
    }

    .block-container {
        padding-top: 1.5rem;
        max-width: 1600px;
    }

    /* HERO */

    .hero {
        background:
        linear-gradient(
            90deg,
            rgba(20, 10, 2, 0.95),
            rgba(20, 10, 2, 0.40)
        ),
        url("assets/hero_background.png");

        background-size: cover;
        background-position: center;

        border: 1px solid #6c4b17;
        border-radius: 22px;

        padding: 35px;

        min-height: 250px;

        box-shadow:
        0 0 30px rgba(255, 180, 0, 0.08);
    }

    .hero h1 {
        font-size: 42px;
        font-weight: 800;
        color: white;
    }

    .hero p {
        font-size: 20px;
        color: #f5eee4;
    }

    .gold {
        color: #ffce32;
    }

    /* STATISTICS */

    .stat-card {
        background:
        linear-gradient(
            145deg,
            #2b1c0d,
            #17110a
        );

        border: 1px solid #65471d;
        border-radius: 18px;

        padding: 18px;

        min-height: 90px;
    }

    .stat-number {
        font-size: 27px;
        font-weight: 800;
        color: white;
    }

    .stat-label {
        font-size: 14px;
        color: #c7c1b7;
    }

    /* COURSES */

    .course-card {
        background: #1d160d;

        border: 1px solid #73501d;
        border-radius: 18px;

        padding: 15px;

        min-height: 230px;
    }

    .course-title {
        font-size: 17px;
        font-weight: 700;
        color: white;
    }

    .course-progress {
        background: #3c3429;
        height: 8px;
        border-radius: 10px;
        overflow: hidden;
    }

    .course-progress-fill {
        background: #ffca2e;
        height: 8px;
        border-radius: 10px;
    }

    /* PANELS */

    .panel {
        background:
        linear-gradient(
            145deg,
            rgba(43, 29, 13, 0.95),
            rgba(18, 13, 8, 0.95)
        );

        border: 1px solid #65471d;
        border-radius: 20px;

        padding: 20px;

        margin-bottom: 15px;
    }

    .schedule-item {
        border-left: 3px solid #ffca2e;
        padding-left: 15px;
        margin-bottom: 18px;
    }

    .small-text {
        color: #c5bdb2;
        font-size: 13px;
    }

    /* BUTTONS */

    div.stButton > button {

        background:
        linear-gradient(
            180deg,
            #573b10,
            #30210c
        );

        border: 1px solid #8b631e;

        color: #ffce32;

        border-radius: 30px;

        font-weight: 700;

        transition: 0.3s;
    }

    div.stButton > button:hover {

        background: #ffca2e;

        color: black;

        border: 1px solid #ffca2e;
    }

    </style>
    """, unsafe_allow_html=True)


# =========================================================
# STUDENT DASHBOARD
# =========================================================

def render_student_dashboard():

    student_id, student_name = get_logged_in_student()

    if student_id is None:

        st.warning(
            "Please log in to access your student dashboard."
        )

        return

    data = load_student_data(student_id)

    dashboard_css()

    # =====================================================
    # SIDEBAR
    # =====================================================

    with st.sidebar:

        st.markdown("""
        <div style="text-align:center;padding:15px">

            <div style="font-size:55px">
                🎓
            </div>

            <h2>
                Smart<span style="color:#ffce32">
                Learn</span>
            </h2>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.button(
            "🏠  Dashboard",
            use_container_width=True
        )

        st.button(
            "📖  My Courses",
            use_container_width=True
        )

        st.button(
            "📋  Assignments",
            use_container_width=True
        )

        st.button(
            "📝  Notes",
            use_container_width=True
        )

        st.button(
            "🏆  Quiz & Tests",
            use_container_width=True
        )

        st.button(
            "📊  Progress",
            use_container_width=True
        )

        st.button(
            "👤  Profile",
            use_container_width=True
        )

        st.button(
            "⚙️  Settings",
            use_container_width=True
        )

        st.markdown("---")

        if st.button(
            "↪  Logout",
            use_container_width=True
        ):

            st.session_state.clear()

            st.rerun()

        st.markdown("""
        <div style="
            background:linear-gradient(135deg,#35220a,#8a570c);
            border:1px solid #8c611c;
            border-radius:20px;
            padding:20px;
            text-align:center;
            margin-top:25px;
        ">

            <div style="font-size:35px">
                🎓
            </div>

            <i>
                Learn Today,<br>
                Lead Tomorrow.
            </i>

        </div>
        """, unsafe_allow_html=True)

    # =====================================================
    # TOP BAR
    # =====================================================

    top_left, top_right = st.columns([5, 1])

    with top_left:

        search = st.text_input(
            "Search",
            placeholder="🔎 Search courses, topics...",
            label_visibility="collapsed"
        )

    with top_right:

        st.markdown(
            f"""
            <div style="text-align:right;padding-top:10px">
                🔔　👤 <b>{student_name}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =====================================================
    # MAIN LAYOUT
    # =====================================================

    main_column, right_column = st.columns(
        [3.5, 1.05],
        gap="medium"
    )

    # =====================================================
    # MAIN DASHBOARD
    # =====================================================

    with main_column:

        # HERO

        st.markdown(
            f"""
            <div class="hero">

                <h1>
                    Welcome Back,
                    <span class="gold">{student_name}!</span> 👋
                </h1>

                <p>
                    Keep learning, keep growing with
                    <b class="gold">SmartLearn.</b>
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.button(
            "Explore Courses  ➜",
            key="explore_courses"
        )

        # -------------------------------------------------
        # STATISTICS
        # -------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        statistics = [
            ("📖", data["enrolled_courses"], "Enrolled Courses"),
            ("✅", data["completed_courses"], "Completed Courses"),
            ("🕒", data["learning_time"], "Learning Time"),
            ("⭐", f'{data["average_score"]}%', "Average Score")
        ]

        for col, statistic in zip(
            [col1, col2, col3, col4],
            statistics
        ):

            icon, number, label = statistic

            with col:

                st.markdown(
                    f"""
                    <div class="stat-card">

                        <div style="font-size:24px">
                            {icon}
                            <span class="stat-number">
                                {number}
                            </span>
                        </div>

                        <div class="stat-label">
                            {label}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # -------------------------------------------------
        # MY COURSES
        # -------------------------------------------------

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="panel">

            <h2>
                📚 My Courses
            </h2>

        </div>
        """, unsafe_allow_html=True)

        courses = data["courses"]

        if search:

            courses = [
                course for course in courses
                if search.lower() in str(course[0]).lower()
            ]

        if not courses:

            st.info(
                "Your enrolled courses will appear here "
                "when your database contains course records."
            )

        else:

            course_columns = st.columns(4)

            for index, course in enumerate(courses):

                course_name = course[0]
                progress = course[1] or 0

                with course_columns[index % 4]:

                    st.markdown(
                        f"""
                        <div class="course-card">

                            <div style="
                                font-size:50px;
                                text-align:center;
                                padding:15px;
                            ">
                                📘
                            </div>

                            <div class="course-title">
                                {course_name}
                            </div>

                            <div class="course-progress">
                                <div class="course-progress-fill"
                                    style="width:{progress}%">
                                </div>
                            </div>

                            <div class="small-text">
                                {progress}% Completed
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.button(
                        "Continue Learning  ➜",
                        key=f"course_{index}",
                        use_container_width=True
                    )

    # =====================================================
    # RIGHT SIDE PANEL
    # =====================================================

    with right_column:

        # -------------------------------------------------
        # UPCOMING CLASSES
        # -------------------------------------------------

        st.markdown("""
        <div class="panel">

            <h3>
                📅 Upcoming Classes
            </h3>

        </div>
        """, unsafe_allow_html=True)

        if data["classes"]:

            for class_data in data["classes"]:

                course, date, start, end = class_data

                st.markdown(
                    f"""
                    <div class="schedule-item">

                        <b>{course}</b>

                        <div class="small-text">
                            {date}
                        </div>

                        <div class="small-text">
                            {start} - {end}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.info(
                "Upcoming classes will appear here."
            )

        # -------------------------------------------------
        # PROGRESS
        # -------------------------------------------------

        st.markdown("""
        <div class="panel">

            <h3>
                📈 Your Progress
            </h3>

        </div>
        """, unsafe_allow_html=True)

        st.progress(
            data["completion"] / 100,
            text=f'{data["completion"]}% Overall Completion'
        )

        st.markdown(
            f"""
            <div style="padding:10px">

                ✅ {data["enrolled_courses"]} Courses<br><br>

                ✅ {data["quizzes"]} Quizzes<br><br>

                ✅ {data["assignments"]} Assignments

            </div>
            """,
            unsafe_allow_html=True
        )

        # -------------------------------------------------
        # MOTIVATIONAL QUOTE
        # -------------------------------------------------

        st.markdown("""
        <div class="panel"
        style="
            background:linear-gradient(135deg,#392207,#a56a10);
            text-align:center;
        ">

            <div style="font-size:35px;color:#ffce32">
                ❝
            </div>

            <i style="font-size:18px">
                Dream big. Learn more.<br>
                Achieve greater.
            </i>

            <div style="font-size:35px;color:#ffce32">
                ♡
            </div>

        </div>
        """, unsafe_allow_html=True)


# =========================================================
# RUN DASHBOARD
# =========================================================

# =========================================================
# APP.PY CONNECTION
# =========================================================

def render():
    render_student_dashboard()


# =========================================================
# RUN DASHBOARD DIRECTLY
# =========================================================

if __name__ == "__main__":
    st.set_page_config(
        page_title="SmartLearn | Student Dashboard",
        page_icon="🎓",
        layout="wide"
    )
    render()
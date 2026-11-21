# SmartLearn – Intelligent Learning Management System

SmartLearn is a web-based Learning Management System (LMS) that helps students discover courses and receive personalised course recommendations based on their learning interests, existing skills, and skill level.

The application combines a course catalogue, student profile management, course enrolment, and a content-based recommendation system to provide a more personalised learning experience.

## Key Features

- **User Registration and Login:** Students can create accounts and securely log in.
- **Student Learning Profile:** Students can add and update their learning interests, skills, and current skill level.
- **Course Catalogue:** Browse, search, and filter courses from the available course collection.
- **Intelligent Course Recommendations:** Receive personalised course suggestions based on the student's profile.
- **Course Enrolment:** Enrol in courses from the catalogue or recommendation results.
- **Student Dashboard:** View learning profile information, enrolled courses, and learning status.
- **Learning Status Management:** Update an enrolled course's status to Enrolled, In Progress, or Completed.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend and Application | Streamlit |
| Programming Language | Python |
| Database | MongoDB Atlas |
| Machine Learning | Scikit-learn |
| Recommendation Technique | TF-IDF and Cosine Similarity |
| Data Processing | Pandas, NumPy |
| Password Security | Bcrypt |
| Model Storage | Joblib |
| Version Control | Git and GitHub |

## Intelligent Course Recommendation System

SmartLearn uses a content-based filtering approach to recommend courses according to a student's learning profile.

### How it works

1. Students provide their learning interests, skills, and skill level.
2. Course information is preprocessed to prepare textual features.
3. TF-IDF (Term Frequency–Inverse Document Frequency) converts course-related text into numerical feature vectors.
4. Cosine similarity measures the similarity between the student's profile and available course content.
5. Additional scoring considers subject relevance, skill relevance, and course-level compatibility.
6. Courses are ranked and presented as personalised recommendations.

The recommendation system uses the following weighted factors:

- Interest relevance: 40%
- Skill relevance: 50%
- Skill-level compatibility: 10%

These weights are used to calculate a recommendation relevance score. The score represents similarity-based relevance and should not be interpreted as a prediction probability or model accuracy.

## Dataset

SmartLearn uses the Udemy Courses dataset available on Kaggle.

**Dataset source:** https://www.kaggle.com/datasets/andrewmvd/udemy-courses

The dataset contains course information such as:

- Course title
- Course subject
- Course level
- Course price
- Number of subscribers
- Number of reviews
- Number of lectures
- Course duration
- Course URL

After preprocessing and duplicate removal, the recommendation dataset contains approximately 3,672 course records.

The recommendation system primarily uses course titles, subjects, and levels. It does not analyse complete course descriptions or syllabi because those fields are not available in the dataset.

## Project Structure

```text
SmartLearn/
│
├── app.py
├── auth.py
├── database.py
├── database_setup.py
├── user_operations.py
├── course_operations.py
│
├── data_preprocessing.py
├── train_model.py
├── recommender.py
├── evaluation.py
│
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── dataset/
│   ├── udemy_courses.csv
│   └── cleaned_courses.csv
│
├── ml_model/
│   ├── tfidf_vectorizer.pkl
│   ├── course_vectors.pkl
│   └── model_courses.csv
│
├── ui/
│   ├── __init__.py
│   ├── home.py
│   ├── login.py
│   ├── navigation.py
│   ├── course_catalogue.py
│   ├── recommendations.py
│   ├── student_dashboard.py
│   └── admin_dashboard.py
│
└── assets/
    ├── style.css
    ├── admin_background.png
    ├── login_background.png
    ├── hero_background.png
    └── reco.png
```

*Note: The structure above describes the intended organisation of the project. Adjust it if the final repository contains additional or differently named files.*

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/diya-patra/SmartLearn.git
cd SmartLearn
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure MongoDB

Create a MongoDB Atlas cluster and configure a database user with the required permissions.

Create a `.env` file in the project root directory and add:

```env
MONGODB_URI=your_mongodb_connection_string
```

Replace the placeholder with your actual MongoDB connection string.

**Important:** Never commit your `.env` file or expose your database credentials publicly.

### 5. Set up the database

Ensure the dataset files are available in the `dataset/` directory.

Run:

```bash
python database_setup.py
```

This imports the course data into MongoDB.

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser, generally at:

```text
http://localhost:8501
```

## Model Preparation

The preprocessing and model-training scripts are included in the repository.

To regenerate the processed dataset:

```bash
python data_preprocessing.py
```

To train the TF-IDF model and generate its supporting files:

```bash
python train_model.py
```

The generated model files are stored in the `ml_model/` directory.

If the existing model artifacts are included in the repository, retraining is not necessary for normal application execution.

## Database Collections

SmartLearn uses MongoDB collections to manage application data:

- **users:** Stores student account details and learning profiles.
- **courses:** Stores the available course catalogue.
- **enrollments:** Stores student course enrolments and learning statuses.

Passwords are hashed using Bcrypt before storage.

## Future Enhancements

Potential improvements include:

- More detailed course metadata and skill tagging.
- Advanced recommendation techniques.
- Detailed learning progress analytics.
- Additional course filtering and discovery options.
- Expanded administrative functionality.

## Project Information

**Project Name:** SmartLearn – Intelligent Learning Management System

**Project Type:** Undergraduate Group Project

**Primary Objective:** To develop a learning management application that provides personalised course recommendations using machine learning techniques.

**Repository:** [MY_GITHUB_REPOSITORY_URL](https://github.com/diya-patra/SmartLearn)

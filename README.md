# MyBlog – Flask Blog Application

## Project Overview
MyBlog is a web-based blogging application developed using Python and Flask. It allows users to register, log in, create blog posts, edit and delete their posts, add comments, search blogs, and filter posts by category.

## Features
- User Registration and Login
- Secure Password Hashing
- Create, Edit and Delete Blog Posts
- Category Management
- Add and Delete Comments
- Search Blogs by Title
- Filter Blogs by Category
- Pagination
- Responsive Frontend Design
- User Authentication

## Technologies Used
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Login
- Flask-WTF
- HTML
- CSS
- SQLite
- Jinja2

## Project Structure
```text
flask_project/
│
├── app/
│   ├── routes/
│   ├── templates/
│   ├── __init__.py
│   ├── models.py
│   └── forms.py
│
├── static/
├── migrations/
├── config.py
├── run.py
├── requirements.txt
├── Procfile
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone Repository
```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open Project Folder
```bash
cd flask_project
```

### 3. Create Virtual Environment
```bash
python -m venv venv
```

### 4. Activate Virtual Environment (Windows)
```bash
venv\Scripts\activate
```

### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

### 6. Run Database Migration
```bash
flask --app run.py db upgrade
```

### 7. Run Application
```bash
python run.py
```

Open your browser and visit:

http://127.0.0.1:5000

## Project Purpose
This project was developed as part of a college learning project to gain practical experience in Python Flask, database management, user authentication, CRUD operations, and web development.

## Developed By
**Yash Ninaji Ingle**

Electronics and Communication Engineering Student
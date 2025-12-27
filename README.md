# 🚗 Vehicle Parking Management System (MAD-2)

A **full-stack Vehicle Parking Management System** built using **Flask (Backend)**, **Vue.js (Frontend)**, and **Celery (Background Jobs)**.  
The application manages vehicle parking operations, tracks entries and exits, allocates parking slots, and processes asynchronous tasks efficiently.

🎥 **Project Demo / Walkthrough Video**  
👉 https://youtu.be/iZ0koglY6c0

---

## 📌 Project Overview

This project was developed as part of the **MAD-2 milestone** and demonstrates a real-world parking management system using modern full-stack development practices.

The system follows a clean separation of concerns:
- **Backend** – Business logic, database, and REST APIs
- **Frontend** – Interactive user interface using Vue.js
- **Celery** – Background and scheduled task processing

---

## 🎯 Objectives

- Automate vehicle entry and exit tracking  
- Efficiently allocate and release parking slots  
- Maintain accurate parking records  
- Implement asynchronous background processing  
- Demonstrate scalable full-stack application architecture  

---

## ✨ Features

### 🚘 Parking Management
- Vehicle entry registration  
- Vehicle exit tracking  
- Automatic parking slot allocation and release  
- Real-time parking availability tracking  

### ⚙️ Backend Features
- RESTful APIs built with Flask  
- Database models and persistence  
- Modular and scalable application structure  
- Celery-based background task execution  

### 🎨 Frontend Features
- Vue.js Single Page Application (SPA)  
- Component-based architecture  
- Client-side routing  
- Clean and responsive user interface  

---

## 🛠️ Tech Stack

### Backend
- Python  
- Flask  
- Celery  
- SQLite (via Flask models)  
- Redis (Celery message broker, if configured)

### Frontend
- Vue.js  
- Vite  
- JavaScript  
- HTML & CSS  

### Tools & Utilities
- Git & GitHub  
- Node.js & npm  

---

## 📂 Project Structure

```text
Vehicle-Parking-App/
│
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── celery_app.py          # Celery configuration
│   ├── celery_worker.py       # Celery worker runner
│   ├── config.py              # App configuration
│   ├── extensions.py          # Flask extensions
│   ├── models.py              # Database models
│   ├── routes/                # API routes
│   ├── tasks/                 # Celery background tasks
│   └── __init__.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── router/
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── style.css
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── instance/                  # Instance-specific configs / database
├── celerybeat-schedule.dat
├── celerybeat-schedule.dir
├── celerybeat-schedule.bak
├── .gitignore
├── package.json
├── package-lock.json
└── README.md

---

## 🚀 How to Run the Project

### 🔹 Backend Setup

1. Navigate to backend directory:
```bash
cd backend

2. Create and activate a virtual environment:
python -m venv venv
venv\Scripts\activate   # Windows

3. Install dependencies:
pip install -r requirements.txt

4. Run the Flask server:
python app.py

🔹 Celery Worker
Start the Celery worker in a new terminal:
celery -A celery_app.celery worker --loglevel=info
Ensure Redis or the configured message broker is running.

🔹 Frontend Setup

1. Navigate to frontend directory:

cd frontend


2. Install frontend dependencies:

npm install


3. Start the development server:

npm run dev

📚 Learning Outcomes

By working on this project, you will gain experience in:

Full-stack application development

REST API design with Flask

Asynchronous task processing using Celery

Vue.js frontend architecture

Modular and scalable project structuring

Writing professional GitHub documentation

🧪 Use Cases

College or university parking systems

Office or corporate parking areas

Residential parking management

Learning reference for Flask + Vue + Celery integration


👩‍💻 Developer

Taniya Chouhan
B.S. in Data Science
IIT Madras

⭐ Notes

This project is developed for educational and demonstration purposes

It can be extended with:

Authentication and user roles

Admin dashboards

Payment integration

Analytics and reporting features


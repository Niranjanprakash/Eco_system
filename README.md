# 🌱 Eco-System AI Prediction Platform

## 📌 Overview

Eco-System is an AI-powered web application built using **Python Flask**, designed to analyze environmental or ecosystem-related data and generate intelligent predictions using a trained Machine Learning model. The platform provides an interactive dashboard, prediction system, and data-driven insights through a simple web interface.

This project combines frontend UI, backend APIs, and ML prediction into a single full-stack Flask application.

---

## 🚀 Features

* 🤖 Machine Learning prediction using trained `.pkl` model
* 📊 Interactive dashboard with data visualization
* 🌐 Responsive web interface using HTML, CSS, and JavaScript
* 🧠 Flask backend handling routing and ML inference
* 🗄️ SQLite/MySQL database support
* 📁 Organized project structure (templates, static files, data folder)

---

## 🧰 Tech Stack

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* Flask
* Gunicorn (Production server)

### Machine Learning

* Scikit-learn
* NumPy
* Pandas

### Database

* SQLite (default)
* MySQL (optional production upgrade)

---

## 📂 Project Structure

```
eco-system/
│
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── Procfile              # Deployment start command
│
├── data/
│   ├── ml_model.pkl      # Trained ML model
│   └── ecoplan.db        # Database file
│
├── templates/            # HTML pages
├── static/               # CSS, JS, Images
└── README.md
```

---

## ⚙️ Installation (Local Setup)

### 1️⃣ Clone the Repository

```
git clone <your-repo-link>
cd eco-system
```

### 2️⃣ Create Virtual Environment

```
python -m venv venv
```

Activate:

```
venv\Scripts\activate   (Windows)
source venv/bin/activate (Mac/Linux)
```

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

## 🌍 Deployment (Render)

This project is optimized for deployment on **Render**.

### Steps:

1. Push project to GitHub
2. Create new Web Service in Render
3. Use following settings:

**Build Command**

```
pip install -r requirements.txt
```

**Start Command**

```
gunicorn app:app
```

After deployment, your app will be live at:

```
https://your-project.onrender.com
```

---

## 🔗 API Flow

```
User Input → Flask Route → ML Model (ml_model.pkl) → Prediction Output → UI Dashboard
```

---

## ⚠️ Notes

* Ensure ML model path is relative (`data/ml_model.pkl`)
* SQLite database may reset on free hosting restart
* For production-scale apps, consider MySQL database

---

## 👨‍💻 Author

Developed as an AI-based ecosystem prediction platform integrating Machine Learning with a full-stack Flask application.

---

## ⭐ Future Enhancements

* Advanced analytics dashboard
* Real-time prediction charts
* Cloud database integration
* Authentication system
* Admin control panel

---

# 🏥 Patient Management System

![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-success)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

A **full-stack Patient Management System** built using **FastAPI** for the backend and **Streamlit** for the frontend.
This project demonstrates clean API design, CRUD operations, and real-world backend–frontend integration.

---

## 🚀 Project Overview

The Patient Management System allows users to manage patient records efficiently through a web interface.
It supports full **CRUD operations**, persistent database storage, and a scalable backend architecture.

This project is ideal for:

* Learning FastAPI and REST APIs
* Practicing backend–frontend integration
* Understanding database-driven applications
* Showcasing real-world development skills

---

## ✨ Key Features

✅ Add new patient records \n
✅ Fetch all patients \n
✅ Retrieve a single patient by ID
✅ Update patient details
✅ Delete patient records
✅ Interactive UI using Streamlit
✅ RESTful API with FastAPI
✅ SQLite-based persistent storage

---

## 🧱 Tech Stack

| Layer    | Technology |
| -------- | ---------- |
| Backend  | FastAPI    |
| Frontend | Streamlit  |
| Database | SQLite     |
| API Docs | Swagger UI |
| Language | Python     |

---

## 📁 Project Structure

```
Patient-Management-System/
│
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # Database models
│   ├── database.py          # Database configuration
│   ├── schemas.py           # Pydantic schemas
│   └── crud.py              # CRUD logic
│
├── frontend/
│   └── app.py               # Streamlit UI
│
├── patients.db              # SQLite database
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/jahanzeb17/Patient-Management-System.git
cd Patient-Management-System
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Backend (FastAPI)

```bash
uvicorn backend.main:app --reload
```

Access API documentation at:

```
http://127.0.0.1:8000/docs
```

### 4️⃣ Run the Frontend (Streamlit)

```bash
streamlit run frontend/app.py
```

---

## 🔄 CRUD Operations Implemented

| Operation  | Description                |
| ---------- | -------------------------- |
| Create     | Add a new patient          |
| Read (All) | Retrieve all patients      |
| Read (One) | Get patient by ID          |
| Update     | Modify patient details     |
| Delete     | Remove patient from system |

---

## 📌 Use Cases

* Clinic or hospital record management (prototype)
* Backend API learning project
* FastAPI + Streamlit integration demo
* Portfolio project for software / AI roles

---

## 🔮 Future Enhancements

* Authentication & authorization (JWT)
* Pagination and filtering
* Search functionality
* Dockerization
* Cloud database integration (PostgreSQL)
* Role-based access control (Admin / Staff)

---

## 👨‍💻 Author

**Jahanzeb Riaz**
Aspiring AI & Software Engineer
GitHub: [@jahanzeb17](https://github.com/jahanzeb17)

---

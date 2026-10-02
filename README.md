# 🎯 Job Matcher & Application Tracker API

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)

A high-performance RESTful microservice built with **FastAPI** and **SQLite** designed for automated Applicant Tracking System (ATS) resume-to-job description keyword alignment scoring, along with a complete CRUD pipeline for tracking job application lifecycles.

---

## 🚀 Key Features

* **ATS Resume Matching Engine**: Compares candidate resumes against target job descriptions to compute keyword overlap, match percentages, missing keywords, and tailored recommendations.
* **Full Application CRUD Lifecycle**: Complete database operations to create, retrieve, update application status, and delete job records.
* **Persistent Storage**: Lightweight, zero-config relational persistence via SQLite and Pydantic validation models.
* **System Metrics & Analytics**: Dedicated endpoint providing aggregate statistics on total tracked applications, status breakdowns, and match metrics.
* **Interactive API Documentation**: Auto-generated Swagger UI (`/docs`) and ReDoc (`/redoc`) interfaces for seamless endpoint testing.

---

## 🛠️ Tech Stack

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **ASGI Server:** [Uvicorn](https://www.uvicorn.org/)
* **Database:** [SQLite](https://www.sqlite.org/)
* **Data Validation:** [Pydantic](https://docs.pydantic.dev/)
* **Language:** Python 3.10+

---

## 📌 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/match` | Compute ATS keyword alignment & match score between a resume and job description. |
| `POST` | `/api/jobs` | Create and store a new job application record in the database. |
| `GET` | `/api/jobs` | Retrieve a list of all tracked job applications. |
| `PUT` | `/api/jobs/{id}` | Update application status or details for a specific job ID. |
| `DELETE` | `/api/jobs/{id}` | Remove a job application record by its unique ID. |
| `GET` | `/api/stats` | Retrieve aggregate database metrics and application pipeline statistics. |

---

## 📂 Project Structure

```text
job-matcher-api/
├── static/
│   └── index.html             # Static frontend web dashboard
├── test_proofs/               # Verification screenshots & test proof logs
├── .gitignore                 # Excludes cache, db, and virtual envs
├── database.py                # SQLite database connection & models
├── main.py                    # FastAPI application entry point & routes
├── matcher.py                 # Keyword matching & scoring algorithms
├── README.md                  # Project documentation
├── requirements.txt           # Project dependencies
└── run_server.bat             # One-click Windows startup script

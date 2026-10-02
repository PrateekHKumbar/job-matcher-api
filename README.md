# JobTrack AI: Application Tracker & ATS Resume Matcher API

An intelligent, production-ready backend REST API and interactive web dashboard built with **FastAPI**, **SQLite**, and **Scikit-Learn (NLP)**. Designed to automate candidate resume matching against industry Job Descriptions (JDs) and track application pipelines through a relational database.

---

## 🌟 Key Technical Features

1. **TF-IDF & Cosine Similarity Resume Matcher:**
   - Preprocesses raw resume and JD text (cleaning, tokenization, stopword removal).
   - Generates n-gram TF-IDF vector embeddings to compute mathematical cosine similarity.
   - Extracts matched technical keywords vs missing keyword gaps with actionable suggestions.

2. **Relational Database Management (SQLite & CRUD):**
   - Full RESTful CRUD endpoints (`POST`, `GET`, `PUT`, `DELETE`) to log and track job applications.
   - Dynamic status transitions: `Applied` $\rightarrow$ `Screening` $\rightarrow$ `Interview` $\rightarrow$ `Offered` $\rightarrow$ `Rejected`.
   - Aggregated pipeline metrics (application count, average match score, interview conversion rate).

3. **Interactive Modern Web Dashboard & Swagger Documentation:**
   - Real-time glassmorphism frontend interface to analyze resumes and manage job records.
   - Built-in interactive API documentation at `/docs` (Swagger UI).

---

## 🛠️ Technology Stack

- **Backend Framework:** FastAPI (Python 3.12)
- **ASGI Web Server:** Uvicorn
- **Machine Learning & NLP:** Scikit-Learn (TF-IDF Vectorizer, Cosine Similarity), NumPy
- **Database:** SQLite (Relational database with connection pooling and schema initialization)
- **Validation & Serialization:** Pydantic v2
- **Frontend Dashboard:** Vanilla JavaScript, Modern CSS (Glassmorphism, Flexbox/Grid)

---

## 🚀 How to Run Locally

### 1. Activate the Virtual Environment:
```powershell
cd C:\Users\Lenovo\.antigravity-ide\job-matcher-api
.venv\Scripts\Activate.ps1
```

### 2. Start the FastAPI Server:
```powershell
.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```

### 3. Open in Browser:
- **Interactive Web Dashboard:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Swagger REST API Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📝 How to Add This to Your Resume

```latex
\textbf{JobTrack AI: Resume Matcher \& Application Tracker API} $|$ \textit{FastAPI, SQLite, Scikit-Learn, Python} \hfill 02/2026
\begin{itemize}
    \item Developed a RESTful API and dashboard using FastAPI and SQLite to track job application pipelines with full CRUD operations.
    \item Implemented an NLP matching algorithm utilizing TF-IDF vectorization and Cosine Similarity to evaluate resume alignment against job descriptions and extract technical keyword gaps.
    \item Architected relational schemas with aggregated analytics endpoints to compute live application metrics and interview conversion rates.
\end{itemize}
```

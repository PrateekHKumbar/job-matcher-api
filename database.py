import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "jobs.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            location TEXT DEFAULT 'Remote',
            status TEXT DEFAULT 'Applied',
            match_score REAL DEFAULT 0.0,
            job_description TEXT,
            applied_date TEXT NOT NULL,
            notes TEXT DEFAULT ''
        )
    """)
    conn.commit()
    conn.close()

def create_job(company: str, role: str, location: str, status: str, match_score: float, job_description: str, notes: str) -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()
    applied_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        INSERT INTO applications (company, role, location, status, match_score, job_description, applied_date, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (company, role, location, status, match_score, job_description, applied_date, notes))
    job_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return get_job(job_id)

def get_all_jobs(status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    if status_filter and status_filter != "All":
        cursor.execute("SELECT * FROM applications WHERE status = ? ORDER BY id DESC", (status_filter,))
    else:
        cursor.execute("SELECT * FROM applications ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_job(job_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applications WHERE id = ?", (job_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_job_status(job_id: int, status: str, notes: Optional[str] = None) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    if notes is not None:
        cursor.execute("UPDATE applications SET status = ?, notes = ? WHERE id = ?", (status, notes, job_id))
    else:
        cursor.execute("UPDATE applications SET status = ? WHERE id = ?", (status, job_id))
    conn.commit()
    conn.close()
    return get_job(job_id)

def delete_job(job_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applications WHERE id = ?", (job_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def get_stats() -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total FROM applications")
    total = cursor.fetchone()["total"]
    
    cursor.execute("SELECT status, COUNT(*) as count FROM applications GROUP BY status")
    status_counts = {row["status"]: row["count"] for row in cursor.fetchall()}
    
    cursor.execute("SELECT AVG(match_score) as avg_score FROM applications WHERE match_score > 0")
    avg_score_row = cursor.fetchone()["avg_score"]
    avg_score = round(avg_score_row, 1) if avg_score_row else 0.0
    
    conn.close()
    return {
        "total_applied": total,
        "status_distribution": status_counts,
        "average_match_score": avg_score
    }

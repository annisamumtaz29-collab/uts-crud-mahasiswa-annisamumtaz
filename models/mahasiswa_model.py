# models/mahasiswa_model.py
# Semua urusan database (SQLite) ada di file ini.
import os
import sqlite3

# File database disimpan di folder project: mahasiswa.db
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mahasiswa.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # supaya hasil query bisa diakses seperti dict
    return conn


def init_db():
    """Membuat tabel mahasiswa kalau belum ada."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS mahasiswa (
            nim INTEGER PRIMARY KEY,          -- unique
            nama TEXT NOT NULL,
            program_studi TEXT NOT NULL,
            angkatan INTEGER NOT NULL,
            ipk REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def get_all():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM mahasiswa ORDER BY nim").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_by_nim(nim):
    conn = get_connection()
    row = conn.execute("SELECT * FROM mahasiswa WHERE nim = ?", (nim,)).fetchone()
    conn.close()
    return dict(row) if row else None


def insert(data):
    conn = get_connection()
    conn.execute(
        "INSERT INTO mahasiswa (nim, nama, program_studi, angkatan, ipk) VALUES (?, ?, ?, ?, ?)",
        (data["nim"], data["nama"], data["program_studi"], data["angkatan"], data["ipk"]),
    )
    conn.commit()
    conn.close()


def update(nim, data):
    conn = get_connection()
    conn.execute(
        "UPDATE mahasiswa SET nama = ?, program_studi = ?, angkatan = ?, ipk = ? WHERE nim = ?",
        (data["nama"], data["program_studi"], data["angkatan"], data["ipk"], nim),
    )
    conn.commit()
    conn.close()


def delete(nim):
    conn = get_connection()
    conn.execute("DELETE FROM mahasiswa WHERE nim = ?", (nim,))
    conn.commit()
    conn.close()
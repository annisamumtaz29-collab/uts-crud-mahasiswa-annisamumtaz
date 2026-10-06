# app.py
from flask import Flask, redirect
from models.mahasiswa_model import init_db
from controllers.mahasiswa_controller import mahasiswa_bp

app = Flask(__name__)
app.secret_key = "uts-lab-pemrograman"  # dibutuhkan untuk flash message

app.register_blueprint(mahasiswa_bp)

@app.route("/")
def home():
    return redirect("/mahasiswa")

if __name__ == "__main__":
    init_db()  # buat file database + tabel kalau belum ada
    app.run(debug=True)
# controllers/mahasiswa_controller.py
# Semua route (alamat URL) dan logika aplikasi ada di file ini.
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, flash
from models import mahasiswa_model as model

mahasiswa_bp = Blueprint("mahasiswa_bp", __name__)


def hitung_lama_studi(angkatan):
    """Lama Studi (tahun) = tahun sekarang - angkatan. Dihitung program, bukan input user."""
    return datetime.now().year - int(angkatan)


def validasi(form, cek_nim=True):
    """Cek input form. Mengembalikan (data_bersih, daftar_error)."""
    errors = []
    data = {
        "nim": form.get("nim", "").strip(),
        "nama": form.get("nama", "").strip(),
        "program_studi": form.get("program_studi", "").strip(),
        "angkatan": form.get("angkatan", "").strip(),
        "ipk": form.get("ipk", "").strip().replace(",", "."),
    }

    # NIM: wajib, harus angka, dan tidak boleh sudah terdaftar
    if cek_nim:
        if not data["nim"]:
            errors.append("NIM wajib diisi.")
        elif not data["nim"].isdigit():
            errors.append("NIM harus berupa angka.")
        elif model.get_by_nim(int(data["nim"])):
            errors.append(f"NIM {data['nim']} sudah terdaftar.")

    # Nama & Program Studi: wajib
    if not data["nama"]:
        errors.append("Nama wajib diisi.")
    if not data["program_studi"]:
        errors.append("Program studi wajib diisi.")

    # Angkatan: wajib, angka, tidak lebih dari tahun sekarang
    if not data["angkatan"]:
        errors.append("Angkatan wajib diisi.")
    elif not data["angkatan"].isdigit():
        errors.append("Angkatan harus berupa angka tahun, misalnya 2023.")
    elif int(data["angkatan"]) > datetime.now().year:
        errors.append("Angkatan tidak boleh lebih dari tahun sekarang.")

    # IPK: wajib, angka, rentang 0.00 - 4.00
    if not data["ipk"]:
        errors.append("IPK wajib diisi.")
    else:
        try:
            ipk = float(data["ipk"])
            if ipk < 0 or ipk > 4:
                errors.append("IPK harus di antara 0.00 dan 4.00.")
        except ValueError:
            errors.append("IPK harus berupa angka, misalnya 3.50.")

    # Ubah ke tipe data yang benar kalau tidak ada error
    if not errors:
        if cek_nim:
            data["nim"] = int(data["nim"])
        data["angkatan"] = int(data["angkatan"])
        data["ipk"] = round(float(data["ipk"]), 2)

    return data, errors


# READ (daftar)  ->  GET /mahasiswa
@mahasiswa_bp.route("/mahasiswa", methods=["GET"])
def daftar():
    semua = model.get_all()
    for m in semua:
        m["lama_studi"] = hitung_lama_studi(m["angkatan"])
    return render_template("index.html", mahasiswa=semua)


# READ (detail)  ->  GET /mahasiswa/24060123
@mahasiswa_bp.route("/mahasiswa/<int:nim>", methods=["GET"])
def detail(nim):
    m = model.get_by_nim(nim)
    if not m:
        flash("Data mahasiswa tidak ditemukan.", "error")
        return redirect("/mahasiswa")
    m["lama_studi"] = hitung_lama_studi(m["angkatan"])
    return render_template("detail.html", m=m)


# CREATE (tampilkan form)  ->  GET /mahasiswa/tambah
@mahasiswa_bp.route("/mahasiswa/tambah", methods=["GET"])
def form_tambah():
    return render_template("form.html", mode="tambah", m={}, errors=[])


# CREATE (simpan)  ->  POST /mahasiswa/tambah
@mahasiswa_bp.route("/mahasiswa/tambah", methods=["POST"])
def tambah():
    data, errors = validasi(request.form, cek_nim=True)
    if errors:
        # tampilkan form lagi beserta pesan error dan isian sebelumnya
        return render_template("form.html", mode="tambah", m=data, errors=errors), 400
    model.insert(data)
    flash(f"Mahasiswa {data['nama']} berhasil ditambahkan.", "success")
    return redirect("/mahasiswa")


# UPDATE (tampilkan form berisi data lama)  ->  GET /mahasiswa/24060123/edit
@mahasiswa_bp.route("/mahasiswa/<int:nim>/edit", methods=["GET"])
def form_edit(nim):
    m = model.get_by_nim(nim)
    if not m:
        flash("Data mahasiswa tidak ditemukan.", "error")
        return redirect("/mahasiswa")
    return render_template("form.html", mode="edit", m=m, errors=[])


# UPDATE (simpan perubahan)  ->  POST /mahasiswa/24060123/edit
@mahasiswa_bp.route("/mahasiswa/<int:nim>/edit", methods=["POST"])
def edit(nim):
    if not model.get_by_nim(nim):
        flash("Data mahasiswa tidak ditemukan.", "error")
        return redirect("/mahasiswa")
    data, errors = validasi(request.form, cek_nim=False)  # NIM tidak bisa diubah
    data["nim"] = nim
    if errors:
        return render_template("form.html", mode="edit", m=data, errors=errors), 400
    model.update(nim, data)
    flash(f"Data mahasiswa {data['nama']} berhasil diperbarui.", "success")
    return redirect("/mahasiswa")


# DELETE  ->  POST /mahasiswa/24060123/hapus
@mahasiswa_bp.route("/mahasiswa/<int:nim>/hapus", methods=["POST"])
def hapus(nim):
    m = model.get_by_nim(nim)
    if m:
        model.delete(nim)
        flash(f"Mahasiswa {m['nama']} berhasil dihapus.", "success")
    else:
        flash("Data mahasiswa tidak ditemukan.", "error")
    return redirect("/mahasiswa")
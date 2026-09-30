# Odoo Custom Module

[![Odoo Version](https://img.shields.io/badge/Odoo-17.0%20%7C%2018.0-714B67?style=flat&logo=odoo)](https://www.odoo.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat&logo=postgresql)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-LGPL--3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0.html)

**Odoo Custom Module** adalah modul kustom Odoo enterprise-ready yang dirancang sebagai standar template dan fondasi pengembangan sistem manajemen bisnis terintegrasi di ekosistem Odoo (kompatibel dengan Odoo 16, 17, dan 18).

---

## 🌟 Fitur Utama (Key Features)

1. **Automated Sequence Generation**
   - Penomoran referensi otomatis berbasis sequence (`CUST/YYYY/0001`) yang terformat rapi dan terindeks.
2. **Multi-Stage Business Workflow**
   - Siklus status lengkap: `Draft` &rarr; `In Progress` &rarr; `Approved` &rarr; `Completed` &rarr; `Cancelled`.
   - Tombol transisi interaktif di statusbar lengkap dengan validasi hak akses.
3. **Chatter & Activity Tracking**
   - Integrasi penuh dengan model `mail.thread` dan `mail.activity.mixin`.
   - Log pesan audit otomatis untuk setiap perubahan status dan catatan komunikasi tim.
4. **Rich Multi-View Ecosystem**
   - **Kanban View**: Pengelompokan visual kartu berdasarkan status, progress bar, avatar penanggung jawab, dan rating prioritas.
   - **Tree / List View**: Pewarnaan baris otomatis berbasis status (*color decorations*) dan tag berwarna.
   - **Form View**: Antarmuka responsif dengan ribbon status (*Cancelled / Completed*), smart group, dan tab notebook.
   - **Search View**: Filter cepat (*My Records, Draft, In Progress, Overdue*) dan pengelompokan dinamis (*Group By*).
5. **Batch Action Wizard**
   - Pop-up wizard (`custom.record.wizard`) untuk memperbarui status banyak dokumen sekaligus (*mass update*) disertai alasan/keterangan audit.
6. **Laporan Cetak QWeb PDF**
   - Template laporan resmi siap cetak (`Custom Record Dossier`) lengkap dengan header perusahaan, rincian biaya, spesifikasi, dan tanda tangan dokumen.
7. **Keamanan & Multi-Company (Security & Access Control)**
   - Kategori hak akses khusus: **User** (akses operasional) dan **Administrator** (akses konfigurasi penuh).
   - Multi-Company Record Rule agar data terisolasi aman antar anak perusahaan.
8. **REST API Endpoint Controller**
   - Contoh rute HTTP JSON controller (`/api/custom_module/ping` dan `/api/custom_module/records`) untuk integrasi sistem pihak ketiga atau frontend eksternal.

---

## 📁 Struktur Direktori (Directory Structure)

```text
odoo custom module/
├── .gitignore                      # Konfigurasi file yang diabaikan Git
├── README.md                       # Dokumentasi lengkap proyek
├── docker-compose.yml              # Konfigurasi container Odoo 17 & PostgreSQL 15
├── odoo.conf                       # Template konfigurasi server Odoo
├── requirements.txt                # Dependensi Python untuk linter & testing
└── custom_addons/
    └── odoo_custom_module/         # Direktori Modul Odoo
        ├── __init__.py             # Inisialisasi modul Python
        ├── __manifest__.py         # Metadata, dependensi, dan deklarasi data modul
        ├── controllers/
        │   ├── __init__.py
        │   └── controllers.py      # HTTP JSON API controller
        ├── models/
        │   ├── __init__.py
        │   ├── custom_tag.py       # Model klasifikasi tag
        │   └── custom_record.py    # Model utama alur kerja kustom
        ├── views/
        │   ├── custom_record_views.xml # Tampilan Form, Tree, Kanban, Search
        │   ├── custom_tag_views.xml    # Tampilan Tag
        │   └── menu_views.xml          # Definisi menu navigasi utama & sub-menu
        ├── security/
        │   ├── security.xml        # Definisi Group User, Manager, dan Record Rule
        │   └── ir.model.access.csv # Matriks hak akses model (ACL)
        ├── data/
        │   └── ir_sequence_data.xml# Definisi nomor urut otomatis
        ├── wizard/
        │   ├── __init__.py
        │   ├── custom_record_wizard.py       # TransientModel untuk batch update
        │   └── custom_record_wizard_views.xml# Dialog pop-up wizard
        ├── report/
        │   └── custom_record_report.xml      # Template laporan cetak QWeb PDF
        ├── demo/
        │   └── demo.xml            # Data dummy untuk pengujian awal
        └── static/
            └── description/
                ├── icon.png        # Ikon aplikasi di Apps Menu
                └── index.html      # Halaman deskripsi katalog Odoo Apps
```

---

## 🚀 Panduan Instalasi & Menjalankan (Getting Started)

### Cara 1: Menggunakan Docker Compose (Direkomendasikan)

Jika Anda telah menginstal **Docker** dan **Docker Compose**, Anda dapat langsung menjalankan seluruh stack (Odoo 17 + PostgreSQL) tanpa perlu setup lokal yang rumit.

1. Buka terminal di folder proyek:
   ```bash
   cd "C:\Users\ASUS Vivobook\.gemini\antigravity-ide\scratch\odoo custom module"
   ```

2. Jalankan container:
   ```bash
   docker compose up -d
   ```

3. Buka browser dan akses antarmuka Odoo di:
   ```text
   http://localhost:8069
   ```

4. Buat database baru di Odoo, login sebagai Administrator, aktifkan **Developer Mode**, buka menu **Apps**, klik **Update Apps List**, lalu cari dan instal **Odoo Custom Module**.

---

### Cara 2: Instalasi ke Instance Odoo Lokal yang Sudah Ada

1. Salin folder `custom_addons/odoo_custom_module` ke direktori addons Odoo Anda, atau tambahkan path folder ini ke konfigurasi `odoo.conf`:
   ```ini
   addons_path = /path/to/odoo/addons,/path/to/odoo custom module/custom_addons
   ```

2. Restart service server Odoo:
   ```bash
   ./odoo-bin -c /path/to/odoo.conf -u odoo_custom_module
   ```

3. Pada browser:
   - Masuk ke Odoo dengan hak akses Administrator.
   - Masuk ke **Settings** &rarr; aktifkan **Developer Mode**.
   - Buka menu **Apps** &rarr; klik **Update Apps List**.
   - Cari kata kunci `Odoo Custom Module` lalu klik tombol **Activate / Install**.

---

## ⚙️ Menggunakan Modul

1. **Membuat Record Baru**:
   - Klik menu navigasi **Custom Management** &rarr; **Operations** &rarr; **Custom Records**.
   - Klik **New**. Masukkan judul, pilih customer/partner, tenggat waktu, dan estimasi biaya.
   - Nomor referensi unik seperti `CUST/2026/0001` akan terbuat secara otomatis saat disimpan.

2. **Alur Status**:
   - Klik tombol **Start Work** untuk memindahkan status ke *In Progress*.
   - Klik **Approve** setelah ditinjau.
   - Klik **Mark as Completed** saat pekerjaan selesai.

3. **Batch Status Update (Wizard)**:
   - Buka Tree / List view dari Custom Records.
   - Centang beberapa baris record.
   - Klik menu **Action** (ikon roda gigi) di bagian atas &rarr; pilih **Batch Status Update**.
   - Pilih status tujuan dan masukkan alasan, lalu klik **Update Status**.

4. **Mencetak Laporan PDF**:
   - Di tampilan form record, klik menu **Print** &rarr; **Custom Record Dossier**.
   - File PDF berformat resmi akan otomatis diunduh.

5. **Pengujian REST API JSON**:
   ```bash
   curl -X POST http://localhost:8069/api/custom_module/ping \
        -H "Content-Type: application/json" \
        -d '{}'
   ```

---

## 🛠️ Pengembangan & Kontribusi (Development Workflow)

Proyek ini terhubung langsung dengan repositori GitHub:
👉 **[https://github.com/vincentjiu23/odoo-custom-module](https://github.com/vincentjiu23/odoo-custom-module)**

Setiap kali melakukan perubahan kode:
1. Periksa perubahan file:
   ```bash
   git status
   ```
2. Tambahkan dan commit perubahan:
   ```bash
   git add .
   git commit -m "Deskripsi perubahan"
   ```
3. Push ke GitHub repository:
   ```bash
   git push origin main
   ```

---

## 📄 Lisensi & Penulis

- **Penulis**: Vincent Jiu ([@vincentjiu23](https://github.com/vincentjiu23))
- **Lisensi**: LGPL-3 (GNU Lesser General Public License v3.0)

# -*- coding: utf-8 -*-
{
    'name': 'Room Booking',
    'version': '17.0.1.0.0',
    'summary': 'Room Booking Management System — Master Ruangan & Pemesanan Ruangan',
    'description': """
Room Booking Module
===================
Sistem manajemen pemesanan ruangan yang mencakup:

* **Master Ruangan** — Pendataan ruangan lengkap dengan tipe, lokasi, foto,
  dan kapasitas.
* **Pemesanan Ruangan** — Pemesanan ruangan dengan nomor otomatis, validasi
  ketersediaan, dan alur status (Draft → On Going → Done).

Fitur Utama
-----------
- Penomoran pemesanan otomatis: ``BOOK/{TIPE_RUANGAN}/{TANGGAL}/{SEQUENCE}``
- Validasi duplikasi nama ruangan (database-level).
- Validasi duplikasi nama pemesan (database-level).
- Validasi satu ruangan hanya bisa dipesan satu kali per tanggal (database-level).
- Validasi kapasitas ruangan tidak boleh negatif.
- Alur status pemesanan: Draft → On Going → Done.
- Tampilan List, Kanban, dan Form untuk Master Ruangan.
- Tampilan List, Form, dan Search untuk Pemesanan Ruangan.
    """,
    'category': 'Services',
    'author': 'Vincent Jiu',
    'website': 'https://github.com/vincentjiu23/odoo-custom-module',
    'license': 'LGPL-3',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/room_views.xml',
        'views/booking_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

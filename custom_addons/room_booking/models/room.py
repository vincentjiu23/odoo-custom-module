# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Room(models.Model):
    """Master Ruangan — stores room master data.

    Uniqueness of room name is enforced at the database level
    via _sql_constraints. Negative capacity is caught by a
    Python @api.constrains to provide a user-friendly error.
    """

    _name = 'room.room'
    _description = 'Master Ruangan'
    _order = 'name asc'

    name = fields.Char(
        string='Nama Ruangan',
        required=True,
        index=True,
    )
    room_type = fields.Selection(
        selection=[
            ('meeting_small', 'Meeting Room Kecil'),
            ('meeting_large', 'Meeting Room Besar'),
            ('aula', 'Aula'),
        ],
        string='Tipe Ruangan',
        required=True,
    )
    location = fields.Selection(
        selection=[
            ('1a', '1A'),
            ('1b', '1B'),
            ('1c', '1C'),
            ('2a', '2A'),
            ('2b', '2B'),
            ('2c', '2C'),
        ],
        string='Lokasi Ruangan',
        required=True,
    )
    photo = fields.Image(
        string='Foto Ruangan',
        required=True,
        max_width=1024,
        max_height=1024,
    )
    capacity = fields.Integer(
        string='Kapasitas Ruangan',
        required=True,
    )
    description = fields.Text(
        string='Keterangan',
    )

    # ------------------------------------------------------------------
    # Constraints
    # ------------------------------------------------------------------

    _sql_constraints = [
        (
            'unique_room_name',
            'UNIQUE(name)',
            'Nama Ruangan sudah ada! Nama Ruangan harus unik.',
        ),
    ]

    @api.constrains('capacity')
    def _check_capacity_positive(self):
        """Capacity must not be negative."""
        for rec in self:
            if rec.capacity < 0:
                raise ValidationError(
                    _("Kapasitas Ruangan tidak boleh bernilai negatif. "
                      "Nilai yang diberikan: %s") % rec.capacity
                )

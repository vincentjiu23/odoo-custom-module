# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


# Maps internal room_type key → short code for the booking number.
ROOM_TYPE_CODE_MAP = {
    'meeting_small': 'MRK',   # Meeting Room Kecil
    'meeting_large': 'MRB',   # Meeting Room Besar
    'aula': 'AUL',            # Aula
}


class RoomBooking(models.Model):
    """Pemesanan Ruangan — handles room booking lifecycle.

    Booking number format (design decision — see README):
        BOOK/{ROOM_TYPE_CODE}/{YYYYMMDD}/{SEQUENCE}
        Example: BOOK/MRK/20260930/0001

    Workflow:  Draft  →  On Going  →  Done
    Transition is handled by a single ``action_process()`` method.
    """

    _name = 'room.booking'
    _description = 'Pemesanan Ruangan'
    _order = 'booking_date desc, id desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Nomor Pemesanan',
        required=True,
        readonly=True,
        copy=False,
        index=True,
        default='New',
    )
    room_id = fields.Many2one(
        comodel_name='room.room',
        string='Ruangan',
        required=True,
        ondelete='restrict',
    )
    booking_name = fields.Char(
        string='Nama Pemesan',
        required=True,
    )
    booking_date = fields.Date(
        string='Tanggal Pemesanan',
        required=True,
        default=fields.Date.context_today,
    )
    status = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('ongoing', 'On Going'),
            ('done', 'Done'),
        ],
        string='Status Pemesanan',
        default='draft',
        required=True,
    )
    notes = fields.Text(
        string='Catatan Pemesanan',
    )

    # Related fields for convenient display in views
    room_type = fields.Selection(
        related='room_id.room_type',
        string='Tipe Ruangan',
        store=True,
        readonly=True,
    )

    # ------------------------------------------------------------------
    # Constraints
    # ------------------------------------------------------------------

    _sql_constraints = [
        (
            'unique_booking_name',
            'UNIQUE(booking_name)',
            'Nama Pemesan sudah terdaftar! Nama Pemesan harus unik.',
        ),
        (
            'unique_room_date',
            'UNIQUE(room_id, booking_date)',
            'Ruangan sudah dipesan pada tanggal tersebut! '
            'Satu ruangan hanya dapat dipesan satu kali per hari.',
        ),
    ]

    # ------------------------------------------------------------------
    # CRUD Overrides
    # ------------------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        """Generate booking number on creation.

        Format: BOOK/{ROOM_TYPE_CODE}/{YYYYMMDD}/{SEQ}
        The running sequence number comes from ir.sequence 'room.booking.seq'.
        """
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                # Resolve room type code
                room = self.env['room.room'].browse(vals.get('room_id'))
                room_type_code = ROOM_TYPE_CODE_MAP.get(room.room_type, 'XXX')

                # Resolve date string
                booking_date = vals.get('booking_date')
                if not booking_date:
                    booking_date = fields.Date.context_today(self)
                if isinstance(booking_date, str):
                    date_str = booking_date.replace('-', '')
                else:
                    date_str = booking_date.strftime('%Y%m%d')

                # Get next sequence number
                seq = self.env['ir.sequence'].next_by_code(
                    'room.booking.seq'
                ) or '0001'

                vals['name'] = "BOOK/%s/%s/%s" % (
                    room_type_code, date_str, seq
                )

        return super().create(vals_list)

    # ------------------------------------------------------------------
    # Actions / Workflow
    # ------------------------------------------------------------------

    def action_process(self):
        """Advance booking status one step forward.

        Draft   →  On Going
        On Going →  Done
        Done    →  (raises UserError)
        """
        for rec in self:
            if rec.status == 'draft':
                rec.status = 'ongoing'
            elif rec.status == 'ongoing':
                rec.status = 'done'
            elif rec.status == 'done':
                raise UserError(
                    _("Pemesanan dengan status 'Done' tidak dapat "
                      "diproses lagi.")
                )

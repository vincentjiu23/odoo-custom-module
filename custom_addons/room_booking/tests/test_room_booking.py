# -*- coding: utf-8 -*-
"""
Automated Tests for Room Booking Module
========================================

Covers all business rules specified in the assessment:
 1. Create a valid room.
 2. Cannot create duplicate room name.
 3. Create a valid booking.
 4. Booking defaults to Draft.
 5. Draft → On Going works.
 6. On Going → Done works.
 7. Cannot book the same room on the same date.
 8. Can book the same room on another date.
 9. Can book another room on the same date.
10. Cannot duplicate booking name.
11. Booking number is generated correctly.
12. Negative capacity is rejected.
13. Done status cannot be processed further.

Run with:
    odoo-bin -d <db> --test-tags /room_booking -i room_booking --stop-after-init
"""
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError, UserError
from odoo.tools import mute_logger


# Minimal 1x1 pixel PNG encoded as base64 — used for the required photo field.
DUMMY_IMAGE = (
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVQI'
    '12NgAAIABQABNjN9GQAAAABJRU5ErkJggg=='
)


class TestRoom(TransactionCase):
    """Tests for the room.room model (Master Ruangan)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Room = cls.env['room.room']

    def _create_room(self, **overrides):
        """Helper: create a room with sensible defaults."""
        vals = {
            'name': 'Ruangan Test',
            'room_type': 'meeting_small',
            'location': '1a',
            'photo': DUMMY_IMAGE,
            'capacity': 10,
        }
        vals.update(overrides)
        return self.Room.create(vals)

    # ------------------------------------------------------------------
    # Test 1: Create a valid room
    # ------------------------------------------------------------------
    def test_01_create_valid_room(self):
        """A room with all required fields should be created successfully."""
        room = self._create_room(name='Ruangan Alpha')
        self.assertTrue(room.id, "Room should be created with a valid ID.")
        self.assertEqual(room.name, 'Ruangan Alpha')
        self.assertEqual(room.room_type, 'meeting_small')
        self.assertEqual(room.location, '1a')
        self.assertEqual(room.capacity, 10)

    # ------------------------------------------------------------------
    # Test 2: Cannot create duplicate room name
    # ------------------------------------------------------------------
    @mute_logger('odoo.sql_db')
    def test_02_duplicate_room_name_rejected(self):
        """Two rooms with the same name must raise an error (SQL UNIQUE)."""
        self._create_room(name='Ruangan Duplikat')
        with self.assertRaises(Exception):
            self._create_room(name='Ruangan Duplikat', location='2a')

    # ------------------------------------------------------------------
    # Test: Negative capacity is rejected
    # ------------------------------------------------------------------
    def test_03_negative_capacity_rejected(self):
        """Room capacity must not be negative."""
        with self.assertRaises(ValidationError):
            self._create_room(name='Ruangan Negatif', capacity=-5)

    # ------------------------------------------------------------------
    # Test: Zero capacity is allowed
    # ------------------------------------------------------------------
    def test_04_zero_capacity_allowed(self):
        """Zero capacity is technically valid (requirement says 'negative')."""
        room = self._create_room(name='Ruangan Nol', capacity=0)
        self.assertEqual(room.capacity, 0)


class TestBooking(TransactionCase):
    """Tests for the room.booking model (Pemesanan Ruangan)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Room = cls.env['room.room']
        cls.Booking = cls.env['room.booking']

        # Ensure ir.sequence exists (safety net for test environments)
        if not cls.env['ir.sequence'].search(
            [('code', '=', 'room.booking.seq')]
        ):
            cls.env['ir.sequence'].create({
                'name': 'Room Booking Sequence',
                'code': 'room.booking.seq',
                'padding': 4,
            })

        # Shared test rooms
        cls.room_a = cls.Room.create({
            'name': 'Ruangan A',
            'room_type': 'meeting_small',
            'location': '1a',
            'photo': DUMMY_IMAGE,
            'capacity': 10,
        })
        cls.room_b = cls.Room.create({
            'name': 'Ruangan B',
            'room_type': 'meeting_large',
            'location': '2a',
            'photo': DUMMY_IMAGE,
            'capacity': 30,
        })
        cls.room_c = cls.Room.create({
            'name': 'Ruangan C',
            'room_type': 'aula',
            'location': '1c',
            'photo': DUMMY_IMAGE,
            'capacity': 100,
        })

    def _create_booking(self, **overrides):
        """Helper: create a booking with sensible defaults."""
        vals = {
            'room_id': self.room_a.id,
            'booking_name': 'Pemesan Default',
            'booking_date': '2026-09-30',
        }
        vals.update(overrides)
        return self.Booking.create(vals)

    # ------------------------------------------------------------------
    # Test 3: Create a valid booking
    # ------------------------------------------------------------------
    def test_01_create_valid_booking(self):
        """A booking with all required fields should be created."""
        booking = self._create_booking(booking_name='Rapat Harian Tim A')
        self.assertTrue(booking.id)
        self.assertEqual(booking.room_id, self.room_a)
        self.assertEqual(booking.booking_name, 'Rapat Harian Tim A')

    # ------------------------------------------------------------------
    # Test 4: Booking defaults to Draft
    # ------------------------------------------------------------------
    def test_02_booking_default_status_draft(self):
        """New bookings must default to 'draft' status."""
        booking = self._create_booking(booking_name='Pemesan Status Default')
        self.assertEqual(booking.status, 'draft')

    # ------------------------------------------------------------------
    # Test 5: Draft → On Going works
    # ------------------------------------------------------------------
    def test_03_draft_to_ongoing(self):
        """action_process() should transition Draft → On Going."""
        booking = self._create_booking(
            booking_name='Pemesan Draft-Ongoing',
            booking_date='2026-10-01',
        )
        self.assertEqual(booking.status, 'draft')
        booking.action_process()
        self.assertEqual(booking.status, 'ongoing')

    # ------------------------------------------------------------------
    # Test 6: On Going → Done works
    # ------------------------------------------------------------------
    def test_04_ongoing_to_done(self):
        """action_process() should transition On Going → Done."""
        booking = self._create_booking(
            booking_name='Pemesan Ongoing-Done',
            booking_date='2026-10-02',
        )
        booking.action_process()   # Draft → On Going
        booking.action_process()   # On Going → Done
        self.assertEqual(booking.status, 'done')

    # ------------------------------------------------------------------
    # Test: Done cannot be processed further
    # ------------------------------------------------------------------
    def test_05_done_cannot_process(self):
        """action_process() on Done status should raise UserError."""
        booking = self._create_booking(
            booking_name='Pemesan Done-Error',
            booking_date='2026-10-03',
        )
        booking.action_process()   # Draft → On Going
        booking.action_process()   # On Going → Done
        with self.assertRaises(UserError):
            booking.action_process()

    # ------------------------------------------------------------------
    # Test 7: Cannot book the same room on the same date
    # ------------------------------------------------------------------
    @mute_logger('odoo.sql_db')
    def test_06_same_room_same_date_rejected(self):
        """Two bookings for the same room on the same date must fail."""
        self._create_booking(
            booking_name='Pemesan Pertama',
            room_id=self.room_a.id,
            booking_date='2026-11-01',
        )
        with self.assertRaises(Exception):
            self._create_booking(
                booking_name='Pemesan Kedua',
                room_id=self.room_a.id,
                booking_date='2026-11-01',
            )

    # ------------------------------------------------------------------
    # Test 8: Can book the same room on another date
    # ------------------------------------------------------------------
    def test_07_same_room_different_date_allowed(self):
        """Same room on different dates should be allowed."""
        b1 = self._create_booking(
            booking_name='Pemesan Tanggal 1',
            room_id=self.room_a.id,
            booking_date='2026-11-10',
        )
        b2 = self._create_booking(
            booking_name='Pemesan Tanggal 2',
            room_id=self.room_a.id,
            booking_date='2026-11-11',
        )
        self.assertTrue(b1.id)
        self.assertTrue(b2.id)

    # ------------------------------------------------------------------
    # Test 9: Can book another room on the same date
    # ------------------------------------------------------------------
    def test_08_different_room_same_date_allowed(self):
        """Different rooms on the same date should be allowed."""
        b1 = self._create_booking(
            booking_name='Pemesan Room A',
            room_id=self.room_a.id,
            booking_date='2026-12-01',
        )
        b2 = self._create_booking(
            booking_name='Pemesan Room B',
            room_id=self.room_b.id,
            booking_date='2026-12-01',
        )
        self.assertTrue(b1.id)
        self.assertTrue(b2.id)

    # ------------------------------------------------------------------
    # Test 10: Cannot duplicate booking name
    # ------------------------------------------------------------------
    @mute_logger('odoo.sql_db')
    def test_09_duplicate_booking_name_rejected(self):
        """Two bookings with the same booking_name must fail."""
        self._create_booking(
            booking_name='Nama Sama',
            room_id=self.room_a.id,
            booking_date='2026-12-10',
        )
        with self.assertRaises(Exception):
            self._create_booking(
                booking_name='Nama Sama',
                room_id=self.room_b.id,
                booking_date='2026-12-11',
            )

    # ------------------------------------------------------------------
    # Test 11: Booking number is generated correctly
    # ------------------------------------------------------------------
    def test_10_booking_number_format(self):
        """Booking number should follow BOOK/{TYPE}/{DATE}/{SEQ} format."""
        booking = self._create_booking(
            booking_name='Pemesan Format Nomor',
            room_id=self.room_a.id,
            booking_date='2026-09-30',
        )
        # Expected format: BOOK/MRK/20260930/XXXX
        self.assertTrue(
            booking.name.startswith('BOOK/MRK/20260930/'),
            f"Expected 'BOOK/MRK/20260930/XXXX', got '{booking.name}'"
        )
        parts = booking.name.split('/')
        self.assertEqual(len(parts), 4, "Booking number should have 4 parts.")
        self.assertEqual(parts[0], 'BOOK')
        self.assertEqual(parts[1], 'MRK')   # Meeting Room Kecil
        self.assertEqual(parts[2], '20260930')
        self.assertEqual(len(parts[3]), 4, "Sequence should be 4 digits.")

    def test_11_booking_number_room_type_codes(self):
        """Each room type should produce the correct code in the number."""
        # MRB = Meeting Room Besar
        b_mrb = self._create_booking(
            booking_name='Pemesan MRB',
            room_id=self.room_b.id,
            booking_date='2026-12-20',
        )
        self.assertIn('/MRB/', b_mrb.name)

        # AUL = Aula
        b_aul = self._create_booking(
            booking_name='Pemesan AUL',
            room_id=self.room_c.id,
            booking_date='2026-12-20',
        )
        self.assertIn('/AUL/', b_aul.name)

    def test_12_booking_number_not_new(self):
        """Booking number must not be 'New' after creation."""
        booking = self._create_booking(
            booking_name='Pemesan Bukan New',
            room_id=self.room_a.id,
            booking_date='2026-12-25',
        )
        self.assertNotEqual(booking.name, 'New')
        self.assertTrue(booking.name.startswith('BOOK/'))

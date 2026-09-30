# -*- coding: utf-8 -*-
"""
Unit Tests for Arithmetic Sequence Generator
=============================================

Run with:
    python -m pytest test_arithmetic_sequence.py -v
or:
    python -m unittest test_arithmetic_sequence -v
"""
import unittest
import sys
import os

# Ensure the arithmetic_sequence module is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from arithmetic_sequence import arithmetic_sequence, format_sequence


class TestArithmeticSequence(unittest.TestCase):
    """Test suite for the arithmetic_sequence function."""

    # --- Valid inputs ---

    def test_n_equals_1(self):
        """N=1 should return the first term only."""
        self.assertEqual(arithmetic_sequence(1), [2])

    def test_n_equals_4(self):
        """N=4 should return [2, 5, 8, 11] as per the assessment example."""
        self.assertEqual(arithmetic_sequence(4), [2, 5, 8, 11])

    def test_n_equals_7(self):
        """N=7 should return [2, 5, 8, 11, 14, 17, 20] as per the assessment example."""
        self.assertEqual(arithmetic_sequence(7), [2, 5, 8, 11, 14, 17, 20])

    def test_n_equals_10(self):
        """N=10 should return 10 terms following the formula a(n) = 2 + (n-1)*3."""
        expected = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29]
        self.assertEqual(arithmetic_sequence(10), expected)

    def test_formula_consistency(self):
        """Each term should satisfy a(n) = 2 + (n-1) * 3."""
        result = arithmetic_sequence(20)
        for i, value in enumerate(result):
            expected = 2 + (i * 3)
            self.assertEqual(value, expected, f"Term {i+1} mismatch")

    def test_common_difference(self):
        """Consecutive terms should differ by exactly 3."""
        result = arithmetic_sequence(15)
        for i in range(1, len(result)):
            self.assertEqual(result[i] - result[i - 1], 3)

    # --- Invalid inputs ---

    def test_n_equals_0(self):
        """N=0 should raise ValueError."""
        with self.assertRaises(ValueError):
            arithmetic_sequence(0)

    def test_negative_input(self):
        """Negative N should raise ValueError."""
        with self.assertRaises(ValueError):
            arithmetic_sequence(-1)

    def test_large_negative_input(self):
        """Large negative N should raise ValueError."""
        with self.assertRaises(ValueError):
            arithmetic_sequence(-100)

    def test_string_input(self):
        """String input should raise TypeError."""
        with self.assertRaises(TypeError):
            arithmetic_sequence("abc")

    def test_float_input(self):
        """Float input should raise TypeError."""
        with self.assertRaises(TypeError):
            arithmetic_sequence(3.5)

    def test_none_input(self):
        """None input should raise TypeError."""
        with self.assertRaises(TypeError):
            arithmetic_sequence(None)

    def test_boolean_input(self):
        """Boolean input should raise TypeError (bool is subclass of int)."""
        with self.assertRaises(TypeError):
            arithmetic_sequence(True)

    def test_list_input(self):
        """List input should raise TypeError."""
        with self.assertRaises(TypeError):
            arithmetic_sequence([4])

    # --- format_sequence helper ---

    def test_format_n_4(self):
        """format_sequence(4) should return '2,5,8,11'."""
        self.assertEqual(format_sequence(4), "2,5,8,11")

    def test_format_n_7(self):
        """format_sequence(7) should return '2,5,8,11,14,17,20'."""
        self.assertEqual(format_sequence(7), "2,5,8,11,14,17,20")

    def test_format_n_1(self):
        """format_sequence(1) should return '2'."""
        self.assertEqual(format_sequence(1), "2")


if __name__ == "__main__":
    unittest.main()

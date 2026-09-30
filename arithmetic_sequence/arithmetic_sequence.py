# -*- coding: utf-8 -*-
"""
Arithmetic Sequence Generator
==============================

Generates an arithmetic sequence starting at 2 with a common difference of 3.

Formula:
    a(n) = 2 + (n - 1) * 3

Examples:
    >>> arithmetic_sequence(4)
    [2, 5, 8, 11]

    >>> arithmetic_sequence(7)
    [2, 5, 8, 11, 14, 17, 20]
"""

FIRST_TERM = 2
COMMON_DIFFERENCE = 3


def arithmetic_sequence(n):
    """Generate N terms of the arithmetic sequence.

    The sequence starts at 2 and increases by 3:
    2, 5, 8, 11, 14, 17, 20, ...

    Args:
        n (int): Number of terms to generate. Must be a positive integer.

    Returns:
        list[int]: A list containing N terms of the sequence.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is zero or negative.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(
            f"N must be a positive integer, got {type(n).__name__}: {n!r}"
        )
    if n <= 0:
        raise ValueError(
            f"N must be a positive integer, got {n}"
        )

    return [FIRST_TERM + (i * COMMON_DIFFERENCE) for i in range(n)]


def format_sequence(n):
    """Generate and format the sequence as a comma-separated string.

    Args:
        n (int): Number of terms to generate.

    Returns:
        str: Comma-separated string of the sequence terms.
    """
    return ",".join(str(x) for x in arithmetic_sequence(n))


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python arithmetic_sequence.py <N>")
        print("  N = number of terms (positive integer)")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
        result = format_sequence(n)
        print(result)
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)

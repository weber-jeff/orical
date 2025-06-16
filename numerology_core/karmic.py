from typing import Union, Set
from backend.services.numerology_core.utils_num import PYTHAGOREAN_MAP

class KarmicLessonCalculator:
    """
    Computes Karmic Lesson numbers from a full name.
    A Karmic Lesson exists for any digit 1–9 missing from the name.
    If none are missing, 0 is returned.
    """

    @staticmethod
    def calculate(full_name: str) -> Union[int, str]:
        """
        Returns the lowest missing number (1–9) from the name's letter-to-digit mapping.
        If all digits are present, returns 0.
        Returns a string on error (e.g., invalid input).

        Args:
            full_name (str): The person's full name.

        Returns:
            Union[int, str]: Karmic Lesson number or error string.
        """
        if not isinstance(full_name, str) or not full_name.strip():
            return "Invalid input: name must be a non-empty string."

        letters = [ch for ch in full_name.upper() if ch.isalpha()]
        if not letters:
            return "Name Required: No alphabetic characters found."

        digits_present: Set[int] = {
            PYTHAGOREAN_MAP[ch] for ch in letters if ch in PYTHAGOREAN_MAP
        }

        for digit in range(1, 10):
            if digit not in digits_present:
                return digit  # First missing digit = karmic lesson

        return 0  # All digits 1-9 are present → no karmic lesson


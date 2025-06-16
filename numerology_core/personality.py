# personality.py - Module for calculating and analyzing the Personality number
import os
import sys
from typing import Optional
from backend.services.numerology_core.utils_num import PYTHAGOREAN_MAP, reduce_number, VOWELS, normalize_name

# Ensure project root is in sys.path for imports (adjust path as needed)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


class PersonalityCalculator:
    """
    Calculates the Personality Number based on consonants in the full name.
    No meanings or external data loaded here - pure calculation only.
    """

    @staticmethod
    def calculate(full_name: str) -> Optional[int]:
        """
        Calculate Personality Number from consonants only.
        Returns None if no valid consonants are found.
        """
        normalized_name = normalize_name(full_name)
        consonant_values = [
            PYTHAGOREAN_MAP[char]
            for char in normalized_name
            if char not in VOWELS and char in PYTHAGOREAN_MAP
        ]
        if not consonant_values:
            return None

        total = sum(consonant_values)
        return reduce_number(total)


# Example usage
if __name__ == "__main__":
    name = "jeffrey allen louis weber"
    result = PersonalityCalculator.calculate(name)
    if result is None:
        print("Could not calculate Personality Number from the given name.")
    else:
        print(f"Personality Number: {result}")

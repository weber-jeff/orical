from collections import Counter
from typing import Union, Optional
from backend.services.numerology_core.utils_num import PYTHAGOREAN_MAP, reduce_number


class HiddenPassionCalculator:
    """
    Calculates the Hidden Passion number based on the most frequently occurring letters in the full name.
    """

    @staticmethod
    def calculate(full_name: str) -> Union[int, str]:
        """
        Calculate the Hidden Passion number.

        Args:
            full_name (str): Full name string (any case, may include spaces or punctuation).

        Returns:
            int: Reduced Hidden Passion number.
            str: Error message if input is invalid.
        """
        if not isinstance(full_name, str):
            return "Invalid input: name must be a string."

        # Filter and uppercase only alphabetic characters
        clean_name = ''.join(filter(str.isalpha, full_name.upper()))
        if not clean_name:
            return "No alphabetic characters in name."

        # Map letters to numerology digits
        digits = [PYTHAGOREAN_MAP.get(char) for char in clean_name if char in PYTHAGOREAN_MAP]
        if not digits:
            return "No valid numerology letters found in name."

        # Count frequencies of each digit
        frequency = Counter(digits)

        # Find digits with the highest frequency
        max_occurrence = max(frequency.values())
        most_frequent_digits = [num for num, count in frequency.items() if count == max_occurrence]

        # Sum and reduce
        hidden_passion_value = reduce_number(sum(most_frequent_digits))

        return hidden_passion_value

    @staticmethod
    def calculate_or_raise(full_name: str) -> int:
        """
        Same as calculate but raises ValueError on invalid input.

        Args:
            full_name (str): Full name string.

        Returns:
            int: Hidden Passion number.

        Raises:
            ValueError: If input is invalid or no valid letters found.
        """
        result = HiddenPassionCalculator.calculate(full_name)
        if isinstance(result, str):
            raise ValueError(result)
        return result

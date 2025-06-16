from typing import Optional

try:
    from backend.services.numerology_core.utils_num import PYTHAGOREAN_MAP, VOWELS
except ImportError:
    raise ImportError("PYTHAGOREAN_MAP and VOWELS must be defined in utils_num.")


def reduce_number(n: int) -> int:
    """
    Reduce a number to a single digit or master number (11, 22, 33).
    """
    if not isinstance(n, int):
        return 0
    n = abs(n)
    while n > 9 and n not in {11, 22, 33}:
        n = sum(int(d) for d in str(n))
    return n


class SoulUrgeCalculator:
    """
    Calculates the Soul Urge Number based on vowels in the full name.
    """

    @staticmethod
    def calculate(full_name: str) -> Optional[int]:
        """
        Calculate the Soul Urge number by summing the values of vowels in the full name.
        Returns None if input is invalid or no vowels found.

        Args:
            full_name (str): Full name string.

        Returns:
            Optional[int]: Reduced Soul Urge number or None.
        """
        if not isinstance(full_name, str) or not full_name.strip():
            return None

        total = sum(
            PYTHAGOREAN_MAP.get(ch, 0) for ch in full_name.upper() if ch in VOWELS
        )
        if total == 0:
            return None

        return reduce_number(total)


# Example usage:
if __name__ == "__main__":
    name = "Jeffrey Allen Louis Weber"
    result = SoulUrgeCalculator.calculate(name)
    if result is None:
        print("Could not calculate Soul Urge Number from the given name.")
    else:
        print(f"Soul Urge Number: {result}")

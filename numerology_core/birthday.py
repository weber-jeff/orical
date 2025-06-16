from typing import Dict
from datetime import datetime

from backend.services.numerology_core.utils_num import reduce_number


class BirthdayCalculator:
    """
    Computes birthday numerology core values from a YYYY-MM-DD birthdate string.
    No meanings are loaded — only pure number logic is returned.
    """

    @staticmethod
    def parse_birthdate(date_str: str) -> datetime:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Expected YYYY-MM-DD.")

    @classmethod
    def calculate(cls, date_str: str) -> Dict[str, int]:
        """
        Returns:
            {
                "day_of_birth": int (1–31),
                "birth_month": int (1–12),
                "birth_year": int (1–9, 11, 22, 33 if reduced),
            }
        """
        date_obj = cls.parse_birthdate(date_str)
        day = date_obj.day
        month = date_obj.month
        year = date_obj.year

        birth_year = reduce_number(year)

        return {
            "day_of_birth": day,
            "birth_month": month,
            "birth_year": birth_year
        }

    @classmethod
    def print_report(cls, date_str: str) -> str:
        data = cls.calculate(date_str)
        return "\n".join([
            "=" * 40,
            f"📅 Birthday Numerology Breakdown ({date_str})",
            "=" * 40,
            f"Day of Birth: {data['day_of_birth']}",
            f"Birth Month:  {data['birth_month']}",
            f"Birth Year: {data['birth_year']}",
            "=" * 40,
        ])

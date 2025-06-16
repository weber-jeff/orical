import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

MASTER_NUMBERS = {11, 22, 33}


class PersonalCalculator:
    """
    Calculates Personal Year, Month, and Day numbers for given birth data and target date.
    Loads personal meanings optionally but can operate meaning-free if needed.
    """

    def __init__(self, meanings_path: Optional[str] = None):
        self.meanings = {}
        if meanings_path:
            try:
                with open(meanings_path, 'r', encoding='utf-8') as f:
                    self.meanings = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                print(f"[WARN] Could not load personal meanings from {meanings_path}")

    @staticmethod
    def reduce_number(n: int, allow_master: bool = True) -> int:
        """
        Reduces a number to a single digit or master number.
        """
        while n > 9:
            if allow_master and n in MASTER_NUMBERS:
                break
            n = sum(int(d) for d in str(n))
        return n

    def get_meaning(self, number: int) -> Dict[str, Any]:
        """
        Retrieves meaning for the given number or returns a default placeholder.
        """
        meaning = self.meanings.get(str(number))
        if meaning:
            return meaning
        return {
            "title": f"Meaning for {number}",
            "description": f"No predefined meaning found for number {number}.",
            "traits": [],
            "advice": "Reflect on personal themes and observe patterns for deeper understanding."
        }

    def calculate_personal_cycle(
        self, birth_month: int, birth_day: int, target_date: datetime
    ) -> Dict[str, Dict[str, Any]]:
        """
        Calculate Personal Year, Month, and Day numbers for the given target date.

        Args:
            birth_month (int): Month of birth (1-12).
            birth_day (int): Day of birth (1-31).
            target_date (datetime): The date for which to calculate personal cycles.

        Returns:
            Dict[str, Dict]: Each key (personal_year, personal_month, personal_day) maps
                             to a dict with 'number' and 'meaning'.
        """
        personal_year = self.reduce_number(birth_month + birth_day + target_date.year)
        personal_month = self.reduce_number(personal_year + target_date.month)
        personal_day = self.reduce_number(personal_month + target_date.day)

        return {
            "personal_year": {
                "number": personal_year,
                "meaning": self.get_meaning(personal_year)
            },
            "personal_month": {
                "number": personal_month,
                "meaning": self.get_meaning(personal_month)
            },
            "personal_day": {
                "number": personal_day,
                "meaning": self.get_meaning(personal_day)
            }
        }


# Usage example:
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# MEANINGS_PATH = os.path.join(BASE_DIR, 'data', 'personal_meanings.json')
# calculator = PersonalCalculator(meanings_path=MEANINGS_PATH)
# data = calculator.calculate_personal_cycle(7, 24, datetime.now())

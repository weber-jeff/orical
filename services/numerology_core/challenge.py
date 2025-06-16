from typing import Dict, Union
from backend.services.numerology_core.utils_num import reduce_number, get_reduced_date_components


class ChallengeCalculator:
    """
    Calculates the four core numerology Challenge Numbers from a birthdate.
    Challenge 3 is considered the Main Challenge.
    """

    @staticmethod
    def _safe_reduce(value: int) -> int:
        return reduce_number(value, keep_master_as_is=False)

    @classmethod
    def calculate(cls, birth_date_str: str) -> Union[Dict[str, int], Dict[str, str]]:
        """
        Args:
            birth_date_str (str): Date string in YYYY-MM-DD format.
        
        Returns:
            dict: {
                'challenge1': int,
                'challenge2': int,
                'challenge3': int,  # Main Challenge
                'challenge4': int
            }
        """
        components = get_reduced_date_components(birth_date_str)
        if isinstance(components, str):
            return {"error": components}

        reduced_month, reduced_day, reduced_year = components

        try:
            sd_month = cls._safe_reduce(reduced_month)
            sd_day = cls._safe_reduce(reduced_day)
            sd_year = cls._safe_reduce(reduced_year)

            challenge1 = cls._safe_reduce(abs(sd_month - sd_day))
            challenge2 = cls._safe_reduce(abs(sd_day - sd_year))
            challenge3 = cls._safe_reduce(abs(challenge1 - challenge2))
            challenge4 = cls._safe_reduce(abs(sd_month - sd_year))

            return {
                "challenge1": challenge1,
                "challenge2": challenge2,
                "challenge3": challenge3,  # Main Challenge
                "challenge4": challenge4
            }

        except Exception as e:
            return {"error": f"Exception during challenge calculation: {e}"}

    @classmethod
    def print_report(cls, birth_date_str: str) -> str:
        data = cls.calculate(birth_date_str)

        if "error" in data:
            return f"[Error] {data['error']}"

        return "\n".join([
            "=" * 40,
            f"🔐 Challenge Numbers for {birth_date_str}",
            "=" * 40,
            f"Challenge 1: {data['challenge1']}",
            f"Challenge 2: {data['challenge2']}",
            f"Challenge 3 (Main): {data['challenge3']}",
            f"Challenge 4: {data['challenge4']}",
            "=" * 40
        ])

from datetime import datetime
from typing import Dict, Any, Union

from backend.services.numerology_core.utils_num import reduce_number

class LifePathCalculator:
    @staticmethod
    def _reduce_part(number_str: str) -> int:
        """Helper to reduce a date part (year, month, day) string to a single digit or master number."""
        digits_sum = sum(int(d) for d in number_str)
        return reduce_number(digits_sum)

    @staticmethod
    def _calculate(date_obj: datetime) -> int:
        # Reduce year, month, and day separately
        year_reduced = LifePathCalculator._reduce_part(str(date_obj.year))
        month_reduced = LifePathCalculator._reduce_part(f"{date_obj.month:02d}")
        day_reduced = LifePathCalculator._reduce_part(f"{date_obj.day:02d}")

        total = year_reduced + month_reduced + day_reduced
        life_path = reduce_number(total)
        return life_path

    @staticmethod
    def calculate(date_str: str) -> Union[Dict[str, Any], Dict[str, str]]:
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return {"error": f"Invalid date format: '{date_str}'. Expected YYYY-MM-DD."}

        number = LifePathCalculator._calculate(date_obj)
        return {
            "number": number,
            "is_master_number": number in {11, 22, 33},
            "date_parts": {
                "year": date_obj.year,
                "month": date_obj.month,
                "day": date_obj.day,
            },
            "original_date_str": date_str,
        }

    @staticmethod
    def print_report(date_str: str) -> str:
        result = LifePathCalculator.calculate(date_str)
        if "error" in result:
            return f"[Error] {result['error']}"

        dp = result["date_parts"]
        return "\n".join([
            "=" * 40,
            f"🌟 Life Path Report for {result['original_date_str']}",
            "=" * 40,
            f"Year reduced: {LifePathCalculator._reduce_part(str(dp['year']))}",
            f"Month reduced: {LifePathCalculator._reduce_part(f'{dp['month']:02d}')}",
            f"Day reduced: {LifePathCalculator._reduce_part(f'{dp['day']:02d}')}",
            f"Final Life Path Number: {result['number']}",
            f"Master Number: {'Yes' if result['is_master_number'] else 'No'}",
            "=" * 40,
        ])

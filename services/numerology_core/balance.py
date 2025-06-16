# backend/services/numerology_core/balance.py

from datetime import datetime
from typing import Dict, Any

from .utils_num import reduce_number



class BalanceCalculator:
    @staticmethod
    def calculate(date_str: str) -> int:
        """
        Computes the Balance Number using birth month/day and year reduction difference.
        """
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        md_reduced = reduce_number(date_obj.month + date_obj.day)
        year_reduced = reduce_number(date_obj.year)
        diff = abs(md_reduced - year_reduced)
        return reduce_number(diff)

   
        

    @staticmethod
    def format_report(date_str: str, data: Dict[str, Any]) -> str:
        """
        Generates a printable report for the balance number and its meaning.
        """
        number = data["number"]
        meaning = data["meaning"]

        report_lines = [
            "=" * 40,
            f"Balance Number Report for {date_str}",
            "=" * 40,
            f"Balance Number: {number}",
            f"Description: {meaning.get('description', 'N/A')}",
            f"Advice: {meaning.get('advice', 'N/A')}",
            f"Traits: {', '.join(meaning.get('traits', [])) or 'N/A'}",
            f"Strengths: {', '.join(meaning.get('strengths', [])) or 'N/A'}",
            f"Weaknesses: {', '.join(meaning.get('weaknesses', [])) or 'N/A'}",
            f"Element: {meaning.get('element', 'N/A')}",
            f"Color: {meaning.get('color', 'N/A')}",
            f"Business: {meaning.get('business', 'N/A')}",
            f"Relationships: {meaning.get('relationships', 'N/A')}",
            f"Purpose: {meaning.get('purpose', 'N/A')}",
            "=" * 40,
        ]
        return "\n".join(report_lines)


# Example usage for debugging or CLI testing
if __name__ == "__main__":
    test_date = "1990-06-08"
    data = BalanceCalculator.generate_data(test_date)
    print(BalanceCalculator.format_report(test_date, data))
    print(data)

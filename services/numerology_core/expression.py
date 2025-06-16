from typing import Dict, Any
from .utils_num import reduce_number, normalize_name, PYTHAGOREAN_MAP


class ExpressionCalculator:
    """
    Calculates the Expression (Destiny) Number from a full name using the Pythagorean system.
    Does not load or return any external meanings—pure calculation only.
    """

    @staticmethod
    def calculate(full_name: str) -> Dict[str, Any]:
        normalized = normalize_name(full_name)
        if not normalized:
            return {"error": "Name contains no valid letters."}

        raw_sum = sum(PYTHAGOREAN_MAP.get(char, 0) for char in normalized)
        expression_number = reduce_number(raw_sum)

        return {
            "number": expression_number,
            "is_master_number": expression_number in [11, 22, 33],
            "calculation_details": {
                "original_name": full_name,
                "normalized_name": normalized,
                "raw_sum": raw_sum
            }
        }

    @staticmethod
    def print_report(full_name: str) -> str:
        result = ExpressionCalculator.calculate(full_name)
        if "error" in result:
            return f"[Error] {result['error']}"

        details = result["calculation_details"]
        return "\n".join([
            "=" * 40,
            f"🧠 Expression Number Report for: {details['original_name']}",
            "=" * 40,
            f"Normalized Name: {details['normalized_name']}",
            f"Raw Pythagorean Sum: {details['raw_sum']}",
            f"Final Expression Number: {result['number']}",
            f"Master Number: {'Yes' if result['is_master_number'] else 'No'}",
            "=" * 40
        ])
if __name__ == "__main__":
    print(ExpressionCalculator.print_report("jeffery allen louis weber"))

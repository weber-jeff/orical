from typing import Optional

from backend.services.numerology_core.life_path import LifePathCalculator
from backend.services.numerology_core.expression import ExpressionCalculator


def reduce_number(n: int, allow_master: bool = True) -> int:
    """
    Reduce a number to a single digit or master number (11, 22, 33).
    """
    while n > 9:
        if allow_master and n in {11, 22, 33}:
            break
        n = sum(int(d) for d in str(n))
    return n


class MaturityCalculator:
    """
    Calculate the Maturity Number from full name and birthdate.
    This class only performs calculation, no meanings or reports.
    """

    @staticmethod
    def calculate(full_name: str, birthdate_str: str) -> Optional[int]:
        """
        Calculates the Maturity Number by summing Life Path and Expression numbers,
        preserving master numbers (11, 22, 33).

        Returns None if calculation fails.
        """
        life_path_num = LifePathCalculator.calculate(birthdate_str)
        if not isinstance(life_path_num, int) or life_path_num <= 0:
            return None

        expression_num = ExpressionCalculator.calculate(full_name)
        if not isinstance(expression_num, int) or expression_num <= 0:
            return None

        total = life_path_num + expression_num
        return reduce_number(total, allow_master=True)


# Example usage:
if __name__ == "__main__":
    full_name = "Jeffrey Allen Louis Weber"
    birthdate = "1970-05-12"
    maturity_num = MaturityCalculator.calculate(full_name, birthdate)
    if maturity_num is None:
        print("Maturity Number calculation failed.")
    else:
        print(f"Maturity Number: {maturity_num}")

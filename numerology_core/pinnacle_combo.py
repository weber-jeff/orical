from typing import Dict, Any


class CompoundCalculator:
    """
    Calculates compound numbers from two input numbers.
    Purely computational with strict validation.
    """

    MIN_COMPOUND = 2
    MAX_COMPOUND = 66

    @staticmethod
    def _calculate(num1: int, num2: int) -> int:
        """
        Adds two numbers and validates the result is within allowed range.

        Args:
            num1 (int): First number.
            num2 (int): Second number.

        Returns:
            int: The compound number.

        Raises:
            ValueError: If the result is outside the valid range [2, 66].
        """
        compound = num1 + num2
        if CompoundCalculator.MIN_COMPOUND <= compound <= CompoundCalculator.MAX_COMPOUND:
            return compound
        raise ValueError(f"Compound result {compound} is out of valid range ({CompoundCalculator.MIN_COMPOUND}–{CompoundCalculator.MAX_COMPOUND}).")

    @staticmethod
    def generate(num1: int, num2: int) -> Dict[str, Any]:
        """
        Generates compound number data without meanings.

        Args:
            num1 (int): First component number.
            num2 (int): Second component number.

        Returns:
            dict: Contains 'number' (compound number) and 'components' (input numbers),
                  or 'error' key with error message if invalid input or calculation fails.
        """
        try:
            compound_num = CompoundCalculator._calculate(num1, num2)
            return {
                "number": compound_num,
                "components": [num1, num2]
            }
        except ValueError as e:
            return {"error": str(e)}

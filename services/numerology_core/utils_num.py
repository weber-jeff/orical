# utils.py
from datetime import datetime
from typing import Union, Tuple
import os
import unicodedata
import re

# Pythagorean numerology letter mapping
PYTHAGOREAN_MAP = {
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9,
    "J": 1, "K": 2, "L": 3, "M": 4, "N": 5, "O": 6, "P": 7, "Q": 8, "R": 9,
    "S": 1, "T": 2, "U": 3, "V": 4, "W": 5, "X": 6, "Y": 7, "Z": 8
}

VOWELS = {"A", "E", "I", "O", "U", "Y"}  # Vowels for Soul Urge

# Define path for numerology data files relative to this file
NUMEROLOGY_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

def normalize_name(name: str) -> str:
    """
    Normalize a name string: strip spaces, remove accents/special chars, and return uppercase letters only.
    """
    name = unicodedata.normalize("NFD", name)
    name = name.encode("ascii", "ignore").decode("utf-8")  # removes accents
    name = re.sub(r"[^A-Z]", "", name.upper())  # keep only A-Z letters
    return name


def parse_birthdate(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Expected YYYY-MM-DD.")

def reduce_number(n: int, keep_master_as_is: bool = True) -> int:
    """
    Reduce a number to a single digit or keep master numbers (11, 22, 33) intact.
    """
    master_numbers = {11, 22, 33}
    if keep_master_as_is and n in master_numbers:
        return n
    while n > 9:
        n = sum(int(d) for d in str(n))
        if keep_master_as_is and n in master_numbers:
            break
    return n

def reduce_name_to_number(name: str) -> int:
    """
    Convert a normalized name to a numerology number using Pythagorean map, then reduce it.
    """
    normalized = normalize_name(name)
    total = sum(PYTHAGOREAN_MAP.get(char, 0) for char in normalized)
    return reduce_number(total)

def validate_date_format(date_str: str) -> bool:
    """
    Validate if the date string is in YYYY-MM-DD format.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def get_reduced_date_components(date_str: str) -> Union[Tuple[int, int, int], str]:
    """
    Validate date format and return tuple of (reduced_month, reduced_day, reduced_year).
    Returns error string if invalid.
    """
    if not validate_date_format(date_str):
        return "Invalid date format: Expected YYYY-MM-DD"

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        r_month = reduce_number(date_obj.month)
        r_day = reduce_number(date_obj.day)
        year_sum = sum(int(d) for d in str(date_obj.year))
        r_year = reduce_number(year_sum)
        return (r_month, r_day, r_year)
    except Exception as e:
        return f"Error reducing date components: {e}"

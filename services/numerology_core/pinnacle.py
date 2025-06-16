from datetime import datetime
from typing import Dict, List, Any, Tuple

# --- Utility: Reduce a number to single digit or master (11, 22, 33) ---
def reduce_number(n: int, is_master_check_final_step_only: bool = False) -> int:
    if not isinstance(n, int): return 0
    n = abs(n)

    if not is_master_check_final_step_only and n in {11, 22, 33}:
        return n

    while n > 9:
        if not is_master_check_final_step_only and n in {11, 22, 33}:
            break
        n = sum(int(d) for d in str(n))

    if is_master_check_final_step_only and n not in {11, 22, 33} and n > 9:
        n = sum(int(d) for d in str(n))

    return n

# --- Calculate Life Path Number ---
def calculate_life_path_number(day: int, month: int, year: int) -> Tuple[int, int]:
    r_day = reduce_number(day, is_master_check_final_step_only=True)
    r_month = reduce_number(month, is_master_check_final_step_only=True)
    r_year = reduce_number(year, is_master_check_final_step_only=True)

    total = r_day + r_month + r_year
    life_path = reduce_number(total, is_master_check_final_step_only=True) if total not in {11, 22, 33} else total

    return life_path, total

# --- Pinnacle Calculation Core ---
def calculate_pinnacle_details(day: int, month: int, year: int) -> Dict[str, Any]:
    r_day = reduce_number(day)
    r_month = reduce_number(month)
    r_year = reduce_number(year)

    life_path, _ = calculate_life_path_number(day, month, year)
    lp_duration = reduce_number(life_path, is_master_check_final_step_only=True)

    pinnacles = []

    # First Pinnacle
    inter1 = r_day + r_month
    final1 = reduce_number(inter1)
    age1 = 36 - lp_duration
    pinnacles.append({
        "number": final1,
        "intermediate_sum": inter1,
        "period": f"Birth to age {age1}"
    })

    # Second Pinnacle
    inter2 = r_day + r_year
    final2 = reduce_number(inter2)
    age2_start = age1 + 1
    age2_end = age1 + 9
    pinnacles.append({
        "number": final2,
        "intermediate_sum": inter2,
        "period": f"Age {age2_start} to {age2_end}"
    })

    # Third Pinnacle
    inter3 = final1 + final2
    final3 = reduce_number(inter3)
    age3_start = age2_end + 1
    age3_end = age2_end + 9
    pinnacles.append({
        "number": final3,
        "intermediate_sum": inter3,
        "period": f"Age {age3_start} to {age3_end}"
    })

    # Fourth Pinnacle
    inter4 = r_month + r_year
    final4 = reduce_number(inter4)
    age4_start = age3_end + 1
    pinnacles.append({
        "number": final4,
        "intermediate_sum": inter4,
        "period": f"Age {age4_start} onwards"
    })

    return {
        "life_path_number": life_path,
        "pinnacles": pinnacles
    }

# --- Primary API Function: Takes YYYY-MM-DD string and returns raw data ---
def get_pinnacle_data(birthdate_str: str) -> Dict[str, Any]:
    try:
        date_obj = datetime.strptime(birthdate_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        return {
            "error": f"Invalid birthdate format. Must be 'YYYY-MM-DD': {birthdate_str}",
            "birthdate": birthdate_str
        }

    day = date_obj.day
    month = date_obj.month
    year = date_obj.year

    result = calculate_pinnacle_details(day, month, year)
    result["birthdate"] = f"{year:04d}-{month:02d}-{day:02d}"
    return result

# --- CLI test block ---
if __name__ == "__main__":
    import sys
    test_dates = ["1987-02-16", "1990-11-11", "2000-01-01", "1975-06-25", "1963-09-07"]

    if len(sys.argv) == 2:
        test_dates = [sys.argv[1]]

    for date_str in test_dates:
        print(f"\n--- {date_str} ---")
        data = get_pinnacle_data(date_str)
        print(data)

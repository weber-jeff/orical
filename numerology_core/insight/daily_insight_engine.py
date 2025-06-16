import json
from datetime import datetime, timedelta
import math
import unicodedata
import re

# Constants and Data
PYTHAGOREAN_MAP = {
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9,
    "J": 1, "K": 2, "L": 3, "M": 4, "N": 5, "O": 6, "P": 7, "Q": 8, "R": 9,
    "S": 1, "T": 2, "U": 3, "V": 4, "W": 5, "X": 6, "Y": 7, "Z": 8
}

SUN_SIGN_DATES = [
    ("Capricorn", (12, 22), (1, 19)),
    ("Aquarius", (1, 20), (2, 18)),
    ("Pisces", (2, 19), (3, 20)),
    ("Aries", (3, 21), (4, 19)),
    ("Taurus", (4, 20), (5, 20)),
    ("Gemini", (5, 21), (6, 20)),
    ("Cancer", (6, 21), (7, 22)),
    ("Leo", (7, 23), (8, 22)),
    ("Virgo", (8, 23), (9, 22)),
    ("Libra", (9, 23), (10, 22)),
    ("Scorpio", (10, 23), (11, 21)),
    ("Sagittarius", (11, 22), (12, 21)),
]

CHAKRA_ENERGY_MAP = {
    1: "Root Chakra - grounding, stability",
    2: "Sacral Chakra - creativity, emotions",
    3: "Solar Plexus Chakra - personal power, confidence",
    4: "Heart Chakra - love, compassion",
    5: "Throat Chakra - communication, expression",
    6: "Third Eye Chakra - intuition, insight",
    7: "Crown Chakra - spirituality, enlightenment",
    8: "Root Chakra - grounding (repeat)",
    9: "Sacral Chakra - creativity (repeat)",
}

PSYCHOLOGICAL_ARCHETYPE = {
    "Aries": "The Warrior - courageous, energetic, pioneering",
    "Taurus": "The Builder - patient, reliable, practical",
    "Gemini": "The Communicator - adaptable, curious, witty",
    "Cancer": "The Nurturer - sensitive, protective, empathetic",
    "Leo": "The Leader - confident, charismatic, creative",
    "Virgo": "The Analyst - detail-oriented, thoughtful, diligent",
    "Libra": "The Diplomat - charming, balanced, fair-minded",
    "Scorpio": "The Transformer - intense, passionate, resourceful",
    "Sagittarius": "The Explorer - optimistic, independent, philosophical",
    "Capricorn": "The Strategist - disciplined, responsible, ambitious",
    "Aquarius": "The Visionary - innovative, humanitarian, original",
    "Pisces": "The Dreamer - intuitive, artistic, compassionate",
}

VOWELS = {"A", "E", "I", "O", "U", "Y"}

# Utilities

def normalize_name(name: str) -> str:
    name = unicodedata.normalize("NFD", name)
    name = name.encode("ascii", "ignore").decode("utf-8")
    name = re.sub(r"[^A-Z]", "", name.upper())
    return name

def reduce_number(n: int, keep_master_as_is: bool = True) -> int:
    master_numbers = {11, 22, 33}
    if keep_master_as_is and n in master_numbers:
        return n
    while n > 9:
        n = sum(int(d) for d in str(n))
        if keep_master_as_is and n in master_numbers:
            break
    return n

def calculate_life_path_number(birthdate: str) -> int:
    # expects YYYY-MM-DD
    dt = datetime.strptime(birthdate, "%Y-%m-%d")
    total = dt.year + dt.month + dt.day
    return reduce_number(total)

def calculate_soul_urge_number(name: str) -> int:
    normalized = normalize_name(name)
    total = 0
    for ch in normalized:
        if ch in VOWELS:
            total += PYTHAGOREAN_MAP.get(ch, 0)
    return reduce_number(total)

def calculate_sun_sign(birthdate: str) -> str:
    dt = datetime.strptime(birthdate, "%Y-%m-%d")
    month = dt.month
    day = dt.day
    for sign, start, end in SUN_SIGN_DATES:
        if (month == start[0] and day >= start[1]) or (month == end[0] and day <= end[1]) or (
            start[0] > end[0] and (month == start[0] and day >= start[1] or month == end[0] and day <= end[1])
        ):
            return sign
    # fallback if no match
    return "Unknown"

def moon_phase(date: datetime) -> float:
    """Calculate moon phase (0=new, 0.5=full) approx"""
    diff = date - datetime(2001, 1, 1)
    days = diff.days + (diff.seconds / 86400)
    lunations = days / 29.53058867
    phase = lunations % 1
    return phase

def moon_phase_name(phase: float) -> str:
    if phase < 0.03 or phase > 0.97:
        return "New Moon"
    elif phase < 0.22:
        return "Waxing Crescent"
    elif phase < 0.28:
        return "First Quarter"
    elif phase < 0.47:
        return "Waxing Gibbous"
    elif phase < 0.53:
        return "Full Moon"
    elif phase < 0.72:
        return "Waning Gibbous"
    elif phase < 0.78:
        return "Last Quarter"
    else:
        return "Waning Crescent"

def chakra_energy(life_path: int) -> str:
    # Map life path number to chakra energy (1-9)
    return CHAKRA_ENERGY_MAP.get(life_path, "Balanced Energy")

# Placeholder AI feedback mechanism
class FeedbackService:
    def __init__(self):
        self.feedback_samples = 0
        self.accuracy = 0.8  # Dummy static accuracy

    def get_learning_insights(self, sun_sign: str, life_path: int):
        # In real app: query DB or ML model feedback stats
        return {
            "total_samples": self.feedback_samples,
            "accuracy_metrics": {"overall": self.accuracy * 10}
        }

    def log_feedback(self, user_id: str, feedback: dict):
        # Save user feedback for ML training (placeholder)
        self.feedback_samples += 1
        print(f"Feedback logged for {user_id}: {feedback}")

# Core Insight Generator

class CosmicInsightGenerator:
    def __init__(self):
        self.feedback_service = FeedbackService()

    def generate_daily_insight(self, name: str, birthdate: str, target_date: str = None):
        if target_date is None:
            target_date = datetime.now().strftime("%Y-%m-%d")
        dt_target = datetime.strptime(target_date, "%Y-%m-%d")

        # Calculate numerology core
        life_path = calculate_life_path_number(birthdate)
        soul_urge = calculate_soul_urge_number(name)

        # Astrology core
        sun_sign = calculate_sun_sign(birthdate)
        moon_phase_value = moon_phase(dt_target)
        moon_phase_desc = moon_phase_name(moon_phase_value)

        # Chakra energy
        chakra_desc = chakra_energy(life_path)

        # Psychological archetype
        archetype = PSYCHOLOGICAL_ARCHETYPE.get(sun_sign, "Unique Individual")

        # Feedback data (stub)
        learning = self.feedback_service.get_learning_insights(sun_sign, life_path)

        # Compose insight text
        insights = [
            f"Your Life Path number is {life_path}, indicating your core life purpose.",
            f"Soul Urge number is {soul_urge}, representing your inner desires.",
            f"Your Sun Sign is {sun_sign} — {archetype}.",
            f"Today’s Moon Phase is '{moon_phase_desc}', affecting emotions and intuition.",
            f"Energy centers influenced: {chakra_desc}.",
            f"AI Confidence score based on feedback samples: {learning['accuracy_metrics']['overall']}/10"
        ]

        return {
            "date": target_date,
            "name": name,
            "birthdate": birthdate,
            "life_path": life_path,
            "soul_urge": soul_urge,
            "sun_sign": sun_sign,
            "moon_phase": moon_phase_desc,
            "chakra_energy": chakra_desc,
            "archetype": archetype,
            "insights": insights,
            "feedback_data": learning
        }

# Example Usage:
if __name__ == "__main__":
    name = "Alice Johnson"
    birthdate = "1990-04-15"
    target_date = datetime.now().strftime("%Y-%m-%d")

    insight_gen = CosmicInsightGenerator()
    daily_insight = insight_gen.generate_daily_insight(name, birthdate, target_date)
    print(json.dumps(daily_insight, indent=2))

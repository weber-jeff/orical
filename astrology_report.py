import logging
from collections import Counter

from astrology.core_astrology.birth_chart import generate_birth_chart
from astrology.core_astrology.constants import ZODIAC_ELEMENTS, ZODIAC_MODALITIES
from astrology.astro_data.load_meanings import MeaningLoader
from astrology.core_astrology.utils import degree_to_sign

logger = logging.getLogger(__name__)

MAJOR_PLANETS = {
    "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", 
    "Saturn", "Uranus", "Neptune", "Pluto"
}


loader = MeaningLoader()
meaning = loader.get_meaning("planet_sign_meanings", "Sun", "Taurus")


def get_dominant_trait(planet_positions: dict, trait_map: dict) -> str:
    traits = []
    for planet, data in planet_positions.items():
        if planet not in MAJOR_PLANETS:
            continue
        sign = data.get("sign")
        if sign and sign in trait_map:
            traits.append(trait_map[sign])
    if not traits:
        return "Unknown"
    return Counter(traits).most_common(1)[0][0]

def enrich_aspect_report(aspect_name: str, planets_involved: list) -> dict:
    details = loader.get_meaning("aspect_meanings", aspect_name, default={})
    if not details:
        return {"error": f"No description found for {aspect_name}."}

    return {
        "aspect": aspect_name,
        "planets": planets_involved,
        "meaning": details.get("meaning"),
        "keywords": details.get("keywords"),
        "challenges": details.get("challenges"),
        "strengths": details.get("strengths"),
        "spiritual_lesson": details.get("spiritual_lesson"),
        "archetype": details.get("archetype"),
        "relationship_effect": details.get("relationship_effect"),
        "career_effect": details.get("career_effect"),
    }

def generate_astrology_report(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    timezone_str: str,
    latitude: float,
    longitude: float
) -> dict:
    try:
        birth_chart = generate_birth_chart(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            timezone_str=timezone_str,
            lat=latitude,
            lon=longitude
        )

        # Enrich aspect report example (loop through actual aspects in real use)
        example_aspect_name = "Conjunction"
        example_planets = ["Sun", "Moon"]
        aspect_report = enrich_aspect_report(example_aspect_name, example_planets)
        birth_chart["aspect_details"] = aspect_report

        # Enrich planet-in-sign meanings for full report
        planet_in_sign = {}
        for planet, pos_data in birth_chart.get("planet_positions", {}).items():
            sign = pos_data.get("sign")
            if sign:
                meaning = loader.get_meaning("planet_sign_meanings", planet, sign, default={})
                planet_in_sign[planet] = meaning
        birth_chart["planet_sign_meanings"] = planet_in_sign

        return birth_chart

    except Exception as e:
        logger.error(f"Error in astrology report generation: {e}")
        return {"error": str(e)}
# Assuming your MeaningLoader has a method get_meaning(category, planet, sign=None)



if __name__ == "__main__":
    report = generate_astrology_report(
        year=1987,
        month=5,
        day=8,
        hour=2,
        minute=45,
        timezone_str="America/New_York",
        latitude=40.5754,
        longitude=-122.3826
    )
    import json
    print(json.dumps(report, indent=4))

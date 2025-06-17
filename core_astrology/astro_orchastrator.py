import logging
import json
from pathlib import Path
from typing import Optional, Dict
import sys
import swisseph as swe

from backend.astrology.astro_data.load_meanings import MeaningLoader
from backend.astrology.core_astrology.birth_chart import generate_birth_chart
from backend.astrology.core_astrology.utils import degree_to_sign, aspect_glyphs
sys.path.append(str(Path(__file__).resolve().parents[3]))
# Initialize the loader globally (once)
meaning_loader = MeaningLoader()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# --- Constants ---
PLANET_LIST_FOR_REPORT = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
    "Chiron": swe.CHIRON,
    "TrueNode": swe.TRUE_NODE,
}

# --- Initialize MeaningLoader ---
meaning_loader = MeaningLoader() 


# --- Format planetary longitude into degrees + sign ---
def format_longitude(lon: Optional[float]) -> str:
    if lon is None:
        return "Unknown"
    sign_name = degree_to_sign(lon)
    deg_in_sign = lon % 30
    degrees = int(deg_in_sign)
    minutes_full = (deg_in_sign - degrees) * 60
    minutes = int(minutes_full)
    seconds = int((minutes_full - minutes) * 60)
    return f"{degrees:02d}° {sign_name} {minutes:02d}'{seconds:02d}\""


# --- Main Report Generator ---
def generate_astrology_report(year: int, month: int, day: int,
                              hour: int, minute: int,
                              lon: float, lat: float,
                              ut_offset: float = 0.0,
                              alt: float = 0) -> str:
    chart_data = generate_birth_chart(
        year, month, day, hour, minute,
        timezone_str="UTC",
        lat=lat, lon=lon, alt=alt
    )

    if "error" in chart_data:
        logger.error(f"Birth chart error: {chart_data['error']}")
        return f"Error generating birth chart: {chart_data['error']}"

    planet_positions = chart_data.get("planet_positions", {})
    sun_long = planet_positions.get("Sun", {}).get("longitude")
    sun_sign = degree_to_sign(sun_long) if isinstance(sun_long, float) else "Unknown"

    # --- Meaning: Sun in Sign ---
    sun_meaning = (
        meaning_loader.get_meaning("planet_in_sign", "Sun", sun_sign)
        if meaning_loader else "Meanings unavailable."
    )
    if not sun_meaning:
        sun_meaning = f"No specific meaning available for Sun in {sun_sign}."

    moon_sign = chart_data.get("moon_sign", "Unknown")
    ascendant = chart_data.get("ascendant_longitude")
    mc_longitude = chart_data.get("mc_longitude")
    vertex_longitude = chart_data.get("vertex_longitude")

    # --- Aspect processing ---
    aspects = chart_data.get("aspects", {})
    aspect_lines = []
    for planet, aspect_list in aspects.items():
        for aspect in aspect_list:
            aspect_type = aspect.get("aspect_type")
            aspecting = aspect.get("aspecting_planet")
            orb = aspect.get("orb")
            glyph = aspect_glyphs.get(aspect_type, aspect_type)
            aspect_lines.append(f"{planet} {glyph} {aspecting} (orb: {orb:.2f})")

    # --- Compose report ---
    report_lines = [
        "📄 --- Astrology Report ---",
        f"📅 Birth Date/Time (UTC): {chart_data.get('birth_datetime_utc', 'N/A')}",
        f"📍 Location: Lat {chart_data.get('geo_location', {}).get('latitude')}, Lon {chart_data.get('geo_location', {}).get('longitude')}",
        "",
        f"🌞 Sun in {sun_sign} — {sun_meaning}",
        f"🌙 Moon in {moon_sign}",
        f"⬆️ Ascendant at {format_longitude(ascendant)}",
        f"🏔️ Midheaven at {format_longitude(mc_longitude)}",
        f"🎯 Vertex at {format_longitude(vertex_longitude)}",
        "",
        "⚡ Aspects:",
        *aspect_lines,
        "",
        "🏠 House Positions: (TODO)",
        "🪐 Planetary Archetypes: (TODO)"
    ]
    return "\n".join(report_lines)

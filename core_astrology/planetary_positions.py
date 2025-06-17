import os
import sys
import logging
from datetime import datetime
from typing import Dict, Optional, Union, List, Tuple

import pytz
import swisseph as swe

# --- Pydantic Imports (UPDATED) ---
from pydantic import BaseModel, Field, confloat, RootModel # ADDED RootModel

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

# --- Swiss Ephemeris Planet IDs ---
SWISSEPH_PLANETS = {
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
    # Optional: add nodes, Chiron, etc.
}

# --- Ephemeris Path ---
# Make sure this path points to your Swiss Ephemeris data files (.se1, .se2, etc.)
EPHEMERIS_PATH = os.getenv("SWISS_EPHE_PATH", "/media/jeff/numy/numerology_ai/backend/astrology/mp")

# --- Aspect Definitions ---
ASPECT_ANGLES = {
    "Conjunction": (0.0, 8.0),
    "Opposition": (180.0, 8.0),
    "Trine": (120.0, 6.0),
    "Square": (90.0, 6.0),
    "Sextile": (60.0, 4.0),
}

# --- Default Orb Per Planet ---
DEFAULT_PLANET_ORBS = {
    "Sun": 8.0,
    "Moon": 8.0,
    "Mercury": 6.0,
    "Venus": 6.0,
    "Mars": 6.0,
    "Jupiter": 7.0,
    "Saturn": 7.0,
    "Uranus": 5.0,
    "Neptune": 5.0,
    "Pluto": 5.0,
    "Default": 5.0,
}

# --- Rounding Constants ---
ROUND_LONGITUDE = 6
ROUND_LATITUDE = 6
ROUND_DISTANCE_AU = 8
ROUND_SPEED_LONGITUDE = 6
ROUND_ORB = 2

# ----- Pydantic Models -----

class PlanetPosition(BaseModel):
    longitude: confloat(ge=0, lt=360) = Field(
        ..., description="Ecliptic longitude in degrees", json_schema_extra={"example": 123.45}
    )
    latitude: float = Field(
        ..., description="Ecliptic latitude in degrees", json_schema_extra={"example": 5.12}
    )
    distance_au: float = Field(
        ..., description="Distance from Earth in Astronomical Units", json_schema_extra={"example": 1.0}
    )
    speed_longitude: float = Field(
        ..., description="Daily speed in longitude (degrees/day)", json_schema_extra={"example": 0.5}
    )
    sign: str = Field(
        ..., description="Zodiac sign of the planet's longitude", json_schema_extra={"example": "Leo"}
    )


# --- UPDATED PlanetPositions MODEL DEFINITION ---
class PlanetPositions(RootModel[Dict[str, PlanetPosition]]):
    # Pydantic's RootModel handles the single root value directly.
    # The type of the root value (Dict[str, PlanetPosition]) is passed as a generic argument.
    # The `__root__` field is no longer used for definition.
    # If you need to add schema metadata like description or examples for the root model itself,
    # you would typically do it via `model_config` in Pydantic v2.
    pass

class AspectDefinition(BaseModel):
    target_angle: confloat(ge=0, le=360) = Field(
        ..., description="Ideal aspect angle in degrees", json_schema_extra={"example": 0}
    )
    default_orb: confloat(gt=0) = Field(
        ..., description="Default orb allowance in degrees", json_schema_extra={"example": 8}
    )


# --- Utility Functions (previously in utils.py or inline) ---

def set_ephemeris_path(custom_ephe_path: Optional[str] = None) -> str:
    """
    Set Swiss Ephemeris data path.

    Prioritizes custom_ephe_path, then EPHEMERIS_PATH constant.
    Raises FileNotFoundError if no valid path is found.

    Args:
        custom_ephe_path: Optional custom path to ephemeris files.

    Returns:
        The effective ephemeris path used.

    Raises:
        FileNotFoundError: If a valid ephemeris directory cannot be found or set.
    """
    paths_to_try = []
    if custom_ephe_path:
        paths_to_try.append(custom_ephe_path)
    paths_to_try.append(EPHEMERIS_PATH) # Default defined in constants

    for path_attempt in paths_to_try:
        if path_attempt and os.path.isdir(path_attempt):
            try:
                swe.set_ephe_path(path_attempt)
                logger.info(f"Swiss Ephemeris path set to: {path_attempt}")
                return path_attempt
            except Exception as e: # pylint: disable=broad-except
                logger.warning(f"Could not set ephemeris path to {path_attempt} using swe.set_ephe_path: {e}")
        else:
            if path_attempt == custom_ephe_path:
                 logger.warning(f"Provided custom ephemeris path is not a valid directory: {path_attempt}")

    error_msg = (
        f"No valid Swiss Ephemeris directory found. "
        f"Tried custom path: '{custom_ephe_path}', and default: '{EPHEMERIS_PATH}'. "
        f"Please ensure ephemeris files are available and the path is correct."
    )
    logger.error(error_msg)
    raise FileNotFoundError(error_msg)


def normalize_angle(angle: float) -> float:
    """Normalize an angle to the range [0, 360)."""
    return angle % 360.0


def degree_to_sign(degree: float) -> str:
    """Convert a celestial longitude (0-360) to its zodiac sign name."""
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
    ]
    normalized_degree = normalize_angle(degree)
    index = int(normalized_degree // 30)
    return signs[index % 12]


def local_to_utc(
    year: int, month: int, day: int, hour: int, minute: int, timezone_str: str
) -> datetime:
    """
    Convert local date/time with a timezone string to a UTC datetime object.
    """
    try:
        tz = pytz.timezone(timezone_str)
    except pytz.exceptions.UnknownTimeZoneError as e:
        logger.error(f"Invalid timezone string '{timezone_str}': {e}")
        raise ValueError(f"Invalid timezone string: {timezone_str}") from e
    
    local_dt = datetime(year, month, day, hour, minute)
    try:
        localized_dt = tz.localize(local_dt, is_dst=None) 
    except (pytz.exceptions.AmbiguousTimeError, pytz.exceptions.NonExistentTimeError) as e:
        logger.error(f"Could not unambiguously localize {local_dt} to timezone '{timezone_str}': {e}. Consider providing UTC or a non-ambiguous time.")
        raise ValueError(f"Timezone localization failed for {local_dt} in {timezone_str}: {e}") from e
        
    return localized_dt.astimezone(pytz.utc)


def calculate_julian_day_utc(dt_utc: datetime) -> float:
    """
    Calculate Julian Day (UT) from a UTC datetime object.
    """
    if dt_utc.tzinfo is None or dt_utc.tzinfo.utcoffset(dt_utc) != pytz.utc.utcoffset(None):
        raise ValueError("Input datetime must be UTC.")
    
    jd_ut = swe.julday(
        dt_utc.year,
        dt_utc.month,
        dt_utc.day,
        dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0,
    )
    return jd_ut

# --- Core Astrological Calculation Functions ---

def calculate_planet_positions(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    latitude_deg: float,
    longitude_deg: float,
    altitude_m: float = 0.0,
    timezone_str: Optional[str] = None,
    ephe_path_override: Optional[str] = None,
    flags: int = swe.FLG_SWIEPH | swe.FLG_SPEED,
) -> Dict[str, Dict[str, Union[float, str]]]:
    """
    Calculate positions of planets for a given datetime and location.

    Args:
        year, month, day, hour, minute: Date and time.
            If timezone_str is provided, this is treated as local time.
            If timezone_str is None, this is treated as UTC.
        latitude_deg, longitude_deg: Geographic coordinates in degrees.
        altitude_m: Altitude in meters above sea level.
        timezone_str: Timezone name (e.g., 'America/New_York'). If None, UTC is assumed.
        ephe_path_override: Optional path to ephemeris files, overriding the default.
        flags: Swiss Ephemeris calculation flags.

    Returns:
        A dictionary where keys are planet names and values are dictionaries
        containing 'longitude', 'latitude', 'distance_au', 'speed_longitude', 'sign'.
        Returns a dictionary with an 'error' key on failure.
    """
    try:
        # Ensure ephemeris path is set. This will raise FileNotFoundError if unsuccessful.
        effective_ephe_path = set_ephemeris_path(ephe_path_override)

        if timezone_str:
            dt_utc = local_to_utc(year, month, day, hour, minute, timezone_str)
            jd_ut = calculate_julian_day_utc(dt_utc)
        else:
            # Assume UTC if no timezone_str is provided
            jd_ut = swe.julday(year, month, day, hour + minute / 60.0)

        # Set observer's location for topocentric calculations
        swe.set_topo(longitude_deg, latitude_deg, altitude_m)

        positions: Dict[str, Dict[str, Union[float, str]]] = {}
        for name, planet_id in SWISSEPH_PLANETS.items():

            pos_data, return_flag = swe.calc_ut(jd_ut, planet_id, flags)

            if return_flag < 0 or not pos_data or len(pos_data) < 6: # Speed flag adds more elements
                error_msg = (
                    f"Failed to calculate position for {name}. "
                    f"Swiss Ephemeris error flag: {return_flag}. "
                    f"Ensure ephemeris files at '{effective_ephe_path}' are complete and accessible for the given date."
                )
                logger.error(error_msg)
                positions[name] = {"error": f"Calculation failed, flag: {return_flag}"}
                continue

            longitude = normalize_angle(pos_data[0])
            positions[name] = {
                "longitude": round(longitude, ROUND_LONGITUDE),
                "latitude": round(pos_data[1], ROUND_LATITUDE),
                "distance_au": round(pos_data[2], ROUND_DISTANCE_AU),
                "speed_longitude": round(pos_data[3], ROUND_SPEED_LONGITUDE),
                "sign": degree_to_sign(longitude),
            }

        if not positions:
            return {"error": "No planetary positions could be calculated. Check logs for details."}
        
        if any("error" in data for data in positions.values()):
             logger.warning("Some planet positions could not be calculated. See previous errors.")

        return positions

    except FileNotFoundError as e:
        logger.critical(f"Ephemeris path setup failed: {e}")
        return {"error": f"Ephemeris path setup failed: {e}"}
    except ValueError as e:
        logger.error(f"Date/Time/Timezone conversion error: {e}")
        return {"error": f"Date/Time/Timezone conversion error: {e}"}
    except Exception as e:
        logger.exception("Unexpected exception in calculate_planet_positions:")
        return {"error": f"An unexpected error occurred: {e}"}


def calculate_aspects(
    planet_positions: Dict[str, Dict[str, Union[float, str]]],
    aspect_definitions: Optional[Dict[str, Tuple[float, float]]] = None,
    planet_orbs: Optional[Dict[str, float]] = None,
) -> Dict[str, List[Dict[str, Union[str, float]]]]:
    """
    Calculate aspects between planets based on their longitudes.

    Args:
        planet_positions: Dictionary of planet positions (must contain 'longitude').
        aspect_definitions: Custom aspect angles and their type-specific orbs.
                            Defaults to ASPECT_ANGLES.
        planet_orbs: Custom orbs for individual planets. Defaults to DEFAULT_PLANET_ORBS.

    Returns:
        A dictionary where keys are planet names, and values are lists of aspects
        that planet makes, each aspect being a dictionary with
        'aspecting_planet', 'aspect_type', and 'orb'.
    """
    if aspect_definitions is None:
        aspect_definitions = ASPECT_ANGLES
    if planet_orbs is None:
        planet_orbs = DEFAULT_PLANET_ORBS

    aspects_found: Dict[str, List[Dict[str, Union[str, float]]]] = {
        planet: [] for planet in planet_positions if "longitude" in planet_positions[planet]
    }
    
    valid_planets = [
        p_name for p_name, p_data in planet_positions.items() 
        if isinstance(p_data.get("longitude"), (int, float))
    ]

    for i in range(len(valid_planets)):
        for j in range(i + 1, len(valid_planets)):
            p1_name = valid_planets[i]
            p2_name = valid_planets[j]

            p1_lon = planet_positions[p1_name]["longitude"]
            p2_lon = planet_positions[p2_name]["longitude"]

            if not (isinstance(p1_lon, (float, int)) and isinstance(p2_lon, (float, int))):
                logger.warning(f"Skipping aspect between {p1_name} and {p2_name} due to missing/invalid longitude.")
                continue

            angular_separation = abs(p1_lon - p2_lon)
            angular_separation = min(angular_separation, 360.0 - angular_separation) # Shortest arc

            orb_p1 = planet_orbs.get(p1_name, planet_orbs.get("Default", 5.0))
            orb_p2 = planet_orbs.get(p2_name, planet_orbs.get("Default", 5.0))

            for aspect_name, (target_angle, aspect_type_orb) in aspect_definitions.items():
                effective_orb = min(aspect_type_orb, (orb_p1 + orb_p2) / 2.0)

                if abs(angular_separation - target_angle) <= effective_orb:
                    exact_orb_value = round(abs(angular_separation - target_angle), ROUND_ORB)
                    
                    aspect_info_p1 = {
                        "aspecting_planet": p2_name,
                        "aspect_type": aspect_name,
                        "orb": exact_orb_value,
                    }
                    aspect_info_p2 = {
                        "aspecting_planet": p1_name,
                        "aspect_type": aspect_name,
                        "orb": exact_orb_value,
                    }
                    if p1_name in aspects_found:
                         aspects_found[p1_name].append(aspect_info_p1)
                    if p2_name in aspects_found:
                         aspects_found[p2_name].append(aspect_info_p2)
    return aspects_found


def assign_planets_to_houses(
    planet_positions: Dict[str, Dict[str, Union[float, str]]],
    house_cusps_deg: List[float],
    house_system_name: str = "WholeSign",
) -> Dict[str, Union[int, str]]:
    """
    Assign planets to astrological houses based on their longitudes and house cusps.

    Args:
        planet_positions: Dictionary of planet positions (must contain 'longitude').
        house_cusps_deg: A list of 12 floats representing house cusp longitudes in degrees,
                         starting with the 1st house cusp (Ascendant).
        house_system_name: Name of the house system used (e.g., "WholeSign", "Placidus").

    Returns:
        A dictionary mapping planet names to their house number (1-12) or "Unknown".
        Returns a dictionary with 'error' key on critical failure.
    """
    if len(house_cusps_deg) != 12:
        msg = f"Invalid number of house cusps: {len(house_cusps_deg)}. Expected 12."
        logger.error(msg)
        return {"error": msg}

    normalized_cusps = [normalize_angle(cusp) for cusp in house_cusps_deg]

    planet_house_assignments: Dict[str, Union[int, str]] = {}

    for planet_name, p_data in planet_positions.items():
        planet_lon = p_data.get("longitude")

        if not isinstance(planet_lon, (float, int)):
            logger.warning(
                f"Longitude missing or invalid for planet {planet_name}. Cannot assign house."
            )
            planet_house_assignments[planet_name] = "Unknown (No Longitude)"
            continue
        
        planet_lon = normalize_angle(planet_lon)
        assigned_house: Union[int, str] = "Unknown (Logic Error)"


        if house_system_name.lower() == "wholesign":
            # For Whole Sign, the first cusp (Ascendant's longitude) defines the starting point.
            # Each house is a 30-degree segment from this starting point.
            # E.g., if ASC is 15 Leo (135 deg), 1st house is 135-165, 2nd 165-195 etc.
            # This implements a "sign-based" Whole Sign if `normalized_cusps[0]` is 0 degrees of the ASC sign.
            # Or a "degree-based" Whole Sign if `normalized_cusps[0]` is the exact ASC degree.
            # The example uses "degree-based" logic, which matches the function's internal calculation.
            asc_lon_for_ws_reference = normalized_cusps[0] 
            
            # Calculate how many 30-degree segments the planet is from the reference point
            relative_longitude = normalize_angle(planet_lon - asc_lon_for_ws_reference)
            house_number = int(relative_longitude // 30) + 1
            assigned_house = house_number
        else:
            # Generic logic for cusp-based systems (Placidus, Koch, etc.)
            for i in range(12):
                cusp_start = normalized_cusps[i]
                cusp_end = normalized_cusps[(i + 1) % 12] 

                if cusp_start <= cusp_end: 
                    if cusp_start <= planet_lon < cusp_end:
                        assigned_house = i + 1
                        break
                else: # Wrap-around case (house crosses 0° Aries)
                    if planet_lon >= cusp_start or planet_lon < cusp_end:
                        assigned_house = i + 1
                        break
            if assigned_house == "Unknown (Logic Error)" and i == 11 :
                 logger.error(f"Planet {planet_name} at {planet_lon}° could not be assigned to a house with cusps: {normalized_cusps} using {house_system_name} system.")

        planet_house_assignments[planet_name] = assigned_house
    return planet_house_assignments


# --- Example Main Usage ---
if __name__ == "__main__":
    try:
        logger.info("--- Starting Astrological Calculations Example ---")
        
        # Example: Calculate for a specific date, time, and location
        target_year = 1987
        target_month = 5
        target_day = 8
        target_hour = 2
        target_minute = 45
        # New York City coordinates
        observer_lat = 40.5754
        observer_lon = -122.3836
        observer_alt = 151.0 # Altitude in meters
        tz_string = "America/Los_Angeles" # Use a valid timezone string

        logger.info(
            f"Calculating positions for: {target_year}-{target_month:02d}-{target_day:02d} "
            f"{target_hour:02d}:{target_minute:02d} {tz_string} "
            f"at Lat {observer_lat}, Lon {observer_lon}"
        )

        planet_positions_result = calculate_planet_positions(
            target_year, target_month, target_day, target_hour, target_minute,
            observer_lat, observer_lon, observer_alt,
            timezone_str=tz_string,
            # ephe_path_override="/path/to/my/ephe" # Optionally override here
        )

        if "error" in planet_positions_result:
            logger.error(f"Failed to calculate planet positions: {planet_positions_result['error']}")
        else:
            print("\n--- Planet Positions ---")
            for planet_name, data_dict in planet_positions_result.items():
                if "error" in data_dict:
                     print(f"  {planet_name:<10}: {data_dict['error']}")
                elif isinstance(data_dict, dict):
                    lon = data_dict.get('longitude', 'N/A')
                    lat = data_dict.get('latitude', 'N/A')
                    sign = data_dict.get('sign', 'N/A')
                    speed = data_dict.get('speed_longitude', 'N/A')
                    retro = "R" if isinstance(speed, (float,int)) and speed < 0 else ""
                    print(f"  {planet_name:<10}: Lon={lon:>8}° {str(sign):<11} Lat={lat:>8}° Speed={speed:>8}°/day {retro}")
                else:
                    print(f"  {planet_name:<10}: Invalid data format.")


            # --- House Calculation (Dynamic based on chart data) ---
            jd_for_houses = swe.julday(target_year, target_month, target_day, target_hour + target_minute / 60.0)
            if tz_string: 
                dt_utc_for_houses = local_to_utc(target_year, target_month, target_day, target_hour, target_minute, tz_string)
                jd_for_houses = calculate_julian_day_utc(dt_utc_for_houses)

            # Calculate Placidus houses to get the actual Ascendant for the given chart
            _cusps, ascmc = swe.houses(jd_for_houses, observer_lat, observer_lon, b'P')
            actual_asc_lon = normalize_angle(ascmc[0])
            actual_mc_lon = normalize_angle(ascmc[1])
            logger.info(f"\nCalculated Ascendant (Placidus): {actual_asc_lon:.2f}° ({degree_to_sign(actual_asc_lon)})")
            logger.info(f"Calculated Midheaven (Placidus): {actual_mc_lon:.2f}° ({degree_to_sign(actual_mc_lon)})")

            # For Traditional Whole Sign Houses:
            # The 1st house begins at 0 degrees of the sign that contains the Ascendant.
            traditional_ws_start_cusp = (actual_asc_lon // 30) * 30.0 
            
            # Generate the 12 cusps for the `assign_planets_to_houses` function for traditional Whole Sign.
            # The function's "WholeSign" logic uses the first provided cusp as the reference point for segments.
            traditional_whole_sign_cusps_input = [normalize_angle(traditional_ws_start_cusp + 30.0 * i) for i in range(12)]

            print(f"\n--- Planet House Assignments (Traditional Whole Sign, 1st house = {degree_to_sign(traditional_ws_start_cusp)}) ---")
            house_assignments = assign_planets_to_houses(
                planet_positions_result,
                traditional_whole_sign_cusps_input, 
                house_system_name="WholeSign" 
            )
            if "error" in house_assignments:
                logger.error(f"House assignment failed: {house_assignments['error']}")
            else:
                for planet_name, house_num in house_assignments.items():
                    print(f"  {planet_name:<10}: House {house_num}")

            # --- Aspect Calculation ---
            print("\n--- Aspects ---")
            aspect_results = calculate_aspects(planet_positions_result)
            for planet_name, aspect_list in aspect_results.items():
                if aspect_list: 
                    print(f"  {planet_name}:")
                    for aspect_detail in aspect_list:
                        print(
                            f"    - {aspect_detail['aspect_type']} with "
                            f"{aspect_detail['aspecting_planet']} "
                            f"(orb: {aspect_detail['orb']:.2f}°)"
                        )
        
        logger.info("\n--- Astrological Calculations Example Finished ---")

    except FileNotFoundError as e:
        logger.critical(f"CRITICAL: Ephemeris files not found. Please check configuration. Error: {e}")
        print(f"Error: Ephemeris files not found. Please ensure SWISS_EPHE_PATH is set correctly or ephemeris files are at {EPHEMERIS_PATH}")
    except Exception as e:
        logger.critical(f"An unhandled error occurred in main execution: {e}", exc_info=True)
        print(f"An unexpected error occurred: {e}")
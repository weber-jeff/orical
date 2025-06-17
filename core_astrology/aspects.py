from typing import Dict, List, Optional
import logging

from pydantic import BaseModel, Field, RootModel

from .constants import ASPECT_ANGLES, DEFAULT_ASPECT_ORB, ROUNDING_PRECISION

logger = logging.getLogger(__name__)

# ----- Pydantic Models -----

class PlanetPosition(BaseModel):
    longitude: float = Field(
        ...,
        ge=0,
        lt=360,
        description="Ecliptic longitude in degrees"
    )

class PlanetPositions(RootModel[Dict[str, PlanetPosition]]):
    pass

class AspectDefinition(BaseModel):
    target_angle: float = Field(..., ge=0, le=360)
    default_orb: float = Field(..., gt=0)

class AspectDefinitions(RootModel[Dict[str, AspectDefinition]]):
    pass

class AspectData(BaseModel):
    aspecting_planet: str = Field(..., description="Planet forming the aspect")
    aspect_type: str = Field(..., description="Type of the aspect")
    orb: float = Field(..., description="Orb difference in degrees")
    exact_angle_diff: float = Field(..., description="Exact angle difference in degrees")

class AspectsFound(RootModel[Dict[str, List[AspectData]]]):
    pass

class HousesAssigned(RootModel[Dict[str, int]]):
    pass

# ----- Helper Functions -----

def normalize_angle(angle: float) -> float:
    return angle % 360

def shortest_angle_diff(a1: float, a2: float) -> float:
    diff = abs(a1 - a2)
    return min(diff, 360 - diff)

# ----- Main Logic -----

def calculate_aspects(
    planet_positions: PlanetPositions,
    aspect_definitions: Optional[AspectDefinitions] = None,
    planet_orbs: Optional[Dict[str, float]] = None,
    single_aspect_per_pair: bool = False,
) -> AspectsFound:
    aspect_definitions = aspect_definitions or AspectDefinitions(__root__=ASPECT_ANGLES)
    planet_orbs = planet_orbs or DEFAULT_ASPECT_ORB

    aspects_found: Dict[str, List[AspectData]] = {planet: [] for planet in planet_positions.model_dump().keys()}
    planets = list(planet_positions.model_dump().keys())

    for i in range(len(planets)):
        for j in range(i + 1, len(planets)):
            p1, p2 = planets[i], planets[j]
            p1_lon = planet_positions.model_dump()[p1].longitude
            p2_lon = planet_positions.model_dump()[p2].longitude

            angle_diff = shortest_angle_diff(p1_lon, p2_lon)
            orb1 = planet_orbs.get(p1, planet_orbs.get("Default", 6))
            orb2 = planet_orbs.get(p2, planet_orbs.get("Default", 6))

            matched_aspects = []
            for aspect_name, aspect_def in aspect_definitions.model_dump().items():
                weighted_orb = min(aspect_def.default_orb, (orb1 + orb2) / 2)
                orb_diff = abs(angle_diff - aspect_def.target_angle)

                if orb_diff <= weighted_orb:
                    orb = round(orb_diff, 2)  # Hardcoded rounding precision
                    aspect_data = AspectData(
                        aspecting_planet=p2,
                        aspect_type=aspect_name,
                        orb=orb,
                        exact_angle_diff=round(angle_diff, 3),  # Hardcoded precision
                    )
                    matched_aspects.append(aspect_data)
                    if single_aspect_per_pair:
                        break

            if matched_aspects:
                if single_aspect_per_pair and len(matched_aspects) > 1:
                    matched_aspects.sort(key=lambda x: x.orb)
                    matched_aspects = [matched_aspects[0]]

                for aspect_data in matched_aspects:
                    aspects_found[p1].append(aspect_data)
                    mirrored = AspectData(
                        aspecting_planet=p1,
                        aspect_type=aspect_data.aspect_type,
                        orb=aspect_data.orb,
                        exact_angle_diff=aspect_data.exact_angle_diff,
                    )
                    aspects_found[p2].append(mirrored)

    return AspectsFound(__root__=aspects_found)

def assign_planets_to_houses(
    planet_positions: PlanetPositions,
    house_cusps: List[float]
) -> HousesAssigned:
    houses: Dict[str, int] = {}
    for planet, position in planet_positions.model_dump().items():
        lon = normalize_angle(position.longitude)
        for i in range(12):
            start = normalize_angle(house_cusps[i])
            end = normalize_angle(house_cusps[(i + 1) % 12])
            if start < end:
                if start <= lon < end:
                    houses[planet] = i + 1
                    break
            else:
                if lon >= start or lon < end:
                    houses[planet] = i + 1
                    break
    return HousesAssigned(__root__=houses)
if __name__ == "__main__":
    print("Aspects module loaded successfully.")
    # Optionally add minimal test/demo calls here

if __name__ == "__main__":
    print("Aspects module loaded successfully.")

    # Sample planet positions (ecliptic longitudes in degrees)
    sample_positions = {
        "Sun": {"longitude": 10.0},
        "Moon": {"longitude": 40.0},
        "Mercury": {"longitude": 70.0},
    }

    # Create PlanetPositions instance
    planet_positions = PlanetPositions.parse_obj(sample_positions)

    # Use default aspect definitions and orbs (assuming imported constants)
    try:
        aspects_found = calculate_aspects(planet_positions)
    except Exception as e:
        print(f"Error calculating aspects: {e}")
    else:
        # Print results
        for planet, aspects in aspects_found.__root__.items():
            print(f"\nAspects found for {planet}:")
            if not aspects:
                print("  None")
            for aspect in aspects:
                print(
                    f"  Aspect with {aspect.aspecting_planet}: "
                    f"{aspect.aspect_type} (orb: {aspect.orb}, exact angle difference: {aspect.exact_angle_diff})"
                )

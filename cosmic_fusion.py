# services/cosmic_fusion.py

from typing import Dict, Any
from services.astrology_service import AstrologyService
from services.numerology_service import NumerologyService
#from services.feedback_service import FeedbackService
from datetime import datetime
import math

class CosmicFusionService:

    @staticmethod
    def normalize(value: float) -> float:
        return max(0, min(10, value))

    @staticmethod
    def generate_cosmic_profile(sun_sign: str, destiny: int, soul_urge: int, personality: int, life_path: int, birthday: int) -> Dict:
        key_traits = {
            "destiny": destiny,
            "soulUrge": soul_urge,
            "personality": personality
        }

        archetype_summary = AstrologyService.get_archetype_summary(sun_sign)

        love_energy = destiny * 0.4 + personality * 0.4 + AstrologyService.get_love_influence(sun_sign) * 0.2
        career_energy = destiny * 0.5 + soul_urge * 0.3 + AstrologyService.get_career_influence(sun_sign) * 0.2
        health_energy = personality * 0.5 + AstrologyService.get_health_influence(sun_sign) * 0.5
        finance_energy = destiny * 0.6 + soul_urge * 0.2 + AstrologyService.get_finance_influence(sun_sign) * 0.2
        spiritual_energy = soul_urge * 0.5 + AstrologyService.get_spiritual_influence(sun_sign) * 0.5

        energy_vectors = {
            "love": CosmicFusionService.normalize(love_energy),
            "career": CosmicFusionService.normalize(career_energy),
            "health": CosmicFusionService.normalize(health_energy),
            "finance": CosmicFusionService.normalize(finance_energy),
            "spiritual": CosmicFusionService.normalize(spiritual_energy),
        }

        energy_vectors["overall"] = CosmicFusionService.normalize(
            sum(energy_vectors.values()) / 5
        )

        birthday_factor = birthday % 10
        cosmic_alignment = CosmicFusionService.normalize(
            (energy_vectors["overall"] + birthday_factor) / 2
        )

        return {
            "fusedInsights": {
                "cosmicAlignment": cosmic_alignment,
                "archetypeSummary": archetype_summary,
                "keyTraits": key_traits,
                "energyVectors": energy_vectors
            },
            "sunSign": sun_sign,
            "numerologyCore": key_traits,
            "birthday": birthday
        }

    @staticmethod
    def generate_enhanced_daily_insight(cosmic_profile: Dict, target_date: str, learning_insights: Dict[str, Any]) -> Dict:
        base = cosmic_profile["fusedInsights"]["energyVectors"]
        sun_sign = cosmic_profile["sunSign"]
        destiny = cosmic_profile["numerologyCore"]["destiny"]

        date = datetime.strptime(target_date, "%Y-%m-%d")
        transits = CosmicFusionService.get_transit_modifiers(sun_sign, date)
        numerology_mods = CosmicFusionService.get_numerology_cycle_modifiers(destiny, date)

        confidence_weight = min(1, learning_insights.get("accuracy_metrics", {}).get("overall", 7) / 10)

        def combined(base_val, transit_mod, num_mod):
            return CosmicFusionService.normalize(
                base_val * (1 - confidence_weight) + ((transit_mod + num_mod) / 2) * confidence_weight
            )

        energy_readings = {
            "overall": combined(base["overall"], transits["overall"], numerology_mods["overall"]),
            "love": combined(base["love"], transits["love"], numerology_mods["love"]),
            "career": combined(base["career"], transits["career"], numerology_mods["career"]),
            "health": combined(base["health"], transits["health"], numerology_mods["health"]),
            "finance": combined(base["finance"], transits["finance"], numerology_mods["finance"]),
        }

        manifestation_power = round((energy_readings["overall"] * 0.6 + base["spiritual"] * 0.4) * confidence_weight)
        spiritual_focus = CosmicFusionService.get_spiritual_focus_message(base["spiritual"])
        optimal_activities = CosmicFusionService.get_optimal_activities(energy_readings)
        caution_areas = CosmicFusionService.get_caution_areas(energy_readings)

        return {
            "energyReadings": energy_readings,
            "manifestationPower": manifestation_power,
            "spiritualFocus": spiritual_focus,
            "optimalActivities": optimal_activities,
            "cautionAreas": caution_areas,
            "cosmicInfluences": [
                f"Your sun sign {sun_sign} supports new beginnings today.",
                f"Numerology destiny number {destiny} encourages persistence and focus."
            ],
            "personalizedGuidance": [
                "Stay open to unexpected opportunities.",
                "Practice mindfulness to enhance clarity."
            ]
        }

    @staticmethod
    def get_transit_modifiers(sun_sign: str, date: datetime) -> Dict[str, float]:
        day = date.day
        return {
            "overall": 5 + math.sin(day) * 2,
            "love": 5 + math.cos(day) * 2,
            "career": 5 + math.sin(day / 2) * 2,
            "health": 5 + math.cos(day / 3) * 2,
            "finance": 5 + math.sin(day / 4) * 2,
        }

    @staticmethod
    def get_numerology_cycle_modifiers(destiny: int, date: datetime) -> Dict[str, float]:
        day = date.day
        mod = 1 if day % 2 == 0 else -1
        base = 5
        return {
            "overall": base + mod,
            "love": base + mod * 0.8,
            "career": base + mod * 0.9,
            "health": base + mod * 0.7,
            "finance": base + mod * 0.85,
        }

    @staticmethod
    def get_spiritual_focus_message(spiritual_energy: float) -> str:
        if spiritual_energy >= 8:
            return "High spiritual awareness; ideal for meditation and inner work."
        elif spiritual_energy >= 5:
            return "Balanced spiritual energy; practice gratitude."
        elif spiritual_energy >= 3:
            return "Low spiritual energy; focus on grounding activities."
        else:
            return "Minimal spiritual energy today; prioritize rest and recuperation."

    @staticmethod
    def get_optimal_activities(energies: Dict[str, float]) -> list:
        activities = []
        if energies["overall"] >= 7:
            activities.append("Initiate new projects")
        if energies["love"] >= 7:
            activities.extend(["Romantic engagements", "Social bonding"])
        if energies["career"] >= 7:
            activities.extend(["Career advancement tasks", "Networking"])
        if energies["health"] >= 7:
            activities.extend(["Physical exercise", "Wellness activities"])
        if energies["finance"] >= 7:
            activities.extend(["Financial planning", "Investments"])
        return activities or ["Rest and reflection"]

    @staticmethod
    def get_caution_areas(energies: Dict[str, float]) -> list:
        cautions = []
        if energies["overall"] <= 3:
            cautions.extend(["Avoid big decisions", "Rest more"])
        if energies["love"] <= 3:
            cautions.append("Avoid relationship conflicts")
        if energies["career"] <= 3:
            cautions.append("Delay negotiations")
        if energies["health"] <= 3:
            cautions.append("Prioritize recovery")
        if energies["finance"] <= 3:
            cautions.append("Avoid risky financial moves")
        return cautions or ["Maintain balance and focus"]

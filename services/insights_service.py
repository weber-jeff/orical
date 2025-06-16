from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import asyncio

# Assume these are your existing Python service modules with corresponding methods
from services.astrology import AstrologyService
from services.numerology_core.numerology_service import NumerologyService
from services.feedback import FeedbackService
from services.cosmic_fusion import CosmicFusionService

class InsightsService:

    @staticmethod
    async def generate_daily_insight(
        sun_sign: str,
        life_path_number: int,
        target_date: str
    ) -> Dict[str, Any]:
        date = datetime.fromisoformat(target_date)
        day_of_year = (date - datetime(date.year, 1, 1)).days + 1

        # Async call to get learning insights
        learning_insights = await FeedbackService.get_learning_insights(sun_sign, life_path_number)

        # Generate cosmic profile with simplified repeated life path number usage
        cosmic_profile = CosmicFusionService.generate_cosmic_profile(
            sun_sign=sun_sign,
            life_path_number=life_path_number,
            destiny_number=life_path_number,
            soul_urge_number=life_path_number,
            personality_number=life_path_number,
            birth_day=date.day
        )

        # Generate enhanced daily insight
        enhanced_insights = CosmicFusionService.generate_enhanced_daily_insight(
            cosmic_profile=cosmic_profile,
            target_date=target_date,
            learning_insights=learning_insights
        )

        # Extract energy readings
        energy = enhanced_insights.get("energyReadings", {})
        overall_energy = energy.get("overall", 0)
        love_energy = energy.get("love", 0)
        career_energy = energy.get("career", 0)
        health_energy = energy.get("health", 0)
        finance_energy = energy.get("finance", 0)

        # Compose key insights
        key_insights = []
        key_insights.extend(enhanced_insights.get("cosmicInfluences", [])[:2])
        key_insights.extend(enhanced_insights.get("personalizedGuidance", [])[:2])
        key_insights.append(f"Manifestation power: {enhanced_insights.get('manifestationPower', 0)}/10")
        key_insights.append(f"Spiritual focus: {enhanced_insights.get('spiritualFocus', '')}")

        # Activities, fallback to traditional if empty
        favorable_activities = enhanced_insights.get("optimalActivities", [])
        avoid_activities = enhanced_insights.get("cautionAreas", [])

        if not favorable_activities:
            favorable_activities = InsightsService.get_favorable_activities(overall_energy, love_energy, career_energy)

        if not avoid_activities:
            avoid_activities = InsightsService.get_avoid_activities(overall_energy, love_energy, career_energy)

        return {
            "overall_energy": overall_energy,
            "love_energy": love_energy,
            "career_energy": career_energy,
            "health_energy": health_energy,
            "finance_energy": finance_energy,
            "favorable_activities": favorable_activities,
            "avoid_activities": avoid_activities,
            "key_insights": key_insights
        }

    @staticmethod
    def get_favorable_activities(overall: int, love: int, career: int) -> List[str]:
        activities = []
        if overall >= 7:
            activities.append("Starting new projects")
        if love >= 7:
            activities.extend(["Romantic dates", "Relationship conversations"])
        if career >= 7:
            activities.extend(["Job interviews", "Business meetings", "Networking"])
        if overall >= 6:
            activities.append("Creative pursuits")
        if love >= 6:
            activities.append("Social gatherings")
        if career >= 6:
            activities.append("Important decisions")
        return activities if activities else ["Meditation", "Self-reflection"]

    @staticmethod
    def get_avoid_activities(overall: int, love: int, career: int) -> List[str]:
        activities = []
        if overall <= 3:
            activities.extend(["Major life changes", "Risky investments"])
        if love <= 3:
            activities.extend(["Difficult conversations", "Confrontations"])
        if career <= 3:
            activities.extend(["Negotiations", "Signing contracts"])
        if overall <= 4:
            activities.extend(["Travel", "Public speaking"])
        return activities if activities else ["Avoid overthinking"]

    @staticmethod
    async def generate_activity_recommendation(
        activity_type: str,
        sun_sign: str,
        life_path_number: int,
        days_ahead: int = 30
    ) -> Dict[str, Any]:
        today = datetime.now()

        learning_insights = await FeedbackService.get_learning_insights(sun_sign, life_path_number)

        cosmic_profile = CosmicFusionService.generate_cosmic_profile(
            sun_sign=sun_sign,
            life_path_number=life_path_number,
            destiny_number=life_path_number,
            soul_urge_number=life_path_number,
            personality_number=life_path_number,
            birth_day=today.day
        )

        best_score = 0.0
        best_date_str = ""
        best_reasoning = ""

        for i in range(days_ahead):
            check_date = today + timedelta(days=i)
            date_str = check_date.date().isoformat()

            enhanced_insights = CosmicFusionService.generate_enhanced_daily_insight(
                cosmic_profile=cosmic_profile,
                target_date=date_str,
                learning_insights=learning_insights
            )

            energy = enhanced_insights.get("energyReadings", {})
            manifestation_power = enhanced_insights.get("manifestationPower", 0)

            score = 0.0
            reasoning = ""

            if activity_type == "wedding":
                score = energy.get("love", 0) * 0.4 + energy.get("overall", 0) * 0.3 + manifestation_power * 0.3
                reasoning = f"Love energy ({energy.get('love', 0)}/10) and manifestation power ({manifestation_power}/10) create ideal conditions for union and celebration"
            elif activity_type == "business_launch":
                score = energy.get("career", 0) * 0.4 + energy.get("finance", 0) * 0.3 + energy.get("overall", 0) * 0.2 + manifestation_power * 0.1
                reasoning = f"Career energy ({energy.get('career', 0)}/10) and financial energy ({energy.get('finance', 0)}/10) align for business success"
            elif activity_type == "travel":
                score = energy.get("overall", 0) * 0.5 + energy.get("health", 0) * 0.3 + manifestation_power * 0.2
                reasoning = f"Overall energy ({energy.get('overall', 0)}/10) and health energy ({energy.get('health', 0)}/10) support safe and enjoyable travel"
            elif activity_type == "investment":
                score = energy.get("finance", 0) * 0.5 + energy.get("overall", 0) * 0.3 + manifestation_power * 0.2
                reasoning = f"Financial energy ({energy.get('finance', 0)}/10) and manifestation power create favorable conditions for investments"
            elif activity_type == "job_interview":
                score = energy.get("career", 0) * 0.5 + energy.get("overall", 0) * 0.3 + manifestation_power * 0.2
                reasoning = f"Career energy ({energy.get('career', 0)}/10) and personal magnetism favor professional success"
            else:
                score = energy.get("overall", 0) * 0.6 + manifestation_power * 0.4
                reasoning = "Overall cosmic alignment and manifestation power create favorable conditions"

            optimal_activities = " ".join(enhanced_insights.get("optimalActivities", [])).lower()
            if any(keyword in optimal_activities for keyword in [activity_type.replace("_", " "), "important", "business", "meeting"]):
                score += 1
                reasoning += ". Enhanced by cosmic activity alignment"

            if score > best_score:
                best_score = score
                best_date_str = date_str
                best_reasoning = reasoning

        base_confidence = min(best_score / 12, 0.95)
        if learning_insights and learning_insights.get("total_samples", 0) > 5:
            avg_accuracy = learning_insights.get("accuracy_metrics", {}).get("overall", 5) / 10
            base_confidence = (base_confidence + avg_accuracy) / 2

        alignment_boost = (cosmic_profile.get("fusedInsights", {}).get("cosmicAlignment", 5) - 5) * 0.05
        base_confidence = min(0.95, max(0.1, base_confidence + alignment_boost))

        enhanced_reasoning = (
            f"{best_reasoning}. Your {sun_sign} sun sign and life path {life_path_number} combine "
            f"with cosmic alignment ({cosmic_profile.get('fusedInsights', {}).get('cosmicAlignment', 5)}/10) "
            f"to create this optimal timing. "
            f"{f'Confidence enhanced by {learning_insights.get('total_samples')} user feedback samples.' if learning_insights and learning_insights.get('total_samples', 0) > 5 else ''}"
        )

        return {
            "date": best_date_str,
            "confidence": base_confidence,
            "reasoning": enhanced_reasoning
        }

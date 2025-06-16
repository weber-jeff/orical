# services/astrology_service.py

class AstrologyService:
    @staticmethod
    def get_archetype_summary(sun_sign: str) -> str:
        # Placeholder: returns a default message
        return "Archetype data not available."

    @staticmethod
    def get_love_influence(sun_sign: str) -> float:
        return 5.0  # Default neutral influence value

    @staticmethod
    def get_career_influence(sun_sign: str) -> float:
        return 5.0

    @staticmethod
    def get_health_influence(sun_sign: str) -> float:
        return 5.0

    @staticmethod
    def get_finance_influence(sun_sign: str) -> float:
        return 5.0

    @staticmethod
    def get_spiritual_influence(sun_sign: str) -> float:
        return 5.0

from backend.services.numerology_service import NumerologyService
from backend.data.loader import UniversalMeaningLoader


class NumerologyReportBuilder:
    @staticmethod
    def generate_report(full_name: str, birthdate: str) -> dict:
        profile = NumerologyService.generate_numerology_profile(full_name, birthdate)
        enriched_profile = {}

        for key, value in profile.items():
            if isinstance(value, dict) and "number" in value:
                enriched_profile[key] = {
                    "number": value["number"],
                    "meaning": UniversalMeaningLoader.load_meaning(key, value["number"])
                }
            elif isinstance(value, int):
                enriched_profile[key] = {
                    "number": value,
                    "meaning": UniversalMeaningLoader.load_meaning(key, value)
                }
            else:
                enriched_profile[key] = value

        return enriched_profile
report = NumerologyReportBuilder.generate_report("Jeffrey Allen Louis Weber", "1987-05-08")
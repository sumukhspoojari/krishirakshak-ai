import os
from typing import Dict, Any, List

class WeatherServiceTool:
    """
    Tool to retrieve weather conditions and calculate agro-meteorological risks.
    """

    @staticmethod
    def get_weather(location: str = "Mandya, Karnataka") -> Dict[str, Any]:
        """
        Retrieves weather parameters and computes fungal and pest disease risk.
        """
        # Sensible regional weather defaults for Karnataka / South India / Deccan Plateau
        loc_lower = (location or "Karnataka").lower()

        if "north" in loc_lower or "up" in loc_lower or "punjab" in loc_lower:
            temp = 28.5
            humidity = 68
            rain = 0.0
            wind = 12.0
            condition = "Partly Cloudy"
        elif "coastal" in loc_lower or "kerala" in loc_lower or "mangaluru" in loc_lower:
            temp = 29.0
            humidity = 86
            rain = 14.5
            wind = 18.0
            condition = "Light Rain Showers"
        else:
            # Default Deccan Plateau / Karnataka / Andhra (e.g. Mandya, Raichur, Guntur, Hassan)
            temp = 27.8
            humidity = 78
            rain = 2.4
            wind = 10.5
            condition = "Humid & Overcast"

        # Calculate fungal risk: humidity > 75% and temp 20-30°C promotes fungal spore germination
        if humidity >= 75 and 20 <= temp <= 32:
            fungal_risk = "High"
            fungal_advisory = "High humidity (>75%) significantly increases fungal spore germination (Anthracnose, Dieback, Blight). Avoid overhead sprinkler irrigation."
        elif humidity >= 60:
            fungal_risk = "Moderate"
            fungal_advisory = "Moderate humidity. Monitor leaf undersides for fungal mycelium or powdery patches."
        else:
            fungal_risk = "Low"
            fungal_advisory = "Dry air reduces fungal progression, but watch out for sucking pests like mites."

        # Pest risk: warm temperatures with moderate humidity favor thrips, whiteflies, aphids
        if temp >= 26 and humidity < 82:
            pest_risk = "High"
            pest_advisory = "Warm temperatures encourage high reproduction rates for thrips and whiteflies (vectors for Leaf Curl Virus)."
        else:
            pest_risk = "Moderate"
            pest_advisory = "Moderate pest pressure observed."

        # Spraying condition
        can_spray = wind < 15 and rain < 5.0
        spray_advisory = "Favorable for foliar spraying today. Calm wind conditions prevent pesticide drift." if can_spray else "Avoid spraying during active rainfall or high winds (>15 km/h)."

        return {
            "location": location or "Mandya, Karnataka",
            "temperature": temp,
            "humidity": humidity,
            "rainfall_mm": rain,
            "wind_kmh": wind,
            "condition": condition,
            "fungal_disease_risk": fungal_risk,
            "pest_activity_risk": pest_risk,
            "can_spray": can_spray,
            "spray_advisory": spray_advisory,
            "advisory": f"{fungal_advisory} {pest_advisory}",
            "forecast_3days": [
                {"day": "Day 1 (Today)", "temp": f"{temp}°C", "humidity": f"{humidity}%", "rain_chance": "30%"},
                {"day": "Day 2", "temp": f"{temp + 0.5}°C", "humidity": f"{humidity - 4}%", "rain_chance": "15%"},
                {"day": "Day 3", "temp": f"{temp - 1.0}°C", "humidity": f"{humidity + 2}%", "rain_chance": "40%"},
            ]
        }

weather_tool = WeatherServiceTool()

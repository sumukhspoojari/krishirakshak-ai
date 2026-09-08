from typing import Dict, Any

class FertilizerCalculatorTool:
    """
    Calculates recommended fertilizer doses (Urea, DAP/SSP, MOP, Micronutrients)
    based on crop, area in acres, and standard agronomic university guidelines.
    """

    RECOMMENDED_DOSES = {
        # Values in kg/acre (N:P:K)
        "chilli": {"N": 60, "P": 30, "K": 30, "name": "Chilli / Menasinakayi"},
        "tomato": {"N": 50, "P": 40, "K": 40, "name": "Tomato / Tamata"},
        "rice": {"N": 40, "P": 20, "K": 20, "name": "Rice / Paddy / Vari"},
        "cotton": {"N": 60, "P": 30, "K": 30, "name": "Cotton / Hatti"}
    }

    @classmethod
    def calculate(cls, crop: str, land_area_acres: float = 1.0, soil_info: str = "Medium fertility") -> Dict[str, Any]:
        crop_clean = (crop or "chilli").lower()
        key = "chilli"
        for k in cls.RECOMMENDED_DOSES:
            if k in crop_clean:
                key = k
                break

        dose = cls.RECOMMENDED_DOSES[key]
        area = max(0.25, land_area_acres)

        # Standard commercial fertilizer conversions:
        # DAP (18% N, 46% P2O5)
        # Urea (46% N)
        # MOP (60% K2O)
        dap_kg = round((dose["P"] * area) / 0.46, 1)
        n_from_dap = dap_kg * 0.18
        remaining_n = max(0.0, (dose["N"] * area) - n_from_dap)
        urea_kg = round(remaining_n / 0.46, 1)
        mop_kg = round((dose["K"] * area) / 0.60, 1)

        return {
            "crop": dose["name"],
            "land_area_acres": area,
            "soil_condition": soil_info,
            "recommended_total_nutrients_kg": {
                "Nitrogen_N": round(dose["N"] * area, 1),
                "Phosphorus_P": round(dose["P"] * area, 1),
                "Potassium_K": round(dose["K"] * area, 1),
            },
            "commercial_fertilizers_bags_or_kg": {
                "DAP_kg": dap_kg,
                "Urea_kg": urea_kg,
                "MOP_Potash_kg": mop_kg,
                "Zinc_Sulphate_kg": round(5.0 * area, 1),
                "Neem_Cake_kg": round(100.0 * area, 1)
            },
            "split_application_schedule": [
                "Basal dose (at transplanting/sowing): 100% DAP + 100% MOP + 25% Urea + Zinc Sulphate",
                "First top dressing (30 days after transplanting): 35% Urea",
                "Second top dressing (55-60 days at flowering/fruiting): 40% Urea"
            ],
            "caution": "Avoid applying nitrogenous fertilizers on water-stressed or pest-attacked foliage until pest populations are contained."
        }

fertilizer_tool = FertilizerCalculatorTool()

from typing import List, Dict, Any

class CropDiseaseDatabase:
    """
    Search crop disease, pest, and nutrient deficiency database.
    """

    DISEASE_RECORDS = [
        # CHILLI
        {
            "crop": "chilli",
            "condition": "Chilli Leaf Curl & Thrips Infestation",
            "category": "Pest & Viral Complex",
            "symptoms": ["yellowing leaves", "upward curling", "leaf cupping", "stunted growth", "chlorosis", "brittle leaves"],
            "primary_cause": "Scirtothrips dorsalis (Thrips) and Chilli Leaf Curl Virus transmitted by Whitefly",
            "environmental_factors": "High temperature (28-34°C) with dry or alternating humid weather",
            "probability_weight": 0.85,
            "management": {
                "immediate": [
                    "Install 15-20 blue sticky traps per acre for thrips, and yellow sticky traps for whiteflies",
                    "Spray pure Neem Oil (10,000 ppm) @ 3 ml per litre of water or NSKE 5% as organic deterrent",
                    "Stop excessive chemical nitrogen fertilizer immediately as it attracts sap-sucking pests"
                ],
                "short_term": [
                    "For heavy infestation: Spray Spinetoram 11.7% SC @ 1 ml/litre or Fipronil 5% SC @ 2 ml/litre on both leaf sides",
                    "Apply foliar spray of multi-micronutrient mixture (Zinc + Boron + Iron) @ 2.5 g/litre after 4 days to stimulate chlorophyll recovery"
                ],
                "monitoring": [
                    "Inspect new emerging top shoots after 3 days; newly formed leaves should unroll flat and bright green",
                    "Check sticky traps daily to count pest trap density"
                ],
                "escalation": "If >40% of crop shows irreversible stunted rosettes or stem blackening after 7 days, visit your local KVK officer immediately."
            }
        },
        {
            "crop": "chilli",
            "condition": "Nitrogen / Micronutrient Chlorosis",
            "category": "Nutrient Deficiency",
            "symptoms": ["yellowing leaves", "uniform pale yellow older leaves", "slow growth", "no curling"],
            "primary_cause": "Nitrogen deficiency (or combined Zinc/Iron chlorosis)",
            "environmental_factors": "Leached soil following heavy irrigation or sandy soil",
            "probability_weight": 0.45,
            "management": {
                "immediate": [
                    "Foliar spray with water-soluble 19:19:19 NPK fertilizer @ 5 grams per litre of water",
                    "Inspect soil moisture; avoid waterlogging which hampers root nutrient uptake"
                ],
                "short_term": [
                    "Apply well-decomposed Farm Yard Manure (FYM) or Vermicompost around root zone",
                    "Add Zinc Sulphate (21%) @ 5 kg/acre if interveinal yellowing persists"
                ],
                "monitoring": [
                    "Watch older leaves for green color restoration within 4 to 5 days"
                ],
                "escalation": "If leaves turn white (severe iron chlorosis) or necrosis develops."
            }
        },
        {
            "crop": "chilli",
            "condition": "Chilli Dieback / Anthracnose",
            "category": "Fungal Disease",
            "symptoms": ["yellowing leaves", "drying from tip downwards", "black spots on twigs", "necrosis", "fruit rot"],
            "primary_cause": "Colletotrichum capsici fungal pathogen",
            "environmental_factors": "High humidity (>80%) and warm rainy spells",
            "probability_weight": 0.40,
            "management": {
                "immediate": [
                    "Clip and remove drying diseased branch tips 2 inches below infected portion and destroy them",
                    "Spray Copper Oxychloride 50% WP @ 3 g/litre of water"
                ],
                "short_term": [
                    "Apply systemic fungicide: Azoxystrobin 23% SC @ 1 ml/litre or Tebuconazole 25.9% EC @ 1.5 ml/litre"
                ],
                "monitoring": ["Check if twig drying stops at pruned boundary"],
                "escalation": "Rapid wilting of main stems or rotting on mature green chillies."
            }
        },
        # TOMATO
        {
            "crop": "tomato",
            "condition": "Tomato Early Blight",
            "category": "Fungal Disease",
            "symptoms": ["yellowing leaves", "concentric ring spots", "lower leaves drying", "brown lesions"],
            "primary_cause": "Alternaria solani",
            "environmental_factors": "Warm temperatures with high relative humidity and morning dew",
            "probability_weight": 0.80,
            "management": {
                "immediate": [
                    "Prune and safely discard lower yellowing leaves touching the moist soil surface",
                    "Spray Mancozeb 75% WP @ 2.5 g/litre"
                ],
                "short_term": [
                    "Spray Chlorothalonil 75% WP @ 2 g/litre after 5 days",
                    "Mulch bed with clean straw to prevent soil-splash onto foliage"
                ],
                "monitoring": ["Check upper foliage for any new target-board spots"],
                "escalation": "Lesions spreading to green tomatoes or stem cankers."
            }
        },
        # RICE / PADDY
        {
            "crop": "rice",
            "condition": "Paddy Leaf Blast",
            "category": "Fungal Disease",
            "symptoms": ["spindle shaped spots", "yellowish leaf margins", "drying leaves", "gray center spots"],
            "primary_cause": "Magnaporthe oryzae",
            "environmental_factors": "Overcast weather, high humidity (>85%), and night temperatures around 20°C",
            "probability_weight": 0.80,
            "management": {
                "immediate": [
                    "Suspend urea/nitrogen top dressing immediately",
                    "Spray Tricyclazole 75% WP @ 0.6 g/litre of water"
                ],
                "short_term": [
                    "Alternate with Isoprothiolane 40% EC @ 1.5 ml/litre if humidity continues",
                    "Ensure adequate field drainage"
                ],
                "monitoring": ["Inspect leaf spindles after 4 days for lesion margin arrest"],
                "escalation": "Neck blast infection at heading stage."
            }
        }
    ]

    @classmethod
    def search(cls, crop: str, symptoms: List[str]) -> List[Dict[str, Any]]:
        crop_clean = (crop or "").lower().strip()
        results = []

        # Find matching crop records
        matched_records = [r for r in cls.DISEASE_RECORDS if r["crop"] in crop_clean or crop_clean in r["crop"]]
        if not matched_records:
            # Fallback to chilli as primary reference if general
            matched_records = [r for r in cls.DISEASE_RECORDS if r["crop"] == "chilli"]

        symptom_text = " ".join(symptoms).lower()

        for rec in matched_records:
            match_count = 0
            for sym in rec["symptoms"]:
                if any(word in symptom_text for word in sym.split()):
                    match_count += 1
            
            # Compute confidence score
            score = rec["probability_weight"]
            if match_count > 1:
                score = min(0.95, score + 0.10)
            elif match_count == 0:
                score = max(0.20, score - 0.25)

            prob_label = "High" if score >= 0.70 else ("Medium" if score >= 0.40 else "Low")

            results.append({
                "condition": rec["condition"],
                "category": rec["category"],
                "probability": prob_label,
                "confidence_score": round(score, 2),
                "primary_cause": rec["primary_cause"],
                "environmental_factors": rec["environmental_factors"],
                "management": rec["management"],
                "matched_symptoms_count": match_count
            })

        # Sort by confidence score descending
        results.sort(key=lambda x: x["confidence_score"], reverse=True)
        return results

disease_database_tool = CropDiseaseDatabase()

from typing import List, Dict, Any

class GovtSchemesTool:
    """
    Search government schemes, subsidies, crop insurance, and farmer assistance.
    Supports Central Government & State initiatives (Karnataka Raitha Siri, Rythu Bharosa, etc.).
    """

    SCHEMES = [
        {
            "id": "pm-kisan",
            "name": "PM-KISAN Samman Nidhi",
            "name_kn": "ಪಿಎಂ-ಕಿಸಾನ್ ಸಮ್ಮಾನ್ ನಿಧಿ",
            "name_hi": "पीएम-किसान सम्मान निधि",
            "name_te": "పీఎం-కిసాన్ సమ్మాన్ నిధి",
            "category": "Direct Income Support",
            "eligibility": "All landholding farmer families with cultivable land across India.",
            "benefits": "₹6,000 per year paid in three equal installments of ₹2,000 directly into Aadhaar-seeded bank accounts.",
            "how_to_apply": "Register via pmkisan.gov.in portal or visit nearest Grama One / CSC centre with Aadhaar and Pahani (RTC).",
            "official_link": "https://pmkisan.gov.in"
        },
        {
            "id": "pmfby",
            "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
            "name_kn": "ಪ್ರಧಾನ ಮಂತ್ರಿ ಫಸಲ್ ಬಿಮಾ ಯೋಜನೆ (ಬೆಳೆ ವಿಮೆ)",
            "name_hi": "प्रधानमंत्री फसल बीमा योजना (फसल बीमा)",
            "name_te": "ప్రధాన మంత్రి ఫసల్ బీమా యోజన (పంట బీమా)",
            "category": "Crop Insurance",
            "eligibility": "Farmers growing notified crops (including Chilli, Paddy, Cotton, Pulses) in notified areas.",
            "benefits": "Comprehensive insurance coverage against non-preventable natural risks, pests, and localized post-harvest losses. Premium is just 1.5% - 2% for farmers.",
            "how_to_apply": "Apply through Samrakshane portal (Karnataka) or national pmfby.gov.in portal before crop enrollment cut-off date.",
            "official_link": "https://pmfby.gov.in"
        },
        {
            "id": "kcc",
            "name": "Kisan Credit Card (KCC)",
            "name_kn": "ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್ (ಕೆಸಿಸಿ ಸಾಲ)",
            "name_hi": "किसान क्रेडिट कार्ड (केसीसी)",
            "name_te": "కిసాన్ క్రెడిట్ కార్డ్ (కెసిసి)",
            "category": "Subsidized Credit",
            "eligibility": "Individual farmers, joint borrowers, tenant farmers, and SHGs.",
            "benefits": "Short-term production credit up to ₹3 Lakh at an effective interest rate of only 4% (with timely repayment prompt incentive).",
            "how_to_apply": "Submit one-page KCC application at any commercial, rural, or cooperative bank branch.",
            "official_link": "https://sbi.co.in/web/agri-rural/agriculture-banking/crop-loan/kisan-credit-card"
        },
        {
            "id": "soil-health-card",
            "name": "Soil Health Card Scheme",
            "name_kn": "ಮಣ್ಣು ಆರೋಗ್ಯ ಕಾರ್ಡ್ ಯೋಜನೆ",
            "name_hi": "मृदा स्वास्थ्य कार्ड योजना",
            "name_te": "సాయిల్ హెల్త్ కార్డ్ పథకం",
            "category": "Soil Testing & Fertility",
            "eligibility": "All farmers with agricultural land.",
            "benefits": "Free testing of 12 soil chemical and micronutrient parameters (N, P, K, S, Zn, Fe, Cu, Mn, Bo, pH, EC, OC) with tailored crop-wise fertilizer dosage recommendations.",
            "how_to_apply": "Collect and submit soil sample at local Raitha Samparka Kendra (RSK) or KVK soil testing lab.",
            "official_link": "https://soilhealth.dac.gov.in"
        },
        {
            "id": "krishi-yantradhare",
            "name": "Custom Hiring Centre (Farm Machinery Subsidy)",
            "name_kn": "ಕೃಷಿ ಯಂತ್ರಧಾರೆ (ಬಾಡಿಗೆ ಯಂತ್ರೋಪಕರಣಗಳು)",
            "name_hi": "कृषि यंत्रीकरण उप-मिशन (सब्सिडी)",
            "name_te": "కస్టమ్ హైరింగ్ సెంటర్ (వ్యవసాయ యంత్రాలు)",
            "category": "Mechanization & Subsidy",
            "eligibility": "Small and marginal farmers.",
            "benefits": "Rent tractors, rotavators, power tillers, and sprayers at 40-50% subsidized rental rates, or 50% capital subsidy on battery-operated sprayers.",
            "how_to_apply": "Visit your Hobli Raitha Samparka Kendra or Department of Agriculture office.",
            "official_link": "https://agricoop.nic.in"
        }
    ]

    @classmethod
    def search(cls, location: str = "", farmer_context: str = "") -> List[Dict[str, Any]]:
        context = (farmer_context or "").lower()
        if "insurance" in context or "damage" in context or "loss" in context:
            return [cls.SCHEMES[1], cls.SCHEMES[0], cls.SCHEMES[2]]
        elif "fertilizer" in context or "soil" in context or "nutrient" in context:
            return [cls.SCHEMES[3], cls.SCHEMES[0], cls.SCHEMES[4]]
        elif "loan" in context or "credit" in context or "money" in context:
            return [cls.SCHEMES[2], cls.SCHEMES[0]]
        return cls.SCHEMES

govt_schemes_tool = GovtSchemesTool()

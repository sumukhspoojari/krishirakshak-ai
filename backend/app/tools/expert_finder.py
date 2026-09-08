from typing import List, Dict, Any

class ExpertFinderTool:
    """
    Finds verified agricultural experts, Krishi Vigyan Kendras (KVK),
    Raitha Samparka Kendras (RSK), and national toll-free helplines.
    """

    CENTRAL_HELPLINES = [
        {
            "name": "Kisan Call Centre (KCC) National Toll-Free",
            "number": "1800-180-1551",
            "timings": "6:00 AM to 10:00 PM (All 7 Days)",
            "description": "Direct consultation with agricultural graduates in local language (Kannada, Hindi, Telugu, etc.).",
            "type": "Toll-Free Helpline"
        },
        {
            "name": "Karnataka Raitha Sahayavani (Dept of Agriculture)",
            "number": "1800-425-3553",
            "timings": "9:30 AM to 6:00 PM",
            "description": "Direct state department assistance, seeds, fertilizer quality, and scheme grievance.",
            "type": "State Helpline"
        }
    ]

    KVK_CENTRES = [
        {
            "district": "Mandya / South Karnataka",
            "name": "Krishi Vigyan Kendra (KVK), V.C. Farm, Mandya",
            "institution": "University of Agricultural Sciences, Bangalore",
            "officer_title": "Senior Scientist & Head (Plant Protection / Agronomy)",
            "phone": "08232-277448",
            "address": "V.C. Farm Campus, Mandya - 571405",
            "type": "KVK Research Centre"
        },
        {
            "district": "Dharwad / North Karnataka",
            "name": "Krishi Vigyan Kendra (KVK), UAS Dharwad",
            "institution": "University of Agricultural Sciences, Dharwad",
            "officer_title": "Agronomist & Plant Pathologist",
            "phone": "0836-2447494",
            "address": "Agricultural College Campus, Dharwad - 580005",
            "type": "KVK Research Centre"
        },
        {
            "district": "Guntur / Andhra Pradesh",
            "name": "Krishi Vigyan Kendra (KVK), Lam, Guntur",
            "institution": "Acharya N.G. Ranga Agricultural University (ANGRAU)",
            "officer_title": "Chilli & Cotton Specialist Agronomist",
            "phone": "0863-2524017",
            "address": "Regional Agricultural Research Station, Lam, Guntur",
            "type": "KVK Research Centre"
        },
        {
            "district": "National / Any Location",
            "name": "Local Raitha Samparka Kendra (RSK)",
            "institution": "Department of Agriculture",
            "officer_title": "Hobli Agricultural Officer (AO)",
            "phone": "Visit Taluk Office",
            "address": "Nearest Hobli Centre",
            "type": "Local Field Office"
        }
    ]

    @classmethod
    def find_experts(cls, location: str = "") -> List[Dict[str, Any]]:
        loc = (location or "").lower()
        matched_kvks = []
        for kvk in cls.KVK_CENTRES:
            if any(k in loc for k in kvk["district"].lower().split("/")):
                matched_kvks.append(kvk)

        if not matched_kvks:
            matched_kvks = [cls.KVK_CENTRES[0], cls.KVK_CENTRES[1]]

        return cls.CENTRAL_HELPLINES + matched_kvks

expert_finder_tool = ExpertFinderTool()

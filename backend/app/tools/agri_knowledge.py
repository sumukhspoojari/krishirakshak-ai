from typing import List, Dict, Any

class AgriKnowledgeBase:
    """
    Search verified agricultural knowledge base (ICAR, UAS Dharwad/Bangalore, TNAU, KVK).
    """

    KNOWLEDGE_ENTRIES = [
        {
            "topic": "Chilli Yellowing & Leaf Curl",
            "keywords": ["chilli", "menasinakayi", "mirchi", "yellow", "curl", "thrips", "mites"],
            "summary": "Yellowing of chilli leaves coupled with upward curling is predominantly caused by Chilli Thrips (Scirtothrips dorsalis) or Chilli Leaf Curl Begomovirus transmitted by Whiteflies (Bemisia tabaci). When curling is downward with oily leaves, yellow mites are responsible.",
            "cultural_practices": [
                "Install blue sticky traps (15-20 traps/acre) for thrips and yellow sticky traps for whiteflies",
                "Avoid excessive chemical nitrogen application which makes leaves succulent and attracts sucking pests",
                "Spray 5% Neem Seed Kernel Extract (NSKE) or Neem Oil 10,000 ppm @ 3 ml/litre as preventive organic measure",
                "Ensure weed-free border to prevent pest reservoirs"
            ],
            "approved_interventions": [
                "Bio-pesticide: Beauveria bassiana @ 5 g/litre foliar spray on underside of leaves",
                "For severe thrips infestation: Fipronil 5% SC @ 2 ml/litre or Spinetoram 11.7% SC @ 1 ml/litre",
                "For nutrient yellowing: Foliar spray of Micronutrient mixture @ 2.5 g/litre + 19:19:19 @ 5 g/litre"
            ]
        },
        {
            "topic": "Chilli Anthracnose / Dieback & Fruit Rot",
            "keywords": ["chilli", "dieback", "anthracnose", "fruit rot", "black spot"],
            "summary": "Caused by Colletotrichum capsici. Twigs dry from tip downwards. Black dots (acervuli) appear on dead twigs and circular sunken spots on ripe fruits.",
            "cultural_practices": [
                "Prune and destroy infected dead twigs 2 inches below infected area",
                "Disinfect pruning shears with 0.1% sodium hypochlorite solution"
            ],
            "approved_interventions": [
                "Foliar spray with Copper Oxychloride 50% WP @ 3 g/litre or Mancozeb 75% WP @ 2.5 g/litre",
                "For systemic cure: Azoxystrobin 23% SC @ 1 ml/litre or Tebuconazole 25.9% EC @ 1.5 ml/litre"
            ]
        },
        {
            "topic": "Tomato Early & Late Blight",
            "keywords": ["tomato", "tamata", "blight", "spot", "drying"],
            "summary": "Early blight (Alternaria solani) causes target-board concentric spots on lower leaves. Late blight (Phytophthora infestans) causes fast-spreading water-soaked greasy patches under cool, wet weather.",
            "cultural_practices": [
                "Remove and bury infected lower leaves touching soil",
                "Drip irrigation preferred over flood irrigation to keep canopy dry"
            ],
            "approved_interventions": [
                "Preventive: Mancozeb 75% WP @ 2.5 g/litre",
                "Curative: Metalaxyl 8% + Mancozeb 64% WP @ 2 g/litre"
            ]
        },
        {
            "topic": "Rice / Paddy Blast & Brown Spot",
            "keywords": ["rice", "paddy", "vari", "blast", "brown spot"],
            "summary": "Paddy blast (Magnaporthe oryzae) manifests as spindle-shaped spots with ash-colored centers. Rapidly flares under high nitrogen and prolonged morning dew.",
            "cultural_practices": [
                "Split nitrogen application into 3-4 doses instead of heavy single dose",
                "Maintain thin water film during critical stages"
            ],
            "approved_interventions": [
                "Tricyclazole 75% WP @ 0.6 g/litre or Isoprothiolane 40% EC @ 1.5 ml/litre"
            ]
        }
    ]

    @classmethod
    def search(cls, query: str) -> List[Dict[str, Any]]:
        query_terms = set(query.lower().split())
        matched = []

        for entry in cls.KNOWLEDGE_ENTRIES:
            # Check overlap
            entry_keywords = set(k.lower() for k in entry["keywords"])
            topic_words = set(entry["topic"].lower().split())
            if query_terms & entry_keywords or query_terms & topic_words:
                matched.append(entry)

        if not matched:
            # Return general knowledge if no exact match
            matched = [cls.KNOWLEDGE_ENTRIES[0]]

        return matched

agri_knowledge_tool = AgriKnowledgeBase()

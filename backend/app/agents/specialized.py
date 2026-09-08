import re
from typing import Dict, Any, List
from datetime import datetime, timedelta

from app.services.multilingual import MultilingualService
from app.tools.crop_image_analyzer import crop_image_analyzer
from app.tools.weather_service import weather_tool
from app.tools.agri_knowledge import agri_knowledge_tool
from app.tools.disease_db import disease_database_tool
from app.tools.govt_schemes import govt_schemes_tool
from app.tools.fertilizer_calculator import fertilizer_tool
from app.tools.expert_finder import expert_finder_tool
from app.tools.follow_up_planner import follow_up_planner_tool
from app.tools.image_comparator import image_comparator_tool


class ConversationalAgent:
    """
    AGENT 0 — Conversational & FAQ Agent
    Handles greetings, assistant identity, capabilities, gratitude,
    and general agricultural queries with warmth and prompts for next query.
    """

    RESPONSES = {
        "greeting": {
            "kn": (
                "ನಮಸ್ಕಾರ ರೈತ ಬಾಂಧವರೇ! 🙏\n\n"
                "ನಾನು ಕೃಷಿರಕ್ಷಕ್ AI (KrishiAI) — ನಿಮ್ಮ ಬೆಳೆ ವೈದ್ಯ ಮತ್ತು ಡಿಜಿಟಲ್ ಕೃಷಿ ಸಹಾಯಕ.\n\n"
                "ನಾನು ನಿಮ್ಮ ಬೆಳೆ ರೋಗ ಪತ್ತೆ, ಕೀಟ ನಿಯಂತ್ರಣ, ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ ಹಾಗೂ ಸರ್ಕಾರದ ಕೃಷಿ ಯೋಜನೆಗಳ ಬಗ್ಗೆ ನಿಖರ ಮಾಹಿತಿ ನೀಡಬಲ್ಲೆ.\n\n"
                "👉 ಇಂದು ನಿಮ್ಮ ಕೃಷಿ ಅಥವಾ ಬೆಳೆಗೆ ಸಂಬಂಧಿಸಿದಂತೆ ಯಾವ ಸಮಸ್ಯೆ ಅಥವಾ ಪ್ರಶ್ನೆ ಇದೆ? ದಯವಿಟ್ಟು ತಿಳಿಸಿ, ಸಹಾಯ ಮಾಡುತ್ತೇನೆ! 🌾"
            ),
            "hi": (
                "नमस्ते किसान भाई! 🙏\n\n"
                "मैं कृषिरक्षक AI (KrishiAI) हूँ — आपका फसल डॉक्टर और डिजिटल कृषि सहायक।\n\n"
                "मैं फसल रोग निदान, कीट नियंत्रण, मौसम जोखिम पूर्वानुमान और सरकारी योजनाओं के बारे में आपकी सहायता कर सकता हूँ।\n\n"
                "👉 आज आपकी फसल या खेती से संबंधित क्या समस्या या प्रश्न है? कृपया अपनी समस्या बताएं या पौधे की फोटो साझा करें! 🌾"
            ),
            "te": (
                "నమస్కారం రైతు మిత్రమా! 🙏\n\n"
                "నేను కృషిరక్షక్ AI (KrishiAI) — మీ పంట వైద్యుడిని మరియు డిజిటల్ వ్యవసాయ సహాయకుడిని.\n\n"
                "పంట తెగుళ్ల గుర్తింపు, నివారణ మందులు, స్థానిక వాతావరణ సమాచారం మరియు ప్రభుత్వ పథకాలపై మీకు సహాయం చేయగలను.\n\n"
                "👉 ఈరోజు మీ పంట లేదా వ్యవసాయం గురించి మీ ప్రశ్న ఏమిటి? వివరాలు తెలపండి, సహాయం చేస్తాను! 🌾"
            ),
            "en": (
                "Hello and welcome to KrishiRakshak AI (KrishiAI)! 🙏\n\n"
                "I am your autonomous AI Crop Doctor and farming assistant.\n\n"
                "I can help you diagnose crop diseases and pest attacks, recommend immediate action plans, monitor weather risks, and guide you through government farmer welfare schemes.\n\n"
                "👉 How can I help you today? Please tell me about your crop problem or ask any agricultural query you have! 🌾"
            )
        },
        "identity": {
            "kn": (
                "ನಾನು ಕೃಷಿರಕ್ಷಕ್ AI (KrishiAI), ರೈತರ ಬೆಳೆ ರಕ್ಷಣೆಗಾಗಿ ರೂಪಿಸಲಾದ ಸ್ವಾಯತ್ತ ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ ಸಹಾಯಕ.\n\n"
                "ನನ್ನ ಪ್ರಮುಖ ಸಾಮರ್ಥ್ಯಗಳು:\n"
                "• 🔍 ಎಲೆಯ ಫೋಟೋ ವಿಶ್ಲೇಷಿಸಿ ರೋಗ ಮತ್ತು ಕೀಟಬಾಧೆ ಪತ್ತೆ ಹಚ್ಚುವುದು.\n"
                "• 📋 ರೋಗ ನಿಯಂತ್ರಣಕ್ಕೆ ಹಂತ-ಹಂತದ ತಕ್ಷಣದ ಕಾರ್ಯ ಯೋಜನೆ ಮತ್ತು ಔಷಧ ಶಿಫಾರಸು.\n"
                "• 🗓 ಬೆಳೆ ಚೇತರಿಕೆಯನ್ನು ಮೇಲ್ವಿಚಾರಣೆ ಮಾಡಲು 3 ದಿನಗಳ ಅನುಸರಣಾ (Follow-up) ಯೋಜನೆ.\n"
                "• 🌦 ಸ್ಥಳೀಯ ಹವಾಮಾನ ಅಪಾಯ ಮತ್ತು ಶಿಲೀಂಧ್ರ ರೋಗದ ಎಚ್ಚರಿಕೆ.\n"
                "• 🏛 ಪಿಎಂ-ಕಿಸಾನ್, ಬೆಳೆ ವಿಮೆ (PMFBY), ಮತ್ತು ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್ ವಿವರಗಳು.\n\n"
                "👉 ನಿಮ್ಮ ಹೊಲದಲ್ಲಿ ಯಾವುದೇ ಬೆಳೆ ಸಮಸ್ಯೆ ಕಂಡುಬಂದಿದೆಯೇ? ಬೆಳೆಯ ಹೆಸರು ಅಥವಾ ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ತಿಳಿಸಿ!"
            ),
            "hi": (
                "मैं कृषिरक्षक AI (KrishiAI) हूँ, किसानों की सहायता के लिए तैयार किया गया डिजिटल फसल डॉक्टर।\n\n"
                "मेरी प्रमुख विशेषताएं:\n"
                "• 🔍 पत्ती की तस्वीर से रोग और कीटों की सटीक पहचान।\n"
                "• 📋 त्वरित रोकथाम और दवाइयों की चरणबद्ध कार्य योजना।\n"
                "• 🗓 फसल सुधार की निगरानी हेतु 3-दिवसीय फॉलो-अप योजना।\n"
                "• 🌦 स्थानीय मौसम और फंगल संक्रमण की अग्रिम चेतावनी।\n"
                "• 🏛 पीएम-किसान, फसल बीमा (PMFBY) एवं किसान क्रेडिट कार्ड (KCC) की जानकारी।\n\n"
                "👉 क्या आपकी फसल में कोई समस्या है? कृपया अपनी फसल का नाम या प्रश्न साझा करें!"
            ),
            "te": (
                "నేను కృషిరక్షక్ AI (KrishiAI), రైతుల కోసం రూపొందించబడిన డిజిటల్ పంట వైద్యుడిని.\n\n"
                "నా ముఖ్య సేవలు:\n"
                "• 🔍 ఆకుల ఫోటోలను విశ్లేషించి తెగుళ్లను గుర్తించడం.\n"
                "• 📋 మందులు మరియు సమగ్ర నివారణ కార్యాచరణ ప్రణాళిక.\n"
                "• 🗓 పంట రికవరీని పర్యవేక్షించడానికి 3 రోజుల ఫాలో-అప్ చెక్‌పాయింట్.\n"
                "• 🌦 స్థానిక వాతావరణం మరియు తెగుళ్ల ముందస్తు హెచ్చరికలు.\n"
                "• 🏛 ప్రభుత్వ వ్యవసాయ సబ్సిడీలు మరియు పంట బీమా పథకాలు.\n\n"
                "👉 మీ పంటలో ఏదైనా సమస్య ఉందా? దయచేసి మీ ప్రశ్నను లేదా సమస్యను తెలపండి!"
            ),
            "en": (
                "I am KrishiRakshak AI (KrishiAI), an autonomous multi-agent assistant built to protect crops and empower farmers.\n\n"
                "My core capabilities include:\n"
                "• 🔍 Diagnosing crop diseases, pests, and nutrient deficiencies from leaf photos.\n"
                "• 📋 Providing actionable, safe treatment plans and chemical/organic spray dosages.\n"
                "• 🗓 Scheduling 3-day follow-up checkpoints to track crop recovery.\n"
                "• 🌦 Analyzing hyper-local weather risks (humidity, rain, fungal spore alerts).\n"
                "• 🏛 Offering full guidance on PM-KISAN, PMFBY Crop Insurance, and KCC.\n\n"
                "👉 Do you have a question about your crop or field? Please ask your query or share a leaf photo!"
            )
        },
        "gratitude": {
            "kn": (
                "ನಿಮಗೆ ಸಹಾಯ ಮಾಡಲು ಸಂತೋಷವಾಯಿತು! 🌾\n\n"
                "ನಿಮ್ಮ ಕೃಷಿ ಸಮೃದ್ಧವಾಗಿರಲಿ ಮತ್ತು ಉತ್ತಮ ಇಳುವರಿ ಬರಲಿ ಎಂದು ಹಾರೈಸುತ್ತೇನೆ.\n\n"
                "👉 ನಿಮ್ಮ ಬೆಳೆ, ರಸಗೊಬ್ಬರ ಅಥವಾ ಕೃಷಿಗೆ ಸಂಬಂಧಿಸಿದಂತೆ ಇನ್ನಾವುದಾದರೂ ಪ್ರಶ್ನೆ ಅಥವಾ ಸಂದೇಹವಿದ್ದರೆ ದಯವಿಟ್ಟು ಕೇಳಿ!"
            ),
            "hi": (
                "आपको सहायता प्रदान करके खुशी हुई! 🌾\n\n"
                "हम आपकी अच्छी और समृद्ध फसल की कामना करते हैं।\n\n"
                "👉 आपकी फसल, उर्वरक या खेती से संबंधित कोई अन्य सवाल या संदेह हो तो बेझिझक पूछें!"
            ),
            "te": (
                "మీకు సహాయపడటం చాలా సంతోషంగా ఉంది! 🌾\n\n"
                "మీ పంట సమృద్ధిగా పండాలని కోరుకుంటున్నాము.\n\n"
                "👉 మీ పంట, ఎరువులు లేదా వ్యవసాయంపై ఇంకేదైనా సందేహం లేదా ప్రశ్న ఉంటే దయచేసి అడగండి!"
            ),
            "en": (
                "You are very welcome! 🌾\n\n"
                "Wishing you a healthy crop and a bountiful harvest.\n\n"
                "👉 If you have any other questions about crop care, fertilizers, or pest management, feel free to ask!"
            )
        },
        "crops_supported": {
            "kn": (
                "ಕೃಷಿರಕ್ಷಕ್ AI ಪ್ರಸ್ತುತ ಈ ಕೆಳಗಿನ ಬೆಳೆಗಳಿಗೆ ವಿಶೇಷ ತಜ್ಞತೆ ಮತ್ತು ರೋಗ ಪತ್ತೆ ಸೌಲಭ್ಯವನ್ನು ಹೊಂದಿದೆ:\n\n"
                "• 🌶 **ಮೆಣಸಿನಕಾಯಿ (Chilli)**: ಎಲೆ ಮುದುಡು ರೋಗ (Leaf Curl), ನುಸಿ/ಜಿಗಿದುಂಬಿ ಹಾನಿ, ಹಳದಿ ರೋಗ, ಕೊಳೆ ರೋಗ.\n"
                "• 🍅 **ಟೊಮೆಟೊ (Tomato)**: ಅರ್ಲಿ/ಲೇಟ್ ಬ್ಲೈಟ್ (Blight), ಎಲೆ ಚುಕ್ಕೆ, ಸೊರಗು ರೋಗ.\n"
                "• 🌾 **ಭತ್ತ (Paddy/Rice)**: ಬ್ಲಾಸ್ಟ್ ರೋಗ (Blast), ಕಂದು ಜಿಗಿಹುಳು (BPH), ಶೀತ್ ಬ್ಲೈಟ್.\n"
                "• ☁️ **ಹತ್ತಿ (Cotton)**: ದುಂಡಾಣು ರೋಗ, ಗುಲಾಬಿ ಬೋಲ್‌ವರ್ಮ್, ಎಲೆ ಕೆಂಪಾಗುವಿಕೆ.\n"
                "• ಮತ್ತು ಇತರ ತರಕಾರಿ ಹಾಗೂ ತೋಟಗಾರಿಕಾ ಬೆಳೆಗಳು.\n\n"
                "👉 ನೀವು ಪ್ರಸ್ತುತ ಯಾವ ಬೆಳೆಯನ್ನು ಬೆಳೆಯುತ್ತಿದ್ದೀರಿ? ಅದರ ಸಮಸ್ಯೆ ಅಥವಾ ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ತಿಳಿಸಿ!"
            ),
            "hi": (
                "कृषिरक्षक AI वर्तमान में इन प्रमुख फसलों के लिए रोग निदान और समाधान प्रदान करता है:\n\n"
                "• 🌶 **मिर्च (Chilli)**: लीफ कर्ल (पत्ती मुड़ना), थ्रिप्स/माइट्स, पीलापन, डाईबैक।\n"
                "• 🍅 **टमाटर (Tomato)**: अर्ली व लेट ब्लाइट (झुलसा), पत्ती धब्बा, उकठा रोग।\n"
                "• 🌾 **धान (Paddy/Rice)**: ब्लास्ट, शीथ ब्लाइट, भूरा फुदका (BPH)।\n"
                "• ☁️ **कपास (Cotton)**: गुलाबी सुंडी (Pink Bollworm), पत्ती लाल होना।\n\n"
                "👉 आप वर्तमान में कौन सी फसल उगा रहे हैं? अपनी फसल की समस्या या सवाल साझा करें!"
            ),
            "te": (
                "కృషిరక్షక్ AI ప్రస్తుతం ఈ పంటలకు సమగ్ర సలహాలు అందిస్తుంది:\n\n"
                "• 🌶 **మిరప (Chilli)**: ఆకు ముడుత తెగులు, బూడిద తెగులు, పసుపు రంగు మారడం.\n"
                "• 🍅 **టమాటా (Tomato)**: ఎర్లీ/లేట్ బ్లైట్, ఆకు మచ్చల తెగులు.\n"
                "• 🌾 **వరి (Paddy)**: అగ్గితెగులు (Blast), సుడి దోమ (BPH).\n"
                "• ☁️ **పత్తి (Cotton)**: గులాబీ రంగు కాయ తొలుచు పురుగు.\n\n"
                "👉 మీరు ప్రస్తుతం ఏ పంట సాగు చేస్తున్నారు? మీ సమస్య లేదా ప్రశ్నను తెలపండి!"
            ),
            "en": (
                "KrishiRakshak AI currently specializes in disease diagnosis and care for the following major crops:\n\n"
                "• 🌶 **Chilli**: Leaf Curl Virus, Thrips/Mite Infestation, Yellowing, Dieback.\n"
                "• 🍅 **Tomato**: Early & Late Blight, Leaf Spot, Bacterial Wilt.\n"
                "• 🌾 **Paddy / Rice**: Rice Blast, Brown Plant Hopper (BPH), Sheath Blight.\n"
                "• ☁️ **Cotton**: Pink Bollworm, Leaf Reddening, Bacterial Blight.\n"
                "• Along with horticultural and vegetable crops.\n\n"
                "👉 Which crop are you cultivating right now? Feel free to ask any question or share a leaf photo!"
            )
        },
        "general_inquiry": {
            "kn": (
                "ಕೃಷಿರಕ್ಷಕ್ AI ಗೆ ಸ್ವಾಗತ! ನಾನು ನಿಮ್ಮ ಬೆಳೆ ವೈದ್ಯ.\n\n"
                "ನೀವು ಯಾವುದೇ ಸಮಯದಲ್ಲಿ:\n"
                "1. ನಿಮ್ಮ ಬೆಳೆಯ ಹೆಸರು ಮತ್ತು ಸಮಸ್ಯೆಯನ್ನು ಬರೆಯಬಹುದು (ಉದಾ: 'ಮೆಣಸಿನಕಾಯಿ ಎಲೆ ಹಳದಿಯಾಗುತ್ತಿದೆ').\n"
                "2. ಬಾಧಿತ ಎಲೆಯ ಫೋಟೋವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಬಹುದು.\n"
                "3. ಧ್ವನಿ ಬಟನ್ ಒತ್ತಿ ಕನ್ನಡದಲ್ಲೇ ಮಾತನಾಡಬಹುದು.\n\n"
                "👉 ನಿಮ್ಮ ಹೊಲದಲ್ಲಿರುವ ಬೆಳೆ ಅಥವಾ ಕೃಷಿ ಸಮಸ್ಯೆ ಕುರಿತು ನಿಮ್ಮ ಮುಂದಿನ ಪ್ರಶ್ನೆ ಏನು? ದಯವಿಟ್ಟು ತಿಳಿಸಿ!"
            ),
            "hi": (
                "कृषिरक्षक AI में आपका स्वागत है! मैं आपका डिजिटल फसल डॉक्टर हूँ।\n\n"
                "आप आसानी से:\n"
                "1. अपनी फसल का नाम और समस्या लिख सकते हैं (उदा: 'मिर्च के पत्ते मुड़ रहे हैं')।\n"
                "2. पत्ती की तस्वीर अपलोड कर सकते हैं।\n"
                "3. माइक बटन दबाकर हिंदी में बोल सकते हैं।\n\n"
                "👉 आपकी फसल से संबंधित आपका क्या प्रश्न या समस्या है? कृपया बताएं!"
            ),
            "te": (
                "కృషిరక్షక్ AI కి స్వాగతం! నేను మీ డిజిటల్ పంట వైద్యుడిని.\n\n"
                "మీరు సులభంగా:\n"
                "1. మీ పంట పేరు మరియు సమస్యను టైప్ చేయవచ్చు.\n"
                "2. ఆకు ఫోటోను అప్‌లోడ్ చేయవచ్చు.\n"
                "3. మైక్ బటన్ నొక్కి తెలుగులో మాట్లాడవచ్చు.\n\n"
                "👉 మీ పంటకు సంబంధించి మీ తదుపరి ప్రశ్న ఏమిటి? దయచేసి తెలపండి!"
            ),
            "en": (
                "Welcome to KrishiRakshak AI! I am your AI Crop Doctor.\n\n"
                "To get started:\n"
                "1. Type your crop name and symptoms (e.g., 'chilli leaves turning yellow').\n"
                "2. Upload a clear photo of the infected leaf or plant.\n"
                "3. Or tap the mic icon to dictate your query in your preferred language.\n\n"
                "👉 What crop issue or agricultural question can I help you with right now?"
            )
        }
    }


    @classmethod
    def get_groq_agronomy_response(cls, user_text: str, lang: str) -> str:
        """
        Uses Groq Cloud API via httpx / Groq SDK with automatic multi-model failover
        to generate an authoritative, step-by-step crop cultivation guide in the farmer's language.
        """
        import os
        import httpx
        from app.config import settings

        api_key = (settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY") or "").strip()
        if not api_key:
            return cls.get_fallback_agronomy_response(user_text, lang)

        lang_prompts = {
            "kn": "ಕನ್ನಡ ಭಾಷೆಯಲ್ಲೇ ಸಂಪೂರ್ಣ ಉತ್ತರ ನೀಡಿ. ಪ್ರತಿಯೊಂದು ಹಂತವನ್ನು ವಿವರವಾಗಿ ಮತ್ತು ಸ್ಪಷ್ಟವಾಗಿ ಬರೆಯಿರಿ.",
            "hi": "हिंदी भाषा में संपूर्ण उत्तर दें। प्रत्येक चरण को विस्तार से और सरल शब्दों में समझाएं।",
            "te": "తెలుగు భాషలో సమాధానం ఇవ్వండి. ప్రతి దశను స్పష్టంగా మరియు వివరంగా తెలపండి.",
            "en": "Respond in English. Format clearly with bullet points and bold section headings."
        }
        lang_instruction = lang_prompts.get(lang, lang_prompts["en"])

        prompt_system = (
            "You are KrishiRakshak AI (ಕೃಷಿರಕ್ಷಕ್ AI), an expert Indian Council of Agricultural Research (ICAR) "
            "and Krishi Vigyan Kendra (KVK) senior agricultural scientist and agronomist.\n"
            "Provide a comprehensive, highly practical, step-by-step crop cultivation guide tailored for Indian farmers.\n\n"
            "Include:\n"
            "1. 🌾 Soil & Climate Requirements\n"
            "2. 🌱 Recommended High-Yielding Varieties\n"
            "3. 🚜 Land Preparation & Seed Treatment\n"
            "4. 📏 Sowing Time, Seed Rate & Spacing\n"
            "5. 🧪 Manure & Fertilizer Schedule (NPK dosage per acre)\n"
            "6. 💧 Irrigation & Weed Control\n"
            "7. 🛡️ Major Pest/Disease Prevention\n"
            "8. 🧺 Harvesting & Expected Yield\n\n"
            f"{lang_instruction}\n\n"
            "Always conclude with this helpful prompt:\n"
            "👉 Do you have questions about specific fertilizer calculations (NPK dosages), pest control recommendations, or seed varieties? Feel free to ask your next query!"
        )

        models = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b", "groq/compound"]
        
        for model_name in models:
            try:
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": model_name,
                    "messages": [
                        {"role": "system", "content": prompt_system},
                        {"role": "user", "content": user_text}
                    ],
                    "max_tokens": 1200,
                    "temperature": 0.3
                }
                resp = httpx.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=25.0
                )
                if resp.status_code == 200:
                    data = resp.json()
                    ans = data["choices"][0]["message"]["content"]
                    if ans and len(ans.strip()) > 50:
                        return ans.strip()
            except Exception as e:
                print(f"Groq model {model_name} attempt failed:", e)

        return cls.get_fallback_agronomy_response(user_text, lang)

    @classmethod
    def get_fallback_agronomy_response(cls, user_text: str, lang: str) -> str:
        """
        Built-in curated agronomic cultivation guide covering ALL major Indian crops
        (Wheat, Rice, Cotton, Maize, Chilli, Tomato, Sugarcane, Groundnut, Onion, Potato, etc.).
        """
        lower = user_text.lower()

        # 1. WHEAT (ಗೋಧಿ / गेहूं)
        if any(w in lower for w in ["wheat", "ಗೋಧಿ", "गेहूं", "గోధుమ"]):
            if lang == "kn":
                return (
                    "🌾 **ಗೋಧಿ (Wheat) ಬೆಳೆಯುವ ಹಂತ-ಹಂತದ ಸಂಪೂರ್ಣ ಮಾರ್ಗದರ್ಶನ:**\n\n"
                    "1. **ಮಣ್ಣು ಮತ್ತು ಹವಾಗುಣ:**\n"
                    "• ಫಲವತ್ತಾದ ಗೋಡು ಮತ್ತು ಜೇಡಿ ಗೋಡು ಮಣ್ಣು ಸೂಕ್ತ. ಚಳಿಗಾಲದ ತಂಪಾದ ವಾತಾವರಣ (15°C–25°C) ಅಗತ್ಯ.\n\n"
                    "2. **ಉನ್ನತ ಇಳುವರಿ ತಳಿಗಳು:**\n"
                    "• HD-2967, PBW-550, DBW-187 (Karan Vandana), DWR-162, ಮತ್ತು DWR-2006 (ಕರ್ನಾಟಕಕ್ಕೆ ಸೂಕ್ತ).\n\n"
                    "3. **ಭೂಮಿ ಸಿದ್ಧತೆ ಮತ್ತು ಬಿತ್ತನೆ:**\n"
                    "• 2–3 ಬಾರಿ ಉಳುಮೆ ಮಾಡಿ ಮಣ್ಣನ್ನು ಹದಗೊಳಿಸಿ. ಬಿತ್ತನೆ ಸಮಯ: ನವೆಂಬರ್ ಮೊದಲನೇ ವಾರದಿಂದ ನವೆಂಬರ್ 25.\n"
                    "• ಬೀಜದ ಪ್ರಮಾಣ: ಎಕರೆಗೆ 40–45 ಕೆ.ಜಿ. ಸಾಲಿನಿಂದ ಸಾಲಿಗೆ 20 ಸೆಂ.ಮೀ. ಅಂತರವಿರಲಿ.\n\n"
                    "4. **ರಸಗೊಬ್ಬರ ಪ್ರಮಾಣ (ಎಕರೆಗೆ NPK):**\n"
                    "• 40 ಕೆ.ಜಿ. ಸಾರಜನಕ, 20 ಕೆ.ಜಿ. ರಂಜಕ, 15 ಕೆ.ಜಿ. ಪೊಟ್ಯಾಶ್. ಬಿತ್ತನೆ ವೇಳೆ ಅರ್ಧ ಸಾರಜನಕ, ಪೂರ್ಣ ರಂಜಕ ಮತ್ತು ಪೊಟ್ಯಾಶ್ ನೀಡಿ; ಉಳಿದ ಸಾರಜನಕವನ್ನು ಮೊದಲ ನೀರಾವರಿ ವೇಳೆ (21ನೇ ದಿನ) ನೀಡಿ.\n\n"
                    "5. **ಕ್ರಾಂತಿಕಾರಿ ನೀರಾವರಿ ಹಂತಗಳು:**\n"
                    "• ಬಿತ್ತಿದ 21ನೇ ದಿನ (ಕಿರೀಟ ಬೇರು ಬಿಡುವ ಹಂತ – CRI), ತೆನೆ ಹೊರಬರುವ ಹಂತ ಮತ್ತು ಕಾಳು ಕಟ್ಟುವ ಹಂತಗಳಲ್ಲಿ ನೀರು ಅತ್ಯಗತ್ಯ.\n\n"
                    "6. **ಕಟಾವು ಮತ್ತು ಇಳುವರಿ:**\n"
                    "• ತೆನೆಗಳು ಬಂಗಾರದ ಬಣ್ಣಕ್ಕೆ ತಿರುಗಿ ಕಾಳುಗಳು ಗಟ್ಟಿಯಾದಾಗ ಕಟಾವು ಮಾಡಿ. ಎಕರೆಗೆ 18–24 ಕ್ವಿಂಟಾಲ್ ಇಳುವರಿ ನಿರೀಕ್ಷಿಸಬಹುದು.\n\n"
                    "👉 ಗೋಧಿ ತಳಿಗಳು, ಕಳೆನಾಶಕ ಅಥವಾ ರಸಗೊಬ್ಬರ ನಿರ್ವಹಣೆಯ ಬಗ್ಗೆ ಇನ್ನಷ್ಟು ತಿಳಿಯಬೇಕೆ? ದಯವಿಟ್ಟು ಕೇಳಿ! 🌾"
                )
            else:
                return (
                    "🌾 **Step-by-Step Cultivation Guide for Wheat (Triticum aestivum):**\n\n"
                    "1. **Soil & Climate Requirements:**\n"
                    "• Well-drained fertile loamy to clay-loam soils with pH 6.0–7.5. Requires cool winter temperatures during vegetative growth.\n\n"
                    "2. **Popular High-Yielding Varieties:**\n"
                    "• HD-2967, PBW-550, DBW-187 (Karan Vandana), HD-3086, GW-322, and DWR-162.\n\n"
                    "3. **Land Preparation & Sowing:**\n"
                    "• Plow 2–3 times to create a fine, pulverized seedbed. Apply 4–5 tonnes/acre of compost or FYM.\n"
                    "• Optimum Sowing: November 1 to November 25. Seed rate: 40–45 kg/acre. Spacing: 20 cm between rows, 4–5 cm deep.\n\n"
                    "4. **Fertilizer Schedule (NPK per Acre):**\n"
                    "• Irrigated Wheat: 48 kg Nitrogen, 24 kg Phosphorus, 16 kg Potash.\n"
                    "• Apply 50% N + 100% P & K as basal dose at sowing; top-dress remaining 50% N at first irrigation (CRI stage, 21 days).\n\n"
                    "5. **Critical Irrigation Stages:**\n"
                    "• 1st: Crown Root Initiation (CRI) at 20–25 days (crucial!)\n"
                    "• 2nd: Tillering (40–45 days)\n"
                    "• 3rd: Boot/Flowering stage (60–65 days)\n"
                    "• 4th: Milking and Grain filling stage (80–95 days)\n\n"
                    "6. **Harvesting & Expected Yield:**\n"
                    "• Harvest when straw turns golden-yellow and moisture drops below 14%. Expected yield: 18–25 quintals per acre.\n\n"
                    "👉 Do you need specific advice on weed control, rust prevention, or fertilizer calculations for your farm? Feel free to ask!"
                )

        # 2. RICE / PADDY (ಭತ್ತ / धान / चावल)
        elif any(w in lower for w in ["rice", "paddy", "ಭತ್ತ", "ಅಕ್ಕಿ", "धान", "चावल", "వరి"]):
            if lang == "kn":
                return (
                    "🌾 **ಭತ್ತ (Paddy / Rice) ಬೆಳೆಯುವ ಹಂತ-ಹಂತದ ಸಂಪೂರ್ಣ ಮಾರ್ಗದರ್ಶನ:**\n\n"
                    "1. **ಮಣ್ಣು:** ನೀರು ಹಿಡಿದಿಟ್ಟುಕೊಳ್ಳುವ ಜೇಡಿ ಮಣ್ಣು ಅಥವಾ ಗೋಡು ಜೇಡಿ ಮಣ್ಣು ಅತ್ಯುತ್ತಮ.\n"
                    "2. **ಉನ್ನತ ತಳಿಗಳು:** ಜ್ಯೋತಿ, ಗಂಗಾವತಿ ಸೋನಾ, ಜಿಂಟೆಕ್ಸ್-1001, ತನು, ಬಿಪಿಟಿ-5204 (ಸಾಂಬಾ ಮಸೂರಿ).\n"
                    "3. **ನಾಟಿ ಮತ್ತು ಬೀಜೋಪಚಾರ:** ಎಕರೆಗೆ 15–20 ಕೆ.ಜಿ. ಬೀಜ. ಸ್ಯೂಡೋಮೊನಾಸ್ ಅಥವಾ ಕಾರ್ಬೆಂಡಾಜಿಮ್‌ನಿಂದ ಬೀಜೋಪಚಾರ ಮಾಡಿ 25 ದಿನಗಳ ಸಸಿಗಳನ್ನು ನಾಟಿ ಮಾಡಿ (20x10 ಸೆಂ.ಮೀ. ಅಂತರ).\n"
                    "4. **ರಸಗೊಬ್ಬರ (NPK):** ಎಕರೆಗೆ 40 ಕೆ.ಜಿ. N, 20 ಕೆ.ಜಿ. P, 20 ಕೆ.ಜಿ. K. ಸಾರಜನಕವನ್ನು ಮೂರು ಕಂತುಗಳಲ್ಲಿ (ನಾಟಿ ವೇಳೆ, ತೆನೆ ಕಟ್ಟುವಾಗ, ಹೂವಾಡುವಾಗ) ನೀಡಿ.\n"
                    "5. **ಇಳುವರಿ:** ಎಕರೆಗೆ 22–28 ಕ್ವಿಂಟಾಲ್ ಭತ್ತ ನಿರೀಕ್ಷಿಸಬಹುದು."
                )
            else:
                return (
                    "🌾 **Step-by-Step Cultivation Guide for Paddy / Rice:**\n\n"
                    "1. **Soil & Field Prep:** Clayey loams with high water retention capacity. Puddle the field 2–3 times and level thoroughly.\n"
                    "2. **Top High-Yield Varieties:** BPT-5204 (Samba Mahsuri), MTU-1010, IR-64, Swarna, Jyothi, and DRR-44.\n"
                    "3. **Sowing & Nursery:** Seed rate: 15–20 kg/acre. Transplant 21–25 day old seedlings at 20 cm x 10 cm spacing (2–3 seedlings per hill).\n"
                    "4. **Fertilizer Management (NPK per acre):** 40 kg Nitrogen, 20 kg Phosphorus, 20 kg Potash. Split N: 50% basal, 25% at tillering, 25% at panicle initiation.\n"
                    "5. **Water & Weed Control:** Keep 2–3 cm standing water till grain hardening; drain 10 days before harvest.\n"
                    "6. **Harvest & Yield:** Harvest at 80% golden grains. Expected yield: 22–30 quintals/acre."
                )

        # 3. MAIZE / CORN (ಮೆಕ್ಕೆಜೋಳ / मक्का)
        elif any(w in lower for w in ["maize", "corn", "ಮೆಕ್ಕೆಜೋಳ", "ಜೋಳ", "मक्का", "మొక్కజొన్న"]):
            return (
                "🌽 **Step-by-Step Cultivation Guide for Maize / Corn:**\n\n"
                "1. **Soil & Sowing:** Well-drained fertile loamy soils. Sowing: Kharif (June–July) or Rabi (Oct–Nov). Seed rate: 7–8 kg/acre. Spacing: 60 cm x 20 cm.\n"
                "2. **Top Hybrids:** CP-818, Dekalb 9108, Pioneer P3396, NK-6240, and NAH-1137.\n"
                "3. **Fertilizer Dosage (per acre):** 60 kg Nitrogen, 24 kg Phosphorus, 20 kg Potash + 10 kg Zinc Sulphate.\n"
                "4. **Fall Armyworm Protection:** Spray *Bacillus thuringiensis* (Bt) or Emamectin benzoate @ 0.4g/litre of water into the whorls.\n"
                "5. **Harvest & Yield:** Harvest when husk covers turn dry-brown. Expected yield: 25–35 quintals/acre."
            )

        # 4. COTTON (ಹತ್ತಿ / कपास)
        elif any(w in lower for w in ["cotton", "ಹತ್ತಿ", "कपास", "పత్తి"]):
            return (
                "🌱 **Step-by-Step Cultivation Guide for Cotton:**\n\n"
                "1. **Soil & Sowing:** Deep black cotton soils (Vertisols) or fertile loams. Sowing time: May to July. Spacing: 90 cm x 60 cm (Bt Cotton).\n"
                "2. **Top Bt Varieties:** RCH-659, Kaveri Jadu, Ankur-3028, and Mallika.\n"
                "3. **NPK Schedule (per acre):** 48 kg Nitrogen, 24 kg Phosphorus, 24 kg Potash applied in 3 splits at vegetative, square, and boll development stages.\n"
                "4. **Pink Bollworm Management:** Install pheromone traps @ 5/acre and spray Neem oil (1500 ppm) or Chlorantraniliprole 18.5% SC @ 0.3 ml/L.\n"
                "5. **Yield:** 10–14 quintals/acre of seed cotton."
            )

        # 5. CHILLI (ಮೆಣಸಿನಕಾಯಿ / मिर्च)
        elif any(w in lower for w in ["chilli", "chilly", "mirchi", "ಮೆಣಸಿನಕಾಯಿ", "ಮೆಣಸಿನ", "मिर्च", "మిర్చి"]):
            return (
                "🌶️ **Step-by-Step Cultivation Guide for Chilli:**\n\n"
                "1. **Soil:** Well-drained sandy loam or clay loam with organic matter. Avoid waterlogged fields.\n"
                "2. **Top Varieties:** G-4, Byadagi Kaddi, Sitara, Teja, and Indam-5.\n"
                "3. **Transplanting:** 30–35 days old seedlings at 60 cm x 45 cm spacing.\n"
                "4. **Fertilizer (NPK per acre):** 40 kg Nitrogen, 20 kg Phosphorus, 20 kg Potash. Apply 50% N + full P, K at planting; balance N in 2 splits.\n"
                "5. **Sucking Pest Control (Thrips/Mites):** Spray Fipronil 5% SC @ 1.5 ml/L or Diafenthiuron 50% WP @ 1g/L.\n"
                "6. **Yield:** Dry chilli 10–15 quintals/acre; green chilli 60–80 quintals/acre."
            )

        # 6. TOMATO (ಟೊಮೆಟೊ / टमाटर)
        elif any(w in lower for w in ["tomato", "ಟೊಮ್ಯಾಟೋ", "ಟೊಮೆಟೊ", "टमाटर", "టమాటా"]):
            return (
                "🍅 **Step-by-Step Cultivation Guide for Tomato:**\n\n"
                "1. **Soil & Nursery:** Deep, loamy soil with good drainage. 25-day seedlings transplanted at 60 cm x 45 cm (or 90 cm on raised beds).\n"
                "2. **Top Hybrids:** Arka Rakshak (triple disease resistant), Arka Abhed, Syngenta Abhinav, and US-440.\n"
                "3. **Fertilizer per Acre:** 60 kg N, 40 kg P, 40 kg K. Drip fertigation with 19:19:19 recommended.\n"
                "4. **Trellising & Staking:** Stake plants with bamboo or twine at 30 days to protect fruits from soil rot.\n"
                "5. **Yield:** 25–35 tonnes per acre under good management."
            )

        # 7. SUGARCANE (ಕಬ್ಬು / गन्ना)
        elif any(w in lower for w in ["sugarcane", "ಕಬ್ಬು", "गन्ना", "చెరకు"]):
            return (
                "🎋 **Step-by-Step Cultivation Guide for Sugarcane:**\n\n"
                "1. **Soil & Planting:** Deep fertile loams or clay loams. Planting seasons: Adsali (July–Aug), Eksali (Jan–Feb). Spacing: 4 to 5 feet row width.\n"
                "2. **Top Varieties:** Co-86032 (Nayana), Co-0238, Co-62175, and VSI-434.\n"
                "3. **Fertilizer (NPK per acre):** 100 kg Nitrogen, 40 kg Phosphorus, 48 kg Potash. Complete earthing up at 120 days.\n"
                "4. **Expected Yield:** 50–70 tonnes/acre."
            )

        # 8. GROUNDNUT / PEANUT (ಕಡಲೆಕಾಯಿ / मूंगफली)
        elif any(w in lower for w in ["groundnut", "peanut", "ಕಡಲೆಕಾಯಿ", "ಶೇಂಗಾ", "मूंगफली", "వేరుశనగ"]):
            return (
                "🥜 **Step-by-Step Cultivation Guide for Groundnut:**\n\n"
                "1. **Soil & Season:** Sandy loams with loose texture to facilitate easy peg penetration. Kharif (June–July) or Rabi/Summer (Dec–Jan).\n"
                "2. **Top Varieties:** TMV-2, JL-24, K-6 (Kadiri), GPBD-4 (rust resistant), and G2-52.\n"
                "3. **Seed Treatment:** Treat pods/kernels with *Trichoderma* @ 5g/kg + Rhizobium culture.\n"
                "4. **Fertilizer:** 10 kg N, 20 kg P, 15 kg K per acre + **Gypsum @ 200 kg/acre at flowering/pegging stage** (critical for pod filling!).\n"
                "5. **Yield:** 10–14 quintals/acre."
            )

        # 9. RAGI / FINGER MILLET (ರಾಗಿ / रागी)
        elif any(w in lower for w in ["ragi", "raagi", "finger millet", "ರಾಗಿ", "रागी", "రాగి"]):
            return (
                "🌾 **Step-by-Step Cultivation Guide for Raagi (Finger Millet):**\n\n"
                "1. **Soil & Climate:** Thrives in red loamy soils. Sowing time: July 15 to August 15. Seed rate: 4–5 kg/acre.\n"
                "2. **Top Varieties:** GPU-28, GPU-48, ML-365, KMR-301, and MR-6.\n"
                "3. **Fertilizer (per acre):** 20 kg Nitrogen, 16 kg Phosphorus, 12 kg Potash (rainfed); double for irrigated.\n"
                "4. **Yield:** 12–16 quintals of grain and 2 tonnes of nutritious straw per acre."
            )

        # 10. GENERAL AGRONOMY GUIDE FOR ANY OTHER CROP
        crop_name = lower.replace("how to grow", "").replace("steps to grow", "").replace("how to cultivate", "").replace("cultivation of", "").replace("guide", "").strip()
        crop_title = crop_name.title() if crop_name else "Crop"
        
        return (
            f"🌾 **Step-by-Step Cultivation Guide for {crop_title}:**\n\n"
            f"1. **Soil & Land Preparation:**\n"
            f"• Deep plow 2–3 times to create a loose, friable seedbed. Incorporate 4–5 tonnes/acre of well-decomposed farmyard manure (FYM).\n\n"
            f"2. **Seed Treatment & Sowing:**\n"
            f"• Treat certified seeds with *Trichoderma viride* @ 5g/kg or Carbendazim @ 2g/kg to prevent damping-off and root diseases.\n"
            f"• Follow recommended regional spacing and sowing depth for {crop_title}.\n\n"
            f"3. **Balanced Plant Nutrition (NPK per Acre):**\n"
            f"• Apply balanced Nitrogen, Phosphorus, and Potash based on soil testing. Provide 50% N and all P & K at planting; top-dress the remaining Nitrogen during peak vegetative growth.\n\n"
            f"4. **Irrigation & Weed Management:**\n"
            f"• Keep the field weed-free during the critical first 30–45 days through inter-cultivation or hand weeding.\n"
            f"• Ensure moisture availability during flowering and yield-forming stages.\n\n"
            f"5. **Plant Protection:**\n"
            f"• Regularly scout for early signs of sucking pests or leaf spots. Apply biological bio-pesticides or recommended ICAR-approved sprays promptly.\n\n"
            f"👉 What specific variety, region, or problem are you facing with {crop_title}? Ask away and I will provide exact dosages!"
        )

    @classmethod
    def get_response(cls, intent: str, lang: str, user_text: str = "") -> str:
        lang = lang if lang in ["kn", "hi", "te", "en"] else "kn"
        if intent == "agronomy_query":
            return cls.get_groq_agronomy_response(user_text, lang)
        intent_responses = cls.RESPONSES.get(intent, cls.RESPONSES["general_inquiry"])
        return intent_responses.get(lang, intent_responses.get("en", ""))


class GoalUnderstandingAgent:
    """
    AGENT 1 — Goal Understanding Agent
    Understands farmer input, detects language, extracts crop, symptoms,
    determines urgency, defines the internal goal, and finds missing info.
    """

    CROP_KEYWORDS = {
        "chilli": ["chilli", "chilly", "mirchi", "ಮೆಣಸಿನಕಾಯಿ", "ಮೆಣಸಿನ", "मिर्च", "మిర్చి", "మిరప"],
        "tomato": ["tomato", "ಟೊಮ್ಯಾಟೋ", "ಟೊಮೆಟೊ", "टमाटर", "టమాటా"],
        "rice": ["rice", "paddy", "ಭತ್ತ", "ಅಕ್ಕಿ", "धान", "चावल", "వరి"],
        "cotton": ["cotton", "ಹತ್ತಿ", "कपास", "పత్తి"],
        "ragi": ["ragi", "raagi", "finger millet", "ರಾಗಿ", "रागी", "రాగి"],
        "maize": ["maize", "corn", "ಮೆಕ್ಕೆಜೋಳ", "ಜೋಳ", "मक्का", "మొక్కజొన్న"],
        "wheat": ["wheat", "ಗೋಧಿ", "गेहूं", "గోధుమ"],
        "sugarcane": ["sugarcane", "ಕಬ್ಬು", "गन्ना", "చెరకు"],
        "groundnut": ["groundnut", "peanut", "ಕಡಲೆಕಾಯಿ", "ಶೇಂಗಾ", "मूंगफली", "వేరుశనగ"],
        "onion": ["onion", "ಈರುಳ್ಳಿ", "ಉಳ್ಳಾಗಡ್ಡಿ", "प्याज", "ఉల్లిపాయ"],
        "potato": ["potato", "ಆಲೂಗಡ್ಡೆ", "ಆಲೂ", "आलू", "బంగాళాదుంప"],
        "brinjal": ["brinjal", "eggplant", "ಬದನೆಕಾಯಿ", "ಬದನೆ", "बैंगन", "వంకాయ"],
        "banana": ["banana", "ಬಾಳೆ", "ಬಾಳೆಹಣ್ಣು", "केला", "అరటి"],
    }

    SYMPTOM_KEYWORDS = {
        "yellowing": ["yellow", "yellowing", "ಹಳದಿ", "ಹಳದಿಯಾಗುತ್ತಿದೆ", "पीला", "पीले", "పసుపు", "పసుపుపచ్చ"],
        "curling": ["curl", "curling", "ಮುದುಡು", "ಮುದುಡುತ್ತಿದೆ", "ಮುದುರಿಕೊಂಡಿದೆ", "मुड़", "ముడుచుకుపోవడం"],
        "drying": ["dry", "drying", "drying up", "ಒಣಗುತ್ತಿದೆ", "ಬಾಡುತ್ತಿದೆ", "सूख", "ఎండిపోవడం"],
        "spots": ["spot", "spots", "ಚುಕ್ಕೆ", "ಮಚ್ಚೆ", "धब्बे", "మచ్చలు"],
        "wilting": ["wilt", "wilting", "ಸೊರಗು", "ಬಾಡು", "मुरझा", "వడలిపోవడం"]
    }

    GREETING_PATTERNS = [
        r"^(hi|hello|hey|hai|namaste|namaskara|namaskar|good\s+morning|good\s+evening|good\s+afternoon)\b",
        r"^(ನಮಸ್ಕಾರ|ಹಲೋ|ಹಾಯ್|ನಮಸ್ತೆ|ಶುಭೋದಯ|ಶುಭ ಸಂಜೆ)",
        r"^(नमस्ते|नमस्कार|हैलो|हेलो|हाय|सुप्रभात)",
        r"^(నమస్కారం|నమస్తే|హలో|హాయ్|శుభోదయం)",
    ]

    IDENTITY_PATTERNS = [
        r"(who\s+are\s+you|what\s+can\s+you\s+do|what\s+is\s+this|what\s+is\s+krishiai|how\s+can\s+you\s+help|what\s+do\s+you\s+do|how\s+to\s+use)",
        r"(ನೀವು\s*ಯಾರು|ನಿಮ್ಮ\s*ಕೆಲಸ\s*ಏನು|ಏನು\s*ಮಾಡಬಲ್ಲಿರಿ|ಹೇಗೆ\s*ಸಹಾಯ|ಕೃಷಿರಕ್ಷಕ್\s*ಅಂದರೇನು|ನೀವು\s*ಹೇಗೆ\s*ಕೆಲಸ)",
        r"(आप\s*कौन\s*हैं|तुम\s*कौन\s*हो|आप\s*क्या\s*कर\s*सकते\s*हैं|कृषि\s*एआई|कैसे\s*मदद)",
        r"(మీరు\s*ఎవరు|మీరు\s*ఏమి\s*చేయగలరు|ఎలా\s*సహాయం)",
    ]

    GRATITUDE_PATTERNS = [
        r"^(thanks|thank\s+you|thx|great|awesome|dhanyavad|dhanyavada)\b",
        r"(ಧನ್ಯವಾದಗಳು|ಧನ್ಯವಾದ|ತುಂಬಾ\s*ಉಪಕಾರ)",
        r"(धन्यवाद|शुक्रिया|बहुत\s*अच्छा)",
        r"(ధన్యవాదాలు|చాలా\s*కృతజ్ఞతలు)",
    ]

    AGRONOMY_PATTERNS = [
        r"(steps\s+to\s+grow|how\s+to\s+grow|how\s+to\s+cultivate|how\s+to\s+plant|cultivation\s+steps|growing\s+guide|package\s+of\s+practices)",
        r"(best\s+fertilizer|fertilizer\s+schedule|seed\s+treatment|seed\s+rate|spacing|sowing\s+time|nursery|transplanting|harvesting|irrigation)",
        r"(ಹಂತಗಳು|ಬೆಳೆಯುವುದು\s*ಹೇಗೆ|ಬೇಸಾಯ\s*ಕ್ರಮ|ಬೆಳೆ\s*ಪದ್ಧತಿ|ಬಿತ್ತನೆ|ಗೊಬ್ಬರ\s*ನಿರ್ವಹಣೆ|ತಳಿಗಳು|ಇಳುವರಿ|ಕಟಾವು)",
        r"(उगाने\s*के\s*चरण|कैसे\s*उगाएं|खेती\s*की\s*विधि|पैदावार|बुवाई|उर्वरक\s*प्रबंधन|किस्में)",
        r"(సాగు\s*విధానం|ఎలా\s*పండించాలి|విత్తన\s*శుద్ధి|ఎరువుల\s*యాజమాన్యం)",
    ]

    CROPS_SUPPORTED_PATTERNS = [
        r"(which\s+crops|what\s+crops|crops\s+supported|list\s+crops)",
        r"(ಯಾವ\s*ಬೆಳೆಗಳು|ಬೆಳೆಗಳ\s*ಪಟ್ಟಿ|ಯಾವ\s*ಬೆಳೆಗೆ\s*ಸಹಾಯ)",
        r"(कौन\s*सी\s*फसलें|फसलों\s*की\s*सूची)",
        r"(ఏ\s*పంటలు|పంటల\s*జాబితా)",
    ]

    PROBLEM_KEYWORDS = [
        "damage", "damaged", "dying", "disease", "pest", "rot", "symptom", "help", "attack",
        "ಹಾಳಾಗಿದೆ", "ಹಾಳಾಗುತ್ತಿದೆ", "ಸಾಯುತ್ತಿದೆ", "ಸಮಸ್ಯೆ", "ರೋಗ", "ಕೀಟ", "ಬಾಡಿದೆ", "ಸಹಾಯ ಮಾಡಿ",
        "नुकसान", "खराब", "मर", "बीमारी", "कीड़ा", "समस्या", "मदद",
        "నష్టం", "పాడైపోయింది", "చనిపోతున్నాయి", "తెగులు", "పురుగు", "సమస్య"
    ]

    @classmethod
    def classify_intent(cls, text: str, has_image: bool = False) -> str:
        if has_image:
            return "crop_problem"

        text_clean = text.strip().lower()
        if not text_clean:
            return "greeting"

        # 1. Check if text matches agronomy / cultivation guide questions (e.g., 'steps to grow raagi')
        if any(re.search(p, text_clean) for p in cls.AGRONOMY_PATTERNS):
            return "agronomy_query"

        # 2. Check if text mentions explicit symptoms
        has_symptoms = False
        for sym_type, words in cls.SYMPTOM_KEYWORDS.items():
            if any(w in text_clean for w in words):
                has_symptoms = True
                break

        # 3. Check if text mentions problem / damage / emergency
        has_problem = any(w in text_clean for w in cls.PROBLEM_KEYWORDS)

        if has_symptoms or has_problem:
            return "crop_problem"

        # 4. Check crops supported query
        if any(re.search(p, text_clean) for p in cls.CROPS_SUPPORTED_PATTERNS):
            return "crops_supported"

        # 5. Check identity / capabilities
        if any(re.search(p, text_clean) for p in cls.IDENTITY_PATTERNS):
            return "identity"

        # 6. Check gratitude
        if any(re.search(p, text_clean) for p in cls.GRATITUDE_PATTERNS):
            return "gratitude"

        # 7. Check pure greeting
        if any(re.search(p, text_clean) for p in cls.GREETING_PATTERNS):
            return "greeting"

        # 8. Check if crop name is mentioned alone
        has_crop = False
        for crop, words in cls.CROP_KEYWORDS.items():
            if any(w in text_clean for w in words):
                has_crop = True
                break

        if has_crop:
            # If asking how / steps / growing
            if any(w in text_clean for w in ["grow", "step", "plant", "cultivat", "yield", "rate", "time", "season"]):
                return "agronomy_query"
            return "crops_supported"

        # 9. Short pure conversational input (strictly no question/agronomy terms)
        words = text_clean.split()
        if len(words) <= 3 and not any(w in text_clean for w in ["step", "grow", "how", "what", "why", "when"]):
            return "greeting"

        return "agronomy_query" if any(w in text_clean for w in ["grow", "crop", "plant", "farm", "fertilizer"]) else "general_inquiry"

    @classmethod
    def process(cls, text: str, preferred_lang: str = None, has_image: bool = False) -> Dict[str, Any]:
        detected_lang = preferred_lang or MultilingualService.detect_language(text)
        text_lower = text.lower()

        # Extract crop
        identified_crop = "chilli"  # default reference crop
        for crop, words in cls.CROP_KEYWORDS.items():
            if any(w in text_lower for w in words):
                identified_crop = crop
                break

        # Extract symptoms
        identified_symptoms = []
        for sym_type, words in cls.SYMPTOM_KEYWORDS.items():
            if any(w in text_lower for w in words):
                identified_symptoms.append(sym_type)

        has_explicit_symptoms = len(identified_symptoms) > 0
        if not identified_symptoms:
            identified_symptoms = ["yellowing", "curling"]

        # Detect urgency
        urgency = "Medium"
        if any(w in text_lower for w in ["dying", "ಹಾಳಾಗುತ್ತಿದೆ", "ಸಾಯುತ್ತಿದೆ", "मर रहे", "नाश", "తీవ్రం", "emergency", "urgent", "help"]):
            urgency = "High"

        # Missing information analysis
        missing_info = []
        if not has_image:
            missing_info.append("crop_leaf_image")
        if "few" not in text_lower and "whole" not in text_lower and "ಎಷ್ಟು" not in text_lower and "ಎಲ್ಲಾ" not in text_lower:
            missing_info.append("spread_extent")

        # Intent classification
        intent = cls.classify_intent(text, has_image)

        if intent != "crop_problem":
            # Conversational or general FAQ intent
            goal_titles = {
                "kn": "ಸಾಮಾನ್ಯ ವಿಚಾರಣೆ ಮತ್ತು ಕೃಷಿ ಮಾರ್ಗದರ್ಶನ",
                "hi": "सामान्य पूछताछ एवं कृषि मार्गदर्शन",
                "te": "సాధారణ విచారణ మరియు వ్యవసాయ మార్గదర్శకత్వం",
                "en": "General Inquiry & Farming Assistance"
            }
            return {
                "language": detected_lang,
                "crop": identified_crop,
                "symptoms": [],
                "urgency": "Low",
                "farmer_goal": goal_titles.get(detected_lang, goal_titles["en"]),
                "missing_info": [],
                "is_sufficient": True,
                "intent": intent
            }

        # Sufficient only if image is attached or explicit symptoms were provided with crop
        is_sufficient = bool(has_image or (has_explicit_symptoms and len(identified_symptoms) >= 2))
        crop_names = {
            "chilli": {"kn": "ಮೆಣಸಿನಕಾಯಿ", "hi": "मिर्च", "te": "మిర్చి", "en": "Chilli"},
            "tomato": {"kn": "ಟೊಮೆಟೊ", "hi": "टमाटर", "te": "టమాటా", "en": "Tomato"},
            "rice": {"kn": "ಭತ್ತ", "hi": "धान", "te": "వరి", "en": "Paddy/Rice"},
            "cotton": {"kn": "ಹತ್ತಿ", "hi": "कपास", "te": "పత్తి", "en": "Cotton"}
        }
        c_name = crop_names.get(identified_crop, {}).get(detected_lang, identified_crop.capitalize())

        goal_templates = {
            "kn": f"{c_name} ಬೆಳೆಯಲ್ಲಿ ಎಲೆ ಹಳದಿ ಮತ್ತು ಮುದುಡುವ ಸಮಸ್ಯೆಯ ಮೂಲ ಕಾರಣವನ್ನು ಪತ್ತೆಹಚ್ಚುವುದು, ಹಾನಿ ತಡೆಗಟ್ಟಲು ತಕ್ಷಣದ ಕ್ರಮಗಳನ್ನು ಶಿಫಾರಸು ಮಾಡುವುದು ಮತ್ತು ಬೆಳೆ ಚೇತರಿಕೆಯನ್ನು ಮೇಲ್ವಿಚಾರಣೆ ಮಾಡುವುದು.",
            "hi": f"{c_name} की फसल में पत्तियों के पीलेपन और मुड़ने के संभावित कारणों की जांच करना, तत्काल कार्रवाई योजना बनाना और फसल सुधार की निगरानी करना।",
            "te": f"{c_name} పంటలో ఆకులు పసుపు రంగులోకి మారడం మరియు ముడుచుకుపోవడానికి గల కారణాలను గుర్తించి, తక్షణ కార్యాచరణ ప్రణాళికను సిద్ధం చేయడం మరియు పర్యవేక్షించడం.",
            "en": f"Investigate the {identified_crop} crop problem, identify likely causes, recommend immediate actionable remedies, and monitor crop recovery over multiple days."
        }
        farmer_goal = goal_templates.get(detected_lang, goal_templates["kn"])

        return {
            "language": detected_lang,
            "crop": identified_crop,
            "symptoms": identified_symptoms,
            "urgency": urgency,
            "farmer_goal": farmer_goal,
            "missing_info": missing_info,
            "is_sufficient": is_sufficient,
            "intent": "crop_problem"
        }


class InvestigationAgent:
    """
    AGENT 2 — Investigation Agent
    Determines what information is missing, asks only the single most targeted next question,
    requests a crop photo, and selects required tools.
    """

    @classmethod
    def get_targeted_question(cls, missing_info: List[str], lang: str) -> str:
        if "crop_leaf_image" in missing_info:
            return MultilingualService.get_question("request_image", lang)
        elif "spread_extent" in missing_info:
            return MultilingualService.get_question("spread_question", lang)
        return MultilingualService.get_question("irrigation_question", lang)

    @classmethod
    def select_tools(cls, crop: str, symptoms: List[str], has_image: bool) -> List[str]:
        tools = ["search_crop_disease_database", "get_weather", "search_agriculture_knowledge_base"]
        if has_image:
            tools.insert(0, "analyze_crop_image")
        tools.append("create_follow_up_plan")
        return tools


class CropDiagnosisAgent:
    """
    AGENT 3 — Crop Diagnosis Agent
    Combines: Image Analysis + Farmer Symptoms + Weather Risk + Agronomic Knowledge
    Returns ranked causes with calibrated confidence levels.
    """

    @classmethod
    def diagnose(
        cls,
        crop: str,
        symptoms: List[str],
        image_result: Dict[str, Any] = None,
        weather_result: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        # Query disease knowledge base
        disease_results = disease_database_tool.search(crop, symptoms)

        # Incorporate visual features if image was provided
        if image_result and image_result.get("status") == "success":
            visual_symptoms = image_result.get("detected_symptoms", [])
            for res in disease_results:
                if any("curl" in vs.lower() for vs in visual_symptoms) and "curl" in res["condition"].lower():
                    res["confidence_score"] = min(0.92, res["confidence_score"] + 0.12)
                    res["probability"] = "High"
                elif any("spot" in vs.lower() or "dieback" in vs.lower() for vs in visual_symptoms) and "dieback" in res["condition"].lower():
                    res["confidence_score"] = min(0.88, res["confidence_score"] + 0.15)
                    res["probability"] = "High"

        # Incorporate weather risk factors
        if weather_result:
            if weather_result.get("fungal_disease_risk") == "High":
                for res in disease_results:
                    if res["category"] == "Fungal Disease":
                        res["confidence_score"] = min(0.89, res["confidence_score"] + 0.08)

        # Ensure probabilities are calibrated
        formatted_causes = []
        for item in disease_results[:3]:
            conf = item["confidence_score"]
            prob = "High" if conf >= 0.70 else ("Medium" if conf >= 0.40 else "Low")
            formatted_causes.append({
                "cause": item["condition"],
                "probability": prob,
                "confidence_score": conf,
                "symptoms_matched": symptoms,
                "explanation": f"{item['primary_cause']} ({item['category']}). Environmental trigger: {item['environmental_factors']}."
            })

        return formatted_causes


class WeatherRiskAgent:
    """
    AGENT 4 — Weather Risk Agent
    Checks local temperature, humidity, rainfall, and wind to flag fungal/pest windows.
    """

    @classmethod
    def evaluate_weather(cls, location: str = "Mandya, Karnataka") -> Dict[str, Any]:
        return weather_tool.get_weather(location)


class ActionPlanningAgent:
    """
    AGENT 5 — Agricultural Action Planning Agent
    Converts investigation results into a practical, step-by-step action plan:
    IMMEDIATE ACTIONS, SHORT-TERM ACTIONS, WHAT TO MONITOR, WHEN TO ESCALATE.
    Translates into user language (Kannada, Hindi, Telugu, English).
    """

    @classmethod
    def build_action_plan(
        cls,
        crop: str,
        top_cause: Dict[str, Any],
        lang: str,
        weather_info: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        # Localized action plans for Chilli Leaf Curl / Yellowing (the central demo scenario)
        if "chilli" in crop.lower():
            if lang == "kn":
                immediate = [
                    "ಪ್ರತಿ ಎಕರೆಗೆ 15-20 ನೀಲಿ ಅಂಟು ಬಲೆಗಳನ್ನು (Blue sticky traps) ಗಿಡದ ಎತ್ತರದಲ್ಲಿ ಕಟ್ಟಿ - ಇದು ಎಲೆ ಮುದುಡುವ ಥ್ರಿಪ್ಸ್ ಕೀಟಗಳನ್ನು ನಿಯಂತ್ರಿಸುತ್ತದೆ.",
                    "1 ಲೀಟರ್ ನೀರಿಗೆ 3 ಮಿಲಿ ಬೇವಿನ ಎಣ್ಣೆ (Neem Oil 10,000 ppm) ಅಥವಾ 5% ಬೇವಿನ ಬೀಜದ ಕಷಾಯ (NSKE) ಮಿಶ್ರಣ ಮಾಡಿ ಎಲೆಗಳ ಕೆಳಭಾಗಕ್ಕೆ ಸಂಪೂರ್ಣವಾಗಿ ಸಿಂಪಡಿಸಿ.",
                    "ಹೆಚ್ಚಿನ ಯೂರಿಯಾ (ಸಾರಜನಕ) ಗೊಬ್ಬರ ನೀಡುವುದನ್ನು ತಕ್ಷಣ ನಿಲ್ಲಿಸಿ; ಇದು ಎಲೆಗಳನ್ನು ಮೃದುಗೊಳಿಸಿ ರಸಹೀರುವ ಕೀಟಗಳನ್ನು ಹೆಚ್ಚು ಆಕರ್ಷಿಸುತ್ತದೆ."
                ]
                short_term = [
                    "ಕೀಟ ಬಾಧೆ ಹೆಚ್ಚಾಗಿದ್ದರೆ: 1 ಲೀಟರ್ ನೀರಿಗೆ 1 ಮಿಲಿ ಸ್ಪಿನೆಟೋರಾಮ್ 11.7% SC (Spinetoram) ಅಥವಾ 2 ಮಿಲಿ ಫಿಪ್ರೋನಿಲ್ 5% SC ಸಿಂಪಡಿಸಿ.",
                    "4 ದಿನಗಳ ನಂತರ ಎಲೆಗಳು ಮತ್ತೆ ಹಸಿರಾಗಲು: 1 ಲೀಟರ್ ನೀರಿಗೆ 2.5 ಗ್ರಾಂ ಸೂಕ್ಷ್ಮ ಪೋಷಕಾಂಶಗಳ ಮಿಶ್ರಣ (Multi-Micronutrient) ಮತ್ತು 5 ಗ್ರಾಂ 19:19:19 ಗೊಬ್ಬರ ಬೆರೆಸಿ ಸಿಂಪಡಿಸಿ."
                ]
                monitoring = [
                    "3 ದಿನಗಳ ನಂತರ ಗಿಡದ ತುದಿಯಲ್ಲಿ ಹೊಸದಾಗಿ ಬರುವ ಎಲೆಗಳನ್ನು ಗಮನಿಸಿ - ಹೊಸ ಎಲೆಗಳು ಮುದುಡದೆ ಅಗಲವಾಗಿ, ಹಸಿರಾಗಿ ಬೆಳೆಯಬೇಕು.",
                    "ಅಂಟು ಬಲೆಗಳಿಗೆ ಬಿದ್ದಿರುವ ಕೀಟಗಳ ಸಂಖ್ಯೆ ಕಡಿಮೆಯಾಗುತ್ತಿದೆಯೇ ಎಂದು ಪ್ರತಿದಿನ ಪರಿಶೀಲಿಸಿ."
                ]
                escalation = [
                    "7 ದಿನಗಳ ನಂತರವೂ ಶೇಕಡಾ 40 ಕ್ಕಿಂತ ಹೆಚ್ಚು ಗಿಡಗಳು ಹಳದಿಯಾಗಿ ಗಿಡ್ಡವಾಗಿದ್ದರೆ ತಕ್ಷಣ ಸ್ಥಳೀಯ ರೈತ ಸಂಪರ್ಕ ಕೇಂದ್ರ ಅಥವಾ ಕೃಷಿ ವಿಜ್ಞಾನ ಕೇಂದ್ರ (KVK) ಅಧಿಕಾರಿಯನ್ನು ಭೇಟಿ ಮಾಡಿ."
                ]
                summary = "ಮೆಣಸಿನಕಾಯಿ ಬೆಳೆಯಲ್ಲಿ ಎಲೆ ಹಳದಿ ಮತ್ತು ಮುದುಡುವಿಕೆಗೆ ಕೀಟಗಳ ಹಾವಳಿ ಪ್ರಮುಖ ಕಾರಣವಾಗಿದೆ. ತಕ್ಷಣ ಬೇವಿನ ಸಿಂಪರಣೆ ಮತ್ತು ಅಂಟು ಬಲೆಗಳನ್ನು ಬಳಸಿ."

            elif lang == "hi":
                immediate = [
                    "प्रति एकड़ 15-20 नीले चिपचिपे ट्रैप (Blue sticky traps) लगाएं ताकि थ्रिप्स कीट नियंत्रित हो सकें।",
                    "1 लीटर पानी में 3 मिली नीम का तेल (10,000 ppm) मिलाकर पत्तियों के निचले हिस्से पर अच्छी तरह छिड़काव करें।",
                    "यूरिया (रासायनिक नाइट्रोजन) का अत्यधिक उपयोग तुरंत रोकें, क्योंकि इससे पत्तियां कोमल होकर कीटों को आकर्षित करती हैं।"
                ]
                short_term = [
                    "यदि कीट अधिक हैं: 1 लीटर पानी में 1 मिली स्पिनेटोरम (Spinetoram 11.7% SC) या 2 मिली फिप्रोनिल (Fipronil 5% SC) का छिड़काव करें।",
                    "4 दिन बाद पत्तियों के हरित लवक सुधार के लिए: 19:19:19 घुलनशील उर्वरक (5 ग्राम/लीटर) और सूक्ष्म पोषक तत्वों का छिड़काव करें।"
                ]
                monitoring = [
                    "3 दिन बाद नई आने वाली कोपलों को देखें—नई पत्तियां बिना मुड़े सपाट और हरी निकलनी चाहिए।",
                    "चिपचिपे ट्रैप पर पकड़े गए कीटों की संख्या की दैनिक जांच करें।"
                ]
                escalation = [
                    "यदि 7 दिनों के बाद भी 40% से अधिक पौधे पीले और बौने रह जाएं, तो नजदीकी कृषि विज्ञान केंद्र (KVK) के वैज्ञानिक से संपर्क करें।"
                ]
                summary = "मिर्च की फसल में पत्तियों के पीलेपन और मुड़ने का मुख्य कारण थ्रिप्स कीट है। तुरंत नीम छिड़काव और ट्रैप स्थापित करें।"

            elif lang == "te":
                immediate = [
                    "ఎకరాకు 15-20 నీలి రంగు జిగురు అట్టలను (Blue Sticky Traps) అమర్చండి; ఇది తామర పురుగులను (Thrips) నివారిస్తుంది.",
                    "లీటరు నీటికి 3 మి.లీ వేప నూనె (10,000 ppm) కలిపి ఆకుల అడుగుభాగం తడిచేలా పిచికారీ చేయండి.",
                    "రసాయన యూరియా వినియోగాన్ని వెంటనే తాత్కాలికంగా నిలిపివేయండి."
                ]
                short_term = [
                    "పురుగుల ఉధృతి ఎక్కువగా ఉంటే: లీటరు నీటికి 1 మి.లీ స్పినెటోరామ్ 11.7% SC లేదా 2 మి.లీ ఫిప్రోనిల్ 5% SC పిచికారీ చేయండి.",
                    "4 రోజుల తర్వాత ఆకులు పచ్చబడటానికి: 19:19:19 ఎరువు (5 గ్రా/లీ) మరియు సూక్ష్మ పోషకాలను పిచికారీ చేయండి."
                ]
                monitoring = [
                    "3 రోజుల తర్వాత పైభాగాన వచ్చే కొత్త చిగుర్లను గమనించండి—కొత్త ఆకులు ముడుచుకోకుండా నిటారుగా రావాలి.",
                    "జిగురు అట్టలపై పురుగుల తీవ్రత తగ్గుతోందో లేదో రోజూ చూడండి."
                ]
                escalation = [
                    "7 రోజుల తర్వాత కూడా సమస్య తగ్గకపోతే సమీప కృషి విజ్ఞాన కేంద్రాన్ని (KVK) సంప్రదించండి."
                ]
                summary = "మిరప పంటలో ఆకుల పసుపు రంగు మరియు ముడుతకు రసం పీల్చే పురుగులు కారణం. తక్షణ నివారణ చర్యలు చేపట్టండి."

            else:
                immediate = [
                    "Install 15-20 blue sticky traps per acre at canopy level to trap flying thrips, and yellow traps for whiteflies.",
                    "Foliar spray with 10,000 ppm Neem Oil @ 3 ml/litre or 5% NSKE, ensuring thorough coverage on the underside of leaves.",
                    "Halt excessive chemical nitrogen top-dressing immediately; lush tender growth aggravates sucking pests."
                ]
                short_term = [
                    "For acute pest pressure: Spray Spinetoram 11.7% SC @ 1 ml/litre or Fipronil 5% SC @ 2 ml/litre in calm weather.",
                    "After 4 days: Apply foliar multi-micronutrient mixture @ 2.5 g/litre + water-soluble 19:19:19 @ 5 g/litre for chlorophyll recovery."
                ]
                monitoring = [
                    "Inspect new apical flushes on Day 3: newly emerging leaves should unfold flat, glossy, and green without crinkles.",
                    "Monitor sticky trap counts daily to verify reduction in pest vectors."
                ]
                escalation = [
                    "If over 40% of plants show irreversible stunted rosette growth or black dieback after 7 days, escalate directly to your local KVK agronomist."
                ]
                summary = "Chilli leaf yellowing and upward curling is primarily driven by thrips and leaf curl vectors. Begin with sticky traps and bio-botanical spray immediately."

        else:
            # Fallback general crop plan
            immediate = [
                "Inspect soil moisture around the root zone; ensure no standing water or severe drought stress.",
                "Spray organic 10,000 ppm Neem Oil @ 3 ml/litre as a broad-spectrum preventive shield."
            ]
            short_term = [
                "Apply balanced foliar 19:19:19 NPK (5 g/litre) after 4 days to stimulate leaf greening."
            ]
            monitoring = ["Observe newly emerging leaves for healthy color on Day 3."]
            escalation = ["Consult local Agricultural Officer if yellowing turns necrotic or spreads rapidly."]
            summary = "Immediate protective measures initiated for your crop. Follow the monitoring schedule."

        return {
            "immediate_actions": immediate,
            "short_term_actions": short_term,
            "monitoring_actions": monitoring,
            "escalation_conditions": escalation,
            "localized_summary": summary
        }


class GovtAssistanceAgent:
    """
    AGENT 6 — Government Assistance Agent
    Connects farmer context to relevant government schemes (PMFBY, PM-KISAN, KCC, Soil Health).
    """

    @classmethod
    def find_relevant_assistance(cls, crop: str, problem: str, location: str = "") -> List[Dict[str, Any]]:
        return govt_schemes_tool.search(location, problem)


class FollowUpAgent:
    """
    AGENT 7 — Follow-Up Agent
    Closed-loop progress tracking: Day 1 vs Day 3/5/7.
    Compares observations, classifies progress (Improving / Stable / Worsening),
    adapts action plan or completes goal with prevention advice.
    """

    @classmethod
    def evaluate_follow_up(
        cls,
        previous_image: str,
        new_image: str,
        farmer_response: str,
        condition_assessment: str,
        lang: str,
        crop: str = "chilli"
    ) -> Dict[str, Any]:
        comparison = image_comparator_tool.compare_crop_images(
            previous_image=previous_image,
            new_image=new_image,
            farmer_feedback_text=farmer_response,
            condition_hint=condition_assessment
        )

        status = comparison["comparison_result"]  # Improving, Stable, Worsening

        if status == "Improving":
            goal_status = "Improving"
            if lang == "kn":
                response_text = "ಅಭಿನಂದನೆಗಳು! ನಿಮ್ಮ ಬೆಳೆಯ ಸ್ಥಿತಿಯಲ್ಲಿ ಸಕಾರಾತ್ಮಕ ಸುಧಾರಣೆ ಕಂಡುಬಂದಿದೆ. ಹೊಸದಾಗಿ ಚಿಗುರುತ್ತಿರುವ ಎಲೆಗಳು ಹಸಿರಾಗಿ ಹರಡಿಕೊಳ್ಳುತ್ತಿವೆ ಮತ್ತು ಹಳದಿ ಬಣ್ಣ ಕಡಿಮೆಯಾಗಿದೆ. ಈ ಯಶಸ್ವಿ ಚೇತರಿಕೆಯ ನಂತರ ಮುನ್ನೆಚ್ಚರಿಕಾ ಕ್ರಮಗಳನ್ನು ಮುಂದುವರಿಸಿ."
                prevention = "ಮುನ್ನೆಚ್ಚರಿಕೆ: ಪ್ರತಿ 15 ದಿನಗಳಿಗೊಮ್ಮೆ ಬೇವಿನ ಎಣ್ಣೆ (3 ಮಿಲಿ/ಲೀಟರ್) ಸಿಂಪಡಿಸಿ. ಹೊಲದ ಬದುಗಳಲ್ಲಿ ಕಳೆಗಳನ್ನು ಬೆಳೆಯಲು ಬಿಡಬೇಡಿ."
            elif lang == "hi":
                response_text = "बधाई हो! आपकी फसल की स्थिति में सकारात्मक सुधार देखा गया है। नई पत्तियां हरी निकल रही हैं और पीलापन काफी कम हुआ है। उपचार जारी रखें।"
                prevention = "रोकथाम सलाह: हर 15 दिनों में नीम तेल (3 मिली/लीटर) का छिड़काव जारी रखें। खेत की मेड़ों को खरपतवार मुक्त रखें।"
            elif lang == "te":
                response_text = "అభినందనలు! మీ పంట పరిస్థితిలో మంచి మెరుగుదల కనిపిస్తోంది. కొత్తగా వచ్చే ఆకులు పచ్చగా, వెడల్పుగా వస్తున్నాయి. ఇదే జాగ్రత్తలను కొనసాగించండి."
                prevention = "ముందస్తు జాగ్రత్త: ప్రతి 15 రోజులకు ఒకసారి వేపనూనె (3 మి.లీ/లీ) పిచికారీ చేయండి. గట్లపై కలుపు లేకుండా చూసుకోండి."
            else:
                response_text = "Great news! Noticeable crop recovery detected. New apical flushes are unfolding glossy and green with a 35% decrease in chlorosis. Goal is on track to completion!"
                prevention = "Long-term prevention: Maintain bi-weekly preventive neem sprays (3 ml/L) and keep field bunds free of weed hosts."

            escalation = False
            experts = []
            updated_plan = None

        elif status == "Worsening":
            goal_status = "Needs Attention"
            escalation = True
            experts = expert_finder_tool.find_experts()

            if lang == "kn":
                response_text = "ಎಚ್ಚರಿಕೆ: ನಿಮ್ಮ ಬೆಳೆಯ ಹಾನಿ ಹೆಚ್ಚಾಗಿದೆ ಅಥವಾ ಹಳದಿ ಬಣ್ಣ ಮುಂದುವರಿದಿದೆ. ಸಾಮಾನ್ಯ ಮನೆಮದ್ದುಗಳು ಸಾಕಾಗುತ್ತಿಲ್ಲ. ಬೆಳೆ ರಕ್ಷಣೆಗಾಗಿ ತಕ್ಷಣ ಕೃಷಿ ಅಧಿಕಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸಲು ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ."
                prevention = "ತಕ್ಷಣ ತುರ್ತು ಕೀಟನಾಶಕ ಬದಲಾವಣೆ ಅಗತ್ಯವಿದೆ."
            elif lang == "hi":
                response_text = "सावधानी: फसल में क्षति बढ़ रही है और पत्तियां अधिक प्रभावित हो रही हैं। तत्काल कृषि विशेषज्ञ से संपर्क करने की सलाह दी जाती है।"
                prevention = "तत्काल वैकल्पिक उपचार और विशेषज्ञ निरीक्षण की आवश्यकता है।"
            elif lang == "te":
                response_text = "హెచ్చరిక: పంట సమస్య తీవ్రమవుతోంది. సాధారణ నివారణ సరిపోవడం లేదు. వెంటనే వ్యవసాయ అధికారి లేదా KVK శాస్త్రవేత్తను సంప్రదించండి."
                prevention = "వెంటనే నిపుణుల సలహాతో బలమైన రసాయన పిచికారీ చేయాలి."
            else:
                response_text = "Urgent: Symptoms are worsening and yellowing is spreading to higher foliage. Normal intervention insufficient. Escalating directly to local agricultural experts."
                prevention = "Requires on-site agronomist inspection and targeted curative systemic intervention."

            updated_plan = {
                "immediate_actions": [
                    "Halt all current foliar sprays immediately to avoid phytotoxicity.",
                    "Collect 3 symptomatic plant samples in a clean plastic bag.",
                    "Call Kisan Call Centre Toll-Free (1800-180-1551) or visit nearest KVK office today."
                ],
                "short_term_actions": [
                    "Follow official pesticide prescription issued by the visiting agricultural officer."
                ],
                "monitoring_actions": [
                    "Check daily for any plant stem wilting or root rot."
                ],
                "escalation_conditions": [
                    "Active severe escalation in progress."
                ],
                "localized_summary": "Urgent expert intervention triggered."
            }

        else:
            # Stable
            goal_status = "Monitoring"
            escalation = False
            experts = []
            if lang == "kn":
                response_text = "ನಿಮ್ಮ ಬೆಳೆಯ ಸ್ಥಿತಿ ಸ್ಥಿರವಾಗಿದೆ (ಹಾನಿ ಹರಡುವುದು ನಿಂತಿದೆ). ಆದರೆ ಸಂಪೂರ್ಣ ಚೇತರಿಕೆಗೆ ಇನ್ನೂ 3-4 ದಿನಗಳು ಬೇಕಾಗಬಹುದು. ಪೋಷಕಾಂಶಗಳ ಸಿಂಪರಣೆಯನ್ನು ಮುಂದುವರಿಸಿ."
                prevention = "ಹೊಸ ಚಿಗುರು ಬರುವವರೆಗೆ ಮಣ್ಣಿನಲ್ಲಿ ಹದವಾದ ತೇವಾಂಶ ಕಾಪಾಡಿಕೊಳ್ಳಿ."
            elif lang == "hi":
                response_text = "आपकी फसल की स्थिति स्थिर है। क्षति का फैलाव रुक गया है। पूर्ण सुधार के लिए पोषण छिड़काव जारी रखें।"
                prevention = "हल्की नमी बनाए रखें।"
            elif lang == "te":
                response_text = "మీ పంట పరిస్థితి స్థిరంగా ఉంది. నష్టం వ్యాపించడం ఆగింది. కొత్త చిగుళ్లు వచ్చే వరకు తగిన పోషణ ఇవ్వండి."
                prevention = "తేలికపాటి తేమను కొనసాగించండి."
            else:
                response_text = "Crop condition is stable. Disease progression is arrested. Continue supportive micronutrient foliar spray and monitor for new flush."
                prevention = "Maintain steady root zone moisture without waterlogging."

            updated_plan = None

        return {
            "comparison_result": status,
            "goal_status": goal_status,
            "response_text": response_text,
            "prevention_guidance": prevention,
            "expert_escalation_recommended": escalation,
            "expert_contacts": experts,
            "updated_action_plan": updated_plan,
            "comparison_details": comparison
        }

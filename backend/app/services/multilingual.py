import re
from typing import Dict, Any, List

class MultilingualService:
    @staticmethod
    def detect_language(text: str) -> str:
        if not text:
            return "kn"
        
        # Check Kannada script: U+0C80 to U+0CFF
        kannada_chars = len(re.findall(r'[\u0C80-\u0CFF]', text))
        # Check Devanagari (Hindi) script: U+0900 to U+097F
        hindi_chars = len(re.findall(r'[\u0900-\u097F]', text))
        # Check Telugu script: U+0C00 to U+0C7F
        telugu_chars = len(re.findall(r'[\u0C00-\u0C7F]', text))
        
        counts = {
            "kn": kannada_chars,
            "hi": hindi_chars,
            "te": telugu_chars,
        }
        
        max_lang = max(counts, key=counts.get)
        if counts[max_lang] > 0:
            return max_lang
            
        return "en"

    # UI and Agent activity translations
    ACTIVITY_MESSAGES = {
        "kn": {
            "understanding": "✓ ನಿಮ್ಮ ಕೃಷಿ ಸಮಸ್ಯೆಯನ್ನು ಅರ್ಥೈಸಿಕೊಳ್ಳಲಾಗುತ್ತಿದೆ",
            "checking_crop": "✓ ಬೆಳೆ ಮತ್ತು ರೋಗಲಕ್ಷಣಗಳ ವಿವರ ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ",
            "analyzing_image": "✓ ನಿಮ್ಮ ಬೆಳೆಯ ಚಿತ್ರವನ್ನು ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ",
            "checking_weather": "✓ ಸ್ಥಳೀಯ ಹವಾಮಾನ ಅಪಾಯಗಳನ್ನು ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ",
            "preparing_plan": "✓ ನಿಖರವಾದ ಕಾರ್ಯ ಯೋಜನೆಯನ್ನು ಸಿದ್ಧಪಡಿಸಲಾಗುತ್ತಿದೆ",
            "evaluating_followup": "✓ ಬೆಳೆಯ ಸುಧಾರಣೆಯ ಸ್ಥಿತಿಯನ್ನು ಹೋಲಿಸಿ ಮೌಲ್ಯಮಾಪನ ಮಾಡಲಾಗುತ್ತಿದೆ",
            "greeting_handled": "✓ ಆತ್ಮೀಯ ಸ್ವಾಗತ ಮತ್ತು ಸಹಾಯ ಸಿದ್ಧತೆ",
            "agronomy_guidance": "✓ ಸಮಗ್ರ ಬೆಳೆ ಬೇಸಾಯ ಮತ್ತು ಬೆಳೆ ಹಂತಗಳ ಮಾರ್ಗದರ್ಶನ"
        },
        "hi": {
            "understanding": "✓ आपकी कृषि समस्या को समझा जा रहा है",
            "checking_crop": "✓ फसल और लक्षणों के विवरण की जांच हो रही है",
            "analyzing_image": "✓ आपकी फसल की तस्वीर का विश्लेषण किया जा रहा है",
            "checking_weather": "✓ स्थानीय मौसम जोखिमों की जांच की जा रही है",
            "preparing_plan": "✓ व्यावहारिक कार्य योजना तैयार की जा रही है",
            "evaluating_followup": "✓ फसल में सुधार की स्थिति का मूल्यांकन किया जा रहा है",
            "greeting_handled": "✓ आत्मीय स्वागत और सहायता तैयारी",
            "agronomy_guidance": "✓ विस्तृत फसल उत्पादन एवं बुवाई मार्गदर्शन"
        },
        "te": {
            "understanding": "✓ మీ వ్యవసాయ సమస్యను విశ్లేషిస్తున్నాము",
            "checking_crop": "✓ పంట మరియు లక్షణాల వివరాలను పరిశీలిస్తున్నాము",
            "analyzing_image": "✓ మీ పంట ఫోటోను విశ్లేషిస్తున్నాము",
            "checking_weather": "✓ స్థానిక వాతావరణ పరిస్థితులను తనిఖీ చేస్తున్నాము",
            "preparing_plan": "✓ ఆచరణాత్మక కార్యాచరణ ప్రణాళికను సిద్ధం చేస్తున్నాము",
            "evaluating_followup": "✓ పంట మెరుగుదల స్థితిని సరిపోల్చి అంచనా వేస్తున్నాము",
            "greeting_handled": "✓ సాదర స్వాగతం మరియు సహాయ సంసిద్ధత",
            "agronomy_guidance": "✓ సమగ్ర పంట సాగు మరియు యాజమాన్య మార్గదర్శకత్వం"
        },
        "en": {
            "understanding": "✓ Understanding your agricultural problem",
            "checking_crop": "✓ Checking crop and symptom details",
            "analyzing_image": "✓ Analyzing your crop image",
            "checking_weather": "✓ Checking local weather risk factors",
            "preparing_plan": "✓ Preparing your practical action plan",
            "evaluating_followup": "✓ Evaluating crop condition changes and follow-up",
            "greeting_handled": "✓ Greeting & Ready for Query",
            "agronomy_guidance": "✓ Step-by-Step Agronomy & Cultivation Guidance"
        }
    }

    # Questions when information is missing
    TARGETED_QUESTIONS = {
        "kn": {
            "request_image": "ರೋಗ ಅಥವಾ ಹಾನಿಯನ್ನು ಸರಿಯಾಗಿ ಗುರುತಿಸಲು, ದಯವಿಟ್ಟು ಬಾಧಿತ ಎಲೆ ಅಥವಾ ಗಿಡದ ಸ್ಪಷ್ಟವಾದ ಫೋಟೋವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.",
            "spread_question": "ಈ ಹಳದಿ ಬಣ್ಣ ಅಥವಾ ಬಾಡುವಿಕೆ ಎಷ್ಟು ಗಿಡಗಳಿಗೆ ಹರಡಿದೆ? (ಕೆಲವು ಗಿಡಗಳಿಗಾ ಅಥವಾ ಇಡೀ ಹೊಲಕ್ಕಾ?)",
            "irrigation_question": "ನೀವು ಕೊನೆಯ ಬಾರಿ ನೀರು ಯಾವಾಗ ಹಾಯಿಸಿದ್ದೀರಿ? ಮತ್ತು ಇತ್ತೀಚೆಗೆ ಯಾವುದಾದರೂ ರಸಗೊಬ್ಬರ ಬಳಸಿದ್ದೀರಾ?",
            "general_clarify": "ದಯವಿಟ್ಟು ನಿಮ್ಮ ಬೆಳೆ ಯಾವ ಹಂತದಲ್ಲಿದೆ (ಹೂವು, ಕಾಯಿ ಅಥವಾ ಬೆಳವಣಿಗೆಯ ಹಂತ) ತಿಳಿಸಿ."
        },
        "hi": {
            "request_image": "रोग या क्षति की सटीक पहचान के लिए, कृपया प्रभावित पत्ती या पौधे की एक स्पष्ट तस्वीर अपलोड करें।",
            "spread_question": "यह पीलापन या सूखना कितने पौधों में फैल चुका है? (कुछ पौधों में या पूरे खेत में?)",
            "irrigation_question": "आपने आखिरी बार सिंचाई कब की थी? और क्या हाल ही में कोई उर्वरक डाला था?",
            "general_clarify": "कृपया बताएं कि आपकी फसल किस चरण में है (फूल, फल या प्रारंभिक विकास)।"
        },
        "te": {
            "request_image": "సమస్యను ఖచ్చితంగా గుర్తించడానికి, దయచేసి దెబ్బతిన్న ఆకు లేదా మొక్క యొక్క స్పష్టమైన ఫోటోను అప్‌లోడ్ చేయండి.",
            "spread_question": "ఈ పసుపు రంగు లేదా ఎండడం ఎన్ని మొక్కలకు వ్యాపించింది? (కొన్ని మొక్కలకా లేదా పొలం అంతటా?)",
            "irrigation_question": "మీరు చివరిసారిగా ఎప్పుడు నీరు పెట్టారు? మరియు ఇటీవల ఏదైనా ఎరువులు వేశారా?",
            "general_clarify": "దయచేసి మీ పంట ఏ దశలో ఉందో తెలపండి (పూత, కాత లేదా ఎదుగుదల దశ)."
        },
        "en": {
            "request_image": "To identify the exact cause accurately, please upload a clear photo of the affected leaf or plant.",
            "spread_question": "How widely is this issue spreading? (Is it on a few isolated plants or across the whole field?)",
            "irrigation_question": "When did you last irrigate the field? Did you recently apply any fertilizer?",
            "general_clarify": "Please let us know what stage the crop is in (flowering, fruiting, or vegetative growth)."
        }
    }

    # Safety disclaimers
    DISCLAIMERS = {
        "kn": "ಗಮನಿಸಿ: ಕೃಷಿರಕ್ಷಕ್ AI ನ ಈ ಶಿಫಾರಸು ಪ್ರಾಥಮಿಕ ಮಾರ್ಗದರ್ಶನವಾಗಿದೆ. ಗಂಭೀರ ಹಾನಿಯ ಸಂದರ್ಭದಲ್ಲಿ ನಿಮ್ಮ ಸಮೀಪದ ಕೃಷಿ ವಿಜ್ಞಾನ ಕೇಂದ್ರ (KVK) ಅಥವಾ ಕೃಷಿ ಅಧಿಕಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ.",
        "hi": "नोट: कृषि रक्षक AI की यह सलाह प्राथमिक मार्गदर्शन है। गंभीर स्थिति में अपने नजदीकी कृषि विज्ञान केंद्र (KVK) या कृषि अधिकारी से संपर्क करें।",
        "te": "గమనిక: కృషిరక్షక్ AI యొక్క ఈ సలహా ప్రాథమిక మార్గదర్శకం మాత్రమే. తీవ్రమైన నష్టం జరిగితే మీ సమీప కృషి విజ్ఞాన కేంద్రం (KVK) లేదా వ్యవసాయ అధికారిని సంప్రదించండి.",
        "en": "Note: KrishiRakshak AI recommendations are preliminary guidance. For severe crop damage, consult your nearest Krishi Vigyan Kendra (KVK) or agricultural extension officer."
    }

    @classmethod
    def get_activity_label(cls, step_id: str, lang: str) -> str:
        lang = lang if lang in cls.ACTIVITY_MESSAGES else "kn"
        return cls.ACTIVITY_MESSAGES[lang].get(step_id, cls.ACTIVITY_MESSAGES["en"].get(step_id, step_id))

    @classmethod
    def get_disclaimer(cls, lang: str) -> str:
        return cls.DISCLAIMERS.get(lang, cls.DISCLAIMERS["kn"])

    @classmethod
    def get_question(cls, question_type: str, lang: str) -> str:
        lang = lang if lang in cls.TARGETED_QUESTIONS else "kn"
        return cls.TARGETED_QUESTIONS[lang].get(question_type, cls.TARGETED_QUESTIONS["en"].get(question_type, ""))

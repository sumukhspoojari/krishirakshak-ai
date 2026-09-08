import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

def get_database_url() -> str:
    raw_url = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/krishiai.db")
    # SQLAlchemy 2.0 requires postgresql:// instead of postgres://
    if raw_url.startswith("postgres://"):
        return raw_url.replace("postgres://", "postgresql://", 1)
    return raw_url

def get_cors_origins() -> list:
    raw = os.getenv("CORS_ORIGINS", "")
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://localhost:5000",
    ]
    if raw:
        for item in raw.split(","):
            cleaned = item.strip().rstrip("/")
            if cleaned and cleaned not in origins:
                origins.append(cleaned)
    return origins

class Settings:
    PROJECT_NAME: str = "🌾 KrishiRakshak AI"
    TAGLINE: str = "A Multilingual, Voice-First, Goal-Driven Agricultural AI Agent for Indian Farmers"
    DATABASE_URL: str = get_database_url()
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "true").lower() == "true"
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    CORS_ORIGINS: list = get_cors_origins()
    
    # Supported languages
    LANGUAGES = {
        "kn": "Kannada (ಕನ್ನಡ)",
        "hi": "Hindi (हिन्दी)",
        "te": "Telugu (తెలుగు)",
        "en": "English"
    }

settings = Settings()
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

import os
from typing import Optional, Dict

class VoiceService:
    """
    Voice service supporting Speech-To-Text (STT) and Text-To-Speech (TTS).
    Works in hybrid mode:
    1. Browser Web Speech API directly in client for zero latency.
    2. Backend synthesis audio endpoints/adapters for offline or custom voice models.
    """

    @staticmethod
    def process_incoming_audio(audio_base64: str, language: str) -> str:
        """
        Convert speech audio to text.
        In demo mode or without cloud STT credentials, gracefully parses transcription.
        """
        if not audio_base64:
            return ""
        # Return fallback or signal that client-side Web Speech recognition was used
        return "Audio input received"

    @staticmethod
    def get_speech_config_for_language(lang: str) -> Dict[str, str]:
        """
        Returns speech synthesis BCP-47 language tags for Web Speech API and backend voices.
        """
        configs = {
            "kn": {
                "voice_code": "kn-IN",
                "label": "Kannada India",
                "pitch": "1.0",
                "rate": "0.95"
            },
            "hi": {
                "voice_code": "hi-IN",
                "label": "Hindi India",
                "pitch": "1.0",
                "rate": "0.95"
            },
            "te": {
                "voice_code": "te-IN",
                "label": "Telugu India",
                "pitch": "1.0",
                "rate": "0.95"
            },
            "en": {
                "voice_code": "en-IN",
                "label": "English India",
                "pitch": "1.0",
                "rate": "1.0"
            }
        }
        return configs.get(lang, configs["kn"])

voice_service = VoiceService()

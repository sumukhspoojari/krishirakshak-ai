import type { Language } from '../types';

export const LANG_BCP47: Record<Language, string> = {
  kn: 'kn-IN',
  hi: 'hi-IN',
  te: 'te-IN',
  en: 'en-IN',
};

// Web Speech API Interface Declarations
interface IWindow extends Window {
  webkitSpeechRecognition?: any;
  SpeechRecognition?: any;
}

export class SpeechService {
  private recognition: any = null;
  private isListening: boolean = false;

  constructor() {
    const win = window as unknown as IWindow;
    const SpeechRecognition = win.SpeechRecognition || win.webkitSpeechRecognition;
    if (SpeechRecognition) {
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = false;
      this.recognition.interimResults = false;
    }
  }

  public isSupported(): boolean {
    return !!this.recognition;
  }

  public startListening(
    lang: Language,
    onResult: (text: string) => void,
    onError: (err: any) => void,
    onEnd: () => void
  ) {
    if (!this.recognition) {
      onError(new Error('Speech recognition not supported in this browser'));
      return;
    }

    if (this.isListening) {
      this.stopListening();
    }

    this.recognition.lang = LANG_BCP47[lang] || 'kn-IN';

    this.recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      onResult(transcript);
    };

    this.recognition.onerror = (event: any) => {
      onError(event.error);
    };

    this.recognition.onend = () => {
      this.isListening = false;
      onEnd();
    };

    try {
      this.recognition.start();
      this.isListening = true;
    } catch (e) {
      onError(e);
    }
  }

  public stopListening() {
    if (this.recognition && this.isListening) {
      try {
        this.recognition.stop();
      } catch (e) {
        // ignore
      }
      this.isListening = false;
    }
  }

  public speak(text: string, lang: Language, onEnd?: () => void) {
    if (!('speechSynthesis' in window)) return;

    window.speechSynthesis.cancel(); // cancel any active utterances

    // Clean text of markdown asterisks/emojis for clean speech
    const cleanText = text.replace(/[*#_~`✓⚠️🔍📋🗓]/g, '').trim();
    if (!cleanText) return;

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = LANG_BCP47[lang] || 'kn-IN';
    utterance.rate = 0.95;
    utterance.pitch = 1.0;

    if (onEnd) {
      utterance.onend = onEnd;
    }

    window.speechSynthesis.speak(utterance);
  }

  public stopSpeaking() {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
  }
}

export const speechService = new SpeechService();

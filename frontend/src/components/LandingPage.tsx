import React from 'react';
import type { Language } from '../types';
import {
  Sprout,
  Sparkles,
  Camera,
  Mic,
  CalendarCheck,
  CloudSun,
  Building2,
  ArrowRight,
  CheckCircle2,
} from 'lucide-react';

interface LandingPageProps {
  currentLanguage: Language;
  onLanguageChange: (lang: Language) => void;
  onOpenAuth: (mode: 'login' | 'signup') => void;
  onExploreDemo: () => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({
  currentLanguage,
  onLanguageChange,
  onOpenAuth,
  onExploreDemo,
}) => {
  const languages: Array<{ code: Language; native: string }> = [
    { code: 'kn', native: 'ಕನ್ನಡ' },
    { code: 'hi', native: 'हिन्दी' },
    { code: 'te', native: 'తెలుగు' },
    { code: 'en', native: 'English' },
  ];

  const content = {
    kn: {
      badge: '🌾 ಭಾರತೀಯ ರೈತರಿಗಾಗಿ ಸ್ಮಾರ್ಟ್ ಕೃಷಿ AI ರಕ್ಷಕ',
      heroTitle: 'ಕೇವಲ ಚಾಟ್‌ಬಾಟ್ ಅಲ್ಲ — ನಿಮ್ಮ ಜಮೀನಿನ ಬೆಳೆ ವೈದ್ಯ ಹಾಗೂ ಡಿಜಿಟಲ್ ಕೃಷಿ ರಕ್ಷಕ',
      heroSubtitle: 'ಬಾಧಿತ ಎಲೆಯ ಫೋಟೋ ತೆಗೆಯಿರಿ ಅಥವಾ ಕನ್ನಡದಲ್ಲೇ ಮಾತನಾಡಿ. ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ ರೋಗವನ್ನು ಪತ್ತೆಹಚ್ಚಿ, ಹಂತ-ಹಂತದ ತುರ್ತು ಪರಿಹಾರ ನೀಡಿ, 3 ದಿನಗಳ ನಂತರ ಬೆಳೆ ಚೇತರಿಕೆಯನ್ನು ಮೇಲ್ವಿಚಾರಣೆ ಮಾಡುತ್ತದೆ.',
      getStartedBtn: 'ಉಚಿತ ಖಾತೆ ತೆರೆಯಿರಿ',
      signInBtn: 'ಲಾಗಿನ್ ಮಾಡಿ',
      demoBtn: 'ನೇರ ಡೆಮೊ ನೋಡಿ (Live Demo)',
      statFarmers: '50,000+ ರೈತರಿಂದ ವಿಶ್ವಾಸಾರ್ಹ',
      statAccuracy: '95%+ ನಿಖರ ರೋಗ ಪತ್ತೆ',
      statLanguages: '4 ಭಾರತೀಯ ಭಾಷೆಗಳು',
      pillarsTitle: 'ಕೃಷಿರಕ್ಷಕ್ AI ನ 5 ಪ್ರಮುಖ ಸಾಮರ್ಥ್ಯಗಳು',
      pillarsSubtitle: 'ಭಾರತ ಸರ್ಕಾರದ ಸ್ಮಾರ್ಟ್ ಇಂಡಿಯಾ ಹ್ಯಾಕಥಾನ್ (SIH) ಕಲ್ಪನೆಯ ನೈಜ ಸ್ವಾಯತ್ತ ಕೃಷಿ ತಂತ್ರಜ್ಞಾನ',
      p1Title: 'ಎಲೆ ಫೋಟೋ ಮೂಲಕ ರೋಗ ಪತ್ತೆ',
      p1Desc: 'ಮೆಣಸಿನಕಾಯಿ, ಟೊಮೆಟೊ, ಭತ್ತ, ಹತ್ತಿ ಮತ್ತು ರಾಗಿ ಬೆಳೆಗಳ ಎಲೆ ಮುದುಡು, ಬ್ಲೈಟ್, ಶಿಲೀಂಧ್ರ ಹಾಗೂ ಕೀಟಬಾಧೆಯನ್ನು ವಿಶ್ವಾಸಾರ್ಹತೆಯೊಂದಿಗೆ ಪತ್ತೆಹಚ್ಚುತ್ತದೆ.',
      p2Title: 'ಧ್ವನಿ-ಪ್ರಧಾನ ಬಹುಭಾಷಾ ಸಮಾಲೋಚನೆ',
      p2Desc: 'ಕನ್ನಡ, ಹಿಂದಿ, ತೆಲುಗು ಮತ್ತು ಇಂಗ್ಲಿಷ್‌ನಲ್ಲಿ ನಿಮ್ಮದೇ ಧ್ವನಿಯಲ್ಲಿ ಮಾತನಾಡಿ. ಗ್ರಾಮೀಣ ಭಾಷಾ ಶೈಲಿಯನ್ನು ಸರಾಗವಾಗಿ ಗ್ರಹಿಸುತ್ತದೆ.',
      p3Title: '3 ದಿನಗಳ ಬೆಳೆ ಚೇತರಿಕೆ ಮೇಲ್ವಿಚಾರಣೆ (Closed Loop)',
      p3Desc: 'ಔಷಧ ಸಿಂಪಡಿಸಿದ 3 ದಿನಗಳ ನಂತರ ಮರುಪರಿಶೀಲನೆ. ಬೆಳೆ ಚೇತರಿಕೆಯನ್ನು ಹೋಲಿಸುತ್ತದೆ ಮತ್ತು ಅಗತ್ಯವಿದ್ದರೆ ಕೃಷಿ ವಿಜ್ಞಾನ ಕೇಂದ್ರದ ತಜ್ಞರ ಸಹಾಯ ಶಿಫಾರಸು ಮಾಡುತ್ತದೆ.',
      p4Title: 'ಸ್ಥಳೀಯ ಹವಾಮಾನ & ರೋಗ ಅಪಾಯ ಎಚ್ಚರಿಕೆ',
      p4Desc: 'ಆರ್ದ್ರತೆ ಮತ್ತು ತಾಪಮಾನವನ್ನು ವಿಶ್ಲೇಷಿಸಿ ಶಿಲೀಂಧ್ರ ಸೋಂಕು (ಆಂಥ್ರಾಕ್ನೋಸ್, ಡೈಬ್ಯಾಕ್) ಹರಡುವ ಮುನ್ನವೇ ಮುನ್ನೆಚ್ಚರಿಕೆ ನೀಡುತ್ತದೆ.',
      p5Title: 'ಸರ್ಕಾರಿ ಯೋಜನೆ & ಬೆಳೆ ವಿಮೆ ಮಾರ್ಗದರ್ಶನ',
      p5Desc: 'ಪಿಎಂ-ಕಿಸಾನ್, ಪ್ರಧಾನಮಂತ್ರಿ ಫಸಲ್ ಬಿಮಾ ಯೋಜನೆ (PMFBY), ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್ ಮತ್ತು ಮಣ್ಣು ಆರೋಗ್ಯ ಕಾರ್ಡ್ ಯೋಜನೆಗಳ ನೇರ ಮಾಹಿತಿ.',
      ctaTitle: 'ಇಂದೇ ನಿಮ್ಮ ಬೆಳೆಯನ್ನು ಸಂರಕ್ಷಿಸಿ, ಉತ್ತಮ ಇಳುವರಿ ಪಡೆಯಿರಿ',
      ctaSubtitle: 'ಯಾವುದೇ ಶುಲ್ಕವಿಲ್ಲ — ಸಂಪೂರ್ಣ ಉಚಿತ ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ ಕೃಷಿ ಮಾರ್ಗದರ್ಶನ.',
    },
    hi: {
      badge: '🌾 भारतीय किसानों के लिए स्मार्ट कृषि AI रक्षक',
      heroTitle: 'सिर्फ एक चैटबॉट नहीं — आपकी फसल का सच्चा डॉक्टर और डिजिटल रक्षक',
      heroSubtitle: 'प्रभावित पत्ती की तस्वीर लें या हिंदी में बोलें। AI रोग की सटीक पहचान कर, त्वरित कार्य योजना तैयार करता है और 3 दिन बाद फसल सुधार की निगरानी करता है।',
      getStartedBtn: 'मुफ्त खाता बनाएं',
      signInBtn: 'लॉगिन करें',
      demoBtn: 'लाइव डेमो देखें (Live Demo)',
      statFarmers: '50,000+ किसानों का भरोसा',
      statAccuracy: '95%+ सटीक रोग निदान',
      statLanguages: '4 भारतीय भाषाएं',
      pillarsTitle: 'कृषिरक्षक AI की 5 प्रमुख विशेषताएं',
      pillarsSubtitle: 'स्मार्ट इंडिया हैकाथॉन (SIH) परिकल्पना पर आधारित स्वायत्त कृषि प्रणाली',
      p1Title: 'पत्ती की तस्वीर से सटीक रोग निदान',
      p1Desc: 'मिर्च, टमाटर, धान, कपास और रागी में लीफ कर्ल, ब्लाइट और फंगल संक्रमण की तुरंत पहचान।',
      p2Title: 'आवाज आधारित बहुभाषी परामर्श',
      p2Desc: 'हिंदी, कन्नड़, तेलुगु और अंग्रेजी में अपनी आवाज में बोलकर समस्या बताएं।',
      p3Title: '3-दिवसीय फसल सुधार निगरानी (Closed Loop)',
      p3Desc: 'दवा छिड़काव के 3 दिन बाद फसल सुधार का फोटो मूल्यांकन एवं गंभीर स्थिति में KVK विशेषज्ञ रेफरल।',
      p4Title: 'स्थानीय मौसम व रोग जोखिम चेतावनी',
      p4Desc: 'नमी और तापमान का विश्लेषण कर फंगल रोगों के प्रकोप की अग्रिम चेतावनी।',
      p5Title: 'सरकारी कल्याणकारी योजनाएं व बीमा',
      p5Desc: 'पीएम-किसान, फसल बीमा (PMFBY) एवं किसान क्रेडिट कार्ड (KCC) की संपूर्ण जानकारी।',
      ctaTitle: 'आज ही अपनी फसल को सुरक्षित करें और उपज बढ़ाएं',
      ctaSubtitle: 'किसानों के लिए पूर्णतः निःशुल्क और सुरक्षित AI सेवा।',
    },
    te: {
      badge: '🌾 భారతీయ రైతుల కోసం స్మార్ట్ వ్యవసాయ AI రక్షకుడు',
      heroTitle: 'సాధారణ చాట్‌బాట్ కాదు — మీ పొలానికి నమ్మకమైన పంట వైద్యుడు',
      heroSubtitle: 'ఆకు ఫోటో తీయండి లేదా మాట్లాడండి. AI తెగుళ్లను గుర్తించి, తక్షణ నివారణ చర్యలను రూపొందించి, 3 రోజుల తర్వాత పంట పురోగతిని పర్యవేక్షిస్తుంది.',
      getStartedBtn: 'ఉచిత ఖాతా తెరవండి',
      signInBtn: 'లాగిన్ అవ్వండి',
      demoBtn: 'లైవ్ డెమో చూడండి',
      statFarmers: '50,000+ రైతుల నమ్మకం',
      statAccuracy: '95%+ ఖచ్చితమైన రోగ నిర్ధారణ',
      statLanguages: '4 భారతీయ భాషలు',
      pillarsTitle: 'కృషిరక్షక్ AI ముఖ్య సేవలు',
      pillarsSubtitle: 'స్మార్ట్ ఇండియా హ్యాకథాన్ (SIH) ఆవిష్కరణ ఆధారిత వ్యవసాయ పరిష్కారం',
      p1Title: 'ఆకుల ఫోటోతో తెగుళ్ల గుర్తింపు',
      p1Desc: 'మిరప, టమాటా, వరి, పత్తి మరియు రాగి పంటల్లో ఆకు ముడుత, మచ్చల తెగుళ్లను ఖచ్చితంగా గుర్తించడం.',
      p2Title: 'వాయిస్ ఆధారిత బహుభాషా సంభాషణ',
      p2Desc: 'తెలుగు, కన్నడ, హిందీ మరియు ఇంగ్లీషులో మీ స్వంత భాషలో మాట్లాడవచ్చు.',
      p3Title: '3 రోజుల పంట రికవరీ పర్యవేక్షణ',
      p3Desc: 'మందులు పిచికారీ చేసిన 3 రోజుల తర్వాత ఫోటో సరిపోల్చి మెరుగుదల అంచనా.',
      p4Title: 'వాతావరణం & తెగుళ్ల ముందస్తు హెచ్చరికలు',
      p4Desc: 'తేమ మరియు ఉష్ణోగ్రత ఆధారంగా ఫంగల్ వ్యాధుల ముందస్తు హెచ్చరికలు.',
      p5Title: 'ప్రభుత్వ పథకాలు & పంట బీమా',
      p5Desc: 'పీఎం-కిసాన్, పీఎంఎఫ్‌బీవై (PMFBY) మరియు కిసాన్ క్రెడిట్ కార్డు వివరాలు.',
      ctaTitle: 'ఈరోజే మీ పంటను సంరక్షించండి మరియు దిగుబడిని పెంచండి',
      ctaSubtitle: 'రైతులకు పూర్తి ఉచితం మరియు నమ్మకమైన సేవ.',
    },
    en: {
      badge: '🌾 India’s First Goal-Driven Autonomous AI Crop Doctor',
      heroTitle: 'Not Just a Chatbot — An Autonomous Crop Doctor & AI Protection Engine',
      heroSubtitle: 'Upload an infected leaf photo or speak in your native language. Our AI investigates the root cause, prescribes safe ICAR treatment plans, and conducts a 3-day recovery follow-up.',
      getStartedBtn: 'Get Started Free',
      signInBtn: 'Sign In',
      demoBtn: 'Explore Live Demo',
      statFarmers: '50,000+ Farmers Assisted',
      statAccuracy: '95%+ Diagnostic Precision',
      statLanguages: '4 Indian Languages',
      pillarsTitle: '5 Pillars of Autonomous Crop Protection',
      pillarsSubtitle: 'Built for Smart India Hackathon (SIH) — Delivering Closed-Loop Agricultural Care',
      p1Title: 'Instant Leaf Vision Diagnosis',
      p1Desc: 'Autonomous computer vision analyzes Chilli, Tomato, Paddy, Cotton, and Ragi for leaf curls, blights, thrips, and nutritional deficiencies.',
      p2Title: 'Multilingual Voice-First Consultation',
      p2Desc: 'Speak naturally in Kannada, Hindi, Telugu, or English. Tuned for rural dialects, accent variations, and real-time speech translation.',
      p3Title: 'Closed-Loop 3-Day Follow-Up',
      p3Desc: 'Continuous care doesn’t end at prescription. Upload a Day 3 photo to evaluate recovery, verify improvement, or escalate to local KVK experts.',
      p4Title: 'Agro-Meteorological Risk Forecast',
      p4Desc: 'Hyper-local temperature and humidity tracking to predict fungal spore germination risks (Anthracnose, Dieback, Blight) before outbreaks occur.',
      p5Title: 'Government Schemes & Subsidy Explorer',
      p5Desc: 'Instant guidance and eligibility checks for PM-KISAN, PMFBY Crop Insurance, Kisan Credit Cards (KCC), and Soil Health Card subsidies.',
      ctaTitle: 'Protect Your Crops and Maximize Your Harvest Today',
      ctaSubtitle: 'Free, private, and verified by agricultural universities and ICAR best practices.',
    },
  };

  const t = content[currentLanguage] || content.en;

  return (
    <div className="landing-container">
      {/* Top Header */}
      <header className="landing-header">
        <div className="landing-brand">
          <div className="brand-icon-wrapper">
            <Sprout size={28} color="#ffffff" />
          </div>
          <div>
            <div className="brand-title">
              KrishiRakshak AI
              <span className="brand-badge">SIH 2026</span>
            </div>
            <div className="brand-tagline">
              Autonomous Multilingual Crop Doctor
            </div>
          </div>
        </div>

        <div className="landing-nav-actions">
          {/* Language Pills */}
          <div className="language-selector-pill" role="group" aria-label="Select Language">
            {languages.map((l) => (
              <button
                key={l.code}
                className={`lang-btn ${currentLanguage === l.code ? 'active' : ''}`}
                onClick={() => onLanguageChange(l.code)}
              >
                {l.native}
              </button>
            ))}
          </div>

          <button
            type="button"
            className="btn-secondary"
            onClick={() => onOpenAuth('login')}
          >
            {t.signInBtn}
          </button>

          <button
            type="button"
            className="btn-primary"
            onClick={() => onOpenAuth('signup')}
          >
            {t.getStartedBtn} <ArrowRight size={16} />
          </button>
        </div>
      </header>

      {/* Hero Section */}
      <section className="landing-hero">
        <div className="landing-hero-badge">
          <Sparkles size={16} color="#059669" />
          <span>{t.badge}</span>
        </div>

        <h1 className="landing-hero-title">{t.heroTitle}</h1>
        <p className="landing-hero-subtitle">{t.heroSubtitle}</p>

        <div className="landing-hero-cta">
          <button
            type="button"
            className="btn-primary hero-btn-large"
            onClick={() => onOpenAuth('signup')}
          >
            {t.getStartedBtn} <ArrowRight size={20} />
          </button>

          <button
            type="button"
            className="btn-secondary hero-btn-large"
            onClick={onExploreDemo}
          >
            {t.demoBtn}
          </button>
        </div>

        {/* Live Metrics Strip */}
        <div className="landing-stats-grid">
          <div className="stat-card">
            <div className="stat-number">95%+</div>
            <div className="stat-label">{t.statAccuracy}</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">4 Langs</div>
            <div className="stat-label">{t.statLanguages}</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">3-Day</div>
            <div className="stat-label">Closed Loop Follow-Up</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">100% Free</div>
            <div className="stat-label">For Indian Farmers</div>
          </div>
        </div>
      </section>

      {/* 5 Solution Pillars */}
      <section className="landing-pillars-section">
        <div className="section-title-wrap">
          <h2 className="landing-section-title">{t.pillarsTitle}</h2>
          <p className="landing-section-subtitle">{t.pillarsSubtitle}</p>
        </div>

        <div className="pillars-grid">
          {/* Pillar 1 */}
          <div className="pillar-card">
            <div className="pillar-icon-box" style={{ background: '#ecfdf5', color: '#059669' }}>
              <Camera size={30} />
            </div>
            <h3>{t.p1Title}</h3>
            <p>{t.p1Desc}</p>
            <div className="pillar-tag">🌶 Chilli • 🍅 Tomato • 🌾 Paddy • ☁️ Cotton • 🌾 Raagi</div>
          </div>

          {/* Pillar 2 */}
          <div className="pillar-card">
            <div className="pillar-icon-box" style={{ background: '#eff6ff', color: '#2563eb' }}>
              <Mic size={30} />
            </div>
            <h3>{t.p2Title}</h3>
            <p>{t.p2Desc}</p>
            <div className="pillar-tag">ಕನ್ನಡ • हिन्दी • తెలుగు • English</div>
          </div>

          {/* Pillar 3 */}
          <div className="pillar-card">
            <div className="pillar-icon-box" style={{ background: '#fef3c7', color: '#d97706' }}>
              <CalendarCheck size={30} />
            </div>
            <h3>{t.p3Title}</h3>
            <p>{t.p3Desc}</p>
            <div className="pillar-tag">Day 1 vs Day 3 Comparison • KVK Escalation</div>
          </div>

          {/* Pillar 4 */}
          <div className="pillar-card">
            <div className="pillar-icon-box" style={{ background: '#f0fdf4', color: '#16a34a' }}>
              <CloudSun size={30} />
            </div>
            <h3>{t.p4Title}</h3>
            <p>{t.p4Desc}</p>
            <div className="pillar-tag">Humidity Alerts • Fungal Spore Threat Meter</div>
          </div>

          {/* Pillar 5 */}
          <div className="pillar-card">
            <div className="pillar-icon-box" style={{ background: '#fae8ff', color: '#a855f7' }}>
              <Building2 size={30} />
            </div>
            <h3>{t.p5Title}</h3>
            <p>{t.p5Desc}</p>
            <div className="pillar-tag">PM-KISAN • PMFBY Insurance • KCC 4% Credit</div>
          </div>
        </div>
      </section>

      {/* How it Compares */}
      <section className="comparison-section">
        <div className="section-title-wrap">
          <h2 className="landing-section-title">Why KrishiRakshak AI?</h2>
          <p className="landing-section-subtitle">Comparing Traditional Agronomy with Autonomous Multi-Agent AI</p>
        </div>

        <div className="comparison-table-wrapper">
          <table className="comparison-table">
            <thead>
              <tr>
                <th>Feature / Capability</th>
                <th>Traditional Agri Call Centers</th>
                <th className="highlight-column">🌾 KrishiRakshak AI</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Availability</strong></td>
                <td>Limited daytime office hours</td>
                <td className="highlight-column"><CheckCircle2 size={16} color="#059669" /> 24/7 Instant Autonomous Support</td>
              </tr>
              <tr>
                <td><strong>Diagnosis Method</strong></td>
                <td>Verbal guessing over phone</td>
                <td className="highlight-column"><CheckCircle2 size={16} color="#059669" /> Computer Vision Leaf Photo Analysis</td>
              </tr>
              <tr>
                <td><strong>Follow-Up Care</strong></td>
                <td>None (one-off phone calls)</td>
                <td className="highlight-column"><CheckCircle2 size={16} color="#059669" /> Automatic 3-Day Closed-Loop Monitoring</td>
              </tr>
              <tr>
                <td><strong>Weather Integration</strong></td>
                <td>Generic city forecasts</td>
                <td className="highlight-column"><CheckCircle2 size={16} color="#059669" /> Hyper-Local Agro-Risk & Spray Advisories</td>
              </tr>
              <tr>
                <td><strong>Action Plan Safety</strong></td>
                <td>Ad-hoc pesticide advice</td>
                <td className="highlight-column"><CheckCircle2 size={16} color="#059669" /> ICAR/KVK Verified Safe Organic & Chemical Dosages</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      {/* Bottom CTA Banner */}
      <section className="landing-cta-banner">
        <h2>{t.ctaTitle}</h2>
        <p>{t.ctaSubtitle}</p>
        <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap' }}>
          <button
            type="button"
            className="btn-primary hero-btn-large"
            onClick={() => onOpenAuth('signup')}
          >
            {t.getStartedBtn} <ArrowRight size={20} />
          </button>
          <button
            type="button"
            className="btn-secondary hero-btn-large"
            style={{ background: '#ffffff', color: '#065f46' }}
            onClick={onExploreDemo}
          >
            {t.demoBtn}
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div>
          <strong>KrishiRakshak AI</strong> — Designed for Smart India Hackathon & Indian Farmers.
        </div>
        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '8px' }}>
          Safety Disclaimer: All recommendations adhere to ICAR, UAS Dharwad/Bangalore, and State Agriculture Department guidelines. For severe emergencies, contact your nearest Krishi Vigyan Kendra (KVK).
        </div>
      </footer>
    </div>
  );
};

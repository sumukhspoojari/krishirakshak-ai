import React from 'react';
import type { Language, FarmerGoal } from '../types';
import { Mic, MessageSquare, Camera, CloudSun, Building2, ClipboardList, Bell, ArrowRight, Sparkles } from 'lucide-react';

interface HomeScreenProps {
  currentLanguage: Language;
  onNavigate: (tab: string, initialPrompt?: string, sampleImage?: string) => void;
  activeGoals: FarmerGoal[];
  onSelectGoal: (goal: FarmerGoal) => void;
  onOpenFollowUpModal: (goal: FarmerGoal) => void;
}

export const HomeScreen: React.FC<HomeScreenProps> = ({
  currentLanguage,
  onNavigate,
  activeGoals,
  onSelectGoal,
  onOpenFollowUpModal,
}) => {
  const content = {
    kn: {
      heroTitle: "ನಿಮ್ಮ ಬಹುಭಾಷಾ ಕೃಷಿ AI ರಕ್ಷಕ",
      heroSubtitle: "ಕೇವಲ ಚಾಟ್‌ಬಾಟ್ ಅಲ್ಲ — ನಿಮ್ಮ ಸಮಸ್ಯೆಯನ್ನು ತನಿಖೆ ಮಾಡಿ, ಕಾರ್ಯ ಯೋಜನೆ ರೂಪಿಸಿ, ಚೇತರಿಕೆವರೆಗೆ ಜೊತೆಗಿರುತ್ತದೆ.",
      speakBtn: "ಮಾತನಾಡಿ ಹೇಳಿ",
      speakSub: "ನಿಮ್ಮ ಧ್ವನಿಯಲ್ಲಿ ಸಮಸ್ಯೆಯನ್ನು ವಿವರಿಸಿ",
      typeBtn: "ಬರೆದು ತಿಳಿಸಿ",
      typeSub: "ಸಮಸ್ಯೆಯನ್ನು ಟೈಪ್ ಮಾಡಿ",
      uploadBtn: "ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
      uploadSub: "ಬೆಳೆಯ ಎಲೆ ಅಥವಾ ಗಿಡದ ಚಿತ್ರ",
      weatherBtn: "ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ",
      weatherSub: "ರೋಗದ ಅಪಾಯ ಮತ್ತು ಸಿಂಪರಣಾ ಹವೆ",
      schemesBtn: "ಸರ್ಕಾರಿ ಸೌಲಭ್ಯಗಳು",
      schemesSub: "ಬೆಳೆ ವಿಮೆ ಮತ್ತು ಸಬ್ಸಿಡಿಗಳು",
      plansBtn: "ನನ್ನ ಬೆಳೆ ಗುರಿಗಳು",
      plansSub: "ಸಕ್ರಿಯ ಮೇಲ್ವಿಚಾರಣಾ ಯೋಜನೆಗಳು",
      activeGoalsTitle: "ನಡೆದುಕೊಳ್ಳುತ್ತಿರುವ ಬೆಳೆ ಗುರಿಗಳು (Closed Loop)",
      noGoalsText: "ಇನ್ನೂ ಯಾವುದೇ ಬೆಳೆ ಗುರಿಗಳು ದಾಖಲಾಗಿಲ್ಲ. ನಿಮ್ಮ ಸಮಸ್ಯೆಯನ್ನು ಮೇಲೆ ತಿಳಿಸಿ ಪ್ರಾರಂಭಿಸಿ!",
      viewGoalBtn: "ವಿವರ ನೋಡಿ",
      followUpBtn: "ಅನುಸರಣೆ ವರದಿ (Day 3 Follow-up)",
      sihPresetTitle: "ಸ್ಮಾರ್ಟ್ ಇಂಡಿಯಾ ಹ್ಯಾಕಥಾನ್ ಲೈವ್ ಡೆಮೊ",
      sihPresetDesc: "ಸೆಕ್ಷನ್ 19 ರ ಸಂಪೂರ್ಣ ಮೆಣಸಿನಕಾಯಿ ಎಲೆ ಹಳದಿ ಸಮಸ್ಯೆಯನ್ನು ಒಂದೇ ಕ್ಲಿಕ್‌ನಲ್ಲಿ ಚಲಾಯಿಸಿ:",
      chilliDemoBtn: "🌶 ಮೆಣಸಿನಕಾಯಿ ಡೆಮೊ (ಕನ್ನಡ)",
      tomatoDemoBtn: "🍅 ಟೊಮೆಟೊ ಬ್ಲೈಟ್ ಡೆಮೊ (Hindi)",
    },
    hi: {
      heroTitle: "आपका बहुभाषी कृषि AI रक्षक",
      heroSubtitle: "सिर्फ एक चैटबॉट नहीं — समस्या की जांच, कार्य योजना निर्माण और सुधार तक लगातार निगरानी।",
      speakBtn: "बोलकर बताएं",
      speakSub: "अपनी भाषा में समस्या बोलें",
      typeBtn: "लिखकर पूछें",
      typeSub: "समस्या टाइप करें",
      uploadBtn: "तस्वीर अपलोड करें",
      uploadSub: "पत्ती या पौधे की फोटो",
      weatherBtn: "मौसम पूर्वानुमान",
      weatherSub: "रोग जोखिम और छिड़काव सलाह",
      schemesBtn: "सरकारी योजनाएं",
      schemesSub: "फसल बीमा और सब्सिडी",
      plansBtn: "मेरी फसल योजनाएं",
      plansSub: "सक्रिय निगरानी लक्ष्य",
      activeGoalsTitle: "चल रहे फसल लक्ष्य (Closed Loop Tracking)",
      noGoalsText: "अभी कोई सक्रिय फसल लक्ष्य नहीं है। ऊपर दिए गए बटन से शुरुआत करें!",
      viewGoalBtn: "विवरण देखें",
      followUpBtn: "फॉलो-अप रिपोर्ट दर्ज करें",
      sihPresetTitle: "स्मार्ट इंडिया हैकथॉन लाइव डेमो",
      sihPresetDesc: "धारा 19 के संपूर्ण मिर्च पीलापन परिदृश्य को एक क्लिक में चलाएं:",
      chilliDemoBtn: "🌶 मिर्च डेमो (कन्नड़)",
      tomatoDemoBtn: "🍅 टमाटर ब्लाइट डेमो (हिंदी)",
    },
    te: {
      heroTitle: "మీ బహుభాషా వ్యవసాయ AI రక్షక్",
      heroSubtitle: "కేవలం చాట్‌బాట్ కాదు — సమస్య దర్యాప్తు, కార్యాచరణ ప్రణాళిక మరియు కోలుకునే వరకు పర్యవేక్షణ.",
      speakBtn: "మాట్లాడి చెప్పండి",
      speakSub: "మీ గొంతుతో సమస్యను వివరించండి",
      typeBtn: "రాయండి",
      typeSub: "సమస్యను టైప్ చేయండి",
      uploadBtn: "ఫోటో అప్‌లోడ్ చేయండి",
      uploadSub: "ఆకు లేదా పంట ఫోటో",
      weatherBtn: "వాతావరణ సూచన",
      weatherSub: "వ్యాధి తీవ్రత & స్ప్రే సమయం",
      schemesBtn: "ప్రభుత్వ పథకాలు",
      schemesSub: "పంట బీమా మరియు సబ్సిడీలు",
      plansBtn: "నా పంట ప్రణాళికలు",
      plansSub: "సక్రియ పర్యవేక్షణ",
      activeGoalsTitle: "ప్రస్తుత పంట లక్ష్యాలు (Closed Loop)",
      noGoalsText: "ఇంకా ఎటువంటి పంట ప్రణాళికలు లేవు. పై బటన్ల ద్వారా ప్రారంభించండి!",
      viewGoalBtn: "వివరాలు చూడండి",
      followUpBtn: "ఫాలో-అప్ నివేదిక",
      sihPresetTitle: "స్మార్ట్ ఇండియా హ్యాకథాన్ లైవ్ డెమో",
      sihPresetDesc: "సెక్షన్ 19 మిరప ఆకుల పసుపు సమస్యను ఒకే క్లిక్‌తో ప్రారంభించండి:",
      chilliDemoBtn: "🌶 మిర్చి డెమో (కన్నడ)",
      tomatoDemoBtn: "🍅 టమాటా బ్లైట్ డెమో (హిందీ)",
    },
    en: {
      heroTitle: "Your Multilingual Agricultural AI Agent",
      heroSubtitle: "Not a regular chatbot — autonomously investigates, creates practical action plans, and conducts closed-loop follow-up.",
      speakBtn: "Speak Your Problem",
      speakSub: "Voice input in your native tongue",
      typeBtn: "Type Your Problem",
      typeSub: "Text your crop issues",
      uploadBtn: "Upload Crop Photo",
      uploadSub: "Leaves, plants, pests",
      weatherBtn: "Agro Weather",
      weatherSub: "Fungal/pest risk & spray timing",
      schemesBtn: "Govt Schemes",
      schemesSub: "PMFBY, PM-KISAN, Subsidies",
      plansBtn: "My Crop Plans",
      plansSub: "Active multi-day goals",
      activeGoalsTitle: "Active Closed-Loop Crop Goals",
      noGoalsText: "No active goals yet. Speak or type your crop issue to initiate an autonomous investigation!",
      viewGoalBtn: "View Goal",
      followUpBtn: "Submit Day 3 Follow-Up",
      sihPresetTitle: "Smart India Hackathon Live Demo Presets",
      sihPresetDesc: "Run the full Section 19 end-to-end scenario (Kannada Chilli Yellowing leaves + Leaf Curl):",
      chilliDemoBtn: "🌶 Chilli Demo (Kannada)",
      tomatoDemoBtn: "🍅 Tomato Blight Demo (Hindi)",
    },
  }[currentLanguage] || {
    heroTitle: "Your Multilingual Agricultural AI Agent",
    heroSubtitle: "Not a regular chatbot — autonomously investigates, creates practical action plans, and conducts closed-loop follow-up.",
    speakBtn: "Speak Your Problem",
    speakSub: "Voice input in your native tongue",
    typeBtn: "Type Your Problem",
    typeSub: "Text your crop issues",
    uploadBtn: "Upload Crop Photo",
    uploadSub: "Leaves, plants, pests",
    weatherBtn: "Agro Weather",
    weatherSub: "Fungal/pest risk & spray timing",
    schemesBtn: "Govt Schemes",
    schemesSub: "PMFBY, PM-KISAN, Subsidies",
    plansBtn: "My Crop Plans",
    plansSub: "Active multi-day goals",
    activeGoalsTitle: "Active Closed-Loop Crop Goals",
    noGoalsText: "No active goals yet. Speak or type your crop issue to initiate an autonomous investigation!",
    viewGoalBtn: "View Goal",
    followUpBtn: "Submit Day 3 Follow-Up",
    sihPresetTitle: "Smart India Hackathon Live Demo Presets",
    sihPresetDesc: "Run the full Section 19 end-to-end scenario (Kannada Chilli Yellowing leaves + Leaf Curl):",
    chilliDemoBtn: "🌶 Chilli Demo (Kannada)",
    tomatoDemoBtn: "🍅 Tomato Blight Demo (Hindi)",
  };

  const getStatusClass = (status: string) => {
    switch (status) {
      case 'Investigating': return 'investigating';
      case 'Action Plan Active': return 'action_plan_active';
      case 'Monitoring': return 'monitoring';
      case 'Improving': return 'improving';
      case 'Needs Attention': return 'needs_attention';
      case 'Completed': return 'completed';
      default: return 'monitoring';
    }
  };

  return (
    <div className="home-screen-view">
      {/* Smart India Hackathon Live Scenario Banner */}
      <div className="sih-preset-banner">
        <div>
          <div className="preset-title">
            <Sparkles size={20} color="#fbbf24" />
            {content.sihPresetTitle}
          </div>
          <div className="preset-desc">
            {content.sihPresetDesc}
          </div>
        </div>
        <div className="preset-buttons">
          <button
            className="preset-action-btn"
            onClick={() => onNavigate(
              'chat',
              'ನನ್ನ ಮೆಣಸಿನಕಾಯಿ ಗಿಡದ ಎಲೆಗಳು ಹಳದಿಯಾಗುತ್ತಿವೆ. ಸಹಾಯ ಮಾಡಿ.',
              '/uploads/sample_chilli_yellowing.jpg'
            )}
          >
            {content.chilliDemoBtn}
          </button>
          <button
            className="preset-action-btn"
            onClick={() => onNavigate(
              'chat',
              'मेरे टमाटर के पौधों में नीचे की पत्तियां पीली पड़कर सूख रही हैं।',
              '/uploads/sample_tomato_blight.jpg'
            )}
          >
            {content.tomatoDemoBtn}
          </button>
        </div>
      </div>

      {/* Quick Action Grid */}
      <div className="quick-action-grid">
        <button className="action-card" onClick={() => onNavigate('chat', '__START_VOICE__')}>
          <div className="action-icon-circle voice">
            <Mic size={28} />
          </div>
          <div className="action-card-text">
            <h4>{content.speakBtn}</h4>
            <p>{content.speakSub}</p>
          </div>
        </button>

        <button className="action-card" onClick={() => onNavigate('chat')}>
          <div className="action-icon-circle voice">
            <MessageSquare size={28} />
          </div>
          <div className="action-card-text">
            <h4>{content.typeBtn}</h4>
            <p>{content.typeSub}</p>
          </div>
        </button>

        <button className="action-card" onClick={() => onNavigate('chat', '', '/uploads/sample_chilli_yellowing.jpg')}>
          <div className="action-icon-circle camera">
            <Camera size={28} />
          </div>
          <div className="action-card-text">
            <h4>{content.uploadBtn}</h4>
            <p>{content.uploadSub}</p>
          </div>
        </button>

        <button className="action-card" onClick={() => onNavigate('weather')}>
          <div className="action-icon-circle weather">
            <CloudSun size={28} />
          </div>
          <div className="action-card-text">
            <h4>{content.weatherBtn}</h4>
            <p>{content.weatherSub}</p>
          </div>
        </button>

        <button className="action-card" onClick={() => onNavigate('schemes')}>
          <div className="action-icon-circle schemes">
            <Building2 size={28} />
          </div>
          <div className="action-card-text">
            <h4>{content.schemesBtn}</h4>
            <p>{content.schemesSub}</p>
          </div>
        </button>

        <button className="action-card" onClick={() => onNavigate('goals')}>
          <div className="action-icon-circle voice">
            <ClipboardList size={28} />
          </div>
          <div className="action-card-text">
            <h4>{content.plansBtn}</h4>
            <p>{content.plansSub}</p>
          </div>
        </button>
      </div>

      {/* Active Goals Section */}
      <div className="section-header">
        <h3 className="section-title">
          <ClipboardList size={22} color="#047857" />
          {content.activeGoalsTitle}
        </h3>
      </div>

      {activeGoals.length === 0 ? (
        <div className="goal-card" style={{ textAlign: 'center', padding: '36px 20px', color: 'var(--text-muted)' }}>
          <p>{content.noGoalsText}</p>
        </div>
      ) : (
        <div className="goals-list">
          {activeGoals.map((goal) => (
            <div key={goal.id} className="goal-card">
              <div className="goal-card-top">
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span className="crop-badge">🌱 {goal.crop}</span>
                  <span className={`status-badge ${getStatusClass(goal.status)}`}>
                    ● {goal.status}
                  </span>
                </div>
                {goal.next_follow_up_date && (
                  <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                    🗓 Next Check: {goal.next_follow_up_date}
                  </span>
                )}
              </div>

              <div>
                <h4 className="goal-title">{goal.goal}</h4>
                <p className="goal-desc">{goal.problem}</p>
              </div>

              {goal.action_plan && goal.action_plan.immediate_actions.length > 0 && (
                <div style={{ background: '#f8fafc', padding: '10px 14px', borderRadius: '8px', fontSize: '0.84rem' }}>
                  <strong>🚨 Immediate Action: </strong>
                  {goal.action_plan.immediate_actions[0]}
                </div>
              )}

              <div className="goal-footer">
                <span>Updated: {new Date(goal.updated_at).toLocaleDateString()}</span>
                <div className="goal-actions">
                  <button className="btn-secondary" onClick={() => onSelectGoal(goal)}>
                    {content.viewGoalBtn} <ArrowRight size={14} />
                  </button>
                  <button className="btn-primary" onClick={() => onOpenFollowUpModal(goal)}>
                    <Bell size={14} /> {content.followUpBtn}
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

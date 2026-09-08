import React, { useState, useEffect, useRef } from 'react';
import type { Language, ChatMessage, AgentActivityStep } from '../types';
import { apiClient } from '../services/api';
import { speechService } from '../services/speech';
import {
  Send,
  Mic,
  MicOff,
  Image as ImageIcon,
  Volume2,
  CheckCircle2,
  AlertTriangle,
  FileCheck,
  ShieldCheck,
  Calendar,
  Layers,
  Sparkles
} from 'lucide-react';

interface ChatScreenProps {
  currentLanguage: Language;
  onLanguageChange: (lang: Language) => void;
  activeGoalId?: string;
  initialPrompt?: string;
  initialSampleImage?: string;
  onGoalUpdated?: () => void;
}

export const ChatScreen: React.FC<ChatScreenProps> = ({
  currentLanguage,
  activeGoalId,
  initialPrompt,
  initialSampleImage,
  onGoalUpdated,
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [selectedImage, setSelectedImage] = useState<string | null>(initialSampleImage || null);
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [currentActivities, setCurrentActivities] = useState<AgentActivityStep[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const sampleImages = [
    { label: '🌶 Chilli Day 1 (Yellowing)', url: '/uploads/sample_chilli_yellowing.jpg' },
    { label: '🌿 Chilli Recovery (Day 3)', url: '/uploads/sample_chilli_recovered.jpg' },
    { label: '🍅 Tomato Blight', url: '/uploads/sample_tomato_blight.jpg' },
    { label: '🌾 Paddy Blast', url: '/uploads/sample_paddy_blast.jpg' },
  ];

  const placeholders: Record<Language, string> = {
    kn: 'ನಿಮ್ಮ ಬೆಳೆಯ ಸಮಸ್ಯೆ ತಿಳಿಸಿ (ಉದಾ: ಮೆಣಸಿನಕಾಯಿ ಎಲೆ ಹಳದಿಯಾಗುತ್ತಿದೆ)...',
    hi: 'अपनी फसल की समस्या बताएं (उदा: मिर्च की पत्तियां पीली पड़ रही हैं)...',
    te: 'మీ పంట సమస్యను చెప్పండి (ఉదా: మిరప ఆకులు పసుపు రంగులోకి మారాయి)...',
    en: 'Describe your crop problem (e.g., chilli leaves turning yellow)...',
  };

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, currentActivities]);

  // Handle Initial Prompt or Initial Voice Trigger
  useEffect(() => {
    if (initialPrompt === '__START_VOICE__') {
      startVoiceRecording();
    } else if (initialPrompt && initialPrompt.trim()) {
      handleSendMessage(initialPrompt, initialSampleImage || undefined);
    }
  }, [initialPrompt]);

  const handleSendMessage = async (customText?: string, customImage?: string) => {
    const textToSend = customText !== undefined ? customText : inputValue;
    const imageToSend = customImage !== undefined ? customImage : selectedImage;

    if (!textToSend.trim() && !imageToSend) return;

    const userMessageId = 'msg-' + Date.now();
    const userMsg: ChatMessage = {
      id: userMessageId,
      sender: 'farmer',
      text: textToSend,
      image_url: imageToSend || undefined,
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputValue('');
    setSelectedImage(null);
    setIsLoading(true);

    // Initial agent activity indicator
    setCurrentActivities([
      { step_id: 'understanding', label: '✓ Understanding your problem', status: 'active' },
    ]);

    try {
      const response = await apiClient.chat({
        message: textToSend,
        language: currentLanguage,
        image_url: imageToSend || undefined,
        goal_id: activeGoalId,
      });

      // Update activity steps from agent
      if (response.agent_activity_steps) {
        setCurrentActivities(response.agent_activity_steps);
      }

      const agentMsg: ChatMessage = {
        id: 'agent-' + Date.now(),
        sender: 'agent',
        text: response.response_text,
        activity_steps: response.agent_activity_steps,
        action_plan: response.action_plan,
        possible_causes: response.possible_causes,
        goal_id: response.goal_id,
        goal_status: response.goal_status,
        goal_defined: response.goal_defined,
        timestamp: new Date().toLocaleTimeString(),
      };

      setMessages((prev) => [...prev, agentMsg]);
      setCurrentActivities([]);

      if (onGoalUpdated) {
        onGoalUpdated();
      }

      // Auto TTS if voice was used or on initial demo
      if (isRecording || customText) {
        speechService.speak(response.response_text, currentLanguage);
      }
    } catch (err: any) {
      const errorMsg: ChatMessage = {
        id: 'err-' + Date.now(),
        sender: 'agent',
        text: `Error connecting to KrishiRakshak Agent: ${err.message || 'Please check backend server'}.`,
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages((prev) => [...prev, errorMsg]);
      setCurrentActivities([]);
    } finally {
      setIsLoading(false);
    }
  };

  // Voice Recording
  const startVoiceRecording = () => {
    if (isRecording) {
      speechService.stopListening();
      setIsRecording(false);
      return;
    }

    setIsRecording(true);
    speechService.startListening(
      currentLanguage,
      (transcript) => {
        setInputValue(transcript);
        setIsRecording(false);
        // Automatically send after voice capture for true voice-first experience
        handleSendMessage(transcript);
      },
      (err) => {
        console.warn('Speech error:', err);
        setIsRecording(false);
      },
      () => {
        setIsRecording(false);
      }
    );
  };

  // File Upload
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      const res = await apiClient.uploadImage(file);
      setSelectedImage(res.image_url);
    } catch (err) {
      alert('Failed to upload image');
    }
  };

  return (
    <div className="chat-view-container">
      {/* Chat Header Bar */}
      <div className="chat-header-bar">
        <div className="agent-status-indicator">
          <div className="agent-avatar">🌾</div>
          <div>
            <div className="agent-live-text">
              KrishiRakshak AI Agent
              <span className="online-dot" />
            </div>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              Goal-Driven Multi-Agent Decision Engine
            </span>
          </div>
        </div>

        {activeGoalId && (
          <span className="status-badge action_plan_active">
            Goal ID: {activeGoalId.substring(0, 8)}...
          </span>
        )}
      </div>

      {/* Messages Feed */}
      <div className="messages-feed">
        {messages.length === 0 && (
          <div style={{ textAlign: 'center', margin: 'auto', maxWidth: '480px', padding: '20px' }}>
            <div style={{ fontSize: '48px', marginBottom: '12px' }}>🌾</div>
            <h3 style={{ fontSize: '1.2rem', marginBottom: '6px', color: 'var(--primary-900)' }}>
              {currentLanguage === 'kn' && 'ನಮಸ್ಕಾರ! ನಿಮ್ಮ ಕೃಷಿ ಸಮಸ್ಯೆಯನ್ನು ತಿಳಿಸಿ'}
              {currentLanguage === 'hi' && 'नमस्ते! अपनी कृषि समस्या बताएं'}
              {currentLanguage === 'te' && 'నమస్కారం! మీ వ్యవసాయ సమస్యను చెప్పండి'}
              {currentLanguage === 'en' && 'Welcome to KrishiRakshak AI!'}
            </h3>
            <p style={{ fontSize: '0.86rem', color: 'var(--text-medium)', marginBottom: '16px' }}>
              {currentLanguage === 'kn' && 'ಧ್ವನಿ ಬಟನ್ ಒತ್ತಿ ಮಾತನಾಡಿ ಅಥವಾ ಬೆಳೆಯ ಎಲೆಯ ಫೋಟೋವನ್ನು ಹಂಚಿಕೊಳ್ಳಿ.'}
              {currentLanguage === 'hi' && 'माइक दबाकर बोलें या फसल की पत्ती की तस्वीर साझा करें।'}
              {currentLanguage === 'te' && 'మైక్ బటన్ నొక్కి మాట్లాడండి లేదా ఆకు ఫోటోను అప్‌లోడ్ చేయండి.'}
              {currentLanguage === 'en' && 'Press the mic button to speak in your language or upload a crop leaf photo.'}
            </p>

            <div style={{ display: 'flex', gap: '8px', justifyContent: 'center', flexWrap: 'wrap' }}>
              <button
                className="sample-image-pill"
                onClick={() => handleSendMessage(
                  currentLanguage === 'kn' ? 'ನಮಸ್ಕಾರ' : currentLanguage === 'hi' ? 'नमस्ते' : currentLanguage === 'te' ? 'నమస్కారం' : 'Hi, Hello!'
                )}
              >
                👋 {currentLanguage === 'kn' ? 'ನಮಸ್ಕಾರ / ಹಲೋ' : currentLanguage === 'hi' ? 'नमस्ते / हैलो' : currentLanguage === 'te' ? 'నమస్కారం' : 'Say Hi'}
              </button>
              <button
                className="sample-image-pill"
                onClick={() => handleSendMessage(
                  currentLanguage === 'kn' ? 'ನೀವು ಯಾರು ಮತ್ತು ಏನು ಮಾಡಬಲ್ಲಿರಿ?' : currentLanguage === 'hi' ? 'आप कौन हैं और क्या कर सकते हैं?' : currentLanguage === 'te' ? 'మీరు ఎవరు మరియు ఏమి చేయగలరు?' : 'Who are you and what can you do?'
                )}
              >
                ❓ {currentLanguage === 'kn' ? 'ನೀವು ಏನು ಮಾಡಬಲ್ಲಿರಿ?' : currentLanguage === 'hi' ? 'आप क्या कर सकते हैं?' : currentLanguage === 'te' ? 'మీరు ఏమి చేయగలరు?' : 'What can you do?'}
              </button>
              <button
                className="sample-image-pill"
                onClick={() => handleSendMessage(
                  currentLanguage === 'kn' ? 'ಯಾವ ಯಾವ ಬೆಳೆಗಳಿಗೆ ಸಲಹೆ ಸಿಗುತ್ತೆ?' : currentLanguage === 'hi' ? 'कौन सी फसलों के लिए सहायता उपलब्ध है?' : currentLanguage === 'te' ? 'ఏ పంటలకు సహాయం లభిస్తుంది?' : 'Which crops do you support?'
                )}
              >
                🌾 {currentLanguage === 'kn' ? 'ಬೆಳೆಗಳ ಪಟ್ಟಿ' : currentLanguage === 'hi' ? 'समर्थित फसलें' : currentLanguage === 'te' ? 'పంటల జాబితా' : 'Supported Crops'}
              </button>
              <button
                className="sample-image-pill"
                onClick={() => handleSendMessage(
                  'ನನ್ನ ಮೆಣಸಿನಕಾಯಿ ಗಿಡದ ಎಲೆಗಳು ಹಳದಿಯಾಗುತ್ತಿವೆ. ಸಹಾಯ ಮಾಡಿ.',
                  '/uploads/sample_chilli_yellowing.jpg'
                )}
              >
                <Sparkles size={14} /> 🌶 {currentLanguage === 'kn' ? 'ಮೆಣಸಿನಕಾಯಿ ರೋಗ ಮಾದರಿ' : 'Chilli Leaf Scenario'}
              </button>
            </div>
          </div>
        )}

        {messages.map((msg) => (
          <div key={msg.id} className={`message-bubble ${msg.sender}`}>
            {msg.image_url && (
              <img
                src={apiClient.resolveImageUrl(msg.image_url)}
                alt="Crop upload"
                className="message-image-preview"
                onError={(e) => {
                  (e.target as HTMLElement).style.display = 'none';
                }}
              />
            )}

            {/* Goal Definition Badge if agent defined it */}
            {msg.goal_defined && msg.goal_status !== 'Conversational' && (
              <div style={{
                background: '#ecfdf5',
                border: '1px solid #10b981',
                padding: '8px 12px',
                borderRadius: '8px',
                marginBottom: '10px',
                fontSize: '0.82rem',
                color: '#065f46'
              }}>
                <strong>🎯 Agent Goal Defined:</strong> {msg.goal_defined}
              </div>
            )}

            <div style={{ whiteSpace: 'pre-wrap' }}>{msg.text}</div>

            {/* Agent Live Activity Steps */}
            {msg.activity_steps && msg.activity_steps.length > 0 && (
              <div className="agent-activity-banner" style={{ marginTop: '12px' }}>
                <span className="activity-title">
                  <CheckCircle2 size={14} color="#059669" /> Autonomous Tools Executed
                </span>
                <div className="activity-steps-row">
                  {msg.activity_steps.map((s, idx) => (
                    <span key={idx} className="step-chip">
                      {s.label}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Possible Causes & Confidence Meters */}
            {msg.possible_causes && msg.possible_causes.length > 0 && (
              <div className="causes-box">
                <strong style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px' }}>
                  <Layers size={14} /> Identified Causes & Confidence Levels:
                </strong>
                {msg.possible_causes.map((c, i) => (
                  <div key={i} className="cause-item">
                    <div>
                      <strong>{c.cause}</strong> ({c.probability} Probability)
                      <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>{c.explanation}</div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <span style={{ fontWeight: 700 }}>{Math.round(c.confidence_score * 100)}%</span>
                      <div className="confidence-meter">
                        <div
                          className="confidence-fill"
                          style={{ width: `${Math.round(c.confidence_score * 100)}%` }}
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Embedded Action Plan Card */}
            {msg.action_plan && (
              <div className="embedded-action-plan">
                <div className="plan-header">
                  <FileCheck size={18} color="#047857" /> Practical Agricultural Action Plan
                </div>

                <div className="plan-section">
                  <div className="plan-section-title">
                    <ShieldCheck size={15} color="#dc2626" /> Immediate Actions (Day 1):
                  </div>
                  <ul className="plan-list">
                    {msg.action_plan.immediate_actions.map((act, i) => (
                      <li key={i}>{act}</li>
                    ))}
                  </ul>
                </div>

                <div className="plan-section">
                  <div className="plan-section-title">
                    <Calendar size={15} color="#2563eb" /> Short-Term Actions (Day 3-5):
                  </div>
                  <ul className="plan-list">
                    {msg.action_plan.short_term_actions.map((act, i) => (
                      <li key={i}>{act}</li>
                    ))}
                  </ul>
                </div>

                <div className="plan-section">
                  <div className="plan-section-title">
                    <AlertTriangle size={15} color="#d97706" /> What to Monitor:
                  </div>
                  <ul className="plan-list">
                    {msg.action_plan.monitoring_actions.map((act, i) => (
                      <li key={i}>{act}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {/* Text-To-Speech Button on Agent Messages */}
            {msg.sender === 'agent' && (
              <button
                className="tts-play-btn"
                onClick={() => speechService.speak(msg.text, currentLanguage)}
                title="Listen to response in your language"
              >
                <Volume2 size={14} /> ಧ್ವನಿ ಕೇಳಿ (Listen Audio)
              </button>
            )}
          </div>
        ))}

        {/* Live Loading Activity Ticker */}
        {isLoading && (
          <div className="message-bubble agent">
            <div className="agent-activity-banner">
              <span className="activity-title">
                <Sparkles size={14} color="#059669" /> Investigating Problem Autonomously...
              </span>
              <div className="activity-steps-row">
                <span className="step-chip">✓ Understanding problem</span>
                <span className="step-chip">✓ Checking crop information</span>
                <span className="step-chip">✓ Querying disease database</span>
                <span className="step-chip">✓ Checking weather conditions</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Chat Input Bar */}
      <div className="chat-input-bar">
        {/* Sample Image Quick Drawer */}
        <div className="sample-images-bar">
          <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', whiteSpace: 'nowrap' }}>
            📷 Sample Crop Photos:
          </span>
          {sampleImages.map((s, idx) => (
            <button
              key={idx}
              className={`sample-image-pill ${selectedImage === s.url ? 'active' : ''}`}
              onClick={() => setSelectedImage(s.url)}
              style={selectedImage === s.url ? { background: '#d1fae5', borderColor: '#10b981', fontWeight: 700 } : {}}
            >
              {s.label}
            </button>
          ))}
          {selectedImage && (
            <button
              className="sample-image-pill"
              onClick={() => setSelectedImage(null)}
              style={{ color: '#dc2626' }}
            >
              ✕ Clear Image
            </button>
          )}
        </div>

        {selectedImage && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.8rem', color: '#047857' }}>
            <ImageIcon size={16} /> Selected: {selectedImage}
          </div>
        )}

        <div className="input-row">
          <input
            type="file"
            ref={fileInputRef}
            style={{ display: 'none' }}
            accept="image/*"
            onChange={handleFileUpload}
          />
          <button
            type="button"
            className="icon-button"
            onClick={() => fileInputRef.current?.click()}
            title="Upload Crop Photo"
          >
            <ImageIcon size={20} />
          </button>

          <button
            type="button"
            className={`icon-button mic ${isRecording ? 'recording' : ''}`}
            onClick={startVoiceRecording}
            title={isRecording ? 'Stop Recording' : 'Speak Your Problem (Voice Input)'}
          >
            {isRecording ? <MicOff size={20} /> : <Mic size={20} />}
          </button>

          <input
            type="text"
            className="chat-input-field"
            placeholder={placeholders[currentLanguage]}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleSendMessage();
            }}
          />

          <button
            type="button"
            className="send-button"
            onClick={() => handleSendMessage()}
            title="Send Message"
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
};

import React, { useState } from 'react';
import type { FarmerGoal, FollowUpSubmitResponse, Language } from '../types';
import { apiClient } from '../services/api';
import confetti from 'canvas-confetti';
import { X, CheckCircle, AlertOctagon, RefreshCw, PhoneCall, TrendingUp } from 'lucide-react';

interface FollowUpModalProps {
  goal: FarmerGoal;
  currentLanguage: Language;
  onClose: () => void;
  onSuccess: () => void;
}

export const FollowUpModal: React.FC<FollowUpModalProps> = ({
  goal,
  currentLanguage,
  onClose,
  onSuccess,
}) => {
  const [assessment, setAssessment] = useState<'improving' | 'stable' | 'worsening'>('improving');
  const [feedbackText, setFeedbackText] = useState('');
  const [newImageUrl, setNewImageUrl] = useState<string>('/uploads/sample_chilli_recovered.jpg');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [result, setResult] = useState<FollowUpSubmitResponse | null>(null);

  const prevImage = goal.latest_image_url || '/uploads/sample_chilli_yellowing.jpg';

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      const res = await apiClient.submitFollowUp({
        goal_id: goal.id,
        farmer_response: feedbackText || (assessment === 'improving' ? 'ಹೊಸ ಚಿಗುರು ಹಸಿರಾಗಿದೆ, ಚೇತರಿಸಿಕೊಳ್ಳುತ್ತಿದೆ' : 'ಹಾನಿ ಹೆಚ್ಚಾಗಿದೆ, ಒಣಗುತ್ತಿದೆ'),
        new_image_url: newImageUrl,
        condition_assessment: assessment,
        language: currentLanguage,
      });

      setResult(res);

      if (res.observation_result === 'Improving') {
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 },
        });
      }

      onSuccess();
    } catch (err: any) {
      alert('Error submitting follow up: ' + err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="comparison-modal-backdrop" onClick={onClose}>
      <div className="comparison-modal" onClick={(e) => e.stopPropagation()}>
        {/* Modal Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--primary-900)' }}>
              🔔 Day 3 Closed-Loop Follow-Up Check
            </h3>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Goal: {goal.goal} ({goal.crop})
            </span>
          </div>
          <button
            onClick={onClose}
            style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-muted)' }}
          >
            <X size={20} />
          </button>
        </div>

        {!result ? (
          <>
            {/* Step 1: Side-by-Side Crop Photos */}
            <div>
              <h4 style={{ fontSize: '0.88rem', fontWeight: 700, marginBottom: '8px' }}>
                📸 Crop Condition Comparison:
              </h4>
              <div className="side-by-side-images">
                <div className="comparison-photo-card">
                  <img
                    src={apiClient.resolveImageUrl(prevImage)}
                    alt="Day 1 initial leaf"
                    onError={(e) => { (e.target as HTMLElement).style.display = 'none'; }}
                  />
                  <div className="comparison-label">Day 1 (Initial Symptoms)</div>
                </div>

                <div className="comparison-photo-card">
                  <img
                    src={apiClient.resolveImageUrl(newImageUrl)}
                    alt="Day 3 follow-up leaf"
                    onError={(e) => { (e.target as HTMLElement).style.display = 'none'; }}
                  />
                  <div className="comparison-label">Day 3 (Current Photo)</div>
                </div>
              </div>

              {/* Sample Photo Switcher for Demo */}
              <div style={{ display: 'flex', gap: '6px', marginTop: '8px' }}>
                <button
                  type="button"
                  className="sample-image-pill"
                  onClick={() => {
                    setNewImageUrl('/uploads/sample_chilli_recovered.jpg');
                    setAssessment('improving');
                  }}
                  style={newImageUrl.includes('recovered') ? { background: '#d1fae5', borderColor: '#10b981' } : {}}
                >
                  🟢 Select Recovery Image
                </button>
                <button
                  type="button"
                  className="sample-image-pill"
                  onClick={() => {
                    setNewImageUrl('/uploads/sample_chilli_worsened.jpg');
                    setAssessment('worsening');
                  }}
                  style={newImageUrl.includes('worsened') ? { background: '#fee2e2', borderColor: '#ef4444' } : {}}
                >
                  🔴 Select Worsening Image
                </button>
              </div>
            </div>

            {/* Step 2: Farmer Condition Assessment Choice */}
            <div>
              <h4 style={{ fontSize: '0.88rem', fontWeight: 700, marginBottom: '8px' }}>
                ಬೆಳೆಯ ಪ್ರಸ್ತುತ ಸ್ಥಿತಿ ಹೇಗಿದೆ? (Current Condition):
              </h4>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px' }}>
                <button
                  type="button"
                  onClick={() => setAssessment('improving')}
                  style={{
                    padding: '12px 10px',
                    borderRadius: '10px',
                    border: assessment === 'improving' ? '2px solid #10b981' : '1px solid var(--border-light)',
                    background: assessment === 'improving' ? '#ecfdf5' : '#ffffff',
                    fontWeight: 700,
                    cursor: 'pointer',
                    fontSize: '0.82rem',
                    textAlign: 'center'
                  }}
                >
                  <TrendingUp size={20} color="#059669" style={{ margin: '0 auto 4px' }} />
                  <div>ಸುಧಾರಿಸುತ್ತಿದೆ</div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Improving</div>
                </button>

                <button
                  type="button"
                  onClick={() => setAssessment('stable')}
                  style={{
                    padding: '12px 10px',
                    borderRadius: '10px',
                    border: assessment === 'stable' ? '2px solid #d97706' : '1px solid var(--border-light)',
                    background: assessment === 'stable' ? '#fffbeb' : '#ffffff',
                    fontWeight: 700,
                    cursor: 'pointer',
                    fontSize: '0.82rem',
                    textAlign: 'center'
                  }}
                >
                  <RefreshCw size={20} color="#d97706" style={{ margin: '0 auto 4px' }} />
                  <div>ಬದಲಾವಣೆ ಇಲ್ಲ</div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Stable / Unchanged</div>
                </button>

                <button
                  type="button"
                  onClick={() => setAssessment('worsening')}
                  style={{
                    padding: '12px 10px',
                    borderRadius: '10px',
                    border: assessment === 'worsening' ? '2px solid #ef4444' : '1px solid var(--border-light)',
                    background: assessment === 'worsening' ? '#fef2f2' : '#ffffff',
                    fontWeight: 700,
                    cursor: 'pointer',
                    fontSize: '0.82rem',
                    textAlign: 'center'
                  }}
                >
                  <AlertOctagon size={20} color="#dc2626" style={{ margin: '0 auto 4px' }} />
                  <div>ಹಾನಿ ಹೆಚ್ಚಾಗಿದೆ</div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Worsening</div>
                </button>
              </div>
            </div>

            {/* Step 3: Farmer Remarks */}
            <div>
              <label style={{ fontSize: '0.85rem', fontWeight: 600, display: 'block', marginBottom: '6px' }}>
                ಹೆಚ್ಚುವರಿ ವಿವರಗಳು (Farmer Observations):
              </label>
              <textarea
                rows={3}
                style={{
                  width: '100%',
                  padding: '10px',
                  borderRadius: '8px',
                  border: '1px solid var(--border-light)',
                  fontFamily: 'inherit',
                  fontSize: '0.9rem',
                }}
                placeholder="ಹೊಸ ಚಿಗುರು ಹೇಗೆ ಕಾಣುತ್ತಿದೆ? ಅಥವಾ ಕೀಟಗಳು ಕಡಿಮೆಯಾಗಿವೆಯೇ ತಿಳಿಸಿ..."
                value={feedbackText}
                onChange={(e) => setFeedbackText(e.target.value)}
              />
            </div>

            <button
              className="btn-primary"
              style={{ width: '100%', justifyContent: 'center', padding: '12px' }}
              onClick={handleSubmit}
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Evaluating Follow-Up...' : 'ಸಲ್ಲಿಸಿ ಮತ್ತು ಮೌಲ್ಯಮಾಪನ ಪಡೆಯಿರಿ (Submit Follow-Up)'}
            </button>
          </>
        ) : (
          /* Result from Follow-Up Agent */
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            <div style={{
              background: result.observation_result === 'Improving' ? '#ecfdf5' : '#fef2f2',
              border: `1px solid ${result.observation_result === 'Improving' ? '#10b981' : '#ef4444'}`,
              borderRadius: '12px',
              padding: '18px',
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                {result.observation_result === 'Improving' ? (
                  <CheckCircle size={28} color="#059669" />
                ) : (
                  <AlertOctagon size={28} color="#dc2626" />
                )}
                <div>
                  <h4 style={{
                    fontSize: '1.1rem',
                    fontWeight: 700,
                    color: result.observation_result === 'Improving' ? '#065f46' : '#991b1b',
                  }}>
                    Follow-Up Result: {result.observation_result}
                  </h4>
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                    {result.comparison_details.chlorosis_delta}
                  </span>
                </div>
              </div>

              <p style={{ fontSize: '0.92rem', lineHeight: 1.5, color: 'var(--text-dark)' }}>
                {result.response_text}
              </p>
            </div>

            {/* Prevention Guidance if Improving */}
            {result.prevention_guidance && (
              <div style={{ background: '#f8fafc', border: '1px solid #cbd5e1', padding: '14px', borderRadius: '8px', fontSize: '0.85rem' }}>
                <strong>🌱 ದೀರ್ಘಕಾಲೀನ ತಡೆಗಟ್ಟುವಿಕೆ (Long-term Prevention Guidance):</strong>
                <p style={{ marginTop: '4px' }}>{result.prevention_guidance}</p>
              </div>
            )}

            {/* Expert Escalation if Worsening */}
            {result.expert_escalation_recommended && (
              <div className="escalation-alert-card">
                <div className="escalation-header">
                  <PhoneCall size={18} /> ತುರ್ತು ಕೃಷಿ ತಜ್ಞರ ಸಂಪರ್ಕ (Expert Escalation):
                </div>
                <p style={{ fontSize: '0.82rem', marginBottom: '8px' }}>
                  ನಿಮ್ಮ ಬೆಳೆ ಹಾನಿ ತೀವ್ರವಾಗಿರುವುದರಿಂದ ಸ್ಥಳೀಯ ಕೃಷಿ ವಿಜ್ಞಾನ ಕೇಂದ್ರ ಅಥವಾ ಟೋಲ್-ಫ್ರೀ ಸಹಾಯವಾಣಿಗೆ ಸಂಪರ್ಕಿಸಿ:
                </p>
                {result.expert_contacts.slice(0, 3).map((exp, idx) => (
                  <div key={idx} className="expert-contact-row">
                    <div>
                      <strong>{exp.name}</strong>
                      <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>{exp.address || exp.timings}</div>
                    </div>
                    <a
                      href={`tel:${exp.number || exp.phone}`}
                      style={{
                        background: '#dc2626',
                        color: '#ffffff',
                        textDecoration: 'none',
                        padding: '4px 12px',
                        borderRadius: '6px',
                        fontSize: '0.8rem',
                        fontWeight: 700,
                      }}
                    >
                      📞 {exp.number || exp.phone}
                    </a>
                  </div>
                ))}
              </div>
            )}

            <button
              className="btn-primary"
              style={{ width: '100%', justifyContent: 'center', padding: '12px' }}
              onClick={onClose}
            >
              ಮುಕ್ತಾಯಗೊಳಿಸಿ (Close)
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

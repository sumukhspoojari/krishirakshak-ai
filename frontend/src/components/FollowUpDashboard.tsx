import React from 'react';
import type { FarmerGoal, Language } from '../types';
import { ClipboardList, Bell, Calendar, Eye } from 'lucide-react';

interface FollowUpDashboardProps {
  currentLanguage: Language;
  goals: FarmerGoal[];
  onSelectGoal: (goal: FarmerGoal) => void;
  onOpenFollowUpModal: (goal: FarmerGoal) => void;
  onNewGoalClick: () => void;
}

export const FollowUpDashboard: React.FC<FollowUpDashboardProps> = ({
  currentLanguage,
  goals,
  onSelectGoal,
  onOpenFollowUpModal,
  onNewGoalClick,
}) => {
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
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <div className="section-header">
        <div>
          <h3 className="section-title">
            <ClipboardList size={24} color="#047857" />
            {currentLanguage === 'kn' && 'ನನ್ನ ಬೆಳೆ ಗುರಿಗಳು ಮತ್ತು ಅನುಸರಣಾ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್'}
            {currentLanguage === 'hi' && 'मेरी फसल योजनाएं और फॉलो-अप डैशबोर्ड'}
            {currentLanguage === 'te' && 'నా పంట లక్ష్యాలు మరియు ఫాలో-అప్ డాష్‌బోర్డ్'}
            {currentLanguage === 'en' && 'Active Closed-Loop Crop Goals & Monitoring'}
          </h3>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
            Each goal tracks an agricultural problem from initial diagnosis through multi-day recovery.
          </p>
        </div>

        <button className="btn-primary" onClick={onNewGoalClick}>
          + ಹೊಸ ಬೆಳೆ ಸಮಸ್ಯೆ (New Crop Goal)
        </button>
      </div>

      {goals.length === 0 ? (
        <div className="goal-card" style={{ textAlign: 'center', padding: '48px 20px' }}>
          <h4 style={{ fontSize: '1.1rem', marginBottom: '8px' }}>ಯಾವುದೇ ಸಕ್ರಿಯ ಬೆಳೆ ಯೋಜನೆಗಳಿಲ್ಲ</h4>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '16px' }}>
            ಹೊಸ ಸಮಸ್ಯೆಯನ್ನು ಸಲ್ಲಿಸಲು ಚಾಟ್ ಅಥವಾ ಹೋಮ್ ಸ್ಕ್ರೀನ್ ಬಳಸಿ.
          </p>
          <button className="btn-primary" style={{ margin: '0 auto' }} onClick={onNewGoalClick}>
            ಸಮಸ್ಯೆಯನ್ನು ದಾಖಲಿಸಿ (Start Investigation)
          </button>
        </div>
      ) : (
        <div className="goals-list">
          {goals.map((goal) => (
            <div key={goal.id} className="goal-card">
              <div className="goal-card-top">
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span className="crop-badge">🌱 {goal.crop}</span>
                  <span className={`status-badge ${getStatusClass(goal.status)}`}>
                    ● {goal.status}
                  </span>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    Urgency: {goal.urgency}
                  </span>
                </div>

                {goal.next_follow_up_date && (
                  <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#047857', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Calendar size={14} /> Follow-Up: {goal.next_follow_up_date}
                  </span>
                )}
              </div>

              <div>
                <h4 className="goal-title">{goal.goal}</h4>
                <p className="goal-desc">{goal.problem}</p>
              </div>

              {goal.action_plan && (
                <div style={{ background: '#f8fafc', padding: '12px 16px', borderRadius: '10px', fontSize: '0.85rem' }}>
                  <strong style={{ color: '#065f46' }}>📋 ಸಕ್ರಿಯ ಕಾರ್ಯ ಯೋಜನೆ (Active Plan): </strong>
                  <ul style={{ paddingLeft: '20px', marginTop: '6px' }}>
                    {goal.action_plan.immediate_actions.slice(0, 2).map((a, i) => (
                      <li key={i}>{a}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="goal-footer">
                <span>ಪ್ರಾರಂಭವಾದ ದಿನಾಂಕ: {new Date(goal.created_at).toLocaleDateString()}</span>
                <div className="goal-actions">
                  <button className="btn-secondary" onClick={() => onSelectGoal(goal)}>
                    <Eye size={14} /> ಚಾಟ್‌ಗೆ ಹೋಗಿ (Open Chat)
                  </button>
                  <button className="btn-primary" onClick={() => onOpenFollowUpModal(goal)}>
                    <Bell size={14} /> Day 3 Follow-Up Check
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

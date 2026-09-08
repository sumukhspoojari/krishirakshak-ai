import React from 'react';
import type { UserProfile } from '../types';
import {
  X,
  User,
  Mail,
  Phone,
  Globe,
  Calendar,
  ShieldCheck,
  CheckCircle2,
  LogOut
} from 'lucide-react';

interface ProfileModalProps {
  user: UserProfile;
  onClose: () => void;
  onLogout: () => void;
}

export const ProfileModal: React.FC<ProfileModalProps> = ({
  user,
  onClose,
  onLogout,
}) => {
  const languageNames: Record<string, string> = {
    kn: 'ಕನ್ನಡ (Kannada)',
    hi: 'हिन्दी (Hindi)',
    te: 'తెలుగు (Telugu)',
    ta: 'தமிழ் (Tamil)',
    en: 'English',
  };

  const formattedDate = user.created_at
    ? new Date(user.created_at).toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      })
    : 'Active Member';

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="profile-modal-content" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="profile-modal-header">
          <div className="flex items-center space-x-3">
            <div className="profile-avatar-large">
              <User className="w-8 h-8 text-emerald-700" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-slate-900">{user.name}</h2>
              <div className="flex items-center text-xs text-emerald-700 font-semibold mt-0.5">
                <ShieldCheck className="w-4 h-4 mr-1 inline" /> Verified Farmer Account
              </div>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1 rounded-full text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Stored Details Body */}
        <div className="profile-modal-body">
          <div className="section-title">Stored Farmer Details (SQLite Database)</div>

          <div className="details-list">
            <div className="detail-row">
              <div className="detail-label">
                <User className="w-4 h-4 mr-2 text-emerald-600 inline" /> Full Name
              </div>
              <div className="detail-value">{user.name}</div>
            </div>

            <div className="detail-row">
              <div className="detail-label">
                <Mail className="w-4 h-4 mr-2 text-emerald-600 inline" /> Email Address
              </div>
              <div className="detail-value">{user.email || 'Not provided'}</div>
            </div>

            <div className="detail-row">
              <div className="detail-label">
                <Phone className="w-4 h-4 mr-2 text-emerald-600 inline" /> Phone Number
              </div>
              <div className="detail-value">{user.phone || '+91 - Not registered'}</div>
            </div>

            <div className="detail-row">
              <div className="detail-label">
                <Globe className="w-4 h-4 mr-2 text-emerald-600 inline" /> Preferred Language
              </div>
              <div className="detail-value font-medium text-emerald-800">
                {languageNames[user.preferred_language] || user.preferred_language}
              </div>
            </div>

            <div className="detail-row">
              <div className="detail-label">
                <Calendar className="w-4 h-4 mr-2 text-emerald-600 inline" /> Registered On
              </div>
              <div className="detail-value">{formattedDate}</div>
            </div>

            <div className="detail-row">
              <div className="detail-label">
                <CheckCircle2 className="w-4 h-4 mr-2 text-emerald-600 inline" /> Farmer ID
              </div>
              <div className="detail-value text-xs font-mono text-slate-600">
                {user.id}
              </div>
            </div>
          </div>

          <div className="security-note">
            <ShieldCheck className="w-4 h-4 text-emerald-600 mr-2 flex-shrink-0" />
            <span>
              Your password is encrypted with PBKDF2-HMAC-SHA256. Details are securely saved in SQLite.
            </span>
          </div>
        </div>

        {/* Footer */}
        <div className="profile-modal-footer">
          <button
            type="button"
            className="btn-profile-logout"
            onClick={() => {
              onClose();
              onLogout();
            }}
          >
            <LogOut className="w-4 h-4 mr-2 inline" /> Sign Out
          </button>

          <button
            type="button"
            className="btn-profile-close"
            onClick={onClose}
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

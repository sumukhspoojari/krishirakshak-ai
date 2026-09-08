import React from 'react';
import type { Language, UserProfile, AuthMode } from '../types';
import {
  Sprout,
  Home,
  MessageSquare,
  CalendarCheck,
  CloudSun,
  Building2,
  RefreshCw,
  LogOut,
  Globe,
  UserCheck
} from 'lucide-react';

interface NavbarProps {
  currentLanguage: Language;
  onLanguageChange: (lang: Language) => void;
  activeTab: string;
  onTabChange: (tab: string) => void;
  onResetSession: () => void;
  currentUser?: UserProfile | null;
  onLogout?: () => void;
  onOpenAuth?: (mode: AuthMode) => void;
  onOpenProfile?: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentLanguage,
  onLanguageChange,
  activeTab,
  onTabChange,
  onResetSession,
  currentUser,
  onLogout,
  onOpenAuth,
  onOpenProfile,
}) => {
  const languages: { code: Language; label: string; native: string }[] = [
    { code: 'kn', label: 'Kannada', native: 'ಕನ್ನಡ' },
    { code: 'hi', label: 'Hindi', native: 'हिन्दी' },
    { code: 'te', label: 'Telugu', native: 'తెలుగు' },
    { code: 'en', label: 'English', native: 'English' },
  ];

  const tabs = [
    { id: 'home', label: 'Home', icon: Home },
    { id: 'chat', label: 'Diagnosis & Chat', icon: MessageSquare },
    { id: 'followup', label: 'Follow-ups', icon: CalendarCheck },
    { id: 'weather', label: 'Agro-Weather', icon: CloudSun },
    { id: 'schemes', label: 'Govt Schemes', icon: Building2 },
  ];

  return (
    <header className="navbar-container">
      {/* Brand Identity */}
      <div
        className="navbar-brand"
        onClick={() => onTabChange('home')}
        role="button"
        tabIndex={0}
      >
        <div className="brand-logo-pulse">
          <Sprout className="w-6 h-6 text-emerald-600" />
        </div>
        <div className="brand-text-block">
          <span className="brand-title">KrishiRakshak AI</span>
          <span className="brand-badge">Closed-Loop Agronomy</span>
        </div>
      </div>

      {/* Navigation Tabs */}
      <nav className="navbar-tabs" aria-label="Main Navigation">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              type="button"
              className={`nav-tab-button ${isActive ? 'active' : ''}`}
              onClick={() => onTabChange(tab.id)}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Global Controls & Actions */}
      <div className="navbar-actions">
        {/* Language Selector Dropdown */}
        <div className="language-selector-wrapper">
          <Globe className="w-4 h-4 text-emerald-600 mr-1 inline flex-shrink-0" />
          <select
            value={currentLanguage}
            onChange={(e) => onLanguageChange(e.target.value as Language)}
            className="language-select-dropdown"
            title="Select Language"
          >
            {languages.map((lang) => (
              <option key={lang.code} value={lang.code}>
                {lang.native} ({lang.label})
              </option>
            ))}
          </select>
        </div>

        {/* New Diagnosis / Reset Session */}
        <button
          type="button"
          className="btn-reset-session"
          onClick={onResetSession}
          title="Start fresh conversation"
        >
          <RefreshCw className="w-3.5 h-3.5 mr-1" />
          <span>New Query</span>
        </button>

        {/* User Account / Auth Section */}
        {currentUser ? (
          <div className="user-profile-badge">
            <button
              type="button"
              className="user-pill"
              onClick={onOpenProfile}
              title="Click to view stored farmer details"
            >
              <div className="user-avatar-mini">
                <UserCheck className="w-3.5 h-3.5 text-emerald-700" />
              </div>
              <span className="user-name-label">{currentUser.name}</span>
            </button>
            {onLogout && (
              <button
                type="button"
                className="btn-logout"
                onClick={onLogout}
                title="Sign Out"
              >
                <LogOut className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
        ) : (
          <div className="auth-nav-buttons">
            <button
              type="button"
              className="btn-nav-login"
              onClick={() => onOpenAuth && onOpenAuth('login')}
            >
              Sign In
            </button>
            <button
              type="button"
              className="btn-nav-signup"
              onClick={() => onOpenAuth && onOpenAuth('signup')}
            >
              Sign Up
            </button>
          </div>
        )}
      </div>
    </header>
  );
};

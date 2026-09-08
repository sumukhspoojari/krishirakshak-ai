import React, { useState } from 'react';
import type { Language, UserProfile } from '../types';
import { apiClient } from '../services/api';
import {
  Sprout,
  Mail,
  Lock,
  User,
  Phone,
  Eye,
  EyeOff,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
  AlertCircle,
  Home,
  Sparkles,
  Globe
} from 'lucide-react';

interface SignupPageProps {
  currentLanguage: Language;
  onLanguageChange: (lang: Language) => void;
  onNavigate: (path: string) => void;
  onSignupSuccess: (user: UserProfile) => void;
}

export const SignupPage: React.FC<SignupPageProps> = ({
  currentLanguage,
  onLanguageChange,
  onNavigate,
  onSignupSuccess,
}) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState<Language>(currentLanguage);
  const [showPassword, setShowPassword] = useState(false);
  const [termsAgreed, setTermsAgreed] = useState(true);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const languages: Array<{ code: Language; label: string; native: string }> = [
    { code: 'kn', label: 'Kannada', native: 'ಕನ್ನಡ' },
    { code: 'hi', label: 'Hindi', native: 'हिन्दी' },
    { code: 'te', label: 'Telugu', native: 'తెలుగు' },
    { code: 'en', label: 'English', native: 'English' },
  ];

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage('');

    if (!name.trim()) {
      setErrorMessage('Please enter your full name.');
      return;
    }
    if (!email.trim()) {
      setErrorMessage('Please enter your email address.');
      return;
    }
    if (password.length < 6) {
      setErrorMessage('Password must be at least 6 characters long.');
      return;
    }
    if (password !== confirmPassword) {
      setErrorMessage('Passwords do not match. Please verify and re-type.');
      return;
    }
    if (!termsAgreed) {
      setErrorMessage('Please accept the Terms & Agricultural Privacy Policy to continue.');
      return;
    }

    setLoading(true);
    try {
      const resp = await apiClient.signup({
        name: name.trim(),
        email: email.trim(),
        phone: phone.trim() || undefined,
        password,
        preferred_language: selectedLanguage,
      });

      onLanguageChange(selectedLanguage);
      onSignupSuccess(resp.user);
    } catch (err: any) {
      setErrorMessage(
        err?.response?.data?.detail ||
        err?.message ||
        'Failed to create account. An account with this email may already exist.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page-container">
      {/* Top Navbar */}
      <header className="auth-page-header">
        <div className="auth-brand" onClick={() => onNavigate('/')} style={{ cursor: 'pointer' }}>
          <div className="auth-brand-icon">
            <Sprout className="w-6 h-6 text-emerald-600" />
          </div>
          <span className="auth-brand-title">KrishiRakshak AI</span>
        </div>

        <button
          type="button"
          className="btn-back-home"
          onClick={() => onNavigate('/')}
        >
          <Home className="w-4 h-4 mr-1 inline" /> Back to Home
        </button>
      </header>

      {/* Main Content Split Card */}
      <div className="auth-page-body">
        <div className="auth-card-wrapper">
          {/* Left Decorative Side */}
          <div className="auth-card-sidebar">
            <div className="sidebar-pill">
              <Sparkles className="w-4 h-4 text-emerald-300 mr-2 inline" /> Free Farmer Registration
            </div>

            <h2 className="sidebar-heading">Join 50,000+ Smart Farmers Nationwide</h2>
            <p className="sidebar-subtext">
              Create your free KrishiRakshak AI account to safeguard your harvest with precision AI leaf diagnosis and closed-loop followups.
            </p>

            <div className="sidebar-benefits">
              <div className="benefit-item">
                <CheckCircle2 className="w-5 h-5 text-emerald-400 mr-3 flex-shrink-0" />
                <span>Save your farm details & personalized crop timeline</span>
              </div>
              <div className="benefit-item">
                <CheckCircle2 className="w-5 h-5 text-emerald-400 mr-3 flex-shrink-0" />
                <span>3-day automated follow-up recovery tracking</span>
              </div>
              <div className="benefit-item">
                <CheckCircle2 className="w-5 h-5 text-emerald-400 mr-3 flex-shrink-0" />
                <span>Live Agro-weather alerts & fertilizer dosage calculation</span>
              </div>
            </div>

            <div className="sidebar-footer">
              <ShieldCheck className="w-4 h-4 text-emerald-300 mr-2 inline" />
              <span>Free forever for individual farmers | No credit card needed</span>
            </div>
          </div>

          {/* Right Form Side */}
          <div className="auth-card-form-container">
            <div className="form-header">
              <h1 className="form-title">Create Farmer Account</h1>
              <p className="form-subtitle">
                Enter your details to register and save your farm profile.
              </p>
            </div>

            {errorMessage && (
              <div className="auth-alert error">
                <AlertCircle className="w-5 h-5 mr-2 flex-shrink-0" />
                <span>{errorMessage}</span>
              </div>
            )}

            <form onSubmit={handleSignup} className="auth-form">
              {/* Name */}
              <div className="form-group">
                <label className="form-label" htmlFor="signup-name">Full Name *</label>
                <div className="input-with-icon">
                  <User className="input-icon" />
                  <input
                    id="signup-name"
                    type="text"
                    required
                    className="form-input"
                    placeholder="e.g. Ramesh Gowda"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                  />
                </div>
              </div>

              {/* Email */}
              <div className="form-group">
                <label className="form-label" htmlFor="signup-email">Email Address *</label>
                <div className="input-with-icon">
                  <Mail className="input-icon" />
                  <input
                    id="signup-email"
                    type="email"
                    required
                    className="form-input"
                    placeholder="farmer@example.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </div>
              </div>

              {/* Phone (Optional) */}
              <div className="form-group">
                <label className="form-label" htmlFor="signup-phone">Mobile Number (Optional)</label>
                <div className="input-with-icon">
                  <Phone className="input-icon" />
                  <input
                    id="signup-phone"
                    type="tel"
                    className="form-input"
                    placeholder="+91 98765 43210"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                  />
                </div>
              </div>

              {/* Preferred Language */}
              <div className="form-group">
                <label className="form-label">
                  <Globe className="w-4 h-4 mr-1 inline text-emerald-600" /> Preferred Language
                </label>
                <div className="language-selector-grid">
                  {languages.map((lang) => (
                    <button
                      key={lang.code}
                      type="button"
                      className={`lang-select-chip ${selectedLanguage === lang.code ? 'active' : ''}`}
                      onClick={() => setSelectedLanguage(lang.code)}
                    >
                      <span className="lang-native">{lang.native}</span>
                      <span className="lang-sub">{lang.label}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Password */}
              <div className="form-group">
                <label className="form-label" htmlFor="signup-password">Password (min 6 characters) *</label>
                <div className="input-with-icon">
                  <Lock className="input-icon" />
                  <input
                    id="signup-password"
                    type={showPassword ? 'text' : 'password'}
                    required
                    minLength={6}
                    className="form-input"
                    placeholder="Create a strong password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                  <button
                    type="button"
                    className="password-toggle-btn"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              {/* Confirm Password */}
              <div className="form-group">
                <label className="form-label" htmlFor="signup-confirm-password">Confirm Password *</label>
                <div className="input-with-icon">
                  <Lock className="input-icon" />
                  <input
                    id="signup-confirm-password"
                    type={showPassword ? 'text' : 'password'}
                    required
                    minLength={6}
                    className="form-input"
                    placeholder="Re-enter your password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                  />
                </div>
              </div>

              {/* Terms Checkbox */}
              <div className="remember-row">
                <label className="remember-label">
                  <input
                    type="checkbox"
                    checked={termsAgreed}
                    onChange={(e) => setTermsAgreed(e.target.checked)}
                  />
                  <span>I agree to the Agricultural Terms of Service and data storage</span>
                </label>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className="btn-auth-primary"
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    <span className="spinner-sm mr-2"></span> Storing Details & Creating Account...
                  </span>
                ) : (
                  <span className="flex items-center justify-center">
                    Register & Enter Dashboard <ArrowRight className="w-4 h-4 ml-2" />
                  </span>
                )}
              </button>

              <div className="auth-switch-prompt">
                <span>Already have an account? </span>
                <button
                  type="button"
                  className="link-switch-auth"
                  onClick={() => onNavigate('/login')}
                >
                  Sign In
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

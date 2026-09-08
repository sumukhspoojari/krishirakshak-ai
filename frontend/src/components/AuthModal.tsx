import React, { useState } from 'react';
import type { Language, UserProfile, AuthMode } from '../types';
import { apiClient } from '../services/api';
import { X, Lock, Mail, User, Phone, Eye, EyeOff, AlertCircle, CheckCircle2, ArrowRight } from 'lucide-react';

interface AuthModalProps {
  initialMode?: AuthMode;
  currentLanguage: Language;
  onClose: () => void;
  onAuthSuccess: (user: UserProfile) => void;
}

export const AuthModal: React.FC<AuthModalProps> = ({
  initialMode = 'login',
  currentLanguage,
  onClose,
  onAuthSuccess,
}) => {
  const [mode, setMode] = useState<AuthMode>(initialMode);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [preferredLang, setPreferredLang] = useState<Language>(currentLanguage);
  const [resetToken, setResetToken] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [forgotStep, setForgotStep] = useState<'request' | 'reset'>('request');

  const content = {
    kn: {
      signInTitle: 'ರೈತ ಖಾತೆಗೆ ಲಾಗಿನ್ ಮಾಡಿ',
      signUpTitle: 'ಹೊಸ ರೈತ ಖಾತೆ ತೆರೆಯಿರಿ',
      forgotTitle: 'ಪಾಸ್‌ವರ್ಡ್ ಮರುಹೊಂದಿಸಿ',
      nameLabel: 'ಪೂರ್ಣ ಹೆಸರು',
      emailLabel: 'ಇಮೇಲ್ ವಿಳಾಸ',
      phoneLabel: 'ಮೊಬೈಲ್ ಸಂಖ್ಯೆ (ಐಚ್ಛಿಕ)',
      passwordLabel: 'ಪಾಸ್‌ವರ್ಡ್',
      confirmPasswordLabel: 'ಪಾಸ್‌ವರ್ಡ್ ದೃಢೀಕರಿಸಿ',
      langLabel: 'ಆದ್ಯತೆಯ ಭಾಷೆ',
      resetTokenLabel: 'ಮರುಹೊಂದಿಸುವ ಕೋಡ್ (Reset Token)',
      newPasswordLabel: 'ಹೊಸ ಪಾಸ್‌ವರ್ಡ್',
      signInBtn: 'ಲಾಗಿನ್ ಮಾಡಿ',
      signUpBtn: 'ಖಾತೆ ರಚಿಸಿ (Sign Up)',
      sendResetBtn: 'ಮರುಹೊಂದಿಸುವ ಕೋಡ್ ಪಡೆಯಿರಿ',
      applyResetBtn: 'ಪಾಸ್‌ವರ್ಡ್ ಬದಲಾಯಿಸಿ',
      forgotLink: 'ಪಾಸ್‌ವರ್ಡ್ ಮರೆತಿದ್ದೀರಾ?',
      haveAccount: 'ಈಗಾಗಲೇ ಖಾತೆ ಹೊಂದಿದ್ದೀರಾ? ಲಾಗಿನ್ ಮಾಡಿ',
      noAccount: 'ಖಾತೆ ಇಲ್ಲವೇ? ಹೊಸ ಖಾತೆ ತೆರೆಯಿರಿ',
      backToLogin: '← ಲಾಗಿನ್‌ಗೆ ಹಿಂತಿರುಗಿ',
    },
    hi: {
      signInTitle: 'किसान खाते में लॉगिन करें',
      signUpTitle: 'नया किसान खाता बनाएं',
      forgotTitle: 'पासवर्ड रीसेट करें',
      nameLabel: 'पूरा नाम',
      emailLabel: 'ईमेल पता',
      phoneLabel: 'मोबाइल नंबर (वैकल्पिक)',
      passwordLabel: 'पासवर्ड',
      confirmPasswordLabel: 'पासवर्ड की पुष्टि करें',
      langLabel: 'पसंदीदा भाषा',
      resetTokenLabel: 'रीसेट टोकन',
      newPasswordLabel: 'नया पासवर्ड',
      signInBtn: 'लॉगिन करें',
      signUpBtn: 'खाता बनाएं (साइन अप)',
      sendResetBtn: 'रीसेट कोड प्राप्त करें',
      applyResetBtn: 'पासवर्ड बदलें',
      forgotLink: 'पासवर्ड भूल गए?',
      haveAccount: 'पहले से खाता है? लॉगिन करें',
      noAccount: 'खाता नहीं है? नया खाता बनाएं',
      backToLogin: '← लॉगिन पर वापस जाएं',
    },
    te: {
      signInTitle: 'రైతు ఖాతాలోకి లాగిన్ అవ్వండి',
      signUpTitle: 'కొత్త రైతు ఖాతాను సృష్టించండి',
      forgotTitle: 'పాస్‌వర్డ్ రీసెట్ చేయండి',
      nameLabel: 'పూర్తి పేరు',
      emailLabel: 'ఈమెయిల్ చిరునామా',
      phoneLabel: 'మొబైల్ సంఖ్య (ఐచ్ఛికం)',
      passwordLabel: 'పాస్‌వర్డ్',
      confirmPasswordLabel: 'పాస్‌వర్డ్ ధృవీకరించండి',
      langLabel: 'ప్రాధాన్య భాష',
      resetTokenLabel: 'రీసెట్ కోడ్',
      newPasswordLabel: 'కొత్త పాస్‌వర్డ్',
      signInBtn: 'లాగిన్ అవ్వండి',
      signUpBtn: 'ఖాతా సృష్టించండి',
      sendResetBtn: 'రీసెట్ కోడ్ పొందండి',
      applyResetBtn: 'పాస్‌వర్డ్ మార్చండి',
      forgotLink: 'పాస్‌వర్డ్ మర్చిపోయారా?',
      haveAccount: 'ఇప్పటికే ఖాతా ఉందా? లాగిన్ అవ్వండి',
      noAccount: 'ఖాతా లేదా? కొత్త ఖాతా తెరవండి',
      backToLogin: '← లాగిన్‌కు తిరిగి వెళ్లండి',
    },
    en: {
      signInTitle: 'Sign In to KrishiRakshak',
      signUpTitle: 'Create Farmer Account',
      forgotTitle: 'Reset Password',
      nameLabel: 'Full Name',
      emailLabel: 'Email Address',
      phoneLabel: 'Phone Number (Optional)',
      passwordLabel: 'Password',
      confirmPasswordLabel: 'Confirm Password',
      langLabel: 'Preferred Language',
      resetTokenLabel: 'Reset Token / Code',
      newPasswordLabel: 'New Password',
      signInBtn: 'Sign In',
      signUpBtn: 'Create Account',
      sendResetBtn: 'Get Reset Code',
      applyResetBtn: 'Reset Password',
      forgotLink: 'Forgot password?',
      haveAccount: 'Already have an account? Sign In',
      noAccount: "Don't have an account? Sign Up Free",
      backToLogin: '← Back to Sign In',
    },
  };

  const t = content[currentLanguage] || content.en;

  const validateEmail = (val: string) => {
    return /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/.test(val.trim());
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setSuccessMsg(null);

    // Validation
    if (!validateEmail(email)) {
      setErrorMsg('Please enter a valid email address (e.g., farmer@example.com).');
      return;
    }

    if (mode === 'signup') {
      if (!name.trim() || name.trim().length < 2) {
        setErrorMsg('Please enter your full name (at least 2 characters).');
        return;
      }
      if (password.length < 6) {
        setErrorMsg('Password must be at least 6 characters long.');
        return;
      }
      if (password !== confirmPassword) {
        setErrorMsg('Passwords do not match. Please re-enter.');
        return;
      }

      setLoading(true);
      try {
        const resp = await apiClient.signup({
          name: name.trim(),
          email: email.trim().toLowerCase(),
          phone: phone.trim() || undefined,
          password,
          preferred_language: preferredLang,
        });
        setSuccessMsg(resp.message || 'Account created successfully!');
        setTimeout(() => onAuthSuccess(resp.user), 600);
      } catch (err: any) {
        setErrorMsg(err.message || 'Signup failed. Please try again.');
      } finally {
        setLoading(false);
      }
    } else if (mode === 'login') {
      if (!password) {
        setErrorMsg('Please enter your password.');
        return;
      }

      setLoading(true);
      try {
        const resp = await apiClient.login({
          email: email.trim().toLowerCase(),
          password,
        });
        setSuccessMsg('Logged in successfully!');
        setTimeout(() => onAuthSuccess(resp.user), 400);
      } catch (err: any) {
        setErrorMsg(err.message || 'Invalid email or password.');
      } finally {
        setLoading(false);
      }
    } else if (mode === 'forgot_password') {
      if (forgotStep === 'request') {
        setLoading(true);
        try {
          const resp = await apiClient.forgotPassword(email.trim().toLowerCase());
          if (resp.reset_token) {
            setResetToken(resp.reset_token);
            setSuccessMsg(`Reset token generated: ${resp.reset_token}. Please enter your new password below.`);
          } else {
            setSuccessMsg(resp.message);
          }
          setForgotStep('reset');
        } catch (err: any) {
          setErrorMsg(err.message || 'Could not process password reset.');
        } finally {
          setLoading(false);
        }
      } else {
        if (!resetToken.trim()) {
          setErrorMsg('Please enter the reset token.');
          return;
        }
        if (password.length < 6) {
          setErrorMsg('New password must be at least 6 characters.');
          return;
        }

        setLoading(true);
        try {
          const resp = await apiClient.resetPassword({
            email: email.trim().toLowerCase(),
            token: resetToken.trim(),
            new_password: password,
          });
          setSuccessMsg(resp.message + ' Redirecting to login...');
          setTimeout(() => {
            setMode('login');
            setForgotStep('request');
            setPassword('');
            setSuccessMsg(null);
          }, 1500);
        } catch (err: any) {
          setErrorMsg(err.message || 'Failed to update password.');
        } finally {
          setLoading(false);
        }
      }
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="auth-modal-card" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close-btn" onClick={onClose} aria-label="Close">
          <X size={20} />
        </button>

        {/* Modal Header */}
        <div className="auth-modal-header">
          <div className="auth-icon-badge">🌾</div>
          <h3 className="auth-title">
            {mode === 'login' && t.signInTitle}
            {mode === 'signup' && t.signUpTitle}
            {mode === 'forgot_password' && t.forgotTitle}
          </h3>
          <p className="auth-subtitle">
            {mode === 'login' && 'Sign in to access your crop doctor diagnosis, goals, and weather alerts.'}
            {mode === 'signup' && 'Join thousands of farmers protecting their crops with autonomous AI.'}
            {mode === 'forgot_password' && 'Enter your email to verify and reset your account password.'}
          </p>
        </div>

        {/* Mode Switcher Tabs */}
        {mode !== 'forgot_password' && (
          <div className="auth-tabs">
            <button
              type="button"
              className={`auth-tab-btn ${mode === 'login' ? 'active' : ''}`}
              onClick={() => {
                setMode('login');
                setErrorMsg(null);
                setSuccessMsg(null);
              }}
            >
              {t.signInBtn}
            </button>
            <button
              type="button"
              className={`auth-tab-btn ${mode === 'signup' ? 'active' : ''}`}
              onClick={() => {
                setMode('signup');
                setErrorMsg(null);
                setSuccessMsg(null);
              }}
            >
              {t.signUpBtn}
            </button>
          </div>
        )}

        {/* Notification Banners */}
        {errorMsg && (
          <div className="auth-alert error">
            <AlertCircle size={18} />
            <span>{errorMsg}</span>
          </div>
        )}
        {successMsg && (
          <div className="auth-alert success">
            <CheckCircle2 size={18} />
            <span>{successMsg}</span>
          </div>
        )}

        {/* Form Body */}
        <form onSubmit={handleSubmit} className="auth-form">
          {mode === 'signup' && (
            <>
              <div className="form-group">
                <label>{t.nameLabel} *</label>
                <div className="input-with-icon">
                  <User size={18} className="field-icon" />
                  <input
                    type="text"
                    required
                    placeholder="e.g. Ramesh Gowda"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                  />
                </div>
              </div>

              <div className="form-group">
                <label>{t.phoneLabel}</label>
                <div className="input-with-icon">
                  <Phone size={18} className="field-icon" />
                  <input
                    type="tel"
                    placeholder="+91 98765 43210"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                  />
                </div>
              </div>

              <div className="form-group">
                <label>{t.langLabel}</label>
                <select
                  value={preferredLang}
                  onChange={(e) => setPreferredLang(e.target.value as Language)}
                  className="auth-select"
                >
                  <option value="kn">ಕನ್ನಡ (Kannada)</option>
                  <option value="hi">हिन्दी (Hindi)</option>
                  <option value="te">తెలుగు (Telugu)</option>
                  <option value="en">English</option>
                </select>
              </div>
            </>
          )}

          <div className="form-group">
            <label>{t.emailLabel} *</label>
            <div className="input-with-icon">
              <Mail size={18} className="field-icon" />
              <input
                type="email"
                required
                placeholder="farmer@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={mode === 'forgot_password' && forgotStep === 'reset'}
              />
            </div>
          </div>

          {mode === 'forgot_password' && forgotStep === 'reset' && (
            <div className="form-group">
              <label>{t.resetTokenLabel} *</label>
              <input
                type="text"
                required
                placeholder="Enter reset code"
                value={resetToken}
                onChange={(e) => setResetToken(e.target.value)}
              />
            </div>
          )}

          {(mode === 'login' || mode === 'signup' || (mode === 'forgot_password' && forgotStep === 'reset')) && (
            <div className="form-group">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <label>
                  {mode === 'forgot_password' ? t.newPasswordLabel : t.passwordLabel} *
                </label>
                {mode === 'login' && (
                  <button
                    type="button"
                    className="link-btn"
                    onClick={() => {
                      setMode('forgot_password');
                      setForgotStep('request');
                      setErrorMsg(null);
                      setSuccessMsg(null);
                    }}
                  >
                    {t.forgotLink}
                  </button>
                )}
              </div>
              <div className="input-with-icon">
                <Lock size={18} className="field-icon" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  required
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <button
                  type="button"
                  className="eye-toggle-btn"
                  onClick={() => setShowPassword(!showPassword)}
                  tabIndex={-1}
                >
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>
          )}

          {mode === 'signup' && (
            <div className="form-group">
              <label>{t.confirmPasswordLabel} *</label>
              <div className="input-with-icon">
                <Lock size={18} className="field-icon" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  required
                  placeholder="••••••••"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                />
              </div>
            </div>
          )}

          <button type="submit" className="btn-primary auth-submit-btn" disabled={loading}>
            {loading ? 'Processing...' : (
              <>
                {mode === 'login' && t.signInBtn}
                {mode === 'signup' && t.signUpBtn}
                {mode === 'forgot_password' && (forgotStep === 'request' ? t.sendResetBtn : t.applyResetBtn)}
                <ArrowRight size={16} />
              </>
            )}
          </button>
        </form>

        {/* Footer links */}
        <div className="auth-modal-footer">
          {mode === 'login' && (
            <p>
              {t.noAccount}{' '}
              <button
                type="button"
                className="link-btn bold"
                onClick={() => {
                  setMode('signup');
                  setErrorMsg(null);
                  setSuccessMsg(null);
                }}
              >
                Sign Up
              </button>
            </p>
          )}

          {mode === 'signup' && (
            <p>
              {t.haveAccount}{' '}
              <button
                type="button"
                className="link-btn bold"
                onClick={() => {
                  setMode('login');
                  setErrorMsg(null);
                  setSuccessMsg(null);
                }}
              >
                Sign In
              </button>
            </p>
          )}

          {mode === 'forgot_password' && (
            <button
              type="button"
              className="link-btn"
              onClick={() => {
                setMode('login');
                setErrorMsg(null);
                setSuccessMsg(null);
              }}
            >
              {t.backToLogin}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

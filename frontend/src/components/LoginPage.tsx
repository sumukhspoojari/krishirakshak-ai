import React, { useState } from 'react';
import type { Language, UserProfile } from '../types';
import { apiClient } from '../services/api';
import {
  Sprout,
  Mail,
  Lock,
  Eye,
  EyeOff,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
  AlertCircle,
  Home,
  Sparkles
} from 'lucide-react';

interface LoginPageProps {
  currentLanguage: Language;
  onNavigate: (path: string) => void;
  onLoginSuccess: (user: UserProfile) => void;
}

export const LoginPage: React.FC<LoginPageProps> = ({
  currentLanguage: _lang,
  onNavigate,
  onLoginSuccess,
}) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  // Forgot password state
  const [forgotMode, setForgotMode] = useState(false);
  const [forgotEmail, setForgotEmail] = useState('');
  const [resetToken, setResetToken] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [forgotStep, setForgotStep] = useState<1 | 2>(1);
  const [forgotSuccess, setForgotSuccess] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage('');

    if (!email.trim() || !password) {
      setErrorMessage('Please enter both your email and password.');
      return;
    }

    setLoading(true);
    try {
      const resp = await apiClient.login({
        email: email.trim(),
        password,
      });

      if (!rememberMe) {
        // Optional session-only logic
      }

      onLoginSuccess(resp.user);
    } catch (err: any) {
      setErrorMessage(
        err?.response?.data?.detail ||
        err?.message ||
        'Invalid email or password. Please verify and try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleRequestReset = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage('');
    setForgotSuccess('');

    if (!forgotEmail.trim()) {
      setErrorMessage('Please enter your registered email address.');
      return;
    }

    setLoading(true);
    try {
      const resp = await apiClient.forgotPassword(forgotEmail.trim());
      setForgotSuccess(resp.message || 'Reset token generated successfully.');
      if (resp.reset_token) {
        setResetToken(resp.reset_token);
      }
      setForgotStep(2);
    } catch (err: any) {
      setErrorMessage(err?.response?.data?.detail || 'Failed to generate reset token.');
    } finally {
      setLoading(false);
    }
  };

  const handleApplyReset = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage('');
    setForgotSuccess('');

    if (!resetToken.trim() || !newPassword) {
      setErrorMessage('Please fill in both the reset token and your new password.');
      return;
    }

    setLoading(true);
    try {
      const resp = await apiClient.resetPassword({
        email: forgotEmail.trim(),
        token: resetToken.trim(),
        new_password: newPassword,
      });
      setForgotSuccess(resp.message || 'Password updated successfully! You can now log in.');
      setTimeout(() => {
        setForgotMode(false);
        setForgotStep(1);
        setEmail(forgotEmail);
      }, 1500);
    } catch (err: any) {
      setErrorMessage(err?.response?.data?.detail || 'Failed to update password.');
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
              <Sparkles className="w-4 h-4 text-emerald-300 mr-2 inline" /> Verified Farmer Portal
            </div>

            <h2 className="sidebar-heading">Welcome Back to Your Digital Agronomist</h2>
            <p className="sidebar-subtext">
              Log in to track your crop health goals, get instant AI pest diagnosis, and receive agro-weather warnings.
            </p>

            <div className="sidebar-benefits">
              <div className="benefit-item">
                <CheckCircle2 className="w-5 h-5 text-emerald-400 mr-3 flex-shrink-0" />
                <span>Instant leaf disease identification & recovery tracker</span>
              </div>
              <div className="benefit-item">
                <CheckCircle2 className="w-5 h-5 text-emerald-400 mr-3 flex-shrink-0" />
                <span>Multilingual support in Kannada, Hindi, Telugu, Tamil & English</span>
              </div>
              <div className="benefit-item">
                <CheckCircle2 className="w-5 h-5 text-emerald-400 mr-3 flex-shrink-0" />
                <span>Govt scheme advisories (PM-KISAN, PMFBY) tailored to your land</span>
              </div>
            </div>

            <div className="sidebar-footer">
              <ShieldCheck className="w-4 h-4 text-emerald-300 mr-2 inline" />
              <span>Data encrypted & securely stored in SQLite</span>
            </div>
          </div>

          {/* Right Form Side */}
          <div className="auth-card-form-container">
            {!forgotMode ? (
              <>
                <div className="form-header">
                  <h1 className="form-title">Farmer Sign In</h1>
                  <p className="form-subtitle">
                    Enter your credentials to access your farm dashboard.
                  </p>
                </div>

                {errorMessage && (
                  <div className="auth-alert error">
                    <AlertCircle className="w-5 h-5 mr-2 flex-shrink-0" />
                    <span>{errorMessage}</span>
                  </div>
                )}

                <form onSubmit={handleLogin} className="auth-form">
                  <div className="form-group">
                    <label className="form-label" htmlFor="login-email">Email Address</label>
                    <div className="input-with-icon">
                      <Mail className="input-icon" />
                      <input
                        id="login-email"
                        type="email"
                        required
                        className="form-input"
                        placeholder="farmer@example.com"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                      />
                    </div>
                  </div>

                  <div className="form-group">
                    <div className="form-label-row">
                      <label className="form-label" htmlFor="login-password">Password</label>
                      <button
                        type="button"
                        className="forgot-link"
                        onClick={() => {
                          setForgotMode(true);
                          setErrorMessage('');
                          setForgotEmail(email);
                        }}
                      >
                        Forgot password?
                      </button>
                    </div>
                    <div className="input-with-icon">
                      <Lock className="input-icon" />
                      <input
                        id="login-password"
                        type={showPassword ? 'text' : 'password'}
                        required
                        className="form-input"
                        placeholder="Enter your password"
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

                  <div className="remember-row">
                    <label className="remember-label">
                      <input
                        type="checkbox"
                        checked={rememberMe}
                        onChange={(e) => setRememberMe(e.target.checked)}
                      />
                      <span>Keep me signed in</span>
                    </label>
                  </div>

                  <button
                    type="submit"
                    disabled={loading}
                    className="btn-auth-primary"
                  >
                    {loading ? (
                      <span className="flex items-center justify-center">
                        <span className="spinner-sm mr-2"></span> Signing in...
                      </span>
                    ) : (
                      <span className="flex items-center justify-center">
                        Sign In to Dashboard <ArrowRight className="w-4 h-4 ml-2" />
                      </span>
                    )}
                  </button>

                  <div className="auth-switch-prompt">
                    <span>Don't have an account yet? </span>
                    <button
                      type="button"
                      className="link-switch-auth"
                      onClick={() => onNavigate('/signup')}
                    >
                      Create Account
                    </button>
                  </div>
                </form>
              </>
            ) : (
              /* Forgot Password View */
              <>
                <div className="form-header">
                  <h1 className="form-title">Reset Password</h1>
                  <p className="form-subtitle">
                    {forgotStep === 1
                      ? 'Enter your registered email to generate a recovery token.'
                      : 'Enter the recovery token and your new password.'}
                  </p>
                </div>

                {errorMessage && (
                  <div className="auth-alert error">
                    <AlertCircle className="w-5 h-5 mr-2 flex-shrink-0" />
                    <span>{errorMessage}</span>
                  </div>
                )}

                {forgotSuccess && (
                  <div className="auth-alert success">
                    <CheckCircle2 className="w-5 h-5 mr-2 flex-shrink-0" />
                    <span>{forgotSuccess}</span>
                  </div>
                )}

                {forgotStep === 1 ? (
                  <form onSubmit={handleRequestReset} className="auth-form">
                    <div className="form-group">
                      <label className="form-label" htmlFor="forgot-email">Registered Email Address</label>
                      <div className="input-with-icon">
                        <Mail className="input-icon" />
                        <input
                          id="forgot-email"
                          type="email"
                          required
                          className="form-input"
                          placeholder="farmer@example.com"
                          value={forgotEmail}
                          onChange={(e) => setForgotEmail(e.target.value)}
                        />
                      </div>
                    </div>

                    <button
                      type="submit"
                      disabled={loading}
                      className="btn-auth-primary"
                    >
                      {loading ? 'Generating Token...' : 'Get Reset Token'}
                    </button>

                    <button
                      type="button"
                      className="btn-auth-secondary"
                      onClick={() => setForgotMode(false)}
                    >
                      Back to Sign In
                    </button>
                  </form>
                ) : (
                  <form onSubmit={handleApplyReset} className="auth-form">
                    <div className="form-group">
                      <label className="form-label" htmlFor="reset-token">Reset Token</label>
                      <input
                        id="reset-token"
                        type="text"
                        required
                        className="form-input"
                        placeholder="Paste reset token here"
                        value={resetToken}
                        onChange={(e) => setResetToken(e.target.value)}
                      />
                    </div>

                    <div className="form-group">
                      <label className="form-label" htmlFor="reset-new-password">New Password</label>
                      <input
                        id="reset-new-password"
                        type="password"
                        required
                        minLength={6}
                        className="form-input"
                        placeholder="Minimum 6 characters"
                        value={newPassword}
                        onChange={(e) => setNewPassword(e.target.value)}
                      />
                    </div>

                    <button
                      type="submit"
                      disabled={loading}
                      className="btn-auth-primary"
                    >
                      {loading ? 'Updating Password...' : 'Save New Password & Sign In'}
                    </button>

                    <button
                      type="button"
                      className="btn-auth-secondary"
                      onClick={() => {
                        setForgotMode(false);
                        setForgotStep(1);
                      }}
                    >
                      Cancel
                    </button>
                  </form>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

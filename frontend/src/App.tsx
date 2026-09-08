import React, { useState, useEffect } from 'react';
import type { Language, FarmerGoal, UserProfile, AuthMode } from './types';
import { apiClient } from './services/api';
import { Navbar } from './components/Navbar';
import { HomeScreen } from './components/HomeScreen';
import { ChatScreen } from './components/ChatScreen';
import { FollowUpDashboard } from './components/FollowUpDashboard';
import { WeatherView } from './components/WeatherView';
import { SchemesView } from './components/SchemesView';
import { FollowUpModal } from './components/FollowUpModal';
import { LandingPage } from './components/LandingPage';
import { AuthModal } from './components/AuthModal';
import { LoginPage } from './components/LoginPage';
import { SignupPage } from './components/SignupPage';
import { ProfileModal } from './components/ProfileModal';

export const App: React.FC = () => {
  const [currentUser, setCurrentUser] = useState<UserProfile | null>(apiClient.getUser());
  const [isDemoMode, setIsDemoMode] = useState<boolean>(false);
  const [authModalOpen, setAuthModalOpen] = useState<boolean>(false);
  const [authModalMode] = useState<AuthMode>('login');
  const [profileModalOpen, setProfileModalOpen] = useState<boolean>(false);

  // URL Path Routing
  const [currentPath, setCurrentPath] = useState<string>(window.location.pathname || '/');

  const [currentLanguage, setCurrentLanguage] = useState<Language>(
    currentUser?.preferred_language || 'kn'
  );
  const [activeTab, setActiveTab] = useState<string>('home');
  const [activeGoals, setActiveGoals] = useState<FarmerGoal[]>([]);
  const [selectedGoalId, setSelectedGoalId] = useState<string | undefined>(undefined);
  const [initialChatPrompt, setInitialChatPrompt] = useState<string | undefined>(undefined);
  const [initialSampleImage, setInitialSampleImage] = useState<string | undefined>(undefined);
  const [modalGoal, setModalGoal] = useState<FarmerGoal | null>(null);

  // Listen to browser forward/back buttons
  useEffect(() => {
    const handlePopState = () => {
      setCurrentPath(window.location.pathname || '/');
    };
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  const navigateTo = (path: string) => {
    window.history.pushState({}, '', path);
    setCurrentPath(path);
  };

  // Validate active session with backend on load
  useEffect(() => {
    if (apiClient.getToken()) {
      apiClient.getMe().then((user) => {
        setCurrentUser(user);
        if (user.preferred_language) {
          setCurrentLanguage(user.preferred_language);
        }
      }).catch((err) => {
        console.warn('Session check failed, reverting to unauthenticated state:', err);
        setCurrentUser(null);
      });
    }
  }, []);

  const loadGoals = async () => {
    try {
      const goals = await apiClient.getGoals();
      setActiveGoals(goals);
    } catch (err) {
      console.warn('Could not load goals from backend:', err);
    }
  };

  useEffect(() => {
    if (currentUser || isDemoMode) {
      loadGoals();
    }
  }, [activeTab, currentUser, isDemoMode]);

  const handleNavigate = (tab: string, prompt?: string, sampleImg?: string) => {
    if (prompt) setInitialChatPrompt(prompt);
    if (sampleImg) setInitialSampleImage(sampleImg);
    setActiveTab(tab);
  };

  const handleSelectGoal = (goal: FarmerGoal) => {
    setSelectedGoalId(goal.id);
    setCurrentLanguage(goal.language);
    setActiveTab('chat');
  };

  const handleResetSession = () => {
    setSelectedGoalId(undefined);
    setInitialChatPrompt(undefined);
    setInitialSampleImage(undefined);
    setActiveTab('home');
  };

  const handleOpenAuth = (mode: AuthMode) => {
    if (mode === 'signup') {
      navigateTo('/signup');
    } else {
      navigateTo('/login');
    }
  };

  const handleAuthSuccess = (user: UserProfile) => {
    setCurrentUser(user);
    setAuthModalOpen(false);
    setIsDemoMode(false);
    if (user.preferred_language) {
      setCurrentLanguage(user.preferred_language);
    }
    navigateTo('/');
    setActiveTab('home');
  };

  const handleLogout = async () => {
    await apiClient.logout();
    setCurrentUser(null);
    setIsDemoMode(false);
    setProfileModalOpen(false);
    navigateTo('/');
    setActiveTab('home');
  };

  const handleExploreDemo = () => {
    setIsDemoMode(true);
    navigateTo('/');
    setActiveTab('home');
  };

  // 1. Standalone Dedicated Login Page
  if (currentPath === '/login' && !currentUser) {
    return (
      <LoginPage
        currentLanguage={currentLanguage}
        onNavigate={navigateTo}
        onLoginSuccess={handleAuthSuccess}
      />
    );
  }

  // 2. Standalone Dedicated Signup Page
  if (currentPath === '/signup' && !currentUser) {
    return (
      <SignupPage
        currentLanguage={currentLanguage}
        onLanguageChange={(lang) => setCurrentLanguage(lang)}
        onNavigate={navigateTo}
        onSignupSuccess={handleAuthSuccess}
      />
    );
  }

  // 3. If unauthenticated and not in live demo mode, display the public Landing Page
  if (!currentUser && !isDemoMode) {
    return (
      <div className="app-container">
        <LandingPage
          currentLanguage={currentLanguage}
          onLanguageChange={(lang) => setCurrentLanguage(lang)}
          onOpenAuth={handleOpenAuth}
          onExploreDemo={handleExploreDemo}
        />

        {authModalOpen && (
          <AuthModal
            initialMode={authModalMode}
            currentLanguage={currentLanguage}
            onClose={() => setAuthModalOpen(false)}
            onAuthSuccess={handleAuthSuccess}
          />
        )}
      </div>
    );
  }

  // 4. Authenticated / Demo Mode Full App Dashboard
  return (
    <div className="app-container">
      {/* Navigation Header */}
      <Navbar
        currentLanguage={currentLanguage}
        onLanguageChange={(lang) => setCurrentLanguage(lang)}
        activeTab={activeTab}
        onTabChange={(tab) => {
          if (tab !== 'chat') {
            setInitialChatPrompt(undefined);
            setInitialSampleImage(undefined);
          }
          setActiveTab(tab);
        }}
        onResetSession={handleResetSession}
        currentUser={currentUser}
        onLogout={handleLogout}
        onOpenAuth={handleOpenAuth}
        onOpenProfile={() => setProfileModalOpen(true)}
      />

      {/* Main Views */}
      <main style={{ flex: 1 }}>
        {activeTab === 'home' && (
          <HomeScreen
            currentLanguage={currentLanguage}
            onNavigate={handleNavigate}
            activeGoals={activeGoals}
            onSelectGoal={handleSelectGoal}
            onOpenFollowUpModal={(goal) => setModalGoal(goal)}
          />
        )}

        {activeTab === 'chat' && (
          <ChatScreen
            currentLanguage={currentLanguage}
            onLanguageChange={(lang) => setCurrentLanguage(lang)}
            activeGoalId={selectedGoalId}
            initialPrompt={initialChatPrompt}
            initialSampleImage={initialSampleImage}
            onGoalUpdated={() => loadGoals()}
          />
        )}

        {activeTab === 'followup' && (
          <FollowUpDashboard
            currentLanguage={currentLanguage}
            goals={activeGoals}
            onSelectGoal={handleSelectGoal}
            onOpenFollowUpModal={(goal) => setModalGoal(goal)}
            onNewGoalClick={handleResetSession}
          />
        )}

        {activeTab === 'weather' && (
          <WeatherView currentLanguage={currentLanguage} />
        )}

        {activeTab === 'schemes' && (
          <SchemesView currentLanguage={currentLanguage} />
        )}
      </main>

      {/* Follow-up submission modal */}
      {modalGoal && (
        <FollowUpModal
          goal={modalGoal}
          currentLanguage={currentLanguage}
          onClose={() => setModalGoal(null)}
          onSuccess={() => {
            setModalGoal(null);
            loadGoals();
          }}
        />
      )}

      {/* Farmer Profile & Stored Details Modal */}
      {profileModalOpen && currentUser && (
        <ProfileModal
          user={currentUser}
          onClose={() => setProfileModalOpen(false)}
          onLogout={handleLogout}
        />
      )}
    </div>
  );
};

export default App;

import type { FarmerGoal, WeatherInfo, SchemeInfo, FollowUpSubmitResponse, UserProfile, AuthResponse } from '../types';

const API_BASE = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/+$/, '');

export const apiClient = {
  resolveImageUrl(path?: string | null): string {
    if (!path) return '';
    if (path.startsWith('http://') || path.startsWith('https://') || path.startsWith('data:')) {
      return path;
    }
    const cleanPath = path.startsWith('/') ? path : `/${path}`;
    return `${API_BASE}${cleanPath}`;
  },

  getToken(): string | null {
    return localStorage.getItem('krishiai_token');
  },

  setToken(token: string | null) {
    if (token) {
      localStorage.setItem('krishiai_token', token);
    } else {
      localStorage.removeItem('krishiai_token');
    }
  },

  getUser(): UserProfile | null {
    const raw = localStorage.getItem('krishiai_user');
    if (!raw) return null;
    try {
      return JSON.parse(raw);
    } catch {
      return null;
    }
  },

  setUser(user: UserProfile | null) {
    if (user) {
      localStorage.setItem('krishiai_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('krishiai_user');
    }
  },

  getAuthHeaders(): Record<string, string> {
    const token = this.getToken();
    return token ? { Authorization: `Bearer ${token}` } : {};
  },

  async signup(payload: {
    name: string;
    email: string;
    phone?: string;
    password: string;
    preferred_language?: string;
  }): Promise<AuthResponse> {
    const res = await fetch(`${API_BASE}/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || 'Signup failed. Please try again.');
    }
    this.setToken(data.token);
    this.setUser(data.user);
    return data;
  },

  async login(payload: { email: string; password: string }): Promise<AuthResponse> {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || 'Invalid email or password.');
    }
    this.setToken(data.token);
    this.setUser(data.user);
    return data;
  },

  async getMe(): Promise<UserProfile> {
    const res = await fetch(`${API_BASE}/auth/me`, {
      headers: {
        'Content-Type': 'application/json',
        ...this.getAuthHeaders(),
      },
    });
    if (!res.ok) {
      this.logout();
      throw new Error('Session expired. Please log in again.');
    }
    const user = await res.json();
    this.setUser(user);
    return user;
  },

  async logout(): Promise<void> {
    try {
      await fetch(`${API_BASE}/auth/logout`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
      });
    } catch {
      // Ignore network failures on logout
    } finally {
      this.setToken(null);
      this.setUser(null);
    }
  },

  async forgotPassword(email: string): Promise<{ status: string; message: string; reset_token?: string }> {
    const res = await fetch(`${API_BASE}/auth/forgot-password`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Password reset request failed.');
    return data;
  },

  async resetPassword(payload: { email: string; token: string; new_password: string }): Promise<{ status: string; message: string }> {
    const res = await fetch(`${API_BASE}/auth/reset-password`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Failed to reset password.');
    return data;
  },

  async chat(payload: {
    message: string;
    language?: string;
    image_url?: string;
    goal_id?: string;
    user_id?: string;
  }) {
    const user = this.getUser();
    const bodyPayload = {
      ...payload,
      user_id: payload.user_id || (user ? user.id : undefined),
      language: payload.language || (user ? user.preferred_language : 'kn'),
    };
    const res = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...this.getAuthHeaders(),
      },
      body: JSON.stringify(bodyPayload),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || `Chat error: ${res.statusText}`);
    return data;
  },

  async getGoals(): Promise<FarmerGoal[]> {
    const user = this.getUser();
    const url = user ? `${API_BASE}/goals?user_id=${encodeURIComponent(user.id)}` : `${API_BASE}/goals`;
    const res = await fetch(url, {
      headers: this.getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch goals');
    return res.json();
  },

  async getGoalById(id: string): Promise<FarmerGoal> {
    const res = await fetch(`${API_BASE}/goal/${id}`, {
      headers: this.getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch goal details');
    return res.json();
  },

  async submitFollowUp(payload: {
    goal_id: string;
    farmer_response: string;
    new_image_url?: string;
    condition_assessment?: string;
    language?: string;
  }): Promise<FollowUpSubmitResponse> {
    const res = await fetch(`${API_BASE}/goal/${payload.goal_id}/follow-up`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...this.getAuthHeaders(),
      },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Failed to submit follow-up');
    return data;
  },

  async uploadImage(file: File): Promise<{ image_url: string; filename: string }> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}/upload-image`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: formData,
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || 'Image upload failed. Allowed formats: JPG, PNG, WebP (Max 10MB).');
    }
    return data;
  },

  async getWeather(location: string = 'Mandya, Karnataka'): Promise<WeatherInfo> {
    const res = await fetch(`${API_BASE}/weather?location=${encodeURIComponent(location)}`, {
      headers: this.getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch weather');
    return res.json();
  },

  async getSchemes(): Promise<SchemeInfo[]> {
    const res = await fetch(`${API_BASE}/schemes`, {
      headers: this.getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch schemes');
    return res.json();
  },

  async getDashboard() {
    const res = await fetch(`${API_BASE}/dashboard`, {
      headers: this.getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch dashboard');
    return res.json();
  },
};

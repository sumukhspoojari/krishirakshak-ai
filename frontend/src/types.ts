export type Language = 'kn' | 'hi' | 'te' | 'en';

export interface AgentActivityStep {
  step_id: string;
  label: string;
  status: 'pending' | 'active' | 'completed' | 'failed';
  details?: string;
}

export interface PossibleCause {
  cause: string;
  probability: 'High' | 'Medium' | 'Low';
  confidence_score: number;
  symptoms_matched: string[];
  explanation: string;
}

export interface ActionPlan {
  id?: string;
  goal_id?: string;
  immediate_actions: string[];
  short_term_actions: string[];
  monitoring_actions: string[];
  escalation_conditions: string[];
  localized_summary?: string;
}

export interface ChatMessage {
  id: string;
  sender: 'farmer' | 'agent';
  text: string;
  image_url?: string;
  audio_url?: string;
  activity_steps?: AgentActivityStep[];
  action_plan?: ActionPlan;
  possible_causes?: PossibleCause[];
  timestamp: string;
  goal_id?: string;
  goal_status?: string;
  goal_defined?: string;
}

export interface FarmerGoal {
  id: string;
  user_id: string;
  crop: string;
  problem: string;
  goal: string;
  urgency: string;
  status: 'Investigating' | 'Action Plan Active' | 'Monitoring' | 'Improving' | 'Needs Attention' | 'Completed';
  language: Language;
  created_at: string;
  updated_at: string;
  latest_image_url?: string;
  action_plan?: ActionPlan;
  next_follow_up_date?: string;
  possible_causes?: PossibleCause[];
}

export interface WeatherInfo {
  location: string;
  temperature: number;
  humidity: number;
  rainfall_mm: number;
  wind_kmh: number;
  condition: string;
  fungal_disease_risk: 'Low' | 'Moderate' | 'High';
  pest_activity_risk: 'Low' | 'Moderate' | 'High';
  can_spray: boolean;
  spray_advisory: string;
  advisory: string;
  forecast_3days: Array<{
    day: string;
    temp: string;
    humidity: string;
    rain_chance: string;
  }>;
}

export interface SchemeInfo {
  id: string;
  name: string;
  name_kn: string;
  name_hi: string;
  name_te: string;
  category: string;
  eligibility: string;
  benefits: string;
  how_to_apply: string;
  official_link: string;
}

export interface FollowUpSubmitResponse {
  goal_id: string;
  status: string;
  observation_result: 'Improving' | 'Stable' | 'Worsening';
  response_text: string;
  updated_action_plan?: ActionPlan;
  comparison_details: {
    comparison_result: string;
    recovery_index: number;
    chlorosis_delta: string;
    canopy_delta: string;
    analysis_summary: string;
    recommended_next_step: string;
  };
  prevention_guidance?: string;
  expert_escalation_recommended: boolean;
  expert_contacts: Array<{
    name: string;
    number?: string;
    phone?: string;
    timings?: string;
    address?: string;
    type?: string;
  }>;
}

export interface UserProfile {
  id: string;
  name: string;
  email?: string;
  phone?: string;
  preferred_language: Language;
  created_at?: string;
}

export interface AuthResponse {
  token: string;
  user: UserProfile;
  message: string;
}

export type AuthMode = 'login' | 'signup' | 'forgot_password';

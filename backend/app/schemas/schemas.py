from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class AgentActivityStep(BaseModel):
    step_id: str
    label: str
    status: str = "completed"  # 'pending', 'active', 'completed', 'failed'
    details: Optional[str] = None

class PossibleCause(BaseModel):
    cause: str
    probability: str  # 'High', 'Medium', 'Low'
    confidence_score: float  # 0.0 - 1.0
    symptoms_matched: List[str] = []
    explanation: str

class ActionPlanSchema(BaseModel):
    id: Optional[str] = None
    goal_id: Optional[str] = None
    immediate_actions: List[str] = []
    short_term_actions: List[str] = []
    monitoring_actions: List[str] = []
    escalation_conditions: List[str] = []
    localized_summary: Optional[str] = None

class ChatRequest(BaseModel):
    user_id: Optional[str] = None
    conversation_id: Optional[str] = None
    message: str = ""
    language: Optional[str] = None  # 'kn', 'hi', 'te', 'en' or auto-detect
    image_url: Optional[str] = None
    audio_base64: Optional[str] = None
    goal_id: Optional[str] = None

class ChatResponse(BaseModel):
    user_id: str
    conversation_id: str
    goal_id: Optional[str] = None
    detected_language: str
    response_text: str
    audio_url: Optional[str] = None
    agent_activity_steps: List[AgentActivityStep] = []
    goal_defined: Optional[str] = None
    goal_status: str = "Investigating"
    missing_information: List[str] = []
    possible_causes: List[PossibleCause] = []
    action_plan: Optional[ActionPlanSchema] = None
    next_follow_up_date: Optional[str] = None
    urgency: str = "Medium"

class GoalSummaryResponse(BaseModel):
    id: str
    user_id: str
    crop: str
    problem: str
    goal: str
    urgency: str
    status: str
    language: str
    created_at: datetime
    updated_at: datetime
    latest_image_url: Optional[str] = None
    action_plan: Optional[ActionPlanSchema] = None
    next_follow_up_date: Optional[str] = None
    possible_causes: List[PossibleCause] = []

class FollowUpSubmitRequest(BaseModel):
    goal_id: str
    farmer_response: str
    new_image_url: Optional[str] = None
    condition_assessment: Optional[str] = None  # 'improving', 'stable', 'worsening'
    language: Optional[str] = None

class FollowUpSubmitResponse(BaseModel):
    goal_id: str
    status: str
    observation_result: str  # 'Improving', 'Stable', 'Worsening'
    response_text: str
    updated_action_plan: Optional[ActionPlanSchema] = None
    comparison_details: Dict[str, Any] = {}
    prevention_guidance: Optional[str] = None
    expert_escalation_recommended: bool = False
    expert_contacts: List[Dict[str, str]] = []

class WeatherInfoResponse(BaseModel):
    location: str
    temperature: float
    humidity: int
    rainfall_mm: float
    wind_kmh: float
    condition: str
    forecast_3days: List[Dict[str, Any]] = []
    fungal_disease_risk: str  # 'Low', 'Moderate', 'High'
    pest_activity_risk: str
    advisory: str

class SchemeInfoResponse(BaseModel):
    id: str
    name: str
    name_kn: str
    name_hi: str
    name_te: str
    category: str
    eligibility: str
    benefits: str
    how_to_apply: str
    official_link: str

class DashboardDataResponse(BaseModel):
    active_goals_count: int
    resolved_goals_count: int
    recent_goals: List[GoalSummaryResponse]
    weather_summary: WeatherInfoResponse
    top_schemes: List[SchemeInfoResponse]


# --- Authentication Schemas ---

class UserSignupRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    phone: Optional[str] = Field(None, max_length=20)
    password: str = Field(..., min_length=6, max_length=100)
    preferred_language: Optional[str] = "kn"

class UserLoginRequest(BaseModel):
    email: str = Field(..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    password: str = Field(..., min_length=1)

class ForgotPasswordRequest(BaseModel):
    email: str = Field(..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

class ResetPasswordRequest(BaseModel):
    email: str = Field(..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    token: str
    new_password: str = Field(..., min_length=6)

class UserProfileResponse(BaseModel):
    id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    preferred_language: str
    created_at: datetime

class AuthResponse(BaseModel):
    token: str
    user: UserProfileResponse
    message: str = "Success"

from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict, total=False):
    # Context & Identifiers
    user_id: str
    conversation_id: str
    goal_id: Optional[str]
    current_language: str  # 'kn', 'hi', 'te', 'en'
    
    # Farmer Problem & Goal
    farmer_problem: str
    farmer_goal: str
    intent: Optional[str]
    urgency: str  # 'Low', 'Medium', 'High', 'Severe'
    crop: str
    symptoms: List[str]
    
    # Information Completeness
    available_information: Dict[str, Any]
    missing_information: List[str]
    is_information_sufficient: bool
    targeted_question: Optional[str]
    
    # Visual & Environmental Inputs
    image_url: Optional[str]
    image_analysis_result: Optional[Dict[str, Any]]
    weather_info: Optional[Dict[str, Any]]
    
    # Investigation & Tools
    investigation_plan: List[str]
    selected_tools: List[str]
    tool_results: Dict[str, Any]
    
    # Diagnosis & Confidence
    possible_causes: List[Dict[str, Any]]
    confidence_levels: Dict[str, float]
    overall_confidence: float
    confidence_sufficient: bool
    
    # Action Plan & Monitoring
    action_plan: Optional[Dict[str, Any]]
    follow_up_plan: Optional[Dict[str, Any]]
    follow_up_status: str  # 'Pending', 'Scheduled', 'Improving', 'Stable', 'Worsening', 'Completed'
    goal_status: str  # 'Investigating', 'Action Plan Active', 'Monitoring', 'Improving', 'Needs Attention', 'Completed'
    
    # UI Activity Progress
    agent_activity_steps: List[Dict[str, str]]
    final_response_text: str
    prevention_guidance: Optional[str]
    expert_escalation_recommended: bool

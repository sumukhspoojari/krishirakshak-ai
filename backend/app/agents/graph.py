from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.services.multilingual import MultilingualService
from app.agents.specialized import (
    ConversationalAgent,
    GoalUnderstandingAgent,
    InvestigationAgent,
    CropDiagnosisAgent,
    WeatherRiskAgent,
    ActionPlanningAgent,
    GovtAssistanceAgent,
    FollowUpAgent,
)
from app.tools.crop_image_analyzer import crop_image_analyzer
from app.tools.weather_service import weather_tool
from app.tools.disease_db import disease_database_tool
from app.tools.agri_knowledge import agri_knowledge_tool
from app.tools.follow_up_planner import follow_up_planner_tool

# --- LangGraph Node Functions ---

def understand_problem_node(state: AgentState) -> Dict[str, Any]:
    problem = state.get("farmer_problem", "")
    preferred_lang = state.get("current_language")
    has_image = bool(state.get("image_url"))

    result = GoalUnderstandingAgent.process(problem, preferred_lang, has_image)
    
    activity = state.get("agent_activity_steps", [])
    activity.append({
        "step_id": "understanding",
        "label": MultilingualService.get_activity_label("understanding", result["language"]),
        "status": "completed"
    })

    return {
        "current_language": result["language"],
        "crop": result["crop"],
        "symptoms": result["symptoms"],
        "urgency": result["urgency"],
        "farmer_goal": result["farmer_goal"],
        "missing_information": result["missing_info"],
        "is_information_sufficient": result["is_sufficient"],
        "intent": result.get("intent", "crop_problem"),
        "agent_activity_steps": activity,
    }


def check_information_node(state: AgentState) -> Dict[str, Any]:
    # Evaluate if we need to pause and ask a targeted question
    is_sufficient = state.get("is_information_sufficient", False)
    missing = state.get("missing_information", [])
    lang = state.get("current_language", "kn")

    if not is_sufficient and "crop_leaf_image" in missing and not state.get("image_url"):
        question = InvestigationAgent.get_targeted_question(missing, lang)
        return {
            "targeted_question": question,
            "final_response_text": question,
            "goal_status": "Investigating"
        }
    return {}


def create_investigation_plan_node(state: AgentState) -> Dict[str, Any]:
    crop = state.get("crop", "chilli")
    symptoms = state.get("symptoms", [])
    has_image = bool(state.get("image_url"))
    lang = state.get("current_language", "kn")

    selected_tools = InvestigationAgent.select_tools(crop, symptoms, has_image)
    plan = [
        f"Inspect crop symptoms for {crop}",
        "Analyze high-resolution image features" if has_image else "Review reported symptom markers",
        "Check local weather risks (humidity/temperature/rainfall)",
        "Query verified agricultural disease database",
        "Formulate multi-step recovery action plan"
    ]

    activity = state.get("agent_activity_steps", [])
    activity.append({
        "step_id": "checking_crop",
        "label": MultilingualService.get_activity_label("checking_crop", lang),
        "status": "completed"
    })

    return {
        "investigation_plan": plan,
        "selected_tools": selected_tools,
        "agent_activity_steps": activity
    }


def execute_tools_node(state: AgentState) -> Dict[str, Any]:
    tools = state.get("selected_tools", [])
    image_url = state.get("image_url")
    crop = state.get("crop", "chilli")
    symptoms = state.get("symptoms", [])
    lang = state.get("current_language", "kn")
    tool_results = {}
    activity = state.get("agent_activity_steps", [])

    # 1. analyze_crop_image if tool selected
    if "analyze_crop_image" in tools and image_url:
        img_res = crop_image_analyzer.analyze_crop_image(image_url, crop)
        tool_results["analyze_crop_image"] = img_res
        activity.append({
            "step_id": "analyzing_image",
            "label": MultilingualService.get_activity_label("analyzing_image", lang),
            "status": "completed"
        })

    # 2. get_weather
    if "get_weather" in tools:
        w_res = weather_tool.get_weather()
        tool_results["get_weather"] = w_res
        activity.append({
            "step_id": "checking_weather",
            "label": MultilingualService.get_activity_label("checking_weather", lang),
            "status": "completed"
        })

    # 3. search_crop_disease_database & agri_knowledge
    if "search_crop_disease_database" in tools:
        d_res = disease_database_tool.search(crop, symptoms)
        tool_results["search_crop_disease_database"] = d_res

    if "search_agriculture_knowledge_base" in tools:
        k_res = agri_knowledge_tool.search(f"{crop} {' '.join(symptoms)}")
        tool_results["search_agriculture_knowledge_base"] = k_res

    # 4. create_follow_up_plan
    if "create_follow_up_plan" in tools:
        f_res = follow_up_planner_tool.create_follow_up_plan(
            problem=" ".join(symptoms),
            actions=["Foliar spray", "Sticky traps"],
            timeline_days=3,
            crop=crop
        )
        tool_results["create_follow_up_plan"] = f_res

    return {
        "tool_results": tool_results,
        "image_analysis_result": tool_results.get("analyze_crop_image"),
        "weather_info": tool_results.get("get_weather"),
        "follow_up_plan": tool_results.get("create_follow_up_plan"),
        "agent_activity_steps": activity
    }


def evaluate_results_node(state: AgentState) -> Dict[str, Any]:
    crop = state.get("crop", "chilli")
    symptoms = state.get("symptoms", [])
    img_res = state.get("image_analysis_result")
    w_res = state.get("weather_info")

    possible_causes = CropDiagnosisAgent.diagnose(crop, symptoms, img_res, w_res)
    top_confidence = possible_causes[0]["confidence_score"] if possible_causes else 0.70

    return {
        "possible_causes": possible_causes,
        "overall_confidence": top_confidence,
        "confidence_sufficient": top_confidence >= 0.50
    }


def generate_action_plan_node(state: AgentState) -> Dict[str, Any]:
    crop = state.get("crop", "chilli")
    possible_causes = state.get("possible_causes", [{}])
    top_cause = possible_causes[0] if possible_causes else {}
    lang = state.get("current_language", "kn")
    w_res = state.get("weather_info")

    action_plan = ActionPlanningAgent.build_action_plan(crop, top_cause, lang, w_res)
    disclaimer = MultilingualService.get_disclaimer(lang)

    # Compose rich localized final response
    prob_text = top_cause.get("cause", "Crop Pest/Disease")
    prob_level = top_cause.get("probability", "High")
    conf = int(top_cause.get("confidence_score", 0.8) * 100)

    if lang == "kn":
        response_text = (
            f"ನಿಮ್ಮ ಸಮಸ್ಯೆಯನ್ನು ಕೂಲಂಕಷವಾಗಿ ವಿಶ್ಲೇಷಿಸಲಾಗಿದೆ.\n\n"
            f"🔍 ಸಂಭಾವ್ಯ ಕಾರಣ: {prob_text} ({prob_level} ಸಂಭವನೀಯತೆ - {conf}% ವಿಶ್ವಾಸಾರ್ಹತೆ)\n\n"
            f"📋 ಶಿಫಾರಸು ಮಾಡಿದ ತುರ್ತು ಕ್ರಮಗಳು:\n"
            f"1. {action_plan['immediate_actions'][0]}\n"
            f"2. {action_plan['immediate_actions'][1]}\n\n"
            f"🗓 3 ದಿನಗಳ ನಂತರ ನಿಮ್ಮ ಬೆಳೆಯ ಹೊಸ ಚಿಗುರನ್ನು ಪರಿಶೀಲಿಸಲು ಮತ್ತು ಫೋಟೋ ಹಂಚಿಕೊಳ್ಳಲು ಅನುಸರಣಾ ಯೋಜನೆಯನ್ನು ನಿಗದಿಪಡಿಸಲಾಗಿದೆ.\n\n"
            f"⚠️ {disclaimer}"
        )
    elif lang == "hi":
        response_text = (
            f"आपकी समस्या का गहन विश्लेषण किया गया है।\n\n"
            f"🔍 संभावित कारण: {prob_text} ({prob_level} संभावना - {conf}% विश्वास)\n\n"
            f"📋 अनुशंसित त्वरित कदम:\n"
            f"1. {action_plan['immediate_actions'][0]}\n"
            f"2. {action_plan['immediate_actions'][1]}\n\n"
            f"🗓 3 दिनों के बाद फसल की स्थिति की जांच के लिए फॉलो-अप तय किया गया है।\n\n"
            f"⚠️ {disclaimer}"
        )
    elif lang == "te":
        response_text = (
            f"మీ సమస్యను సమగ్రంగా విశ్లేషించాము.\n\n"
            f"🔍 సంభావ్య కారణం: {prob_text} ({prob_level} సంభావ్యత - {conf}% విశ్వసనీయత)\n\n"
            f"📋 తక్షణ చర్యలు:\n"
            f"1. {action_plan['immediate_actions'][0]}\n"
            f"2. {action_plan['immediate_actions'][1]}\n\n"
            f"🗓 3 రోజుల తర్వాత పంట పురోగతిని సమీక్షించడానికి ఫాలో-అప్ ప్రణాళిక సిద్ధం చేయబడింది.\n\n"
            f"⚠️ {disclaimer}"
        )
    else:
        response_text = (
            f"Your crop issue has been thoroughly investigated.\n\n"
            f"🔍 Probable Cause: {prob_text} ({prob_level} Probability - {conf}% Confidence)\n\n"
            f"📋 Recommended Immediate Steps:\n"
            f"1. {action_plan['immediate_actions'][0]}\n"
            f"2. {action_plan['immediate_actions'][1]}\n\n"
            f"🗓 A 3-day follow-up checkpoint has been scheduled to monitor your crop's recovery.\n\n"
            f"⚠️ {disclaimer}"
        )

    activity = state.get("agent_activity_steps", [])
    activity.append({
        "step_id": "preparing_plan",
        "label": MultilingualService.get_activity_label("preparing_plan", lang),
        "status": "completed"
    })

    return {
        "action_plan": action_plan,
        "final_response_text": response_text,
        "goal_status": "Action Plan Active",
        "agent_activity_steps": activity
    }


# Routing condition: is information sufficient to proceed?

def handle_conversational_node(state: AgentState) -> Dict[str, Any]:
    intent = state.get("intent", "greeting")
    lang = state.get("current_language", "kn")
    user_text = state.get("farmer_problem", "")

    response_text = ConversationalAgent.get_response(intent, lang, user_text)

    step_id = "agronomy_guidance" if intent == "agronomy_query" else "greeting_handled"
    goal_title = "Crop Cultivation & Agronomy Guidance" if intent == "agronomy_query" else "General Assistance & Query Resolution"

    activity = state.get("agent_activity_steps", [])
    activity.append({
        "step_id": step_id,
        "label": MultilingualService.get_activity_label(step_id, lang),
        "status": "completed"
    })

    return {
        "final_response_text": response_text,
        "goal_status": "Conversational",
        "farmer_goal": goal_title,
        "possible_causes": [],
        "action_plan": None,
        "agent_activity_steps": activity,
        "is_information_sufficient": True
    }


def should_continue(state: AgentState) -> Literal["handle_conversational", "ask_targeted_question", "create_investigation_plan"]:
    intent = state.get("intent", "crop_problem")
    if intent in ["greeting", "identity", "gratitude", "crops_supported", "general_inquiry", "agronomy_query"]:
        return "handle_conversational"

    is_sufficient = state.get("is_information_sufficient", False)
    if not is_sufficient:
        return "ask_targeted_question"
    return "create_investigation_plan"


# Build the LangGraph Workflow
def build_agent_graph():
    builder = StateGraph(AgentState)

    builder.add_node("understand_problem", understand_problem_node)
    builder.add_node("handle_conversational", handle_conversational_node)
    builder.add_node("ask_targeted_question", check_information_node)
    builder.add_node("create_investigation_plan", create_investigation_plan_node)
    builder.add_node("execute_tools", execute_tools_node)
    builder.add_node("evaluate_results", evaluate_results_node)
    builder.add_node("generate_action_plan", generate_action_plan_node)

    # Edges
    builder.set_entry_point("understand_problem")
    builder.add_conditional_edges(
        "understand_problem",
        should_continue,
        {
            "handle_conversational": "handle_conversational",
            "ask_targeted_question": "ask_targeted_question",
            "create_investigation_plan": "create_investigation_plan"
        }
    )
    builder.add_edge("handle_conversational", END)
    builder.add_edge("ask_targeted_question", END)
    builder.add_edge("create_investigation_plan", "execute_tools")
    builder.add_edge("execute_tools", "evaluate_results")
    builder.add_edge("evaluate_results", "generate_action_plan")
    builder.add_edge("generate_action_plan", END)

    return builder.compile()

agent_graph = build_agent_graph()

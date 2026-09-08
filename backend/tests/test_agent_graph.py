import pytest
from app.agents.graph import agent_graph
from app.services.multilingual import MultilingualService
from app.agents.specialized import FollowUpAgent

def test_multilingual_detection():
    # Kannada
    assert MultilingualService.detect_language("ನನ್ನ ಮೆಣಸಿನಕಾಯಿ ಗಿಡದ ಎಲೆಗಳು ಹಳದಿಯಾಗುತ್ತಿವೆ") == "kn"
    # Hindi
    assert MultilingualService.detect_language("मेरे टमाटर के पौधे सूख रहे हैं") == "hi"
    # Telugu
    assert MultilingualService.detect_language("నా వరి పంటలో ఆకులు ఎండిపోతున్నాయి") == "te"
    # English
    assert MultilingualService.detect_language("My chilli crop has yellow leaves") == "en"

def test_end_to_end_kannada_chilli_graph_execution():
    """
    Validates the core Section 19 scenario:
    Farmer: 'ನನ್ನ ಮೆಣಸಿನಕಾಯಿ ಗಿಡದ ಎಲೆಗಳು ಹಳದಿಯಾಗುತ್ತಿವೆ. ಸಹಾಯ ಮಾಡಿ.'
    With uploaded leaf image -> verifies LangGraph nodes execute, defines goal,
    runs tools, and generates action plan in Kannada.
    """
    initial_state = {
        "user_id": "test-farmer-01",
        "conversation_id": "conv-test-01",
        "farmer_problem": "ನನ್ನ ಮೆಣಸಿನಕಾಯಿ ಗಿಡದ ಎಲೆಗಳು ಹಳದಿಯಾಗುತ್ತಿವೆ. ಸಹಾಯ ಮಾಡಿ.",
        "image_url": "/uploads/sample_chilli_yellowing.jpg",
        "agent_activity_steps": []
    }

    output = agent_graph.invoke(initial_state)

    assert output["current_language"] == "kn"
    assert output["crop"] == "chilli"
    assert "yellowing" in output["symptoms"]
    assert "ಮೆಣಸಿನಕಾಯಿ" in output["farmer_goal"]
    assert len(output["agent_activity_steps"]) >= 4
    assert output["goal_status"] == "Action Plan Active"
    assert output["action_plan"] is not None
    assert len(output["action_plan"]["immediate_actions"]) >= 2
    assert "ಅಂಟು ಬಲೆ" in output["action_plan"]["immediate_actions"][0] or "ಬೇವಿನ" in output["action_plan"]["immediate_actions"][0]
    assert len(output["possible_causes"]) > 0

def test_targeted_question_when_image_missing():
    """
    When farmer gives vague input without image, agent asks targeted question first.
    """
    initial_state = {
        "user_id": "test-farmer-02",
        "conversation_id": "conv-test-02",
        "farmer_problem": "ಸಹಾಯ ಮಾಡಿ ಬೆಳೆ ಹಾಳಾಗಿದೆ (Help crop damaged)",
        "image_url": None,
        "agent_activity_steps": []
    }

    output = agent_graph.invoke(initial_state)
    assert output["goal_status"] == "Investigating"
    assert output.get("targeted_question") is not None

def test_follow_up_closed_loop_recovery_and_escalation():
    """
    Test Day 3 follow-up:
    Case A: Condition improving -> completes goal, gives prevention
    Case B: Condition worsening -> triggers expert escalation
    """
    # Case A: Improving
    improving_res = FollowUpAgent.evaluate_follow_up(
        previous_image="/uploads/sample_chilli_yellowing.jpg",
        new_image="/uploads/sample_chilli_recovered.jpg",
        farmer_response="ಹೊಸ ಚಿಗುರು ಹಸಿರಾಗಿದೆ, ಸುಧಾರಿಸುತ್ತಿದೆ",
        condition_assessment="improving",
        lang="kn",
        crop="chilli"
    )
    assert improving_res["goal_status"] == "Improving"
    assert improving_res["expert_escalation_recommended"] is False
    assert "ಮುನ್ನೆಚ್ಚರಿಕೆ" in improving_res["prevention_guidance"]

    # Case B: Worsening
    worsening_res = FollowUpAgent.evaluate_follow_up(
        previous_image="/uploads/sample_chilli_yellowing.jpg",
        new_image="/uploads/sample_chilli_worsened.jpg",
        farmer_response="ಗಿಡಗಳು ಪೂರ್ತಿ ಮುದುಡಿ ಒಣಗುತ್ತಿವೆ, ಹಾನಿ ಹೆಚ್ಚಾಗಿದೆ",
        condition_assessment="worsening",
        lang="kn",
        crop="chilli"
    )
    assert worsening_res["goal_status"] == "Needs Attention"
    assert worsening_res["expert_escalation_recommended"] is True
    assert len(worsening_res["expert_contacts"]) > 0


def test_kannada_greeting_flow():
    """
    When farmer greets in Kannada ('ಹಲೋ, ನಮಸ್ಕಾರ'), agent warmly responds and asks for their query.
    """
    initial_state = {
        "user_id": "test-farmer-03",
        "conversation_id": "conv-test-03",
        "farmer_problem": "ಹಲೋ, ನಮಸ್ಕಾರ",
        "image_url": None,
        "agent_activity_steps": []
    }
    output = agent_graph.invoke(initial_state)
    assert output["goal_status"] == "Conversational"
    assert "ನಮಸ್ಕಾರ" in output["final_response_text"]
    assert "ಸಮಸ್ಯೆ ಅಥವಾ ಪ್ರಶ್ನೆ" in output["final_response_text"]
    assert output["action_plan"] is None
    assert any(step["step_id"] == "greeting_handled" for step in output["agent_activity_steps"])

def test_english_greeting_flow():
    """
    When user says 'Hi', agent responds warmly and asks for their crop query.
    """
    initial_state = {
        "user_id": "test-farmer-04",
        "conversation_id": "conv-test-04",
        "farmer_problem": "Hi",
        "image_url": None,
        "agent_activity_steps": []
    }
    output = agent_graph.invoke(initial_state)
    assert output["goal_status"] == "Conversational"
    assert "KrishiRakshak" in output["final_response_text"]
    assert "How can I help you" in output["final_response_text"]
    assert output["action_plan"] is None

def test_hindi_greeting_flow():
    """
    When user says 'नमस्ते', agent responds warmly in Hindi and asks for crop query.
    """
    initial_state = {
        "user_id": "test-farmer-05",
        "conversation_id": "conv-test-05",
        "farmer_problem": "नमस्ते",
        "image_url": None,
        "agent_activity_steps": []
    }
    output = agent_graph.invoke(initial_state)
    assert output["goal_status"] == "Conversational"
    assert "नमस्ते किसान भाई" in output["final_response_text"]
    assert "समस्या या प्रश्न" in output["final_response_text"]

def test_identity_and_capabilities_flow():
    """
    When user asks 'Who are you and what can you do?', agent lists capabilities and asks for query.
    """
    initial_state = {
        "user_id": "test-farmer-06",
        "conversation_id": "conv-test-06",
        "farmer_problem": "Who are you and what can you do?",
        "image_url": None,
        "agent_activity_steps": []
    }
    output = agent_graph.invoke(initial_state)
    assert output["goal_status"] == "Conversational"
    assert "diagnos" in output["final_response_text"].lower()
    assert output["action_plan"] is None

def test_crops_supported_flow():
    """
    When user asks 'Which crops do you support?', agent lists crops and asks for their crop query.
    """
    initial_state = {
        "user_id": "test-farmer-07",
        "conversation_id": "conv-test-07",
        "farmer_problem": "Which crops do you support?",
        "image_url": None,
        "agent_activity_steps": []
    }
    output = agent_graph.invoke(initial_state)
    assert output["goal_status"] == "Conversational"
    assert "Chilli" in output["final_response_text"]
    assert "Tomato" in output["final_response_text"]

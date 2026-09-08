import pytest
from app.tools.crop_image_analyzer import crop_image_analyzer
from app.tools.weather_service import weather_tool
from app.tools.disease_db import disease_database_tool
from app.tools.agri_knowledge import agri_knowledge_tool
from app.tools.govt_schemes import govt_schemes_tool
from app.tools.fertilizer_calculator import fertilizer_tool
from app.tools.expert_finder import expert_finder_tool
from app.tools.follow_up_planner import follow_up_planner_tool
from app.tools.image_comparator import image_comparator_tool

def test_crop_image_analyzer():
    res = crop_image_analyzer.analyze_crop_image("uploads/sample_chilli_yellowing.jpg", crop_hint="chilli")
    assert res["status"] == "success"
    assert len(res["detected_symptoms"]) > 0
    assert "estimated_affected_area_percentage" in res

def test_weather_tool():
    w = weather_tool.get_weather("Mandya, Karnataka")
    assert "temperature" in w
    assert "fungal_disease_risk" in w
    assert "spray_advisory" in w
    assert len(w["forecast_3days"]) == 3

def test_disease_database_tool():
    diseases = disease_database_tool.search("chilli", ["yellowing leaves", "upward curling"])
    assert len(diseases) > 0
    top = diseases[0]
    assert "confidence_score" in top
    assert top["confidence_score"] >= 0.50
    assert "management" in top

def test_agri_knowledge_tool():
    kb = agri_knowledge_tool.search("chilli leaf curl thrips")
    assert len(kb) > 0
    assert "cultural_practices" in kb[0]

def test_govt_schemes_tool():
    schemes = govt_schemes_tool.search(farmer_context="damage crop insurance")
    assert len(schemes) >= 3
    assert any(s["id"] == "pmfby" for s in schemes)

def test_fertilizer_tool():
    calc = fertilizer_tool.calculate("chilli", land_area_acres=2.0)
    assert calc["land_area_acres"] == 2.0
    assert calc["commercial_fertilizers_bags_or_kg"]["Urea_kg"] > 0
    assert len(calc["split_application_schedule"]) == 3

def test_expert_finder():
    experts = expert_finder_tool.find_experts("Mandya")
    assert len(experts) >= 2
    assert any("Kisan Call Centre" in e["name"] for e in experts)

def test_follow_up_planner():
    plan = follow_up_planner_tool.create_follow_up_plan("yellowing leaves", ["spraying neem"], timeline_days=3)
    assert "scheduled_follow_up_date" in plan
    assert len(plan["monitoring_milestones"]) == 3

def test_image_comparator():
    comp = image_comparator_tool.compare_crop_images(
        "uploads/sample_chilli_yellowing.jpg",
        "uploads/sample_chilli_recovered.jpg",
        farmer_feedback_text="ಹೊಸ ಎಲೆಗಳು ಹಸಿರಾಗಿ ಚಿಗುರುತ್ತಿವೆ (New leaves are green)",
        condition_hint="improving"
    )
    assert comp["comparison_result"] == "Improving"
    assert comp["recovery_index"] > 0.70

from typing import Dict, Any, List
from datetime import datetime, timedelta

class FollowUpPlannerTool:
    """
    Creates a structured multi-day follow-up and monitoring schedule.
    This ensures the loop does not end after 1 response.
    """

    @staticmethod
    def create_follow_up_plan(
        problem: str,
        actions: List[str],
        timeline_days: int = 3,
        crop: str = "Chilli"
    ) -> Dict[str, Any]:
        scheduled_date = datetime.utcnow() + timedelta(days=timeline_days)
        formatted_date = scheduled_date.strftime("%Y-%m-%d")

        milestones = [
            {
                "day": 1,
                "label": "Day 1 (Immediate)",
                "action": "Complete immediate spray/traps installation and avoid water stress."
            },
            {
                "day": timeline_days,
                "label": f"Day {timeline_days} (First Follow-up Check)",
                "action": "Inspect newly unfolding shoots and upload comparison photo to KrishiRakshak AI."
            },
            {
                "day": timeline_days + 4,
                "label": f"Day {timeline_days + 4} (Secondary Evaluation)",
                "action": "Apply micronutrient booster or escalate to KVK if stunted yellowing continues."
            }
        ]

        questions_to_ask = [
            "ಹೊಸದಾಗಿ ಚಿಗುರುತ್ತಿರುವ ಎಲೆಗಳು ಹಸಿರಾಗಿ ಹರಡಿಕೊಳ್ಳುತ್ತಿವೆಯೇ? (Are newly emerging shoots spreading flat and green?)",
            "ಹಳದಿ ಬಣ್ಣ ಇತರ ಗಿಡಗಳಿಗೆ ಹರಡುವುದು ನಿಂತಿದೆಯೇ? (Has yellowing stopped spreading to adjacent plants?)",
            "ಗಿಡದಲ್ಲಿ ಹೂವು ಅಥವಾ ಕಾಯಿ ಕಟ್ಟುವುದು ಸಾಮಾನ್ಯವಾಗಿ ಆರಂಭವಾಗಿದೆಯೇ? (Has flowering/fruiting resumed normally?)"
        ]

        return {
            "scheduled_follow_up_date": formatted_date,
            "days_interval": timeline_days,
            "monitoring_milestones": milestones,
            "follow_up_check_questions": questions_to_ask,
            "status": "Scheduled",
            "instructions_for_farmer": f"ಕೃಷಿರಕ್ಷಕ್ AI {timeline_days} ದಿನಗಳ ನಂತರ ನಿಮ್ಮ ಬೆಳೆಯ ಚೇತರಿಕೆಯನ್ನು ಮೌಲ್ಯಮಾಪನ ಮಾಡಲು ಅನುಸರಣಾ (Follow-up) ಅಧಿಸೂಚನೆ ನೀಡುತ್ತದೆ."
        }

follow_up_planner_tool = FollowUpPlannerTool()

from __future__ import annotations

from datetime import datetime

from src.predictor import IntentPredictor


class ResponseEngine:
    def __init__(self):
        self.predictor = IntentPredictor()
        self.chat_history: list[dict] = []
        self.starter_questions = [
            "What are the admission requirements?",
            "How much are the fees for engineering?",
            "When are the semester exams scheduled?",
            "Tell me about hostel facilities.",
            "How does attendance condonation work?",
            "What companies visit for placements?",
            "What are the library timings?",
            "How can I check my timetable?",
        ]

    def _get_followup_suggestions(self, intent: str):
        followups = {
            "greeting": [
                "Can you tell me about the admission process?",
                "What are the fees for CSE?",
            ],
            "admission": [
                "Which documents are required for TNEA?",
                "When does admission start?",
                "What is the cutoff for CSE?",
            ],
            "fee_structure": [
                "Is hostel fee included in the total?",
                "What are the tuition and lab charges?",
                "What is the fee for first-year students?",
            ],
            "attendance": [
                "How to apply for attendance condonation?",
                "What documents are needed?",
                "What happens if my attendance is below 75%?",
            ],
            "exam_schedule": [
                "How do I download my hall ticket?",
                "Where can I find the exam timetable?",
                "When are internal exams usually held?",
            ],
            "placement": [
                "What is the average package?",
                "What is the eligibility criteria?",
                "Which companies recruit here?",
            ],
            "hostel": [
                "What is the hostel curfew time?",
                "How many seats are available?",
                "Do hostels have Wi-Fi?",
            ],
            "departments": [
                "Which departments have the best placements?",
                "What is the difference between CSE and IT?",
                "Is ECE available?",
            ],
            "revaluation": [
                "How much is the revaluation fee?",
                "What is the timeline for revaluation results?",
                "Can I request photocopy of the answer sheet?",
            ],
            "timetable": [
                "Is the timetable available on the student portal?",
                "What are the regular lecture timings?",
                "How do I check my section timetable?",
            ],
            "faculty": [
                "Where can I find the faculty directory?",
                "What are the office hours for professors?",
                "How can I contact my HOD?",
            ],
            "library": [
                "What are the library timings?",
                "How many books can I borrow?",
                "Is there an e-library available?",
            ],
            "sports": [
                "What sports facilities are available?",
                "How do I join the cricket team?",
                "Does the college host sports events?",
            ],
            "wifi": [
                "How do I login to college Wi-Fi?",
                "What if my Wi-Fi is not working?",
                "Which SSID should I use?",
            ],
            "scholarship": [
                "What scholarships are available?",
                "How do I apply for government scholarships?",
                "How can I check scholarship status?",
            ],
            "unknown": [
                "Can you rephrase your question?",
                "Try asking about fees, exams, hostel, or placements.",
                "Which topic are you interested in?",
            ],
            "goodbye": [
                "Anything else I can help with?",
                "Want details about admissions or fees?",
            ],
        }

        suggestions = followups.get(intent)
        if suggestions:
            return suggestions[:3]

        # Fallback generic suggestions
        return [
            "Ask me about admissions, fees, exams, hostel, or placements.",
            "Can you share which department or year you are in?",
            "What would you like to know next?",
        ]

    def get_response(self, user_input: str):
        prediction = self.predictor.predict(user_input)

        intent = prediction["intent"]
        confidence = float(prediction["confidence"])
        confidence_percent = f"{confidence * 100:.1f}%"

        # Color based on confidence score
        if confidence >= 0.6:
            confidence_color = "green"
        elif confidence >= 0.35:
            confidence_color = "orange"
        else:
            confidence_color = "red"

        timestamp = datetime.now().strftime("%H:%M")
        followup_suggestions = self._get_followup_suggestions(intent)

        bot_response = prediction["response"]

        response = {
            "user_message": user_input,
            "bot_response": bot_response,
            "intent": intent,
            "confidence": confidence,
            "confidence_percent": confidence_percent,
            "confidence_color": confidence_color,
            "timestamp": timestamp,
            "followup_suggestions": followup_suggestions,
        }

        self.chat_history.append(response)
        return response

    def get_chat_history(self):
        return self.chat_history

    def clear_history(self):
        self.chat_history = []

    def get_suggested_questions(self):
        return self.starter_questions


if __name__ == "__main__":
    engine = ResponseEngine()

    test_inputs = [
        "Hi there",
        "What is the hostel curfew time?",
        "When are the semester exams scheduled?",
        "Tell me about placements",
        "asdfghjkl qwerty gibberish",
    ]

    for inp in test_inputs:
        print("=" * 60)
        print("User:", inp)
        out = engine.get_response(inp)
        print("Bot:", out["bot_response"])
        print("Intent:", out["intent"], "| Confidence:", out["confidence_percent"], "| Color:", out["confidence_color"])
        print("Followups:", out["followup_suggestions"])


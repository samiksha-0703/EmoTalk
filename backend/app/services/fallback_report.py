from datetime import date

def generate_fallback_daily_report(emotion_counts):
    total = sum(emotion_counts.values())
    dominant_emotion = max(emotion_counts, key=emotion_counts.get)

    return {
        "header": {
            "date": date.today().isoformat(),
            "checkIns": total,
            "note": "This report reflects your emotional patterns for today."
        },
        "emotionalSummary": {
            "dominantEmotion": dominant_emotion,
            "confidenceLevel": "Moderate",
            "distribution": emotion_counts
        },
        "psychologicalInsight": (
            "Your emotions show a repeated pattern today. "
            "Experiencing this is a natural response to daily mental demands."
        ),
        "moodStability": {
            "level": "Moderately stable",
            "explanation": "Your emotions fluctuated but remained within a manageable range."
        },
        "focusArea": "Emotional Balance",
        "routineSuggestions": [
            "Take a short walk",
            "Hydrate regularly",
            "Avoid screens before sleep"
        ],
        "exercises": {
            "breathing": "4-4-6 breathing for 5 minutes",
            "movement": "Light stretching",
            "expression": "Write down one feeling you noticed today"
        },
        "positiveReinforcement": "You are showing awareness, and that itself is progress.",
        "safetyNote": (
            "If emotions feel overwhelming, consider talking to someone you trust."
        )
    }

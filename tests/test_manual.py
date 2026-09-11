from risk_engine import calculate_risk


deepfake_result = {
    "score": 0.87,
    "label": "AI_GENERATED",
    "confidence": 0.91
}

speaker_result = {
    "similarity": 0.93,
    "same_speaker_probability": 0.91,
    "label": "MATCH"
}

interaction_result = {
    "anomaly_score": 0.72,
    "features": {
        "speech_rate": 4.1,
        "pause_ratio": 0.18,
        "pitch_variation": 0.32
    }
}


result = calculate_risk(
    deepfake_result,
    speaker_result,
    interaction_result
)

print(result)
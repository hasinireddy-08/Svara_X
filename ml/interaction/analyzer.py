from .features import extract_voice_features
from .classifier import detect_ai_voice


def calculate_anomaly_score(features):
    """
    Calculate a prototype anomaly score from voice characteristics.
    This is an additional heuristic signal, not the AI detector itself.
    """

    score = 0.0

    if features["pitch_variation"] < 0.10:
        score += 0.30

    if features["energy_variation"] < 0.01:
        score += 0.25

    if features["pause_ratio"] < 0.03:
        score += 0.20
    elif features["pause_ratio"] > 0.60:
        score += 0.20

    if features["duration"] < 1.0:
        score += 0.10

    return min(score, 1.0)


def calculate_risk_level(ai_detection):
    """
    Convert AI detector output into a simple risk level.
    """

    label = ai_detection.get("label", "")
    confidence = float(
        ai_detection.get("confidence", 0.0)
    )

    if label == "AI_GENERATED":

        if confidence >= 0.80:
            return "HIGH"

        if confidence >= 0.60:
            return "MEDIUM"

        return "LOW"

    if label == "REAL_HUMAN":
        return "LOW"

    return "UNKNOWN"


def analyze_interaction(audio_path):
    """
    Analyze audio and return a frontend-ready result.
    """

    try:
        # Voice characteristics
        features = extract_voice_features(audio_path)

        # Additional heuristic anomaly signal
        anomaly_score = calculate_anomaly_score(
            features
        )

        # AI/deepfake detection
        ai_detection = detect_ai_voice(
            audio_path
        )

        # Risk level
        risk_level = calculate_risk_level(
            ai_detection
        )

        # Final result
        return {
            "label": ai_detection.get(
                "label",
                "UNKNOWN"
            ),

            "confidence": round(
                float(
                    ai_detection.get(
                        "confidence",
                        0.0
                    )
                ) * 100,
                2
            ),

            "risk_level": risk_level,

            "anomaly_score": round(
                float(anomaly_score),
                3
            ),

            "ai_detection": ai_detection,

            "features": features
        }

    except Exception as e:

        return {
            "label": "ERROR",
            "confidence": 0.0,
            "risk_level": "UNKNOWN",
            "anomaly_score": 0.0,
            "ai_detection": {},
            "features": {},
            "error": str(e)
        }
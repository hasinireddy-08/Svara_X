from .features import extract_voice_features
from .classifier import detect_ai_voice


def calculate_anomaly_score(features):
    """
    Calculate a prototype anomaly score from voice characteristics.

    This is a heuristic score for the hackathon prototype.
    It is NOT a definitive deepfake classifier.
    """

    score = 0.0

    # Very low pitch variation
    if features["pitch_variation"] < 0.10:
        score += 0.30

    # Very low energy variation
    if features["energy_variation"] < 0.01:
        score += 0.25

    # Unusually low or high pause ratio
    if features["pause_ratio"] < 0.03:
        score += 0.20

    elif features["pause_ratio"] > 0.60:
        score += 0.20

    # Extremely short recording
    if features["duration"] < 1.0:
        score += 0.10

    return min(score, 1.0)


def analyze_interaction(audio_path):
    """
    Analyze an audio file and return interaction-analysis results.
    """

    try:

        # --------------------------------
        # 1. Extract voice characteristics
        # --------------------------------

        features = extract_voice_features(
            audio_path
        )


        # --------------------------------
        # 2. Calculate interaction anomaly
        # --------------------------------

        anomaly_score = calculate_anomaly_score(
            features
        )


        # --------------------------------
        # 3. Detect AI-generated voice
        # --------------------------------

        ai_detection = detect_ai_voice(
            audio_path
        )


        # --------------------------------
        # 4. Return combined result
        # --------------------------------

        return {

            "anomaly_score": round(
                anomaly_score,
                3
            ),

            "ai_detection": ai_detection,

            "features": features

        }


    except Exception as e:

        return {

            "anomaly_score": 0.0,

            "ai_detection": {},

            "features": {},

            "error": str(e)

        }
from .preprocessing import load_audio, extract_audio_features


def analyze_deepfake(audio_path):
    """
    Analyze an audio file and return a deepfake detection result.
    """

    try:
        audio, sr = load_audio(audio_path)

        features = extract_audio_features(audio, sr)

        score = calculate_synthetic_score(features)

        if score >= 0.70:
            label = "AI_GENERATED"
        elif score <= 0.30:
            label = "REAL"
        else:
            label = "UNCERTAIN"

        confidence = calculate_confidence(score)

        return {
            "score": round(float(score), 3),
            "label": label,
            "confidence": round(float(confidence), 3)
        }

    except Exception as e:
        return {
            "score": 0.0,
            "label": "UNCERTAIN",
            "confidence": 0.0,
            "error": str(e)
        }


def calculate_synthetic_score(features):
    """
    Prototype scoring logic.
    """

    score = 0.5

    if features["zero_crossing_rate"] < 0.03:
        score += 0.15

    if features["rms_energy"] < 0.03:
        score += 0.10

    if features["spectral_centroid"] < 1500:
        score += 0.10

    return min(max(score, 0.0), 1.0)


def calculate_confidence(score):
    """
    Calculate confidence of the prediction.
    """

    distance = abs(score - 0.5) * 2

    return min(
        0.5 + distance * 0.5,
        0.95
    )
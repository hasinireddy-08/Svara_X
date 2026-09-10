from .preprocessing import load_audio, extract_audio_features


def analyze_deepfake(audio_path):
    """
    Analyze an audio file and return acoustic features.

    Note:
    This is a prototype. The extracted features are not
    sufficient by themselves to prove that audio is AI-generated.
    """

    try:
        audio, sr = load_audio(audio_path)

        features = extract_audio_features(audio, sr)

        return {
            "score": 0.5,
            "label": "UNCERTAIN",
            "confidence": 0.5,
            "features": features
        }

    except Exception as e:
        return {
            "score": 0.0,
            "label": "UNCERTAIN",
            "confidence": 0.0,
            "error": str(e)
        }
from ml.deepfake.detector import analyze_deepfake


def run_deepfake_analysis(audio_path):
    """
    Run deepfake detection through the backend service.
    """
    return analyze_deepfake(audio_path)
from ml.interaction.analyzer import analyze_interaction


def run_interaction_analysis(audio_path):
    """
    Run complete voice interaction and AI detection analysis.

    Parameters
    ----------
    audio_path : str
        Path to the WAV audio file.

    Returns
    -------
    dict
        Frontend-ready analysis result.
    """

    return analyze_interaction(audio_path)
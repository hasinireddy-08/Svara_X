"""
Backend service wrapper for VoxSentinel risk analysis.
"""

from risk_engine.risk import calculate_risk


def run_risk_analysis(
    deepfake_result: dict,
    speaker_result: dict,
    interaction_result: dict
) -> dict:
    """
    Run the complete VoxSentinel risk analysis pipeline.
    """

    return calculate_risk(
        deepfake_result=deepfake_result,
        speaker_result=speaker_result,
        interaction_result=interaction_result
    )
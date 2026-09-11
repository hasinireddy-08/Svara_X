"""
VoxSentinel Dynamic Trust / Risk Engine.

Combines:
    1. Deepfake detection
    2. Speaker verification
    3. Interaction analysis

into one final risk assessment.
"""

from .rules import (
    DEEPFAKE_WEIGHT,
    SPEAKER_WEIGHT,
    INTERACTION_WEIGHT,
    calculate_speaker_risk,
    clamp,
    determine_risk_level,
    generate_reasons,
)


def calculate_risk(
    deepfake_result: dict,
    speaker_result: dict,
    interaction_result: dict
) -> dict:
    """
    Calculate the final VoxSentinel risk assessment.

    Parameters
    ----------
    deepfake_result : dict
        Output from the deepfake detection module.

    Expected example:

        {
            "score": 0.87,
            "label": "AI_GENERATED",
            "confidence": 0.91
        }

    speaker_result : dict
        Output from the speaker verification module.

    Expected example:

        {
            "similarity": 0.93,
            "same_speaker_probability": 0.91,
            "label": "MATCH"
        }

    interaction_result : dict
        Output from the interaction analysis module.

    Expected example:

        {
            "anomaly_score": 0.72,
            "features": {
                "speech_rate": 4.1,
                "pause_ratio": 0.18,
                "pitch_variation": 0.32
            }
        }

    Returns
    -------
    dict

        {
            "risk_score": 0.81,
            "risk_level": "HIGH",
            "reasons": [...]
        }
    """

    # ===============================================================
    # 1. Validate input
    # ===============================================================

    if not isinstance(deepfake_result, dict):
        raise TypeError(
            "deepfake_result must be a dictionary"
        )

    if not isinstance(speaker_result, dict):
        raise TypeError(
            "speaker_result must be a dictionary"
        )

    if not isinstance(interaction_result, dict):
        raise TypeError(
            "interaction_result must be a dictionary"
        )

    # ===============================================================
    # 2. Extract scores
    # ===============================================================

    deepfake_score = clamp(
        deepfake_result.get("score", 0.0)
    )

    interaction_score = clamp(
        interaction_result.get(
            "anomaly_score",
            0.0
        )
    )

    # ===============================================================
    # 3. Calculate speaker risk
    # ===============================================================

    speaker_risk = calculate_speaker_risk(
        deepfake_score,
        speaker_result
    )

    speaker_risk = clamp(
        speaker_risk
    )

    # ===============================================================
    # 4. Calculate weighted risk
    # ===============================================================

    risk_score = (
        deepfake_score * DEEPFAKE_WEIGHT
        +
        speaker_risk * SPEAKER_WEIGHT
        +
        interaction_score * INTERACTION_WEIGHT
    )

    risk_score = clamp(
        risk_score
    )

    # ===============================================================
    # 5. Determine risk level
    # ===============================================================

    risk_level = determine_risk_level(
        risk_score
    )

    # ===============================================================
    # 6. Generate explanations
    # ===============================================================

    reasons = generate_reasons(
        deepfake_result=deepfake_result,
        speaker_result=speaker_result,
        interaction_result=interaction_result,
        speaker_risk=speaker_risk
    )

    # ===============================================================
    # 7. Return standardized result
    # ===============================================================

    return {
        "risk_score": round(
            risk_score,
            3
        ),
        "risk_level": risk_level,
        "reasons": reasons
    }
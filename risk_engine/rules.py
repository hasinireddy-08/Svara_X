"""
Rules and thresholds for the VoxSentinel risk engine.

This module intentionally keeps the prototype's decision rules
separate from the main risk calculation logic.
"""

# -------------------------------------------------------------------
# WEIGHTS
# -------------------------------------------------------------------

DEEPFAKE_WEIGHT = 0.50
SPEAKER_WEIGHT = 0.30
INTERACTION_WEIGHT = 0.20

# -------------------------------------------------------------------
# RISK LEVEL THRESHOLDS
# -------------------------------------------------------------------

LOW_THRESHOLD = 0.35
MEDIUM_THRESHOLD = 0.65

# -------------------------------------------------------------------
# INDICATOR THRESHOLDS
# -------------------------------------------------------------------

HIGH_DEEPFAKE_THRESHOLD = 0.70
MEDIUM_DEEPFAKE_THRESHOLD = 0.40

HIGH_SPEAKER_SIMILARITY_THRESHOLD = 0.75
LOW_SPEAKER_SIMILARITY_THRESHOLD = 0.40

HIGH_INTERACTION_ANOMALY_THRESHOLD = 0.60
MEDIUM_INTERACTION_ANOMALY_THRESHOLD = 0.35


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    """
    Restrict a numeric value to the range [minimum, maximum].
    """

    return max(minimum, min(float(value), maximum))


def determine_risk_level(risk_score: float) -> str:
    """
    Convert a numerical risk score into a human-readable risk level.

    Score range:
        0.00 - 0.34 -> LOW
        0.35 - 0.64 -> MEDIUM
        0.65 - 1.00 -> HIGH
    """

    risk_score = clamp(risk_score)

    if risk_score < LOW_THRESHOLD:
        return "LOW"

    if risk_score < MEDIUM_THRESHOLD:
        return "MEDIUM"

    return "HIGH"


def calculate_speaker_risk(
    deepfake_score: float,
    speaker_result: dict
) -> float:
    """
    Convert speaker-verification output into a risk signal.

    IMPORTANT:
    Speaker similarity by itself is not necessarily suspicious.

    In a voice-impersonation scenario:
        high similarity + high deepfake score
        can indicate possible synthetic impersonation.

    A low similarity score can also be suspicious when a caller
    claims to be the reference speaker.

    This is a prototype rule and should eventually be calibrated
    using real validation data.
    """

    similarity = clamp(
        speaker_result.get("similarity", 0.0)
    )

    label = str(
        speaker_result.get("label", "UNCERTAIN")
    ).upper()

    # Strong possible cloned-voice signal.
    if (
        deepfake_score >= HIGH_DEEPFAKE_THRESHOLD
        and similarity >= HIGH_SPEAKER_SIMILARITY_THRESHOLD
    ):
        return similarity

    # Strong speaker mismatch.
    if similarity <= LOW_SPEAKER_SIMILARITY_THRESHOLD:
        return 0.70

    # Explicit mismatch label.
    if label in {"MISMATCH", "NOT_MATCH", "DIFFERENT_SPEAKER"}:
        return max(0.70, 1.0 - similarity)

    # Explicit match with low/moderate deepfake evidence.
    if label in {"MATCH", "SAME_SPEAKER"}:
        return 0.20

    # Unknown / uncertain speaker result.
    return 0.40


def generate_reasons(
    deepfake_result: dict,
    speaker_result: dict,
    interaction_result: dict,
    speaker_risk: float
) -> list[str]:
    """
    Generate human-readable explanations for the final risk score.
    """

    reasons = []

    deepfake_score = clamp(
        deepfake_result.get("score", 0.0)
    )

    similarity = clamp(
        speaker_result.get("similarity", 0.0)
    )

    anomaly_score = clamp(
        interaction_result.get("anomaly_score", 0.0)
    )

    # ---------------------------------------------------------------
    # Deepfake explanation
    # ---------------------------------------------------------------

    if deepfake_score >= HIGH_DEEPFAKE_THRESHOLD:

        reasons.append(
            "Strong synthetic-voice indicators detected."
        )

    elif deepfake_score >= MEDIUM_DEEPFAKE_THRESHOLD:

        reasons.append(
            "Moderate synthetic-voice indicators detected."
        )

    else:

        reasons.append(
            "Low synthetic-voice indicators detected."
        )

    # ---------------------------------------------------------------
    # Speaker explanation
    # ---------------------------------------------------------------

    if (
        deepfake_score >= HIGH_DEEPFAKE_THRESHOLD
        and similarity >= HIGH_SPEAKER_SIMILARITY_THRESHOLD
    ):

        reasons.append(
            "The analyzed voice is highly similar to the reference "
            "speaker while strong synthetic indicators are present."
        )

    elif similarity <= LOW_SPEAKER_SIMILARITY_THRESHOLD:

        reasons.append(
            "Low similarity to the reference speaker was detected."
        )

    elif similarity >= HIGH_SPEAKER_SIMILARITY_THRESHOLD:

        reasons.append(
            "High similarity to the reference speaker was detected."
        )

    # ---------------------------------------------------------------
    # Interaction explanation
    # ---------------------------------------------------------------

    if anomaly_score >= HIGH_INTERACTION_ANOMALY_THRESHOLD:

        reasons.append(
            "Unusual speech interaction characteristics were detected."
        )

    elif anomaly_score >= MEDIUM_INTERACTION_ANOMALY_THRESHOLD:

        reasons.append(
            "Moderately unusual speech interaction characteristics "
            "were detected."
        )

    else:

        reasons.append(
            "No strong interaction anomaly was detected."
        )

    return reasons
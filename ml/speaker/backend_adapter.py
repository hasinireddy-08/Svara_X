from typing import Dict

from ml.speaker.speaker_verifier import verify_speaker


def verify_speaker_for_backend(
    reference_audio: str,
    incoming_audio: str,
) -> Dict:
    """
    Backend-facing wrapper for speaker verification.

    Args:
        reference_audio: Path to the registered/reference speaker audio.
        incoming_audio: Path to the incoming audio sample.

    Returns:
        Dictionary containing the speaker score and classification.
    """

    result = verify_speaker(
        reference_audio=reference_audio,
        incoming_audio=incoming_audio,
    )

    return {
        "speaker_score": result["speaker_score"],
        "speaker_status": result["speaker_status"],
    }
"""
Speaker verification service.

Compares a reference speaker recording with an incoming recording
using pretrained ECAPA-TDNN speaker embeddings.
"""

from pathlib import Path
from typing import Dict

from ml.speaker.embeddings import get_speaker_embedding
from ml.speaker.similarity import cosine_similarity


# Initial operating threshold based on preliminary testing.
# This should be recalibrated with a larger validation dataset.
DEFAULT_THRESHOLD = 0.60

# Scores below this boundary are treated as a clear mismatch.
# Scores between this boundary and DEFAULT_THRESHOLD are uncertain.
UNCERTAIN_MARGIN = 0.15


def verify_speaker(
    reference_audio: str,
    incoming_audio: str,
    threshold: float = DEFAULT_THRESHOLD,
) -> Dict:
    """
    Compare an incoming voice against a reference speaker.

    Args:
        reference_audio:
            Path to the known/reference speaker recording.

        incoming_audio:
            Path to the incoming recording.

        threshold:
            Minimum cosine similarity required for MATCH.

    Returns:
        Dictionary containing:
            - speaker_score
            - threshold
            - speaker_status

        speaker_status can be:
            MATCH
            UNCERTAIN
            MISMATCH

    Raises:
        FileNotFoundError:
            If either audio file does not exist.

        ValueError:
            If the threshold is outside the valid cosine range.
    """

    # Validate threshold.
    if not 0.0 <= threshold <= 1.0:
        raise ValueError(
            "Threshold must be between 0.0 and 1.0."
        )

    # Validate reference audio.
    if not Path(reference_audio).is_file():
        raise FileNotFoundError(
            f"Reference audio not found: {reference_audio}"
        )

    # Validate incoming audio.
    if not Path(incoming_audio).is_file():
        raise FileNotFoundError(
            f"Incoming audio not found: {incoming_audio}"
        )

    # Generate speaker embeddings.
    reference_embedding = get_speaker_embedding(
        reference_audio
    )

    incoming_embedding = get_speaker_embedding(
        incoming_audio
    )

    # Calculate cosine similarity.
    similarity = cosine_similarity(
        reference_embedding,
        incoming_embedding,
    )

    # Determine speaker status.
    uncertain_threshold = max(
        0.0,
        threshold - UNCERTAIN_MARGIN
    )

    if similarity >= threshold:
        status = "MATCH"

    elif similarity >= uncertain_threshold:
        status = "UNCERTAIN"

    else:
        status = "MISMATCH"

    return {
        "speaker_score": round(similarity, 4),
        "threshold": threshold,
        "speaker_status": status,
    }
from ml.speaker.speaker_verifier import (
    UNCERTAIN_MARGIN,
    verify_speaker,
)


REFERENCE_AUDIO = "test_audio/sample.wav"
SAME_SPEAKER_AUDIO = "test_audio/same_speaker.wav"
DIFFERENT_SPEAKER_AUDIO = "test_audio/different_speaker.wav"


def test_same_speaker():
    """Same speaker recordings should produce MATCH."""

    result = verify_speaker(
        REFERENCE_AUDIO,
        SAME_SPEAKER_AUDIO,
    )

    assert result["speaker_status"] == "MATCH"
    assert result["speaker_score"] >= result["threshold"]


def test_different_speaker():
    """Different speaker recordings should produce MISMATCH."""

    result = verify_speaker(
        REFERENCE_AUDIO,
        DIFFERENT_SPEAKER_AUDIO,
    )

    assert result["speaker_status"] == "MISMATCH"
    assert result["speaker_score"] < 0.45


def test_uncertain_range():
    """
    Verify that the uncertainty boundary is configured correctly.

    Default threshold = 0.60
    Uncertain range starts at approximately 0.45.
    """

    threshold = 0.60

    uncertain_threshold = threshold - UNCERTAIN_MARGIN

    # Floating-point arithmetic can represent 0.45 as
    # 0.44999999999999996, so use a tolerance instead
    # of exact equality.
    assert abs(uncertain_threshold - 0.45) < 1e-9


def test_result_structure():
    """Verify that the speaker verification result has the expected fields."""

    result = verify_speaker(
        REFERENCE_AUDIO,
        SAME_SPEAKER_AUDIO,
    )

    assert "speaker_score" in result
    assert "threshold" in result
    assert "speaker_status" in result

    assert isinstance(result["speaker_score"], float)
    assert isinstance(result["threshold"], float)

    assert result["speaker_status"] in {
        "MATCH",
        "UNCERTAIN",
        "MISMATCH",
    }
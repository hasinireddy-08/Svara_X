from ml.speaker.backend_adapter import verify_speaker_for_backend


REFERENCE_AUDIO = "test_audio/sample.wav"
SAME_SPEAKER_AUDIO = "test_audio/same_speaker.wav"
DIFFERENT_SPEAKER_AUDIO = "test_audio/different_speaker.wav"


def test_backend_adapter_same_speaker():
    result = verify_speaker_for_backend(
        REFERENCE_AUDIO,
        SAME_SPEAKER_AUDIO,
    )

    assert "speaker_score" in result
    assert "speaker_status" in result

    assert result["speaker_status"] in {
        "MATCH",
        "UNCERTAIN",
        "MISMATCH",
    }


def test_backend_adapter_different_speaker():
    result = verify_speaker_for_backend(
        REFERENCE_AUDIO,
        DIFFERENT_SPEAKER_AUDIO,
    )

    assert "speaker_score" in result
    assert "speaker_status" in result

    assert result["speaker_status"] in {
        "MATCH",
        "UNCERTAIN",
        "MISMATCH",
    }
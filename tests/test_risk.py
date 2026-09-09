"""
Tests for the VoxSentinel risk engine.
"""

from risk_engine.risk import calculate_risk


# ================================================================
# Test data
# ================================================================

HIGH_RISK_DEEPFAKE = {
    "score": 0.90,
    "label": "AI_GENERATED",
    "confidence": 0.95
}

HIGH_SIMILARITY = {
    "similarity": 0.90,
    "same_speaker_probability": 0.92,
    "label": "MATCH"
}

HIGH_INTERACTION_ANOMALY = {
    "anomaly_score": 0.80,
    "features": {
        "speech_rate": 4.1,
        "pause_ratio": 0.18,
        "pitch_variation": 0.32
    }
}


LOW_RISK_DEEPFAKE = {
    "score": 0.10,
    "label": "REAL",
    "confidence": 0.95
}

LOW_RISK_SPEAKER = {
    "similarity": 0.90,
    "same_speaker_probability": 0.92,
    "label": "MATCH"
}

LOW_RISK_INTERACTION = {
    "anomaly_score": 0.10,
    "features": {
        "speech_rate": 2.5,
        "pause_ratio": 0.30,
        "pitch_variation": 0.60
    }
}


# ================================================================
# High-risk test
# ================================================================

def test_high_risk_case():

    result = calculate_risk(
        HIGH_RISK_DEEPFAKE,
        HIGH_SIMILARITY,
        HIGH_INTERACTION_ANOMALY
    )

    assert result["risk_level"] == "HIGH"

    assert 0.0 <= result["risk_score"] <= 1.0

    assert len(result["reasons"]) > 0


# ================================================================
# Low-risk test
# ================================================================

def test_low_risk_case():

    result = calculate_risk(
        LOW_RISK_DEEPFAKE,
        LOW_RISK_SPEAKER,
        LOW_RISK_INTERACTION
    )

    assert result["risk_level"] == "LOW"

    assert 0.0 <= result["risk_score"] <= 1.0


# ================================================================
# Medium-risk test
# ================================================================

def test_medium_risk_case():

    deepfake_result = {
        "score": 0.50,
        "label": "UNCERTAIN",
        "confidence": 0.60
    }

    speaker_result = {
        "similarity": 0.60,
        "same_speaker_probability": 0.60,
        "label": "UNCERTAIN"
    }

    interaction_result = {
        "anomaly_score": 0.40
    }

    result = calculate_risk(
        deepfake_result,
        speaker_result,
        interaction_result
    )

    assert result["risk_level"] == "MEDIUM"

    assert 0.0 <= result["risk_score"] <= 1.0


# ================================================================
# Missing values test
# ================================================================

def test_missing_values_are_handled():

    result = calculate_risk(
        {},
        {},
        {}
    )

    assert "risk_score" in result
    assert "risk_level" in result
    assert "reasons" in result

    assert 0.0 <= result["risk_score"] <= 1.0


# ================================================================
# Score clamping test
# ================================================================

def test_scores_are_clamped():

    deepfake_result = {
        "score": 5.0
    }

    speaker_result = {
        "similarity": -2.0
    }

    interaction_result = {
        "anomaly_score": 10.0
    }

    result = calculate_risk(
        deepfake_result,
        speaker_result,
        interaction_result
    )

    assert 0.0 <= result["risk_score"] <= 1.0


# ================================================================
# Invalid input test
# ================================================================

def test_invalid_input():

    try:

        calculate_risk(
            "invalid",
            {},
            {}
        )

    except TypeError:

        assert True

    else:

        assert False
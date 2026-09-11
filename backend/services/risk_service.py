def calculate_risk(voice_score, speaker_score, interaction_score):
    risk = (
        (100 - voice_score) * 0.4
        + (100 - speaker_score) * 0.3
        + (100 - interaction_score) * 0.3
    )

    return round(risk)

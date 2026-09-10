from backend.services.deepfake_service import analyze_voice
from backend.services.speaker_service import verify_speaker
from backend.services.interaction_service import analyze_interaction
from backend.services.risk_service import calculate_risk
from backend.services.context_service import analyze_context


async def run_pipeline(file):

    # 1. Voice authenticity
    voice_result = analyze_voice(file)

    # Convert deepfake score into voice authenticity score
    voice_score = 100 - voice_result["deepfake_score"]

    # 2. Speaker verification
    speaker_result = verify_speaker(file)

    # 3. Interaction DNA
    interaction_result = analyze_interaction(file)

    # 4. Context Intelligence
    context_result = analyze_context()

    # 5. Calculate risk
    risk_level = calculate_risk(
        voice_score,
        speaker_result["speaker_score"],
        interaction_result["interaction_score"]
    )

    # 6. Calculate trust score
    trust_score = round(100 - risk_level)

    # 7. Final security decision
    if trust_score >= 75:
        decision = "SAFE — CONTINUE"
    elif trust_score >= 50:
        decision = "MONITOR"
    elif trust_score >= 25:
        decision = "VERIFY"
    else:
        decision = "BLOCK / ESCALATE"

    return {
        "trust_score": trust_score,
        "voice_score": voice_score,
        "speaker_score": speaker_result["speaker_score"],
        "interaction_score": interaction_result["interaction_score"],
        "context_score": context_result["context_score"],
        "risk_level": risk_level,
        "decision": decision,

        "voice_details": voice_result,
        "speaker_details": speaker_result,
        "interaction_details": interaction_result,
        "context_details": context_result
    }
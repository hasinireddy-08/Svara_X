from pydantic import BaseModel


class AnalysisResponse(BaseModel):
    trust_score: int
    voice_score: int
    speaker_score: int
    interaction_score: int
    context_score: int
    risk_level: int
    decision: str
    filename: str


class WebSocketAnalysisUpdate(BaseModel):
    type: str
    stage: str
    score: int
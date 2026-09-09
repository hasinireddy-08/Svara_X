# Speaker Verification Backend Contract

## Purpose

The Speaker Verification module compares a registered/reference
speaker's voice with an incoming voice sample and returns a
similarity score and speaker classification.

The module is implemented using a pretrained SpeechBrain
ECAPA-TDNN speaker recognition model.

---

## Backend Adapter

The backend should use the following function:

```python
from ml.speaker.backend_adapter import verify_speaker_for_backend

result = verify_speaker_for_backend(
    reference_audio,
    incoming_audio
)
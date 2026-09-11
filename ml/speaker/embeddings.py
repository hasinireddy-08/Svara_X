"""
Speaker embedding generation.

This module converts an audio recording into a speaker embedding
using the pretrained ECAPA-TDNN model from SpeechBrain.
"""

from pathlib import Path

import torch
import torchaudio
from speechbrain.inference.speaker import EncoderClassifier


MODEL_SOURCE = "speechbrain/spkrec-ecapa-voxceleb"
DEVICE = "cpu"
TARGET_SAMPLE_RATE = 16000


class SpeakerEmbedder:
    """Generate speaker embeddings from audio files."""

    def __init__(self):
        """Load the pretrained ECAPA-TDNN speaker model."""

        self.model = EncoderClassifier.from_hparams(
            source=MODEL_SOURCE,
            run_opts={"device": DEVICE},
        )

    def _load_audio(self, audio_path: str) -> torch.Tensor:
        """
        Load and prepare audio for the speaker model.

        The model expects:
        - mono audio
        - 16 kHz sample rate
        """

        waveform, sample_rate = torchaudio.load(audio_path)

        # Convert stereo/multi-channel audio to mono.
        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)

        # Resample if necessary.
        if sample_rate != TARGET_SAMPLE_RATE:
            resampler = torchaudio.transforms.Resample(
                orig_freq=sample_rate,
                new_freq=TARGET_SAMPLE_RATE,
            )
            waveform = resampler(waveform)

        # encode_batch expects [batch, time].
        waveform = waveform.squeeze(0).unsqueeze(0)

        return waveform

    def get_embedding(self, audio_path: str) -> torch.Tensor:
        """
        Generate a speaker embedding from an audio file.

        Args:
            audio_path: Path to the audio file.

        Returns:
            A 192-dimensional speaker embedding.

        Raises:
            FileNotFoundError: If the audio file doesn't exist.
            ValueError: If the path is not a file.
        """

        path = Path(audio_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Audio file not found: {audio_path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Audio path is not a file: {audio_path}"
            )

        waveform = self._load_audio(str(path))

        with torch.no_grad():
            embedding = self.model.encode_batch(waveform)

        return embedding.squeeze().detach().cpu()


_default_embedder = None


def get_speaker_embedding(audio_path: str) -> torch.Tensor:
    """
    Generate a speaker embedding from an audio file.

    The model is loaded once and reused for later calls.
    """

    global _default_embedder

    if _default_embedder is None:
        _default_embedder = SpeakerEmbedder()

    return _default_embedder.get_embedding(audio_path)
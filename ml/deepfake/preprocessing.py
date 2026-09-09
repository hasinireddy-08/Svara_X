import librosa
import numpy as np


def load_audio(audio_path, sample_rate=16000):
    """
    Load an audio file and convert it to 16 kHz mono audio.
    """

    try:
        audio, sr = librosa.load(
            audio_path,
            sr=sample_rate,
            mono=True
        )

        return audio, sr

    except Exception as e:
        raise ValueError(f"Could not process audio file: {str(e)}")


def extract_audio_features(audio, sr):
    """
    Extract basic audio features for deepfake analysis.
    """

    duration = len(audio) / sr

    rms_energy = np.mean(
        librosa.feature.rms(y=audio)
    )

    zero_crossing_rate = np.mean(
        librosa.feature.zero_crossing_rate(y=audio)
    )

    spectral_centroid = np.mean(
        librosa.feature.spectral_centroid(
            y=audio,
            sr=sr
        )
    )

    return {
        "duration": float(duration),
        "rms_energy": float(rms_energy),
        "zero_crossing_rate": float(zero_crossing_rate),
        "spectral_centroid": float(spectral_centroid)
    }
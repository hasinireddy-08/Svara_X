import librosa
import numpy as np


def load_audio(audio_path, sample_rate=16000):
    """
    Load audio and convert it to mono 16 kHz.
    """

    try:
        audio, sr = librosa.load(
            audio_path,
            sr=sample_rate,
            mono=True
        )

        return audio, sr

    except Exception as e:
        raise ValueError(
            f"Could not process audio file: {str(e)}"
        )


def extract_audio_features(audio, sr):
    """
    Extract acoustic features useful for
    prototype synthetic-speech detection.
    """

    duration = len(audio) / sr

    rms = librosa.feature.rms(y=audio)

    zcr = librosa.feature.zero_crossing_rate(audio)

    spectral_centroid = librosa.feature.spectral_centroid(
        y=audio,
        sr=sr
    )

    spectral_bandwidth = librosa.feature.spectral_bandwidth(
        y=audio,
        sr=sr
    )

    spectral_rolloff = librosa.feature.spectral_rolloff(
        y=audio,
        sr=sr
    )

    mfcc = librosa.feature.mfcc(
        y=audio,
        sr=sr,
        n_mfcc=13
    )

    return {
        "duration": float(duration),

        "rms_energy": float(np.mean(rms)),

        "zero_crossing_rate": float(np.mean(zcr)),

        "spectral_centroid": float(
            np.mean(spectral_centroid)
        ),

        "spectral_bandwidth": float(
            np.mean(spectral_bandwidth)
        ),

        "spectral_rolloff": float(
            np.mean(spectral_rolloff)
        ),

        "mfcc_mean": float(
            np.mean(mfcc)
        ),

        "mfcc_std": float(
            np.std(mfcc)
        )
    }
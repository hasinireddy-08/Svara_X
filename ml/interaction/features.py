import librosa
import numpy as np


def load_audio(audio_path, sample_rate=16000):
    """Load audio as mono at a fixed sample rate."""

    audio, sr = librosa.load(
        audio_path,
        sr=sample_rate,
        mono=True
    )

    if len(audio) == 0:
        raise ValueError("Audio file is empty")

    return audio, sr


def calculate_duration(audio, sr):
    """Calculate audio duration in seconds."""

    return float(len(audio) / sr)


def calculate_pause_ratio(audio):
    """Estimate the proportion of low-amplitude audio."""

    if len(audio) == 0:
        return 0.0

    threshold = 0.02

    silent_samples = np.sum(
        np.abs(audio) < threshold
    )

    return float(
        silent_samples / len(audio)
    )


def calculate_pitch_variation(audio, sr):
    """Estimate relative pitch variation."""

    pitches, magnitudes = librosa.piptrack(
        y=audio,
        sr=sr
    )

    pitch_values = []

    for i in range(pitches.shape[1]):

        index = magnitudes[:, i].argmax()

        pitch = pitches[index, i]

        if pitch > 0:
            pitch_values.append(pitch)

    if len(pitch_values) < 2:
        return 0.0

    pitch_values = np.array(pitch_values)

    mean_pitch = np.mean(pitch_values)

    if mean_pitch <= 0:
        return 0.0

    return float(
        np.std(pitch_values) / mean_pitch
    )


def calculate_energy_variation(audio):
    """Measure variation in audio energy."""

    if len(audio) == 0:
        return 0.0

    rms = librosa.feature.rms(
        y=audio
    )[0]

    return float(
        np.std(rms)
    )


def calculate_speech_rate_proxy(audio, sr):
    """
    Estimate speech activity.

    This is a proxy based on active audio
    frames, not an exact words-per-second
    measurement.
    """

    if len(audio) == 0:
        return 0.0

    hop_length = 512

    rms = librosa.feature.rms(
        y=audio,
        hop_length=hop_length
    )[0]

    threshold = np.mean(rms) * 0.5

    active_frames = np.sum(
        rms > threshold
    )

    duration = len(audio) / sr

    if duration <= 0:
        return 0.0

    return float(
        active_frames / duration
    )


def extract_voice_features(audio_path):
    """Extract all interaction-analysis features."""

    audio, sr = load_audio(audio_path)

    duration = calculate_duration(
        audio,
        sr
    )

    speech_rate = calculate_speech_rate_proxy(
        audio,
        sr
    )

    pause_ratio = calculate_pause_ratio(
        audio
    )

    pitch_variation = calculate_pitch_variation(
        audio,
        sr
    )

    energy_variation = calculate_energy_variation(
        audio
    )

    return {
        "duration": round(duration, 3),
        "speech_rate": round(speech_rate, 3),
        "pause_ratio": round(pause_ratio, 3),
        "pitch_variation": round(
            pitch_variation,
            3
        ),
        "energy_variation": round(
            energy_variation,
            3
        )
    }
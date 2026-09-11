import torch
import librosa

from transformers import (
    AutoFeatureExtractor,
    AutoModelForAudioClassification
)


MODEL_NAME = "garystafford/wav2vec2-deepfake-voice-detector"


print("Loading AI voice detection model...")

device = "cuda" if torch.cuda.is_available() else "cpu"

feature_extractor = AutoFeatureExtractor.from_pretrained(
    MODEL_NAME
)

model = AutoModelForAudioClassification.from_pretrained(
    MODEL_NAME
)

model.to(device)
model.eval()

print(f"AI voice detector loaded on: {device}")


def detect_ai_voice(audio_path):

    try:

        # --------------------------------
        # 1. Load audio
        # --------------------------------

        audio, sample_rate = librosa.load(
            audio_path,
            sr=16000,
            mono=True
        )

        if len(audio) == 0:
            raise ValueError("Audio file is empty")


        # --------------------------------
        # 2. Convert audio to model input
        # --------------------------------

        inputs = feature_extractor(
            audio,
            sampling_rate=16000,
            return_tensors="pt"
        )


        # --------------------------------
        # 3. Move input to CPU/GPU
        # --------------------------------

        inputs = {
            key: value.to(device)
            for key, value in inputs.items()
        }


        # --------------------------------
        # 4. Run AI voice detection
        # --------------------------------

        with torch.no_grad():

            outputs = model(**inputs)

            probabilities = torch.softmax(
                outputs.logits,
                dim=1
            )


        # --------------------------------
        # 5. Get prediction
        # --------------------------------

        predicted_class = torch.argmax(
            probabilities,
            dim=1
        ).item()

        confidence = probabilities[
            0
        ][predicted_class].item()


        # --------------------------------
        # 6. Get model label
        # --------------------------------

        label = model.config.id2label[
            predicted_class
        ]

        label_lower = label.lower()


        # --------------------------------
        # 7. Convert model label
        #    into our application label
        # --------------------------------

        if (
            "fake" in label_lower
            or "spoof" in label_lower
            or "deepfake" in label_lower
            or "synthetic" in label_lower
        ):

            result = "AI_GENERATED"

        else:

            result = "REAL_HUMAN"


        # --------------------------------
        # 8. Prepare probabilities
        # --------------------------------

        probability_result = {}

        for index, model_label in model.config.id2label.items():

            probability_result[model_label] = round(
                probabilities[0][index].item(),
                4
            )


        # --------------------------------
        # 9. Return result
        # --------------------------------

        return {

            "label": result,

            "model_label": label,

            "confidence": round(
                confidence,
                4
            ),

            "probabilities": probability_result

        }


    except Exception as e:

        return {

            "label": "ERROR",

            "model_label": "",

            "confidence": 0.0,

            "probabilities": {},

            "error": str(e)

        }
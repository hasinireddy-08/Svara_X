from ml.deepfake.detector import analyze_deepfake

audio_file = "sample.wav"

result = analyze_deepfake(audio_file)

print("Deepfake Detection Result")
print("--------------------------")
print("Score:", result["score"])
print("Label:", result["label"])
print("Confidence:", result["confidence"])
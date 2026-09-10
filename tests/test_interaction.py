from ml.interaction.analyzer import analyze_interaction


AUDIO_PATH = "demo/sample.wav"


def main():

    print("Starting interaction analysis...")
    print()

    result = analyze_interaction(
        AUDIO_PATH
    )

    print("Interaction Analysis Result:")
    print(result)

    print()
    print("Anomaly Score:")
    print(result.get("anomaly_score"))

    print()
    print("Features:")
    print(result.get("features"))


if __name__ == "__main__":
    main()
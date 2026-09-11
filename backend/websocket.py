import asyncio
import json

from fastapi import WebSocket


async def handle_websocket(websocket: WebSocket):
    await websocket.accept()

    print("SVARA-X WebSocket connected")

    try:
        while True:
            message = await websocket.receive()

            # Browser sends JSON messages
            if "text" in message and message["text"] is not None:

                data = json.loads(message["text"])

                if data.get("type") == "start_analysis":

                    print("Live voice analysis started")

                    await websocket.send_json({
                        "type": "status",
                        "message": "Live audio stream connected"
                    })

                    stages = [
                        {
                            "stage": "VOICE AUTHENTICITY",
                            "score": 88
                        },
                        {
                            "stage": "SPEAKER VERIFICATION",
                            "score": 95
                        },
                        {
                            "stage": "INTERACTION DNA",
                            "score": 79
                        },
                        {
                            "stage": "CONTEXT INTELLIGENCE",
                            "score": 86
                        },
                    ]

                    for stage in stages:

                        await asyncio.sleep(1)

                        await websocket.send_json({
                            "type": "analysis_update",
                            "stage": stage["stage"],
                            "score": stage["score"]
                        })

                    await websocket.send_json({
                        "type": "complete",
                        "trust_score": 91,
                        "risk_level": 9,
                        "decision": "SAFE — CONTINUE"
                    })

            # Browser sends audio chunks
            elif "bytes" in message and message["bytes"] is not None:

                audio_chunk = message["bytes"]

                print(
                    f"Received live audio chunk: "
                    f"{len(audio_chunk)} bytes"
                )

    except Exception as e:

        print("WebSocket connection closed:", e)
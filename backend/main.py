from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import os
import shutil
import tempfile

from backend.services.interaction_service import run_interaction_analysis


app = FastAPI(
    title="Svara X Voice Detection API",
    description="AI-generated voice and interaction analysis API",
    version="1.0.0"
)


# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Svara X Voice Detection API is running"
    }


@app.post("/analyze")
async def analyze_voice(
    file: UploadFile = File(...)
):

    # Create temporary file
    suffix = os.path.splitext(file.filename)[1] or ".wav"

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as temp_file:

        shutil.copyfileobj(
            file.file,
            temp_file
        )

        temp_path = temp_file.name

    try:

        # Run your existing AI voice detector
        result = run_interaction_analysis(
            temp_path
        )

        return result

    finally:

        # Delete temporary audio
        if os.path.exists(temp_path):
            os.remove(temp_path)
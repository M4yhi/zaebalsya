import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
import librosa
from pyAudioAnalysis import audioTrainTest as aT

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_GENRE_PATH = "models/genreClassifier"
MODEL_MOOD_PATH = "models/moodClassifier"
MODEL_TYPE = "svm"

@app.on_event("startup")
def startup_event():
    os.makedirs("temp", exist_ok=True)
    if not os.path.isdir(MODEL_GENRE_PATH):
        raise RuntimeError(f"Genre model not found at {MODEL_GENRE_PATH}")
    if not os.path.isdir(MODEL_MOOD_PATH):
        raise RuntimeError(f"Mood model not found at {MODEL_MOOD_PATH}")

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".mp3", ".wav")):
        raise HTTPException(status_code=400, detail="Unsupported file type")
    file_path = os.path.join("temp", file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    y, sr = librosa.load(file_path, sr=None, mono=True)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    bpm = float(np.round(tempo, 2))

    [genre_label, _] = aT.file_classification(file_path, MODEL_GENRE_PATH, MODEL_TYPE)
    [mood_label, _]  = aT.file_classification(file_path, MODEL_MOOD_PATH,  MODEL_TYPE)

    os.remove(file_path)
    return JSONResponse(content={"bpm": bpm, "genre": genre_label, "mood": mood_label})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

# voice_test.py
import os
from pathlib import Path
from dotenv import load_dotenv
from elevenlabs import ElevenLabs

load_dotenv()
api_key = os.getenv("ELEVEN_API_KEY")
if not api_key:
    raise RuntimeError("ELEVEN_API_KEY missing in .env")

client = ElevenLabs(api_key=api_key)

# (A) Get a voice_id by name (e.g., "Emily")
def get_voice_id_by_name(name: str) -> str:
    voices = client.voices.get_all().voices
    for v in voices:
        if v.name.lower() == name.lower():
            return v.voice_id
    raise ValueError(f'Voice "{name}" not found. Available: {[v.name for v in voices]}')

voice_id = "LcfcDJNUP1GQjkzn1xUU" # pick any voice name you like
model_id = "eleven_multilingual_v2"      # good general model

# (B) Convert text → speech (returns chunks)
audio_stream = client.text_to_speech.convert(
    voice_id=voice_id,
    model_id=model_id,
    text="Hello, my name is Solace. Can you hear me?"
)

# (C) Save & play with default player (avoids simpleaudio issues)
out = Path("solace_hello.mp3")
with open(out, "wb") as f:
    for chunk in audio_stream:
        if chunk:  # some SDKs yield empty keep-alives
            f.write(chunk)

os.startfile(out)  # Windows: opens default player
print(f"Saved and playing: {out.resolve()}")

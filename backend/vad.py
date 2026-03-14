import numpy as np
from silero_vad import load_silero_vad, get_speech_timestamps
from config import SAMPLE_RATE

model = load_silero_vad()

def detect_speech(audio_bytes):

    audio = np.frombuffer(audio_bytes, dtype=np.int16).astype("float32") / 32768

    timestamps = get_speech_timestamps(audio, model, sampling_rate=SAMPLE_RATE)

    return timestamps
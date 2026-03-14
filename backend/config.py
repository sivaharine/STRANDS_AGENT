import os
from dotenv import load_dotenv

load_dotenv()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

SARVAM_STT_WS = os.getenv("SARVAM_STT_WS")
SARVAM_TTS_WS = os.getenv("SARVAM_TTS_WS")

BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

MONGO_URI = os.getenv("MONGO_URI")

SAMPLE_RATE = 16000
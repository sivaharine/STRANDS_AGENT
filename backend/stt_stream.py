import websockets
import asyncio
import json
from config import SARVAM_STT_WS, SARVAM_API_KEY

async def transcribe(audio_bytes):

    headers = {"Authorization": f"Bearer {SARVAM_API_KEY}"}

    async with websockets.connect(SARVAM_STT_WS, extra_headers=headers) as ws:

        await ws.send(json.dumps({
            "type":"config",
            "encoding":"pcm_s16le",
            "sample_rate":16000
        }))

        await ws.send(audio_bytes)

        await ws.send(json.dumps({"type":"eof"}))

        transcript=""

        while True:

            msg = await ws.recv()

            data = json.loads(msg)

            if data["type"]=="transcript":

                transcript += data["text"]

            if data["type"]=="final":

                break

        return transcript
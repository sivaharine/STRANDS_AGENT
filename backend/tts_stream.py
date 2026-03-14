import websockets
import json
from config import SARVAM_TTS_WS, SARVAM_API_KEY

async def generate_audio(text):

    headers={"Authorization":f"Bearer {SARVAM_API_KEY}"}

    async with websockets.connect(SARVAM_TTS_WS,extra_headers=headers) as ws:

        await ws.send(json.dumps({
            "type":"config",
            "voice":"shreys",
            "sample_rate":16000
        }))

        await ws.send(json.dumps({
            "type":"text",
            "text":text
        }))

        await ws.send(json.dumps({"type":"flush"}))

        while True:

            msg = await ws.recv()

            if isinstance(msg,bytes):

                yield msg

            else:

                data=json.loads(msg)

                if data.get("type")=="end":

                    break
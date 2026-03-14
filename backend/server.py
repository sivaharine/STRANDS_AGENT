import json
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

# keep your real modules as-is
from stt_stream import transcribe
from tts_stream import generate_audio
from agent import run_agent
from vad import detect_speech

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    print("Client attempting connection...")
    await ws.accept()
    print("Client connected")
    await ws.send_text(json.dumps({"type":"status","message":"Started"}))

    buffer = b""
    try:
        while True:
            # wait for binary frames from client
            try:
                audio = await ws.receive_bytes()
            except RuntimeError:
                # transient issue reading bytes; continue
                continue
            buffer += audio

            # your VAD -> STT -> agent -> TTS flow
            speech = detect_speech(buffer)
            if not speech:
                continue

            await ws.send_text(json.dumps({"type":"status","message":"Processing"}))
            text = await transcribe(buffer)
            response = await run_agent(text)

            await ws.send_text(json.dumps({"type":"status","message":"Speaking"}))
            async for chunk in generate_audio(response):
                # send raw audio chunks (ArrayBuffer on client)
                await ws.send_bytes(chunk)

            buffer = b""
            await ws.send_text(json.dumps({"type":"status","message":"Listening"}))

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print("Server error:", repr(e))

if __name__ == "__main__":
    print("Server running on ws://127.0.0.1:8765/ws")
    uvicorn.run(app, host="127.0.0.1", port=8765)
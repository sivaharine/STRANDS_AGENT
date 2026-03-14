🎙 AI Voice Assistant

A real-time AI voice assistant built with FastAPI, WebSockets, Sarvam STT/TTS, and Strands Agents.
The system captures microphone audio, converts speech to text, processes it using an AI agent with tools, and streams the response back as audio.

🚀 Features

Real-time speech-to-text streaming

AI agent with tools (weather, calculator, web search, database)

Text-to-speech audio streaming

WebSocket-based communication

Voice activity detection for efficient processing

⚙️ Tech Stack

FastAPI

WebSockets

Sarvam STT & TTS

Strands Agents + AWS Bedrock

PyTorch (Silero VAD)

Dependencies are listed in req.txt.

📂 Project Files

server.py – WebSocket server handling audio pipeline

agent.py – AI agent configuration and tools

stt_stream.py – Speech-to-text streaming

tts_stream.py – Text-to-speech streaming

The WebSocket pipeline logic is implemented in server.py.

▶️ Run the Project
pip install -r req.txt
python server.py

Server runs at:

ws://127.0.0.1:8765/ws

import streamlit as st
import os

BACKEND_WS = os.getenv("BACKEND_WS", "ws://127.0.0.1:8765/ws")

st.title("Advanced Voice Assistant")

# inject script into top-level page (not in sandboxed iframe)
# starts audio capture only after websocket is open
html = f'''
<script>
console.log("JS started");

const WS_URL = "{BACKEND_WS}";
let ws = null;
let audioContext = null;
let processor = null;

function startWS() {{
  if (ws && (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)) return;

  ws = new WebSocket(WS_URL);
  ws.binaryType = "arraybuffer";

  ws.onopen = () => {{
    console.log("WebSocket connected");
    startMicAndStream();
  }};

  ws.onerror = (e) => {{
    console.error("WebSocket error", e);
  }};

  ws.onclose = () => {{
    console.log("WebSocket closed, reconnecting in 2s");
    stopMic();
    setTimeout(startWS, 2000);
  }};

  ws.onmessage = async (event) => {{
    if (typeof event.data === "string") {{
      console.log("text:", event.data);
      return;
    }}
    // binary audio chunk
    if (!audioContext) audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const arrayBuffer = await event.data.arrayBuffer();
    audioContext.decodeAudioData(arrayBuffer).then(buf => {{
      const src = audioContext.createBufferSource();
      src.buffer = buf;
      src.connect(audioContext.destination);
      src.start();
    }}).catch(e => console.error("decodeAudioData error", e));
  }};
}}

function startMicAndStream() {{
  if (processor) return; // already running

  navigator.mediaDevices.getUserMedia({{ audio: true }})
    .then(stream => {{
      audioContext = new (window.AudioContext || window.webkitAudioContext)({{ sampleRate: 16000 }});
      const source = audioContext.createMediaStreamSource(stream);

      // ScriptProcessor is deprecated but simpler cross-browser; buffer size tuned to 4096
      processor = audioContext.createScriptProcessor(4096, 1, 1);

      source.connect(processor);
      processor.connect(audioContext.destination);

      processor.onaudioprocess = (e) => {{
        if (!ws || ws.readyState !== WebSocket.OPEN) return;
        const input = e.inputBuffer.getChannelData(0);
        const int16 = new Int16Array(input.length);
        for (let i = 0; i < input.length; i++) {{
          let s = Math.max(-1, Math.min(1, input[i]));
          int16[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
        }}
        ws.send(int16.buffer);
      }};
    }})
    .catch(err => {{
      console.error("Microphone permission / error:", err);
    }});
}}

function stopMic() {{
  if (!processor) return;
  try {{
    processor.disconnect();
  }} catch(e){{}}
  processor = null;
}}

startWS();
</script>
'''

# use unsafe_allow_html to inject script at top-level (avoids about:srcdoc iframe)
st.markdown(html, unsafe_allow_html=True)

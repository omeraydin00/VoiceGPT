# VoiceGPT

A Turkish voice assistant: speak, and it answers in text and out loud.

Python · Whisper · Ollama (Llama 3) · gTTS · Gradio

<img alt="VoiceGPT answering a question" src="https://github.com/user-attachments/assets/6a21b0db-79ca-45e4-a306-bd110e35c112" />

Your recording is turned into text by Whisper, answered in short, natural Turkish by Llama 3 through Ollama, and read back with gTTS. Speech recognition and the language model run on your computer; only the answer text is sent to gTTS to be spoken.

> *"İstanbul'da gezmek için nereye gidebilirim?"*
> *"İstanbul'un birçok cazibe noktası var! Sultanahmet'i ziyaret etmelisiniz…"*

[Watch the demo on YouTube](https://www.youtube.com/watch?v=KPB3i5rgoHY)

## Running it

You need Python 3.10 or newer, [FFmpeg](https://ffmpeg.org/download.html) for Whisper, and [Ollama](https://ollama.com).

```bash
ollama pull llama3

git clone https://github.com/omeraydin00/VoiceGPT.git
cd VoiceGPT/VoiceGPT
pip install -r requirements.txt
python app.py
```

The interface opens at http://127.0.0.1:7860. Record a question and press Submit.

Change `model="llama3"` in `app.py` to use another Ollama model, or swap Whisper's `base` model for `tiny` (faster) or `small` (more accurate).

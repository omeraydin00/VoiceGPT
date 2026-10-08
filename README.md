<div align="center">

# VoiceGPT

**A Turkish voice assistant with local speech recognition and a local language model.**

Speak into the microphone, get a natural Turkish answer as text and as speech.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Whisper](https://img.shields.io/badge/Whisper-Speech%20to%20Text-412991?style=flat-square&logo=openai&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Llama%203-000000?style=flat-square&logo=ollama&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-UI-F97316?style=flat-square)
![gTTS](https://img.shields.io/badge/gTTS-Text%20to%20Speech-4285F4?style=flat-square&logo=google&logoColor=white)

[![VoiceGPT demo video](https://img.youtube.com/vi/KPB3i5rgoHY/hqdefault.jpg)](https://www.youtube.com/watch?v=KPB3i5rgoHY)

*Click the image to watch the demo.*

</div>

---

## How it works

```mermaid
flowchart LR
    M[🎙️ Microphone] --> W[Whisper base<br/>speech to text]
    W --> L[Llama 3 via Ollama<br/>Turkish answer]
    L --> T[Text answer]
    L --> G[gTTS<br/>text to speech]
    G --> S[🔊 Spoken answer]
```

| Step | Component | Runs |
|---|---|---|
| Speech to text | OpenAI Whisper (`base` model, Turkish) | Locally |
| Answer generation | Llama 3 through Ollama, with a system prompt for short, natural Turkish | Locally |
| Text to speech | gTTS | Uses Google's TTS service, needs an internet connection |
| Interface | Gradio, with microphone input and audio output | Locally |

Your voice and your question never leave the machine. Only the generated answer text is sent to gTTS to be turned into speech.

## Screenshots

<img alt="VoiceGPT interface" src="https://github.com/user-attachments/assets/32e8259f-c8b0-4af0-99a8-a6744c128b89" />

> **Question:** *"İstanbul'da gezmek için nereye gidebilirim?"*
> **Answer:** *"İstanbul'un birçok cazibe noktası var! Sultanahmet'i ziyaret etmelisiniz…"*

<img alt="VoiceGPT answer" src="https://github.com/user-attachments/assets/6a21b0db-79ca-45e4-a306-bd110e35c112" />

## Getting started

**Requirements:** Python 3.10+, [FFmpeg](https://ffmpeg.org/download.html) (needed by Whisper) and [Ollama](https://ollama.com).

```bash
# 1. Pull the model
ollama pull llama3

# 2. Clone and install
git clone https://github.com/omeraydin00/VoiceGPT.git
cd VoiceGPT/VoiceGPT
pip install -r requirements.txt

# 3. Run
python app.py
```

The interface opens at **http://127.0.0.1:7860**. Record your question and press submit.

## Customizing

- **Model:** change `model="llama3"` in `app.py` to `mistral`, `gemma` or any model you have in Ollama.
- **Speed vs. accuracy:** swap Whisper's `base` model for `tiny` (faster) or `small` / `medium` (more accurate).
- **Flagging:** the *Flag* button saves the audio, answer and spoken reply to `flagged/` as CSV for later review.

---

<div align="center">
Built by <a href="https://github.com/omeraydin00">Ömer Faruk Aydın</a>
</div>

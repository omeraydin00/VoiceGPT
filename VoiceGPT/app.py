# Gerekli kütüphaneleri içe aktar
import os
import tempfile

import gradio as gr
import ollama
import whisper
from gtts import gTTS

LLM = os.environ.get("VOICEGPT_MODEL", "llama3")  # Alternatif: "mistral", "gemma"
WHISPER = os.environ.get("VOICEGPT_WHISPER", "small")  # "base" daha hızlı, "medium" daha kaliteli

SYSTEM = (
    "Sen sade ve doğal Türkçe konuşan bir sesli asistansın. "
    "Cevapların sesli okunacak: kısa tut, en fazla üç cümle yaz, liste, başlık ya da emoji kullanma. "
    "Yanıtlarında doğru Türkçe karakterler (ç, ğ, ı, ö, ş, ü) kullan."
)

# 1. Whisper modelini yükle (local ses → metin)
model = whisper.load_model(WHISPER)


def text_of(message):
    # The chatbot sends messages back as a list of parts ({"type": "text", "text": ...})
    content = message["content"]
    if isinstance(content, str):
        return content
    return " ".join(part.get("text", "") for part in content if isinstance(part, dict))


# 2. Ollama LLM ile yanıt üret; önceki mesajlar da gider, böylece konuşma sürer
def generate_response_with_ollama(history):
    messages = [{"role": "system", "content": SYSTEM}]
    messages += [{"role": m["role"], "content": text_of(m)} for m in history if text_of(m)]
    response = ollama.chat(model=LLM, messages=messages, options={"temperature": 0.4})
    return response["message"]["content"].strip().strip('"')


# 3. gTTS ile yanıtı sese çevir
def speak(text):
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        gTTS(text=text, lang="tr").write_to_fp(f)
        return f.name


# 4. Ana işlem: ses ya da yazı al > cevapla > sese çevir
def reply(audio_path, typed, history):
    history = history or []
    if audio_path:
        try:
            user_text = model.transcribe(audio_path, language="tr")["text"].strip()
        except Exception as e:
            gr.Warning(f"Ses yazıya çevrilemedi: {e}")
            return history, None, "", None
    else:
        user_text = (typed or "").strip()
    if not user_text:
        return history, None, "", None

    history = history + [{"role": "user", "content": user_text}]
    try:
        answer = generate_response_with_ollama(history)
    except Exception as e:
        gr.Warning(f"Ollama'ya ulaşılamadı: {e}")
        return history, None, "", None
    history = history + [{"role": "assistant", "content": answer}]

    try:
        voice = speak(answer)
    except Exception as e:  # gTTS needs the internet; the text answer still shows
        gr.Warning(f"Sesli yanıt oluşturulamadı: {e}")
        voice = None
    return history, voice, "", None


CSS = """
.gradio-container { max-width: 980px !important; margin: 0 auto !important; }
#baslik h1 { margin-bottom: 0; font-size: 28px; letter-spacing: -0.5px; }
#baslik p { margin-top: 4px; color: var(--body-text-color-subdued); }
footer { display: none !important; }
"""

theme = gr.themes.Soft(primary_hue="orange", neutral_hue="stone", font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"]).set(
    block_label_background_fill="transparent",
    block_label_background_fill_dark="transparent",
    block_label_text_color="*body_text_color_subdued",
    block_label_text_color_dark="*body_text_color_subdued",
    block_label_border_width="0px",
)

# 5. Gradio arayüzü
with gr.Blocks(title="VoiceGPT") as demo:
    gr.Markdown(
        f"# VoiceGPT\nTürkçe sorun, sesli cevap alın. Konuşma tanıma Whisper ({WHISPER}), cevaplar {LLM} ile bu bilgisayarda üretilir.",
        elem_id="baslik",
    )
    chat = gr.Chatbot(label="Konuşma", height=420, buttons=["copy"], placeholder="Mikrofona basıp bir şey sorun, ya da aşağıya yazın.")
    with gr.Row(equal_height=True):
        mic = gr.Audio(sources=["microphone", "upload"], type="filepath", label="Konuşun", scale=3)
        with gr.Column(scale=2):
            typed = gr.Textbox(label="ya da yazın", placeholder="Örn. İstanbul'da nereleri gezmeliyim?", lines=1, max_lines=3)
            with gr.Row():
                send = gr.Button("Gönder", variant="primary")
                new = gr.Button("Yeni konuşma")
    voice = gr.Audio(label="Sesli yanıt", autoplay=True, interactive=False)

    outputs = [chat, voice, typed, mic]
    mic.stop_recording(reply, [mic, typed, chat], outputs)
    mic.upload(reply, [mic, typed, chat], outputs)
    send.click(reply, [gr.State(None), typed, chat], outputs)
    typed.submit(reply, [gr.State(None), typed, chat], outputs)
    new.click(lambda: ([], None, "", None), None, outputs)

# 6. Uygulamayı başlat
if __name__ == "__main__":
    demo.launch(theme=theme, css=CSS)

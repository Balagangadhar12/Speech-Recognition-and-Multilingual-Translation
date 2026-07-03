import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import speech_recognition as sr
from googletrans import Translator
import pyttsx3 as ts
from gtts import gTTS
import os
import subprocess
import tempfile
from PIL import Image, ImageTk

# Initialize TTS
engine = ts.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

# Languages (main Indian + English)
languages = {
    'English': 'en',
    'Hindi': 'hi',
    'Telugu': 'te',
    'Tamil': 'ta',
    'Malayalam': 'ml',
    'Kannada': 'kn',
    'Bengali': 'bn',
    'Marathi': 'mr',
    'Gujarati': 'gu',
    'Punjabi': 'pa',
    'Urdu': 'ur'
}

# Reverse lookup for displaying detected input language
lang_names = {v: k for k, v in languages.items()}

translator = Translator()
last_recognized_text = ""  # store recognized text globally

def convert_to_wav(input_file):
    """Convert any audio to temporary WAV using ffmpeg"""
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    command = ["ffmpeg", "-y", "-i", input_file, "-ar", "16000", "-ac", "1", temp_wav.name]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return temp_wav.name

def set_detected_language(text):
    """Detect input language using googletrans"""
    try:
        detection = translator.detect(text)
        detected_code = detection.lang
        detected_language = lang_names.get(detected_code, detected_code)
        detected_lang_var.set(f"Detected: {detected_language}")
    except Exception:
        detected_lang_var.set("Detected: Unknown")

def recognize_speech():
    """Listen from microphone with full-sentence support"""
    global last_recognized_text
    recognizer = sr.Recognizer()
    full_text = ""
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1.5)
            print("Listening... Speak your full sentence.")

            while True:
                try:
                    audio = recognizer.listen(source, timeout=2, phrase_time_limit=8)
                    text = recognizer.recognize_google(audio)
                    full_text += " " + text
                except sr.WaitTimeoutError:
                    break
                except sr.UnknownValueError:
                    break

        last_recognized_text = full_text.strip()
        recognized_text_var.set(last_recognized_text)

        set_detected_language(last_recognized_text)

        engine.say(last_recognized_text)
        engine.runAndWait()

        translate_text()

    except sr.RequestError as e:
        messagebox.showerror("Error", f"Could not request results; {e}")

def recognize_from_file():
    """Recognize speech from uploaded audio file"""
    global last_recognized_text
    file_path = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.wav *.mp3 *.m4a *.flac *.aac *.ogg")]
    )
    if not file_path:
        return

    try:
        wav_file = convert_to_wav(file_path)
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_file) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)
        last_recognized_text = text
        recognized_text_var.set(last_recognized_text)

        set_detected_language(last_recognized_text)

        engine.say(last_recognized_text)
        engine.runAndWait()

        translate_text()
    except Exception as e:
        messagebox.showerror("Error", f"Could not process file: {e}")

def translate_text(event=None):
    global last_recognized_text
    if not last_recognized_text:
        return

    target_choice = language_var.get()
    if target_choice == "None":
        return

    target_lang = languages[target_choice]
    try:
        trans = translator.translate(last_recognized_text, dest=target_lang)
        translated_text_var.set(trans.text)

        # Save audio
        tts = gTTS(text=trans.text, lang=target_lang, slow=False)
        tts.save("output.mp3")
        play_audio_button.config(state=tk.NORMAL)
    except Exception as e:
        messagebox.showerror("Translation Error", str(e))

def play_audio():
    os.system("start output.mp3")

# GUI setup
win = tk.Tk()
win.title("Voice Assistant - Full Sentence Recognition")
win.geometry("350x600")
bg_color = "#100720"
fg_color = "#61dafb"
win.configure(bg=bg_color)

recognized_text_var = tk.StringVar()
translated_text_var = tk.StringVar()
detected_lang_var = tk.StringVar()
language_var = tk.StringVar(value='English')  # default to English

# Load icons (resize to smaller size ~70px like screenshot)
mic = ImageTk.PhotoImage(Image.open("mic.png").resize((70, 70)))
speak = ImageTk.PhotoImage(Image.open("speaker.png").resize((70, 70)))

# Widgets
tk.Button(win, image=mic, command=recognize_speech,
          bg=bg_color, border=0, activebackground='grey').pack(pady=10)

tk.Button(win, text="Upload Audio", command=recognize_from_file,
          bg="#222244", fg="white", font=("Helvetica", 12)).pack(pady=5)

tk.Label(win, text="Recognized Text", font=("Helvetica", 14),
         bg=bg_color, fg='#FFBF61').pack(pady=5)
tk.Label(win, textvariable=recognized_text_var, wraplength=600,
         font=("Helvetica", 16), bg=bg_color, fg='#F36886').pack(pady=5)

tk.Label(win, textvariable=detected_lang_var, font=("Helvetica", 12),
         bg=bg_color, fg="lightgreen").pack(pady=5)

tk.Label(win, text="Select Output Language", font=("Helvetica", 14),
         bg=bg_color, fg=fg_color).pack(pady=10)
language_menu = ttk.Combobox(win, textvariable=language_var,
                             values=list(languages.keys()), font=("Helvetica", 10), width=10)
language_menu.pack(pady=10)
language_menu.bind("<<ComboboxSelected>>", translate_text)

tk.Label(win, text="Translated Text", font=("Helvetica", 14),
         bg=bg_color, fg='#FFBF61').pack(pady=10)
tk.Label(win, textvariable=translated_text_var, wraplength=600,
         font=("Helvetica", 16), bg=bg_color, fg='#F36886').pack(pady=10)

play_audio_button = tk.Button(win, image=speak, command=play_audio,
                              bg=bg_color, state=tk.DISABLED, border=0, activebackground='grey')
play_audio_button.pack(pady=20)

win.mainloop()

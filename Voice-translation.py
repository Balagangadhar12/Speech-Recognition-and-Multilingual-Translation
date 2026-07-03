import tkinter as tk
from tkinter import messagebox, ttk
import speech_recognition as sr
from googletrans import Translator
import pyttsx3 as ts
from gtts import gTTS
import os
import webbrowser as wb
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

def recognize_speech():
    global last_recognized_text
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)

        # Auto-detect input language
        text = recognizer.recognize_google(audio)  
        last_recognized_text = text  # store for future translations
        recognized_text_var.set(text)

        # Detect language
        detection = translator.detect(text)
        detected_code = detection.lang
        detected_language = lang_names.get(detected_code, detected_code)
        detected_lang_var.set(f"Detected: {detected_language}")

        # Say recognized text
        engine.say(text)
        engine.runAndWait()

        # Translate immediately with selected output
        translate_text()

    except sr.UnknownValueError:
        messagebox.showerror("Error", "Sorry, could not understand the audio.")
    except sr.RequestError as e:
        messagebox.showerror("Error", f"Could not request results; {e}")

def translate_text(event=None):
    """Translate stored text whenever output language changes"""
    global last_recognized_text
    if not last_recognized_text:
        return

    target_choice = language_var.get()
    if target_choice == "None":
        return

    target_lang = languages[target_choice]
    trans = translator.translate(last_recognized_text, dest=target_lang)
    translated = trans.text
    translated_text_var.set(translated)

    # Save as audio
    tts = gTTS(text=translated, lang=target_lang, slow=False)
    tts.save("output.mp3")
    play_audio_button.config(state=tk.NORMAL)

def play_audio():
    os.system("start output.mp3")

# GUI setup
win = tk.Tk()
win.title("Voice Assistant - Auto Detect Input")
win.geometry("350x550")
bg_color = "#100720"
fg_color = "#61dafb"
win.configure(bg=bg_color)

recognized_text_var = tk.StringVar()
translated_text_var = tk.StringVar()
detected_lang_var = tk.StringVar()
language_var = tk.StringVar(value='None')

# Images
p1 = Image.open('mic.jpg')
mic = ImageTk.PhotoImage(p1)
p2 = Image.open("speaker.jpg")
speak = ImageTk.PhotoImage(p2)

# Widgets
tk.Button(win, image=mic, command=recognize_speech,
          bg=bg_color, border=0, activebackground='grey').pack(pady=10)

tk.Label(win, text="Recognized Text", font=("Helvetica", 14),
         bg=bg_color, fg='#FFBF61').pack(pady=5)
tk.Label(win, textvariable=recognized_text_var, wraplength=600,
         font=("Helvetica", 16), bg=bg_color, fg='#F36886').pack(pady=5)

# Detected language display
tk.Label(win, textvariable=detected_lang_var, font=("Helvetica", 12),
         bg=bg_color, fg="lightgreen").pack(pady=5)

tk.Label(win, text="Select Output Language", font=("Helvetica", 14),
         bg=bg_color, fg=fg_color).pack(pady=10)
language_menu = ttk.Combobox(win, textvariable=language_var,
                             values=list(languages.keys()), font=("Helvetica", 10), width=10)
language_menu.pack(pady=10)

# Bind translation when language is changed
language_menu.bind("<<ComboboxSelected>>", translate_text)

tk.Label(win, text="Translated Text", font=("Helvetica", 14),
         bg=bg_color, fg='#FFBF61').pack(pady=10)
tk.Label(win, textvariable=translated_text_var, wraplength=600,
         font=("Helvetica", 16), bg=bg_color, fg='#F36886').pack(pady=10)

play_audio_button = tk.Button(win, image=speak, command=play_audio,
                              bg=bg_color, state=tk.DISABLED, border=0, activebackground='grey')
play_audio_button.pack(pady=20)

win.mainloop()




# import speech_recognition as sr
# from googletrans import Translator
# import pyttsx3 as ts
# from gtts import gTTS
# import os
# import webbrowser as wb


# recognizer = sr.Recognizer()
# Translator=Translator()
# engn=ts.init()
# voices = engn.getProperty('voices')
# engn.setProperty('voice', voices[0].id)  # 0 for male, 1 for female
# engn.setProperty('rate', 150)


# with sr.Microphone() as source:
#     print("Listening...")
#     recognizer.adjust_for_ambient_noise(source)
#     audio= recognizer.listen(source)

#     try:
#         text = recognizer.recognize_google(audio)
#         text=text.lower()
#         if(text.startswith('open')):
#             print("You said:", text)
#             website=text.split()[1]
#             url='www.'+website+'.com'
#             engn.say('opening '+website)
#             engn.runAndWait()
#             wb.open(url)           
#         else:
#             print("You said:", text)
#             engn.say(text)
#             engn.runAndWait()
#             trans=Translator.translate(text,src='en',dest='hindi')
#             print('\n Translated text: ',trans.text)
#             # engn.say(trans)
#             tts = gTTS(text=trans.text, lang='hi', slow=False)
#             tts.save("output.mp3")
#             os.system("start output.mp3")


#     except sr.WaitTimeoutError:
#         print("input not served for long time")
#     except sr.UnknownValueError:
#         print("Sorry, could not understand")
#     except sr.RequestError as e:
#         print("Error: Could not request results ")
    



# import pyttsx3
# import pyaudio
# import speech_recognition as sr

# listener=sr.Recognizer()

# with sr.Microphone() as source:
#     print("Listening...")
#     voice=listener.listen(source)
#     command=listener.recognize_google(voice)
#     command=command.lower()
#     print(command)


# # Initialize the recognizer 
# r = sr.Recognizer() 

# # Function to convert text to
# # speech
# def SpeakText(command):
    
#     # Initialize the engine
#     engine = pyttsx3.init()
#     engine.say(command) 
#     engine.runAndWait()
    
    
# # Loop infinitely for user to
# # speak

# while(1):    
    
#     # Exception handling to handle
#     # exceptions at the runtime
#     try:
        
#         # use the microphone as source for input.
#         with sr.Microphone() as source2:
            
#             # wait for a second to let the recognizer
#             # adjust the energy threshold based on
#             # the surrounding noise level 
#             r.adjust_for_ambient_noise(source2, duration=0.2)
            
#             #listens for the user's input 
#             audio2 = r.listen(source2)
            
#             # Using google to recognize audio
#             MyText = r.recognize_google(audio2)
#             MyText = MyText.lower()

#             print("Did you say ",MyText)
#             SpeakText(MyText)
            
#     except sr.RequestError as e:
#         print("Could not request results; {0}".format(e))
        
#     except sr.UnknownValueError:
#         print("unknown error occurred")
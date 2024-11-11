import pyperclip
from gtts import gTTS
import os
import tkinter as tk
from tkinter import messagebox

# Variabele om de laatste gelezen tekst bij te houden
last_text = ""

def get_text_from_clipboard():
    """Haal tekst op uit het klembord."""
    return pyperclip.paste()

def speak_text():
    """Zet tekst om in spraak en speel het af als het nieuwe tekst is."""
    global last_text
    text = get_text_from_clipboard()
    
    if text and text != last_text:  # Controleer of de tekst nieuw is
        tts = gTTS(text=text, lang='nl')
        tts.save("speech.mp3")
        
        # Gebruik het juiste afspeelcommando afhankelijk van je besturingssysteem
        if os.name == "posix":  # macOS/Linux
            os.system("afplay speech.mp3")
        elif os.name == "nt":  # Windows
            os.system("start speech.mp3")
        
        # Update de laatste tekst
        last_text = text
        messagebox.showinfo("Voorlezen", "Voorlezen voltooid.")
    elif text == last_text:
        messagebox.showinfo("Opmerking", "De geselecteerde tekst is al voorgelezen.")
    else:
        messagebox.showwarning("Fout", "Geen tekst gevonden op het klembord.")

# GUI setup
app = tk.Tk()
app.title("Tekst Voorlezer")

read_button = tk.Button(app, text="Voorlezen", command=speak_text)
read_button.pack(pady=20)

app.mainloop()

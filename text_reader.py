import sys
import pyperclip
import os
import requests
from gtts import gTTS
from PyQt5 import QtWidgets, QtCore
from pynput import mouse

last_text = ""  # Variabele om de laatste tekst bij te houden

def simplify_text(text):
    # API-url voor het BART-model op Hugging Face
    api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": "Bearer YOUR_HUGGING_FACE_API_KEY"}  # Vervang met je eigen API-sleutel

    data = {
        "inputs": text,
        "parameters": {"max_length": 50, "min_length": 25, "do_sample": False},
    }

    response = requests.post(api_url, headers=headers, json=data)
    print("Statuscode van de API-response:", response.status_code)  # Print de statuscode voor debugging
    print("API-response inhoud:", response.json())  # Print de volledige response voor debugging

    if response.status_code == 200:
        # Pak de vereenvoudigde tekst uit de response
        simplified_text = response.json()[0].get("summary_text", "Geen uitleg gevonden")
        return simplified_text
    else:
        return "Sorry, de tekst kan momenteel niet worden uitgelegd."

class TextReaderApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # Instellingen voor het venster
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.setFixedSize(200, 100)

        # Knop voor voorlezen
        self.button_read = QtWidgets.QPushButton("Voorlezen", self)
        self.button_read.clicked.connect(self.speak_text)
        self.button_read.setGeometry(10, 10, 80, 30)

        # Knop voor uitleg
        self.button_explain = QtWidgets.QPushButton("Uitleg", self)
        self.button_explain.clicked.connect(self.explain_text)
        self.button_explain.setGeometry(110, 10, 80, 30)

        # Timer om het klembord regelmatig te controleren
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check_clipboard)
        self.timer.start(1000)  # Controleer elke seconde

    def check_clipboard(self):
        """Controleer het klembord voor nieuwe tekst en toon het menu."""
        global last_text
        text = pyperclip.paste()

        if text and text != last_text:
            last_text = text
            self.show_menu_at_cursor()

    def show_menu_at_cursor(self):
        """Plaats het menu naast de cursorpositie en breng het naar de voorgrond."""
        cursor_position = mouse.Controller().position
        self.move(int(cursor_position[0]), int(cursor_position[1]) + 20)  # Plaats onder de cursor
        self.show()  # Toon het venster
        self.raise_()  # Breng het venster naar de voorgrond
        self.activateWindow()  # Focus het venster

    def speak_text(self):
        """Lees de tekst voor met gTTS en speel het af zonder het venster te sluiten."""
        text = pyperclip.paste()
        if text:
            tts = gTTS(text=text, lang='nl')
            tts.save("speech.mp3")

            if os.name == "posix":  # macOS/Linux
                os.system("afplay speech.mp3")
            elif os.name == "nt":  # Windows
                os.system("start speech.mp3")
        
        # self.hide() is verwijderd zodat het venster open blijft

    def explain_text(self):
        """Vereenvoudig en toon de tekst zonder het venster te sluiten."""
        text = pyperclip.paste()
        print("Tekst op het klembord:", text)  # Print de tekst op het klembord naar de terminal
        if text:
            simplified_text = simplify_text(text)
            QtWidgets.QMessageBox.information(self, "Uitleg", simplified_text)
        
        # self.hide() is verwijderd zodat het venster open blijft

# Start de PyQt5-applicatie
app = QtWidgets.QApplication(sys.argv)
window = TextReaderApp()
sys.exit(app.exec_())

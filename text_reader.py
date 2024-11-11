import sys
import pyperclip
import os
from gtts import gTTS
from PyQt5 import QtWidgets, QtCore
from pynput import mouse

last_text = ""  # Variabele om de laatste tekst bij te houden

class TextReaderApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # Instellingen voor het venster
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.setFixedSize(150, 50)

        # Knop voor het voorlezen van tekst
        self.button = QtWidgets.QPushButton("Voorlezen", self)
        self.button.clicked.connect(self.speak_text)
        self.button.setGeometry(10, 10, 130, 30)

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
        self.show()  # Toon het menu

        # Breng het venster naar de voorgrond
        self.raise_()           # Breng het venster naar voren
        self.activateWindow()    # Focus het venster

    def speak_text(self):
        """Lees de tekst voor met gTTS en speel het af."""
        text = pyperclip.paste()
        if text:
            # Zet de tekst om naar spraak en sla op als mp3
            tts = gTTS(text=text, lang='nl')
            tts.save("speech.mp3")

            # Speel het audiobestand af afhankelijk van het besturingssysteem
            if os.name == "posix":  # macOS/Linux
                os.system("afplay speech.mp3")
            elif os.name == "nt":  # Windows
                os.system("start speech.mp3")
        
        # Verberg het menu na het voorlezen
        self.hide()

# Start de PyQt5-applicatie
app = QtWidgets.QApplication(sys.argv)
window = TextReaderApp()
sys.exit(app.exec_())

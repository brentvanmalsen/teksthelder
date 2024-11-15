import sys
import pyperclip
import os
import requests
from gtts import gTTS
from PyQt5 import QtWidgets, QtCore
from pynput import mouse

last_text = ""  # Variable to keep track of the last text

def simplify_text(text):
    # API URL for Flan-T5 on Hugging Face
    api_url = "https://api-inference.huggingface.co/models/google/flan-t5-large"
    headers = {"Authorization": "Bearer YOUR_HUGGING_FACE_API_KEY"}  # Replace with your API key

    # Send the instruction to the model
    data = {
        "inputs": f"Explain in simple A1 words what this text means: {text}"
    }

    response = requests.post(api_url, headers=headers, json=data)
    print("Status code of the API response:", response.status_code)  # Debugging
    print("API response content:", response.json())  # Debugging

    if response.status_code == 200:
        # Extract the simplified text from the response
        simplified_text = response.json()[0]["generated_text"]
        return simplified_text
    else:
        # Display the full error message for debugging
        error_message = response.json().get("error", "Unknown error")
        return f"Sorry, the text cannot be explained at the moment. Error message: {error_message}"

class TextReaderApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # Window settings
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.setFixedSize(200, 100)

        # Button for reading aloud
        self.button_read = QtWidgets.QPushButton("Voorlezen", self)
        self.button_read.clicked.connect(self.speak_text)
        self.button_read.setGeometry(10, 10, 80, 30)

        # Button for explanation
        self.button_explain = QtWidgets.QPushButton("Uitleg", self)
        self.button_explain.clicked.connect(self.explain_text)
        self.button_explain.setGeometry(110, 10, 80, 30)

        # Timer to regularly check the clipboard
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check_clipboard)
        self.timer.start(1000)  # Check every second

    def check_clipboard(self):
        """Check the clipboard for new text and show the menu."""
        global last_text
        text = pyperclip.paste()

        if text and text != last_text:
            last_text = text
            self.show_menu_at_cursor()

    def show_menu_at_cursor(self):
        """Position the menu next to the cursor and bring it to the foreground."""
        cursor_position = mouse.Controller().position
        self.move(int(cursor_position[0]), int(cursor_position[1]) + 20)  # Position below the cursor
        self.show()  # Show the window
        self.raise_()  # Bring the window to the foreground
        self.activateWindow()  # Focus the window

    def speak_text(self):
        """Read the text aloud using gTTS and play it without closing the window."""
        text = pyperclip.paste()
        if text:
            tts = gTTS(text=text, lang='en')
            tts.save("speech.mp3")

            if os.name == "posix":  # macOS/Linux
                os.system("afplay speech.mp3")
            elif os.name == "nt":  # Windows
                os.system("start speech.mp3")

    def explain_text(self):
        """Simplify and display the text without closing the window."""
        text = pyperclip.paste()
        print("Text on the clipboard:", text)  # Debugging: Print the text on the clipboard
        if text:
            simplified_text = simplify_text(text)
            QtWidgets.QMessageBox.information(self, "Uitleg", simplified_text)

# Start the PyQt5 application
app = QtWidgets.QApplication(sys.argv)
window = TextReaderApp()
sys.exit(app.exec_())

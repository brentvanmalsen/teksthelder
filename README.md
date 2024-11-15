# TekstHelder PC

## Overview
TekstHelder PC is an interactive tool designed to support low-literate users in navigating and understanding digital text on a computer. The application allows users to select text and access options to **read the text aloud** (text-to-speech) and **explain** complex text in simpler terms. The tool aims to enhance accessibility by providing an easy-to-use interface that is triggered whenever text is copied.

## Features
1. **Read Aloud (Voorlezen)**: Converts the selected text to speech in English using Google Text-to-Speech (gTTS).
2. **Explain (Uitleg)**: Simplifies complex text by sending it to the Hugging Face Inference API with the `google/flan-t5-large` model. This model processes the text and provides a simplified explanation.
3. **Cursor-Triggered Menu**: When the user copies text, a pop-up menu appears next to the cursor, allowing easy access to the core functions.

## Installation

### Prerequisites
- **Python 3** is required to run this project.
- **Internet Connection** for using the Hugging Face Inference API and Google Text-to-Speech services.

### Setting Up the Project

1. **Clone the repository**:
    ```bash
    git clone https://github.com/brentvanmalsen/teksthelderpc.git
    cd teksthelderpc
    ```

2. **Create a virtual environment** (recommended for isolating dependencies):
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the API Key**:
   - This project uses the Hugging Face Inference API for text simplification. To enable this, you need an API key from Hugging Face. Once you have the key:
     - Replace `YOUR_HUGGING_FACE_API_KEY` in the code with your actual API key.
     - Ensure that the API key is not committed to the repository for security purposes.

## Usage

1. **Run the application**:
    ```bash
    python text_reader.py
    ```

2. **Selecting and Copying Text**:
   - After running the application, select and copy any text on your computer.
   - A small pop-up menu will appear near the cursor with options:
     - **Voorlezen**: Reads the copied text aloud.
     - **Uitleg**: Explains the copied text in simpler terms.

## Technical Details

### Key Libraries and Frameworks

- **gTTS**: Used for converting text to speech in English.
- **Hugging Face API**: The `google/flan-t5-large` model provides simplified explanations for complex text.
- **pyperclip**: Monitors the clipboard for new text copies.
- **pynput**: Tracks the cursor's position to position the pop-up menu.
- **PyQt5**: Used to create the GUI interface with options for reading aloud and explaining.

### Project Structure

- **text_reader.py**: Main script containing all core functionalities of the application.
- **requirements.txt**: Lists all dependencies required for the project.

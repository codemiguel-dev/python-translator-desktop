import tkinter as tk
from tkinter import ttk, messagebox
from translate import Translator
from gtts import gTTS
import pygame
import os
import tempfile

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Traductor Inglés-Español-Portugués")
        self.create_widgets()
        pygame.mixer.init()

    def create_widgets(self):
        self.input_text = tk.Text(self.root, height=10, width=50)
        self.input_text.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.translate_button = ttk.Button(self.root, text="Traducir", command=self.translate_text)
        self.translate_button.grid(row=1, column=0, pady=10)

        self.play_button = ttk.Button(self.root, text="Escuchar", command=self.play_sound)
        self.play_button.grid(row=1, column=1, pady=10)

        self.output_text = tk.Text(self.root, height=10, width=50)
        self.output_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.lang_var = tk.StringVar(value="Inglés a Español")
        self.lang_selector = ttk.Combobox(self.root, textvariable=self.lang_var, values=[
            "Inglés a Español", "Español a Inglés", "Inglés a Portugués", 
            "Portugués a Inglés", "Español a Portugués", "Portugués a Español"])
        self.lang_selector.grid(row=3, column=0, columnspan=3, pady=10)

    def translate_text(self):
        input_text = self.input_text.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showwarning("Advertencia", "Por favor, ingrese algún texto para traducir.")
            return

        lang_pair = self.lang_var.get()
        try:
            if lang_pair == "Inglés a Español":
                translator = Translator(from_lang='en', to_lang='es')
            elif lang_pair == "Español a Inglés":
                translator = Translator(from_lang='es', to_lang='en')
            elif lang_pair == "Inglés a Portugués":
                translator = Translator(from_lang='en', to_lang='pt')
            elif lang_pair == "Portugués a Inglés":
                translator = Translator(from_lang='pt', to_lang='en')
            elif lang_pair == "Español a Portugués":
                translator = Translator(from_lang='es', to_lang='pt')
            elif lang_pair == "Portugués a Español":
                translator = Translator(from_lang='pt', to_lang='es')
            
            translated = translator.translate(input_text)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, translated)
            
            # Save the translated text for TTS
            self.translated_text = translated
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo traducir el texto. Error: {e}")

    def play_sound(self):
        try:
            # Create a temporary file for the audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
                tts = gTTS(text=self.translated_text, lang=self.tts_lang)
                tts.save(temp_audio_file.name)
                temp_audio_file_path = temp_audio_file.name

            pygame.mixer.music.load(temp_audio_file_path)
            pygame.mixer.music.play()
            
            # Wait until the sound finishes playing
            while pygame.mixer.music.get_busy():
                self.root.update()
                
            pygame.mixer.music.unload()
            
            # Now it is safe to delete the file
            os.remove(temp_audio_file_path)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo reproducir el sonido. Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()

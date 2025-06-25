import customtkinter as ctk
from tkinter import filedialog, messagebox
from deep_translator import GoogleTranslator
from speech_logic import recognize_speech, speak_text
from document_logic import translate_document

# ==================== Language List ====================

# Priority languages including Auto Detect
priority_languages = [
    "Auto Detect",
    "English",
    "Malayalam",
    "Kannada",
    "Tamil",
    "Telugu",
    "Hindi"
]

# Fetch all supported languages as a dictionary {name: code}
all_supported = GoogleTranslator().get_supported_languages(as_dict=True)

# Combine priority list with all supported language names
available_languages = list(
    dict.fromkeys(priority_languages + list(all_supported.keys()))
)

# Build final LANGUAGES dictionary
LANGUAGES = {}
for lang_name in available_languages[:150]:
    if lang_name == "Auto Detect":
        LANGUAGES[lang_name] = "auto"
    elif lang_name in all_supported:
        LANGUAGES[lang_name] = all_supported[lang_name]

# ==================== Translate Helper ====================

def translate_text(text, dest_lang='en', src_lang='auto'):
    try:
        print(f"[DEBUG] Translating '{text}' from {src_lang} to {dest_lang}...")
        translated = GoogleTranslator(source=src_lang, target=dest_lang).translate(text)
        print(f"[DEBUG] Translation result: '{translated}'")
        return translated
    except Exception as e:
        print(f"[DEBUG] Error: {e}")
        return f"Error: {e}"

# ==================== GUI Setup ====================

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🌐 AI Translator App")
app.geometry("800x650")
app.resizable(True, True)

title_label = ctk.CTkLabel(
    app,
    text="🌐 AI Translator App",
    font=ctk.CTkFont(size=28, weight="bold")
)
title_label.pack(pady=10)

tabview = ctk.CTkTabview(app, width=760, height=550)
tabview.pack(padx=10, pady=10, expand=True, fill="both")

# ==================== Text Translator Tab ====================

text_tab = tabview.add("Text Translator")

ctk.CTkLabel(text_tab, text="Input Text:").pack(pady=5)
input_textbox = ctk.CTkTextbox(text_tab, width=700, height=100)
input_textbox.pack(pady=5)

ctk.CTkLabel(text_tab, text="Source Language:").pack(pady=5)
src_lang_var = ctk.StringVar(value="Auto Detect")
src_lang_menu = ctk.CTkOptionMenu(
    text_tab, variable=src_lang_var, values=list(LANGUAGES.keys()), width=200
)
src_lang_menu.pack(pady=5)

ctk.CTkLabel(text_tab, text="Target Language:").pack(pady=5)
dest_lang_var = ctk.StringVar(value="English")
dest_lang_menu = ctk.CTkOptionMenu(
    text_tab, variable=dest_lang_var, values=list(LANGUAGES.keys()), width=200
)
dest_lang_menu.pack(pady=5)

ctk.CTkLabel(text_tab, text="Translated Text:").pack(pady=5)
output_textbox = ctk.CTkTextbox(text_tab, width=700, height=80)
output_textbox.pack(pady=5)

def do_translate_text():
    text = input_textbox.get("1.0", "end").strip()
    if not text:
        messagebox.showerror("Error", "Please enter some text!")
        return
    src_code = LANGUAGES[src_lang_var.get()]
    dest_code = LANGUAGES[dest_lang_var.get()]
    result = translate_text(text, dest_code, src_code)
    output_textbox.delete("1.0", "end")
    output_textbox.insert("end", result)

ctk.CTkButton(
    text_tab,
    text="Translate",
    command=do_translate_text,
    width=180,
    height=40
).pack(pady=10)

# ==================== Speech Translator Tab ====================

speech_tab = tabview.add("Speech Translator")

ctk.CTkLabel(speech_tab, text="Target Language:").pack(pady=10)
speech_dest_lang_var = ctk.StringVar(value="English")
speech_dest_lang_menu = ctk.CTkOptionMenu(
    speech_tab, variable=speech_dest_lang_var, values=list(LANGUAGES.keys()), width=200
)
speech_dest_lang_menu.pack(pady=5)

speech_output_textbox = ctk.CTkTextbox(speech_tab, width=700, height=200)
speech_output_textbox.pack(pady=10)

def do_speech_translate():
    text = recognize_speech()
    if text.startswith("Error"):
        messagebox.showerror("Error", text)
    else:
        dest_code = LANGUAGES[speech_dest_lang_var.get()]
        translated = translate_text(text, dest_code)
        speech_output_textbox.delete("1.0", "end")
        speech_output_textbox.insert(
            "end",
            f"Recognized:\n{text}\n\nTranslated:\n{translated}"
        )
        speak_text(translated)

ctk.CTkButton(
    speech_tab,
    text="Start Voice Translate",
    command=do_speech_translate,
    width=180,
    height=40
).pack(pady=10)

# ==================== Document Translator Tab ====================

doc_tab = tabview.add("Document Translator")

ctk.CTkLabel(doc_tab, text="Target Language:").pack(pady=10)
doc_dest_lang_var = ctk.StringVar(value="English")
doc_dest_lang_menu = ctk.CTkOptionMenu(
    doc_tab, variable=doc_dest_lang_var, values=list(LANGUAGES.keys()), width=200
)
doc_dest_lang_menu.pack(pady=5)

doc_output_textbox = ctk.CTkTextbox(doc_tab, width=700, height=200)
doc_output_textbox.pack(pady=10)

def do_doc_translate():
    file_path = filedialog.askopenfilename(
        filetypes=[("Document files", "*.pdf;*.txt")]
    )
    if file_path:
        dest_code = LANGUAGES[doc_dest_lang_var.get()]
        try:
            translated_text = translate_document(file_path, dest_code)
        except Exception as e:
            messagebox.showerror("Error", f"{e}")
            return
        doc_output_textbox.delete("1.0", "end")
        doc_output_textbox.insert("end", translated_text)

ctk.CTkButton(
    doc_tab,
    text="Browse & Translate Document",
    command=do_doc_translate,
    width=220,
    height=40
).pack(pady=10)

# ==================== Run App ====================

app.mainloop()
# This is the main entry point for the translator application.
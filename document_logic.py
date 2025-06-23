# document_logic.py
from pdfminer.high_level import extract_text
from deep_translator import GoogleTranslator

def extract_text_from_file(file_path):
    """Extracts raw text from PDF or TXT file"""
    if file_path.lower().endswith(".pdf"):
        return extract_text(file_path)
    elif file_path.lower().endswith(".txt"):
        with open(file_path, encoding='utf-8', errors='ignore') as f:
            return f.read()
    else:
        return "Error: Unsupported file format."

def translate_document(file_path, dest_lang='en'):
    text = extract_text_from_file(file_path)
    return GoogleTranslator(source='auto', target=dest_lang).translate(text)
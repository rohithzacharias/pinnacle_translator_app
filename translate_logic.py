# translate_logic.py
from deep_translator import GoogleTranslator

def translate_text(text, dest_lang='en', src_lang='auto'):
    """
    Translate the given text from the source language to the destination language.

    Parameters:
        text (str): The text you want to translate.
        dest_lang (str): The target language code, e.g. 'en', 'ml', etc.
        src_lang (str): The source language code, or 'auto' to auto-detect.

    Returns:
        str: The translated text or an error message.
    """
    try:
        # Perform the translation
        translated = GoogleTranslator(source=src_lang, target=dest_lang).translate(text)
        return translated
    except Exception as e:
        return f"Error: {e}"
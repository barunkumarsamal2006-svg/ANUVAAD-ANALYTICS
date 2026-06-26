from deep_translator import GoogleTranslator
from config import settings
from pipeline.preprocess import clean_text

def translate_odia_to_english(text):
    """
    Translates Odia text to English using deep-translator (Google Translate interface).
    If offline or an error occurs, falls back to a custom local translation map.
    """
    text = clean_text(text)
    if not text:
        return ""
    
    # 1. Try real translation using GoogleTranslator
    try:
        # 'or' is ISO 639-1 code for Odia (Oriya)
        translator = GoogleTranslator(source='or', target='en')
        translated_text = translator.translate(text)
        if translated_text:
            return translated_text
    except Exception as e:
        print(f"Deep translation failed: {e}. Executing dictionary-based offline fallback...")
        
    # 2. Offline Fallback Logic: Look for specific Odia key phrases in the text
    translated_pieces = []
    
    # Search for multi-word and single-word matches in order of descending length (longest first)
    sorted_translations = sorted(settings.FALLBACK_TRANSLATION.items(), key=lambda x: len(x[0]), reverse=True)
    
    temp_text = text
    found_matches = []
    
    # Replace matched Odia tokens with their English equivalents in place
    for odia_phrase, eng_phrase in sorted_translations:
        if odia_phrase in temp_text:
            found_matches.append(eng_phrase)
            temp_text = temp_text.replace(odia_phrase, " ") # remove to avoid double matches
            
    if found_matches:
        # Synthesize fallback translated text
        synthesized = ", ".join(found_matches)
        return f"[Offline Translation] Complaint regarding: {synthesized}"
        
    # Last resort: return text with a header
    return f"[Offline Draft] Local Grievance: {text}"

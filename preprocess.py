import re

def clean_text(text):
    """Basic text cleaning for Odia and English."""
    if not text:
        return ""
    # Strip surrounding whitespace
    text = text.strip()
    # Replace multiple whitespaces with a single space
    text = re.sub(r'\s+', ' ', text)
    return text

def clean_english_text(text):
    """Specific preprocessing for English translation/classification."""
    text = clean_text(text)
    # Lowercase English text for model consistency
    text = text.lower()
    # Remove special characters but keep alphanumeric, spaces, and basic punctuation
    text = re.sub(r'[^a-zA-Z0-9\s.,!?\'"-]', '', text)
    return text

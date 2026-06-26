from textblob import TextBlob
from pipeline.preprocess import clean_text

def analyze_sentiment(english_text):
    """
    Analyzes the sentiment of English text using TextBlob.
    Returns:
        sentiment_label (str): 'Negative (Critical)', 'Neutral', or 'Positive'
        sentiment_score (float): polarity score from -1.0 to 1.0
    """
    cleaned_text = clean_text(english_text)
    if not cleaned_text:
        return "Neutral", 0.0
        
    try:
        # Get polarity score
        blob = TextBlob(cleaned_text)
        polarity = blob.sentiment.polarity
        
        # Categorize polarity
        if polarity < -0.1:
            sentiment_label = "Negative (Critical)"
        elif polarity > 0.1:
            sentiment_label = "Positive"
        else:
            sentiment_label = "Neutral"
            
        return sentiment_label, round(polarity, 2)
    except Exception as e:
        print(f"Sentiment analysis failed: {e}. Defaulting to Neutral.")
        return "Neutral", 0.0

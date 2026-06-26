import os
import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

from config import settings
from pipeline.preprocess import clean_english_text

MODEL_PATH = os.path.join(settings.BASE_DIR, "models", "classifier.pkl")
ENCODER_PATH = os.path.join(settings.BASE_DIR, "models", "label_encoder.pkl")

# Expanded, Odisha-specific training dataset to cover local schemes and common issues
SYNTHETIC_TRAINING_DATA = [
    # ---- Agriculture & Farmers' Empowerment ----
    ("i did not receive my kalia yojana installment money.", "Agriculture & Farmers' Empowerment"),
    ("crop insurance payment is delayed under pradhan mantri fasal bima yojana.", "Agriculture & Farmers' Empowerment"),
    ("paddy procurement at the local mandi is halted. token expired.", "Agriculture & Farmers' Empowerment"),
    ("there is a severe shortage of urea and potash fertilizers in our block store.", "Agriculture & Farmers' Empowerment"),
    ("seeds supplied by the agricultural department are of poor quality and did not germinate.", "Agriculture & Farmers' Empowerment"),
    ("irrigation canal is blocked, water is not reaching my agricultural field.", "Agriculture & Farmers' Empowerment"),
    ("tractor subsidy application is pending at block agriculture office for months.", "Agriculture & Farmers' Empowerment"),
    ("excessive rainfall flooded my paddy fields, need crop compensation assessment.", "Agriculture & Farmers' Empowerment"),
    ("local dealers are black marketing pesticides and fertilizers at high prices.", "Agriculture & Farmers' Empowerment"),
    ("borewell installation under government scheme is not functioning.", "Agriculture & Farmers' Empowerment"),
    ("paddy procurement token not generated, crop is rotting in mandi.", "Agriculture & Farmers' Empowerment"),
    ("assistance for vegetable cultivation not credited to bank account.", "Agriculture & Farmers' Empowerment"),
    
    # ---- Health & Family Welfare ----
    ("doctor was absent at the community health centre chc.", "Health & Family Welfare"),
    ("the government hospital staff did not provide free medicines despite niramaya scheme.", "Health & Family Welfare"),
    ("private hospital refused admission under biju swasthya kalyan yojana bsky card.", "Health & Family Welfare"),
    ("poor sanitation and garbage accumulation inside the district headquarters hospital dhh.", "Health & Family Welfare"),
    ("108 ambulance did not arrive on time during medical emergency.", "Health & Family Welfare"),
    ("nurse demanded a bribe for delivery of newborn child at phc.", "Health & Family Welfare"),
    ("blood bank has no supply of o negative blood during emergency surgery.", "Health & Family Welfare"),
    ("ultrasound and x-ray machines are out of order at the civil hospital.", "Health & Family Welfare"),
    ("doctors are prescribing outside medicines which are very expensive.", "Health & Family Welfare"),
    ("biju swasthya kalyan card activation issue at hospital desk.", "Health & Family Welfare"),
    ("rural medical officer is running private clinic during duty hours.", "Health & Family Welfare"),
    
    # ---- School & Mass Education ----
    ("mid-day meal quality is very bad, students found insects in food.", "School & Mass Education"),
    ("the roof of the government primary school is leaking during rains, dangerous for kids.", "School & Mass Education"),
    ("government high school teachers are not taking classes and playing on mobiles.", "School & Mass Education"),
    ("free textbooks and school uniforms have not been distributed to class 6 students.", "School & Mass Education"),
    ("there is no separate girls toilet in our school, causing dropouts.", "School & Mass Education"),
    ("smart classroom computers and projectors installed under 5t are locked and not used.", "School & Mass Education"),
    ("drinking water facility is unavailable in the school premises.", "School & Mass Education"),
    ("school committee is mismanaging development funds, teacher is absent.", "School & Mass Education"),
    ("mathematics and science teacher posts are vacant for one year.", "School & Mass Education"),
    ("mid day meal not served regularly in primary school.", "School & Mass Education"),
    
    # ---- Panchayati Raj & Drinking Water ----
    ("drinking water tubewell is broken and has been defunct for three weeks.", "Panchayati Raj & Drinking Water"),
    ("our names were removed from pradhan mantri awas yojana pmay list by panchayat.", "Panchayati Raj & Drinking Water"),
    ("the road connecting our village to main road is muddy and filled with deep holes.", "Panchayati Raj & Drinking Water"),
    ("bribe of ten thousand rupees demanded by sarpanch for biju pucca ghar sanction.", "Panchayati Raj & Drinking Water"),
    ("drinking water supply through pipes is irregular and dirty in the block.", "Panchayati Raj & Drinking Water"),
    ("no drainage system in the gram panchayat, rain water flooding houses.", "Panchayati Raj & Drinking Water"),
    ("panchayat executive officer peo is demanding commission to clear mgnregs payments.", "Panchayati Raj & Drinking Water"),
    ("street water tap is broken, water is being wasted in village.", "Panchayati Raj & Drinking Water"),
    ("no community toilet facility in village, open defecation is still happening.", "Panchayati Raj & Drinking Water"),
    ("mgnregs labor wages not credited to post office account after road construction.", "Panchayati Raj & Drinking Water"),
    
    # ---- Home Department ----
    ("police station officer refused to register an fir for mobile theft.", "Home Department"),
    ("police inspector demanded bribe to provide a copy of the fir.", "Home Department"),
    ("a group clash broke out in the village and the police took hours to arrive.", "Home Department"),
    ("frequent thefts and robberies in our locality due to lack of police patrolling.", "Home Department"),
    ("i lost my hard-earned money in a bank OTP cyber fraud, need cyber police help.", "Home Department"),
    ("traffic police are harassing local vehicle owners and collecting illegal fine.", "Home Department"),
    ("local goons are threatening my family and business, we feel unsafe.", "Home Department"),
    ("investigation of my daughter's harassment case is being delayed intentionally.", "Home Department"),
    ("passport verification is pending at the local police station.", "Home Department"),
    
    # ---- Housing & Urban Development ----
    ("municipality cleaning staff have not cleared garbage bins for a week, bad smell.", "Housing & Urban Development"),
    ("sewage line is choked and dirty water is overflowing on the municipal street.", "Housing & Urban Development"),
    ("municipal drinking water is yellow and contains small worms.", "Housing & Urban Development"),
    ("all streetlights in ward 12 are burned out, making streets dark and unsafe.", "Housing & Urban Development"),
    ("illegal construction on public park land by local builder in town.", "Housing & Urban Development"),
    ("delay in approving residential building plan by municipal corporation.", "Housing & Urban Development"),
    ("encroachment of footpaths by vendors in the market area, causing traffic jams.", "Housing & Urban Development"),
    ("public park is full of bushes and stray dogs, municipality not maintaining it.", "Housing & Urban Development"),
    ("municipal tax paid but double tax bill generated online.", "Housing & Urban Development")
]

def train_classifier():
    """Trains a TF-IDF + Logistic Regression pipeline on synthetic data and saves models."""
    print("Training department classifier...")
    texts = [clean_english_text(item[0]) for item in SYNTHETIC_TRAINING_DATA]
    labels = [item[1] for item in SYNTHETIC_TRAINING_DATA]
    
    # Fit Label Encoder
    encoder = LabelEncoder()
    encoded_labels = encoder.fit_transform(labels)
    
    # Define sklearn pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            ngram_range=(1, 2), 
            stop_words='english', 
            min_df=1,
            sublinear_tf=True
        )),
        ('clf', LogisticRegression(C=10.0, class_weight='balanced', max_iter=200))
    ])
    
    # Train
    pipeline.fit(texts, encoded_labels)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    
    # Save model and encoder
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(pipeline, f)
    with open(ENCODER_PATH, 'wb') as f:
        pickle.dump(encoder, f)
        
    print("Model and Label Encoder saved successfully.")

def predict_department(text):
    """
    Predicts the department for a given English grievance.
    Automatically trains the classifier if the model file is not found.
    Returns:
        department_name (str)
        confidence_score (float)
    """
    # 1. Train model if not exists
    if not os.path.exists(MODEL_PATH) or not os.path.exists(ENCODER_PATH):
        train_classifier()
        
    # 2. Load model and label encoder
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(ENCODER_PATH, 'rb') as f:
            encoder = pickle.load(f)
    except Exception as e:
        print(f"Error loading classifier models: {e}. Re-training...")
        train_classifier()
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(ENCODER_PATH, 'rb') as f:
            encoder = pickle.load(f)
            
    # 3. Clean and Predict
    cleaned_text = clean_english_text(text)
    if not cleaned_text:
        # Default fallback if empty
        return "Panchayati Raj & Drinking Water", 0.5
        
    try:
        pred_encoded = model.predict([cleaned_text])[0]
        pred_label = encoder.inverse_transform([pred_encoded])[0]
        
        # Get probability/confidence
        probs = model.predict_proba([cleaned_text])[0]
        confidence = float(np.max(probs))
        
        return pred_label, round(confidence, 2)
    except Exception as e:
        print(f"Prediction failed: {e}. Returning default department.")
        return "Panchayati Raj & Drinking Water", 0.5

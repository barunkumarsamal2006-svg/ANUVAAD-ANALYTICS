# ANUVAAD-ANALYTICS
### AI-Powered Localized Public Grievance Management System (Odisha)

Anuvaad Analytics is an intelligent public grievance redressal portal designed specifically for Odisha. It helps bridge the language barrier between citizens and government officers. The system enables citizens to file complaints in Odia, automatically translates them, classifies them into correct administrative departments, analyzes the severity/sentiment of the complaints, and renders a comprehensive analytics dashboard for administrative oversight and resolution.

---

## 🚀 Key Features

1. **Citizen Portal (Odia Input)**:
   - Accept grievances written in local Odia text.
   - Real-time language translation to English (via `deep-translator` API or a local dictionary fallback if offline).
   - Automated AI Department Prediction using a trained NLP pipeline.
   - Sentiment evaluation (Critical, Neutral, Positive) based on the emotional intensity of the grievance.
   
2. **Officer Analytics & Management Dashboard**:
   - **Key Performance Indicators (KPIs)**: Track total complaints, pending items, resolution rate, and critical alerts.
   - **Interactive Visualizations (Plotly)**: 
     - Department-wise distribution
     - Resolution status split
     - Sentiment distribution
     - Top affected districts of Odisha (30 districts support)
     - Time-series inflow trend
   - **Grievance Resolution Panel**: View, search, and filter grievances. Allow officers to re-assign departments, update grievance statuses (Pending, In Progress, Resolved, Rejected), and input official resolution remarks.

3. **Zero-Setup Local Database**:
   - Integrated with SQLite by default (`data/grievances.db`) to run out-of-the-box.
   - Syncs database edits with `data/grievances.csv` and `data/departments.csv` for data portability.

---

## 📁 Directory Structure

```text
anuvaad-analytics/
├── app.py                  # Main Streamlit Entrypoint
├── requirements.txt        # Application Dependencies
├── README.md               # Documentation
├── .gitignore              # Git Ignore Patterns
│
├── config/
│   └── settings.py         # Application Config, Districts & Fallback Map
│
├── pipeline/
│   ├── __init__.py
│   ├── preprocess.py       # Text sanitization and cleanups
│   ├── translator.py       # Indic translation (Odia -> English)
│   ├── sentiment.py        # Sentiment analysis (TextBlob)
│   └── classifier.py       # Department prediction & Self-training classifier
│
├── database/
│   ├── __init__.py
│   ├── schema.sql          # DB schema definition
│   └── db_handler.py       # SQLite connection, CRUD, and seeding logic
│
├── models/
│   ├── classifier.pkl      # Pickled ML Model (Trained on startup)
│   └── label_encoder.pkl   # Pickled Label Encoder
│
├── data/
│   ├── grievances.csv      # Flat CSV file sync of grievances
│   └── departments.csv     # Flat CSV list of departments
│
├── dashboard/
│   ├── charts.py           # Plotly interactive graphs
│   └── metrics.py          # Custom metric KPI cards
│
└── assets/
    └── logo.png            # Application Brand Logo
```

---

## 🛠️ Installation and Setup

### Prerequisites
- Python 3.8+ (Tested on Python 3.13)
- Internet connection (Recommended for initial run to fetch translations; system falls back to a dictionary if offline)

### Step 1: Clone or Navigate to the Directory
Ensure you are in the project folder:
```bash
cd anuvaad-analytics
```

### Step 2: Install Dependencies
Install all required libraries using pip:
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
Start the Streamlit local server:
```bash
streamlit run app.py
```
This will automatically open the application in your default browser at `http://localhost:8501`.

---

## ⚙️ How the AI Model Works

- **Self-Healing Model Training**: Upon the first invocation of the pipeline, the system checks if the classifier binaries exist in `models/`. If missing, `pipeline/classifier.py` automatically trains a TF-IDF + Logistic Regression pipeline on an Odisha-specific training dataset containing terms like *Kalia Yojana*, *BSKY*, *Mandi*, *police station*, *mid-day meal*, and *streetlights*, saving the trained artifacts instantly.
- **Odisha-Localized Logic**: The classifier handles 6 main departments:
  - Agriculture & Farmers' Empowerment
  - Health & Family Welfare
  - School & Mass Education
  - Panchayati Raj & Drinking Water
  - Home Department
  - Housing & Urban Development
- **Robust Fallback**: If internet connection drops and deep translation fails, the system executes a token-matching offline translation based on key Odia phrases to continue classifying.

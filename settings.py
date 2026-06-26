import os

# Project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database Path
DB_PATH = os.path.join(BASE_DIR, "data", "grievances.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "database", "schema.sql")

# Ensure required directories exist
os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "assets"), exist_ok=True)

# Odisha Districts (30 Districts)
ODISHA_DISTRICTS = [
    "Angul", "Balangir", "Balasore", "Bargarh", "Bhadrak", "Boudh", 
    "Cuttack", "Deogarh", "Dhenkanal", "Gajapati", "Ganjam", "Jagatsinghpur", 
    "Jajpur", "Jharsuguda", "Kalahandi", "Kandhamal", "Kendrapara", "Keonjhar", 
    "Khordha", "Koraput", "Malkangiri", "Mayurbhanj", "Nabarangpur", "Nayagarh", 
    "Nuapada", "Puri", "Rayagada", "Sambalpur", "Subarnapur", "Sundargarh"
]

# Government Departments
DEPARTMENTS = {
    "Agriculture & Farmers' Empowerment": "Issues related to crop insurance (Kalia Yojana), subsidies, seeds, fertilizers, mandi procurement, and irrigation complaints.",
    "Health & Family Welfare": "Complaints regarding government hospitals, BSKY card benefits, doctor absenteeism, medicine shortage, and sanitation in clinics.",
    "School & Mass Education": "Issues with school infrastructure, mid-day meals, teacher attendance, books, uniforms, and local high school facilities.",
    "Panchayati Raj & Drinking Water": "Drinking water supply, tube well repairs, rural housing (PMRY/Biju Pucca Ghar), village roads, and panchayat-level disputes.",
    "Home Department": "Law and order complaints, police behavior, local safety, delays in registering FIRs, and theft investigations.",
    "Housing & Urban Development": "Municipal garbage clearance, sewage cleaning, urban drinking water, streetlights, and municipality tax issues."
}

# Offline/Fallback translation dictionary for demo safety
FALLBACK_TRANSLATION = {
    # Odia phrases -> English
    "ନମସ୍କାର": "hello",
    "କାଳିଆ ଯୋଜନା": "Kalia scheme",
    "କାଳିଆ ଟଙ୍କା": "Kalia scheme money",
    "ଟଙ୍କା ମିଳିନି": "money not received",
    "ବିଏସକେୱାଇ": "BSKY health insurance",
    "ଡାକ୍ତର ନାହାଁନ୍ତି": "doctors not present",
    "ଔଷଧ ମିଳୁନି": "medicine not available",
    "ଡାକ୍ତରଖାନା": "hospital",
    "ପାନୀୟ ଜଳ": "drinking water",
    "ପାଣି ମିଳୁନି": "water not available",
    "ନଳକୂପ ଅଚଳ": "tube well broken",
    "ପିଇବା ପାଣି": "drinking water",
    "ରାସ୍ତା ଖରାପ": "road is bad",
    "ରାସ୍ତା କାମ": "road work",
    "ମଧ୍ୟାହ୍ନ ଭୋଜନ": "mid-day meal",
    "ସ୍କୁଲ": "school",
    "ଶିକ୍ଷକ": "teacher",
    "ଚୋରି": "theft",
    "ମାଡପିଟ": "physical assault",
    "ଥାନା": "police station",
    "ଏଫଆଇଆର": "FIR police complaint",
    "ଆଳୁ": "potato",
    "ମଇଳା ସଫା": "garbage cleaning",
    "ଡ୍ରେନେଜ": "drainage",
    "ଷ୍ଟ୍ରିଟଲାଇଟ": "streetlight",
    "ମ୍ୟୁନିସିପାଲିଟି": "municipality"
}

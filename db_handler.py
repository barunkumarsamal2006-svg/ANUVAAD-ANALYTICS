import sqlite3
import os
import pandas as pd
from datetime import datetime, timedelta
import random

from config import settings

class DatabaseHandler:
    def __init__(self, db_path=None):
        self.db_path = db_path or settings.DB_PATH
        # Ensure database directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def get_connection(self):
        """Returns a connection to the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn

    def init_db(self):
        """Initializes the database schema and seeds initial data if empty."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if tables already exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='departments';")
        tables_exist = cursor.fetchone() is not None
        
        if not tables_exist:
            # Create tables from schema.sql
            schema_path = settings.SCHEMA_PATH
            if os.path.exists(schema_path):
                with open(schema_path, "r", encoding="utf-8") as f:
                    cursor.executescript(f.read())
                conn.commit()
                print("Database tables created successfully.")
                
                # Seed departments
                self._seed_departments(conn)
                # Seed sample grievances
                self._seed_sample_grievances(conn)
            else:
                # In case schema.sql is missing, write a fallback creation
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS departments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT NOT NULL
                );
                """)
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS grievances (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    citizen_name TEXT NOT NULL,
                    contact_number TEXT NOT NULL,
                    district TEXT NOT NULL,
                    complaint_odia TEXT NOT NULL,
                    complaint_english TEXT NOT NULL,
                    predicted_department TEXT NOT NULL,
                    assigned_department TEXT NOT NULL,
                    sentiment TEXT NOT NULL,
                    sentiment_score REAL NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Pending',
                    resolution_remarks TEXT,
                    date_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """)
                conn.commit()
                self._seed_departments(conn)
                self._seed_sample_grievances(conn)
        conn.close()

    def _seed_departments(self, conn):
        """Seeds government departments from config."""
        cursor = conn.cursor()
        for name, desc in settings.DEPARTMENTS.items():
            cursor.execute(
                "INSERT OR IGNORE INTO departments (name, description) VALUES (?, ?);",
                (name, desc)
            )
        conn.commit()
        print("Government departments seeded successfully.")

    def _seed_sample_grievances(self, conn):
        """Seeds a set of realistic, historically distributed sample grievances."""
        cursor = conn.cursor()
        
        # We check if grievances exist
        cursor.execute("SELECT COUNT(*) FROM grievances;")
        if cursor.fetchone()[0] > 0:
            return  # Already seeded
            
        # Standard Odisha seed cases
        base_time = datetime.now()
        
        seed_cases = [
            {
                "citizen_name": "Ramesh Sahoo",
                "contact_number": "9876543210",
                "district": "Khordha",
                "complaint_odia": "କାଳିଆ ଯୋଜନାର ଟଙ୍କା ୩ ମାସ ହେଲା ମିଳିନି। ଚାଷ ପାଇଁ ବହୁତ ଅସୁବିଧା ହେଉଛି।",
                "complaint_english": "Kalia scheme money has not been received for 3 months. Facing lot of issues for farming.",
                "predicted_department": "Agriculture & Farmers' Empowerment",
                "assigned_department": "Agriculture & Farmers' Empowerment",
                "sentiment": "Negative (Critical)",
                "sentiment_score": -0.6,
                "status": "Pending",
                "resolution_remarks": None,
                "days_ago": 4
            },
            {
                "citizen_name": "Gita Mohanty",
                "contact_number": "8765432109",
                "district": "Cuttack",
                "complaint_odia": "ଆମ ଗାଁ ହସ୍ପିଟାଲରେ ଡାକ୍ତର ସମୟରେ ଆସୁନାହାଁନ୍ତି। ରୋଗୀ ମାନେ ହଇରାଣ ହେଉଛନ୍ତି।",
                "complaint_english": "Doctors are not coming on time to our village hospital. Patients are facing difficulties.",
                "predicted_department": "Health & Family Welfare",
                "assigned_department": "Health & Family Welfare",
                "sentiment": "Negative (Critical)",
                "sentiment_score": -0.4,
                "status": "In Progress",
                "resolution_remarks": "Assigned field inspector to verify biometric attendance of doctor.",
                "days_ago": 12
            },
            {
                "citizen_name": "Priyabrata Dash",
                "contact_number": "7654321098",
                "district": "Puri",
                "complaint_odia": "ବିଦ୍ୟାଳୟରେ ମଧ୍ୟାହ୍ନ ଭୋଜନ ଖାଦ୍ୟର ଗୁଣବତ୍ତା ବହୁତ ଖରାପ ଅଛି। ପିଲାମାନେ ଅସୁସ୍ଥ ହେଉଛନ୍ତି।",
                "complaint_english": "The quality of mid-day meal food in the school is very bad. Children are falling sick.",
                "predicted_department": "School & Mass Education",
                "assigned_department": "School & Mass Education",
                "sentiment": "Negative (Critical)",
                "sentiment_score": -0.7,
                "status": "Resolved",
                "resolution_remarks": "School inspection completed. Caterer warned and meal quality improved with weekly monitoring.",
                "days_ago": 20
            },
            {
                "citizen_name": "Mamata Dalai",
                "contact_number": "9938812345",
                "district": "Ganjam",
                "complaint_odia": "ଆମ ସାହିରେ ବିଲ୍ ଗୁଡ଼ିକରେ ପାନୀୟ ଜଳ ଯୋଗାଣ ୪ ଦିନ ହେଲା ବନ୍ଦ ଅଛି। ଟ୍ୟୁବୱେଲ ମଧ୍ୟ ଖରାପ।",
                "complaint_english": "Drinking water supply is stopped in our street for 4 days. Tube well is also broken.",
                "predicted_department": "Panchayati Raj & Drinking Water",
                "assigned_department": "Panchayati Raj & Drinking Water",
                "sentiment": "Negative (Critical)",
                "sentiment_score": -0.5,
                "status": "Pending",
                "resolution_remarks": None,
                "days_ago": 2
            },
            {
                "citizen_name": "Suresh Pradhan",
                "contact_number": "9090123456",
                "district": "Sambalpur",
                "complaint_odia": "ଗତକାଲି ରାତିରେ ମୋ ଦୋକାନରୁ ଚୋରି ହୋଇଛି, କିନ୍ତୁ ପୋଲିସ ଏଫଆଇଆର ରଖିବାକୁ ମନା କରୁଛି।",
                "complaint_english": "Theft happened in my shop last night, but police is refusing to register FIR.",
                "predicted_department": "Home Department",
                "assigned_department": "Home Department",
                "sentiment": "Negative (Critical)",
                "sentiment_score": -0.6,
                "status": "Pending",
                "resolution_remarks": None,
                "days_ago": 1
            },
            {
                "citizen_name": "Subodh Mishra",
                "contact_number": "8895012345",
                "district": "Balasore",
                "complaint_odia": "ମ୍ୟୁନିସିପାଲିଟି କର୍ମଚାରୀମାନେ ଅଳିଆ ଆଦୌ ସଫା କରୁନାହାଁନ୍ତି। ଗନ୍ଧରେ ରହିବା ଅସମ୍ଭବ ହେଲାଣି।",
                "complaint_english": "Municipality workers are not cleaning garbage at all. It is impossible to stay in the smell.",
                "predicted_department": "Housing & Urban Development",
                "assigned_department": "Housing & Urban Development",
                "sentiment": "Negative (Critical)",
                "sentiment_score": -0.8,
                "status": "In Progress",
                "resolution_remarks": "Informed local ward commissioner. Heavy machinery deployed to clear primary dumpsite.",
                "days_ago": 8
            },
            {
                "citizen_name": "Minati Patra",
                "contact_number": "7788990011",
                "district": "Bhadrak",
                "complaint_odia": "ମୋ ବାପାଙ୍କ ବିଏସକେୱାଇ କାର୍ଡ ଥାଇ ମଧ୍ୟ ହସ୍ପିଟାଲ ମାଗଣା ଚିକିତ୍ସା ଦେବାକୁ ମନା କଲା।",
                "complaint_english": "Even though my father has BSKY card, hospital refused to provide free treatment.",
                "predicted_department": "Health & Family Welfare",
                "assigned_department": "Health & Family Welfare",
                "sentiment": "Negative (Critical)",
                "sentiment_score": -0.5,
                "status": "Resolved",
                "resolution_remarks": "Grievance redressed. The private hospital was issued a show-cause notice by CDMO and the bill was waived.",
                "days_ago": 15
            },
            {
                "citizen_name": "Ashok Jena",
                "contact_number": "9437123456",
                "district": "Jajpur",
                "complaint_odia": "ଗାଁ ମୁଖ୍ୟ ରାସ୍ତା ବର୍ଷା ଦିନେ ପଙ୍କୁଆ ହୋଇଯାଉଛି। ଯାତାୟାତ ପାଇଁ ବହୁତ କଷ୍ଟ।",
                "complaint_english": "The main village road becomes muddy during rainy season. Very difficult for transportation.",
                "predicted_department": "Panchayati Raj & Drinking Water",
                "assigned_department": "Panchayati Raj & Drinking Water",
                "sentiment": "Negative (Critical)",
                "sentiment_score": -0.3,
                "status": "In Progress",
                "resolution_remarks": "Work approved under MGNREGS for road reinforcement. Stones laid.",
                "days_ago": 25
            },
            {
                "citizen_name": "Nibedita Nayak",
                "contact_number": "9937012345",
                "district": "Khordha",
                "complaint_odia": "ସ୍କୁଲରେ ଗଣିତ ଶିକ୍ଷକ ନାହାଁନ୍ତି। ପିଲାଙ୍କ ପାଠପଢା ବହୁତ ବ୍ୟାହତ ହେଉଛି।",
                "complaint_english": "There is no math teacher in school. Children's education is highly disrupted.",
                "predicted_department": "School & Mass Education",
                "assigned_department": "School & Mass Education",
                "sentiment": "Negative (Critical)",
                "sentiment_score": -0.4,
                "status": "Pending",
                "resolution_remarks": None,
                "days_ago": 3
            },
            {
                "citizen_name": "Kanhu Charan Behera",
                "contact_number": "9040112233",
                "district": "Koraput",
                "complaint_odia": "ଚାଷୀମାନଙ୍କୁ ସମୟରେ ସାର କିମ୍ବା ବିହନ ମିଳୁନି। ବ୍ଲକ ଅଫିସର ଶୁଣୁନାହାଁନ୍ତି।",
                "complaint_english": "Farmers are not getting fertilizers or seeds on time. Block officer is not listening.",
                "predicted_department": "Agriculture & Farmers' Empowerment",
                "assigned_department": "Agriculture & Farmers' Empowerment",
                "sentiment": "Negative (Critical)",
                "sentiment_score": -0.5,
                "status": "Resolved",
                "resolution_remarks": "Fertilizer stocks allocated to block cooperative society and distributed to registered farmers.",
                "days_ago": 28
            },
            {
                "citizen_name": "Kailash Mishra",
                "contact_number": "8114422334",
                "district": "Sundargarh",
                "complaint_odia": "ଆମ ଅଞ୍ଚଳରେ ବିଦ୍ୟୁତ ସେବା ବହୁତ ବାଧାପ୍ରାପ୍ତ ହେଉଛି। ପ୍ରତିଦିନ ୫-୬ ଘଣ୍ଟା ଲାଇନ କଟୁଛି।",
                "complaint_english": "Electricity service is very disrupted in our area. There is load shedding for 5-6 hours daily.",
                "predicted_department": "Panchayati Raj & Drinking Water", # Can map here or switch
                "assigned_department": "Panchayati Raj & Drinking Water",
                "sentiment": "Negative (Critical)",
                "sentiment_score": -0.4,
                "status": "Resolved",
                "resolution_remarks": "Local transformer upgraded. Loading issues resolved by TP Western Odisha Distribution Limited.",
                "days_ago": 18
            },
            {
                "citizen_name": "Tapan Pradhan",
                "contact_number": "7008123456",
                "district": "Bargarh",
                "complaint_odia": "ପଞ୍ଚାୟତରେ ପକ୍କା ଘର ପାଇଁ ଲାଞ୍ଚ ମାଗୁଛନ୍ତି। ଗରିବ ଲୋକ କେଉଁଠୁ ଆଣିବେ?",
                "complaint_english": "Asking bribe for pucca house in panchayat. From where will poor people get it?",
                "predicted_department": "Panchayati Raj & Drinking Water",
                "assigned_department": "Panchayati Raj & Drinking Water",
                "sentiment": "Negative (Critical)",
                "sentiment_score": -0.7,
                "status": "Pending",
                "resolution_remarks": None,
                "days_ago": 6
            },
            {
                "citizen_name": "Sunita Jena",
                "contact_number": "9123456789",
                "district": "Jagatsinghpur",
                "complaint_odia": "ଡ୍ରେନେଜ ବ୍ୟବସ୍ଥା ନଷ୍ଟ ହୋଇଯାଇଛି। ବର୍ଷା ପାଣି ଘରେ ପଶୁଛି।",
                "complaint_english": "Drainage system is ruined. Rain water is entering houses.",
                "predicted_department": "Housing & Urban Development",
                "assigned_department": "Housing & Urban Development",
                "sentiment": "Negative (Critical)",
                "sentiment_score": -0.6,
                "status": "In Progress",
                "resolution_remarks": "Drainage de-silting is underway. Debris being cleared from channels.",
                "days_ago": 10
            },
            {
                "citizen_name": "Bijay Ketan Mohapatra",
                "contact_number": "9090098765",
                "district": "Khordha",
                "complaint_odia": "ବର୍ତ୍ତମାନ ଆମ ଅଞ୍ଚଳରେ ଶାନ୍ତି ଶୃଙ୍ଖଳା ଠିକ ଅଛି। ଧନ୍ୟବାଦ।",
                "complaint_english": "Currently law and order is fine in our area. Thank you.",
                "predicted_department": "Home Department",
                "assigned_department": "Home Department",
                "sentiment": "Positive",
                "sentiment_score": 0.5,
                "status": "Resolved",
                "resolution_remarks": "Acknowledged and closed.",
                "days_ago": 14
            }
        ]
        
        for case in seed_cases:
            sub_date = base_time - timedelta(days=case["days_ago"])
            sub_date_str = sub_date.strftime("%Y-%m-%d %H:%M:%S")
            # Update date
            cursor.execute(
                """
                INSERT INTO grievances (
                    citizen_name, contact_number, district, complaint_odia, complaint_english, 
                    predicted_department, assigned_department, sentiment, sentiment_score, 
                    status, resolution_remarks, date_submitted, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    case["citizen_name"], case["contact_number"], case["district"],
                    case["complaint_odia"], case["complaint_english"],
                    case["predicted_department"], case["assigned_department"],
                    case["sentiment"], case["sentiment_score"],
                    case["status"], case["resolution_remarks"],
                    sub_date_str, sub_date_str
                )
            )
        conn.commit()
        
        # Save sample data as CSV to data/grievances.csv for compliance with requested project structure
        # Convert seed_cases to dataframe and save
        df_list = []
        for c in seed_cases:
            sub_date = base_time - timedelta(days=c["days_ago"])
            df_list.append({
                "citizen_name": c["citizen_name"],
                "contact_number": c["contact_number"],
                "district": c["district"],
                "complaint_odia": c["complaint_odia"],
                "complaint_english": c["complaint_english"],
                "predicted_department": c["predicted_department"],
                "assigned_department": c["assigned_department"],
                "sentiment": c["sentiment"],
                "sentiment_score": c["sentiment_score"],
                "status": c["status"],
                "resolution_remarks": c["resolution_remarks"],
                "date_submitted": sub_date.strftime("%Y-%m-%d %H:%M:%S")
            })
        pd.DataFrame(df_list).to_csv(os.path.join(settings.BASE_DIR, "data", "grievances.csv"), index=False, encoding="utf-8")
        
        # Save departments list as CSV to data/departments.csv
        dept_list = [{"name": k, "description": v} for k, v in settings.DEPARTMENTS.items()]
        pd.DataFrame(dept_list).to_csv(os.path.join(settings.BASE_DIR, "data", "departments.csv"), index=False, encoding="utf-8")
        
        print("Sample grievances and departments CSVs saved successfully.")

    def insert_grievance(self, citizen_name, contact_number, district, complaint_odia, complaint_english, predicted_department, assigned_department, sentiment, sentiment_score):
        """Inserts a new grievance and returns the inserted row ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            """
            INSERT INTO grievances (
                citizen_name, contact_number, district, complaint_odia, complaint_english, 
                predicted_department, assigned_department, sentiment, sentiment_score, 
                status, date_submitted, last_updated
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending', ?, ?);
            """,
            (
                citizen_name, contact_number, district, complaint_odia, complaint_english,
                predicted_department, assigned_department, sentiment, sentiment_score,
                now_str, now_str
            )
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        
        # Update the CSV file to match
        self.export_db_to_csv()
        return last_id

    def update_grievance_status(self, grievance_id, status, resolution_remarks=None):
        """Updates the status and resolution remarks of a grievance."""
        conn = self.get_connection()
        cursor = conn.cursor()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            """
            UPDATE grievances 
            SET status = ?, resolution_remarks = ?, last_updated = ?
            WHERE id = ?;
            """,
            (status, resolution_remarks, now_str, grievance_id)
        )
        conn.commit()
        conn.close()
        self.export_db_to_csv()

    def update_grievance_department(self, grievance_id, assigned_department):
        """Reassigns the grievance to a different department."""
        conn = self.get_connection()
        cursor = conn.cursor()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            """
            UPDATE grievances 
            SET assigned_department = ?, last_updated = ?
            WHERE id = ?;
            """,
            (assigned_department, now_str, grievance_id)
        )
        conn.commit()
        conn.close()
        self.export_db_to_csv()

    def get_all_grievances(self):
        """Retrieves all grievances from the database as a pandas DataFrame."""
        conn = self.get_connection()
        df = pd.read_sql_query("SELECT * FROM grievances ORDER BY date_submitted DESC;", conn)
        conn.close()
        return df

    def get_grievance_by_id(self, grievance_id):
        """Retrieves a single grievance by ID as a dictionary."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM grievances WHERE id = ?;", (grievance_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def export_db_to_csv(self):
        """Updates CSV in data/grievances.csv to keep it in sync with database edits."""
        try:
            conn = self.get_connection()
            df = pd.read_sql_query("SELECT * FROM grievances;", conn)
            conn.close()
            df.to_csv(os.path.join(settings.BASE_DIR, "data", "grievances.csv"), index=False, encoding="utf-8")
        except Exception as e:
            print(f"Error syncing database to CSV: {e}")
            
    # Metrics and distributions for dashboard helper functions
    def get_metrics_summary(self):
        """Returns dictionary of basic KPIs."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM grievances;")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM grievances WHERE status='Pending';")
        pending = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM grievances WHERE status='In Progress';")
        in_progress = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM grievances WHERE status='Resolved';")
        resolved = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM grievances WHERE sentiment='Negative (Critical)';")
        critical = cursor.fetchone()[0]
        
        conn.close()
        
        resolution_rate = round((resolved / total * 100), 1) if total > 0 else 0.0
        
        return {
            "total": total,
            "pending": pending,
            "in_progress": in_progress,
            "resolved": resolved,
            "critical": critical,
            "resolution_rate": resolution_rate
        }

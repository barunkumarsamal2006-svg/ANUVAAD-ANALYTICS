import os
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

# Slide size: 16:9 ratio in points
WIDTH = 960
HEIGHT = 540

PDF_PATH = "d:/barun/anuvaad_analytics_presentation.pdf"

# Design Theme Colors
COLOR_BG = HexColor("#0b0f19")      # Dark Slate
COLOR_CARD = HexColor("#111827")    # Slightly lighter slate
COLOR_ORANGE = HexColor("#ff8c00")  # Odisha Golden Orange
COLOR_BLUE = HexColor("#3b82f6")    # Accent Blue
COLOR_WHITE = HexColor("#ffffff")   # Main Text
COLOR_GREY = HexColor("#94a3b8")    # Secondary Text
COLOR_LINE = HexColor("#1e293b")    # Grid lines

def draw_slide_template(c, title, subtitle):
    """Draws background, headers, footers, and slide number."""
    # Draw Background
    c.setFillColor(COLOR_BG)
    c.rect(0, 0, WIDTH, HEIGHT, fill=True, stroke=False)
    
    # Draw top header band
    c.setFillColor(COLOR_BLUE)
    c.rect(0, HEIGHT - 5, WIDTH, 5, fill=True, stroke=False)
    
    # Slide Title
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 32)
    c.drawString(50, HEIGHT - 65, title)
    
    # Slide Subtitle / Area
    c.setFillColor(COLOR_ORANGE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, HEIGHT - 90, subtitle.upper())
    
    # Draw Header separator line
    c.setStrokeColor(COLOR_LINE)
    c.setLineWidth(1)
    c.line(50, HEIGHT - 110, WIDTH - 50, HEIGHT - 110)
    
    # Footer
    c.setFillColor(COLOR_GREY)
    c.setFont("Helvetica", 10)
    c.drawString(50, 30, "Anuvaad Analytics  •  AI-Powered Localized Public Grievance Management System (Odisha)")
    c.drawRightString(WIDTH - 50, 30, f"Slide {c.getPageNumber()}")

def create_presentation():
    c = canvas.Canvas(PDF_PATH, pagesize=(WIDTH, HEIGHT))
    
    # ==========================================
    # SLIDE 1: TITLE SLIDE (Odisha themed)
    # ==========================================
    c.setFillColor(COLOR_BG)
    c.rect(0, 0, WIDTH, HEIGHT, fill=True, stroke=False)
    
    # Accent background shapes
    c.setFillColor(HexColor("#1e3a8a"))
    p = c.beginPath()
    p.moveTo(WIDTH - 300, 0)
    p.lineTo(WIDTH, 0)
    p.lineTo(WIDTH, HEIGHT)
    p.lineTo(WIDTH - 150, HEIGHT)
    p.close()
    c.drawPath(p, fill=True, stroke=False)
    
    c.setFillColor(HexColor("#1d4ed8"))
    p = c.beginPath()
    p.moveTo(WIDTH - 200, 0)
    p.lineTo(WIDTH, 0)
    p.lineTo(WIDTH, HEIGHT - 150)
    p.close()
    c.drawPath(p, fill=True, stroke=False)
    
    # Title Text
    c.setFillColor(COLOR_ORANGE)
    c.setFont("Helvetica-Bold", 46)
    c.drawString(80, HEIGHT / 2 + 50, "ANUVAAD-ANALYTICS")
    
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(80, HEIGHT / 2 - 10, "AI-Powered Localized Public Grievance Management")
    
    c.setFillColor(COLOR_GREY)
    c.setFont("Helvetica", 18)
    c.drawString(80, HEIGHT / 2 - 40, "Odisha Government E-Governance Framework")
    
    # Lower details
    c.setStrokeColor(COLOR_ORANGE)
    c.setLineWidth(2)
    c.line(80, HEIGHT / 2 - 80, 400, HEIGHT / 2 - 80)
    
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(80, HEIGHT / 2 - 110, "SYSTEM ARCHITECTURE & TECHNICAL WORKFLOW")
    c.setFillColor(COLOR_GREY)
    c.drawString(80, HEIGHT / 2 - 130, "Automated Translation, NLP Classification & Streamlit Analytics")
    
    c.showPage()
    
    # ==========================================
    # SLIDE 2: THE PROBLEM STATEMENT
    # ==========================================
    draw_slide_template(c, "The Governance Gap", "Problem Statement")
    
    # Left Column: Text
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(80, HEIGHT - 170, "Language Barriers in Public Redressal")
    
    bullets = [
        "Language Divide: 85%+ of citizens in rural Odisha write grievances in Odia.",
        "Systemic Disconnect: Administrative classifications & reporting run in English.",
        "Manual Redressal Bottlenecks: Physical translation is slow, expensive & delayed.",
        "No Priority Insight: Missing automatic sentiment/urgency evaluation of complaints.",
        "Siloed Operations: Lack of direct statistical mapping of district/department performance."
    ]
    
    y = HEIGHT - 210
    c.setFont("Helvetica", 16)
    c.setFillColor(COLOR_GREY)
    for bullet in bullets:
        c.drawString(80, y, f"•  {bullet}")
        y -= 45
        
    # Right Column Box (Callout)
    c.setFillColor(COLOR_CARD)
    c.rect(580, 100, 330, 300, fill=True, stroke=False)
    
    c.setFillColor(COLOR_ORANGE)
    c.setFont("Helvetica-Bold", 64)
    c.drawString(610, 310, "85%")
    
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(610, 270, "Rural Grievance Volume")
    c.setFont("Helvetica", 14)
    c.setFillColor(COLOR_GREY)
    c.drawString(610, 240, "is submitted in native Odia,")
    c.drawString(610, 220, "demanding automated local")
    c.drawString(610, 200, "translation and processing.")
    
    c.showPage()
    
    # ==========================================
    # SLIDE 3: SYSTEM ARCHITECTURE
    # ==========================================
    draw_slide_template(c, "Pipeline Architecture", "Workflow Model")
    
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, HEIGHT - 160, "The Automated Anuvaad Pipeline Flow:")
    
    # Drawing horizontal flow boxes
    steps = [
        {"title": "1. Citizen Input", "desc": "Grievance submitted in Odia text (e.g. BSKY/Kalia schemes)", "color": COLOR_BLUE},
        {"title": "2. Translator", "desc": "Indicator API / Google Translate engine translates to English", "color": COLOR_ORANGE},
        {"title": "3. AI Classifier", "desc": "TF-IDF & Logistic Regression predicts target department", "color": COLOR_BLUE},
        {"title": "4. Sentiment Engine", "desc": "TextBlob calculates polarity & assigns Urgency flags", "color": COLOR_ORANGE},
        {"title": "5. DB & Dashboard", "desc": "Logs to SQLite and renders metrics in Streamlit Dashboard", "color": COLOR_BLUE}
    ]
    
    x = 50
    box_width = 160
    box_height = 200
    y_box = 180
    
    for step in steps:
        # Draw step card
        c.setFillColor(COLOR_CARD)
        c.rect(x, y_box, box_width, box_height, fill=True, stroke=False)
        
        # Color bar
        c.setFillColor(step["color"])
        c.rect(x, y_box + box_height - 6, box_width, 6, fill=True, stroke=False)
        
        # Text
        c.setFillColor(COLOR_WHITE)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(x + 10, y_box + box_height - 35, step["title"])
        
        # Description (wrapped)
        c.setFont("Helvetica", 11)
        c.setFillColor(COLOR_GREY)
        words = step["desc"].split()
        line = ""
        desc_y = y_box + box_height - 65
        for word in words:
            if len(line + " " + word) < 22:
                line += " " + word
            else:
                c.drawString(x + 10, desc_y, line.strip())
                line = word
                desc_y -= 18
        if line:
            c.drawString(x + 10, desc_y, line.strip())
            
        x += box_width + 15
        
    c.setFillColor(COLOR_ORANGE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 120, "RESULT:")
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica", 13)
    c.drawString(120, 120, "Instant department routing, real-time visualization, and urgent negative complaint escalation.")
    
    c.showPage()
    
    # ==========================================
    # SLIDE 4: TRANSLATION ENGINE
    # ==========================================
    draw_slide_template(c, "Indic Translation Engine", "Odia-to-English Conversion")
    
    # Left Column
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(80, HEIGHT - 170, "IndicTrans2 & deep-translator Bridge")
    
    bullets = [
        "API Integration: Powered by deep-translator mapping Odia ('or') to English ('en').",
        "Accuracy: Handles complex Odia conjugations and administrative phrasing.",
        "Sanitization: Removes text symbols, punctuation, and handles double spacing.",
        "Self-Healing Offline Fallback: Integrates local dictionary matching as contingency.",
        "Robustness: Ensures 100% service uptime even in low or offline network conditions."
    ]
    
    y = HEIGHT - 210
    c.setFont("Helvetica", 16)
    c.setFillColor(COLOR_GREY)
    for bullet in bullets:
        c.drawString(80, y, f"•  {bullet}")
        y -= 45
        
    # Right Column Callout (Fallback Dictionary box)
    c.setFillColor(COLOR_CARD)
    c.rect(580, 100, 330, 300, fill=True, stroke=False)
    
    c.setFillColor(COLOR_BLUE)
    c.rect(580, 394, 330, 6, fill=True, stroke=False)
    
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(600, 360, "Offline Local Dictionary")
    c.setFont("Helvetica", 13)
    c.setFillColor(COLOR_GREY)
    c.drawString(600, 330, "Matches Odia keys to Eng meanings:")
    
    dictionary_examples = [
        ("କାଳିଆ ଯୋଜନା", "->  Kalia scheme"),
        ("ବିଏସକେୱାଇ", "->  BSKY health card"),
        ("ଡାକ୍ତରଖାନା", "->  Hospital"),
        ("ପାନୀୟ ଜଳ", "->  Drinking water"),
        ("ଥାନା / ଏଫଆଇଆର", "->  Police / FIR"),
        ("ମଧ୍ୟାହ୍ନ ଭୋଜନ", "->  Mid-day meal")
    ]
    
    dy = 295
    c.setFont("Helvetica-Bold", 12)
    for odia, eng in dictionary_examples:
        c.setFillColor(COLOR_ORANGE)
        c.drawString(600, dy, odia)
        c.setFillColor(COLOR_WHITE)
        c.drawString(710, dy, eng)
        dy -= 28
        
    c.showPage()
    
    # ==========================================
    # SLIDE 5: DEPARTMENT CLASSIFIER
    # ==========================================
    draw_slide_template(c, "AI Department Classifier", "NLP Routing Engine")
    
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(80, HEIGHT - 170, "Automated Machine Learning Categorization")
    
    bullets = [
        "Model Setup: TF-IDF Vectorizer coupled with a Logistic Regression classifier.",
        "Automatic Training: Auto-trains on start if models are missing (self-healing architecture).",
        "Odisha-Specific Focus: Tuned with localized vocabulary (BSKY, Kalia, Mandi, PM Awas, 5T).",
        "High Efficiency: Executes predictions in milliseconds, bypassing human routing errors.",
        "Target Departments: Routes complaints to 6 major sectors (Agriculture, Health, Education, PR & Drinking Water, Home, Urban Development)."
    ]
    
    y = HEIGHT - 210
    c.setFont("Helvetica", 16)
    c.setFillColor(COLOR_GREY)
    for bullet in bullets:
        c.drawString(80, y, f"•  {bullet}")
        y -= 45
        
    # Right Column - Department boxes
    c.setFillColor(COLOR_CARD)
    c.rect(580, 100, 330, 300, fill=True, stroke=False)
    c.setFillColor(COLOR_ORANGE)
    c.rect(580, 394, 330, 6, fill=True, stroke=False)
    
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(600, 360, "Classification Scope")
    
    departments = [
        "1. Agriculture & Farmers",
        "2. Health & Family Welfare",
        "3. School & Mass Education",
        "4. Panchayati Raj & Water",
        "5. Home Department (Police)",
        "6. Housing & Urban Development"
    ]
    
    dy = 320
    c.setFont("Helvetica", 13)
    c.setFillColor(COLOR_GREY)
    for dept in departments:
        c.drawString(600, dy, dept)
        dy -= 32
        
    c.showPage()
    
    # ==========================================
    # SLIDE 6: SENTIMENT & URGENCY SCORING
    # ==========================================
    draw_slide_template(c, "Sentiment & Priority Analytics", "Urgency Detection")
    
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(80, HEIGHT - 170, "Harnessing Emotion for Prioritization")
    
    bullets = [
        "Sentiment Lexicon: Powered by TextBlob analyzer evaluating polarity (-1.0 to +1.0).",
        "Smart Categorization: Automatically labels sentiment: Positive, Neutral, or Negative.",
        "Urgency Escalation: Negative sentiment instantly flags grievances as 'Negative (Critical)'.",
        "Prioritized Action: Critical complaints are moved to the top of the officer's resolution panel.",
        "Empathy Mapping: Helps administration identify distressed areas and sectors dynamically."
    ]
    
    y = HEIGHT - 210
    c.setFont("Helvetica", 16)
    c.setFillColor(COLOR_GREY)
    for bullet in bullets:
        c.drawString(80, y, f"•  {bullet}")
        y -= 45
        
    # Right Column Callout (Sentiment Gauge)
    c.setFillColor(COLOR_CARD)
    c.rect(580, 100, 330, 300, fill=True, stroke=False)
    c.setFillColor(HexColor("#ef4444"))
    c.rect(580, 394, 330, 6, fill=True, stroke=False)
    
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(600, 360, "Priority Mapping Rule")
    
    c.setFont("Helvetica", 13)
    c.setFillColor(COLOR_GREY)
    c.drawString(600, 320, "Polarity < -0.1  -->  Negative (Critical)")
    c.drawString(600, 290, "Polarity > 0.1   -->  Positive")
    c.drawString(600, 260, "Otherwise       -->  Neutral")
    
    c.setStrokeColor(COLOR_LINE)
    c.line(600, 230, 890, 230)
    
    # Alert Box inside
    c.setFillColor(HexColor("#ef4444"))
    c.rect(600, 130, 290, 80, fill=True, stroke=False)
    
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(615, 180, "CRITICAL ALERT SYSTEM")
    c.setFont("Helvetica", 11)
    c.drawString(615, 160, "Severe grievances bypass regular queues,")
    c.drawString(615, 145, "alerting officers immediately.")
    
    c.showPage()
    
    # ==========================================
    # SLIDE 7: OFFICER DASHBOARD
    # ==========================================
    draw_slide_template(c, "Officer Analytics Dashboard", "Administrative Panel")
    
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(80, HEIGHT - 170, "E-Governance Monitoring Hub")
    
    bullets = [
        "Executive KPIs: Live cards showing Total, Pending, Resolved, and Resolution Rate.",
        "Interactive Charts: Plotly graphs displaying department loads and regional volume.",
        "Geographical Heat Map: District-wise breakdown representing top grievance sources.",
        "Timeline Trends: 30-day inflow logs displaying historical filing velocity.",
        "Control Center: Officers can filter, re-assign departments, update status, and log remarks."
    ]
    
    y = HEIGHT - 210
    c.setFont("Helvetica", 16)
    c.setFillColor(COLOR_GREY)
    for bullet in bullets:
        c.drawString(80, y, f"•  {bullet}")
        y -= 45
        
    # Right Column Callout (Dashboard visual mockup)
    c.setFillColor(COLOR_CARD)
    c.rect(580, 100, 330, 300, fill=True, stroke=False)
    c.setFillColor(COLOR_BLUE)
    c.rect(580, 394, 330, 6, fill=True, stroke=False)
    
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(600, 360, "Dashboard Core Metrics")
    
    # Custom display boxes inside
    metrics_box = [
        ("Total Active cases", "14 Active Cases", COLOR_BLUE),
        ("Resolution Rate", "35.7% Closed", HexColor("#10b981")),
        ("Critical Grievances", "13 Flagged Cases", HexColor("#ef4444"))
    ]
    
    dy = 300
    for name, stat, col in metrics_box:
        c.setFillColor(HexColor("#1e293b"))
        c.rect(600, dy, 290, 45, fill=True, stroke=False)
        
        c.setFillColor(COLOR_WHITE)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(615, dy + 25, name)
        
        c.setFillColor(col)
        c.setFont("Helvetica-Bold", 12)
        c.drawRightString(875, dy + 15, stat)
        dy -= 60
        
    c.showPage()
    
    # ==========================================
    # SLIDE 8: VALUE PROPOSITION
    # ==========================================
    draw_slide_template(c, "Impact & Value Proposition", "Key Governance Outcomes")
    
    # 2x2 Grid of benefits
    benefits = [
        {
            "title": "Language-Inclusive Governance",
            "desc": "Empowers non-English speaking rural citizens to raise issues directly in Odia, making governance accessible to all.",
            "color": COLOR_ORANGE
        },
        {
            "title": "Operational Automation",
            "desc": "Reduces inter-departmental routing times from weeks to milliseconds, eliminating manual administrative delays.",
            "color": COLOR_BLUE
        },
        {
            "title": "Empathetic Prioritization",
            "desc": "Automatically extracts emotional urgency from text, prioritizing distressed citizens in critical need.",
            "color": COLOR_BLUE
        },
        {
            "title": "Data-Driven Decisions",
            "desc": "Renders visual analytics of district and department performance, highlighting bottlenecks for policy makers.",
            "color": COLOR_ORANGE
        }
    ]
    
    # Positions
    positions = [
        (80, 270),  # Top Left
        (510, 270), # Top Right
        (80, 100),  # Bottom Left
        (510, 100)  # Bottom Right
    ]
    
    for benefit, pos in zip(benefits, positions):
        bx, by = pos
        c.setFillColor(COLOR_CARD)
        c.rect(bx, by, 370, 140, fill=True, stroke=False)
        
        # Color bar
        c.setFillColor(benefit["color"])
        c.rect(bx, by + 134, 370, 6, fill=True, stroke=False)
        
        # Title
        c.setFillColor(COLOR_WHITE)
        c.setFont("Helvetica-Bold", 15)
        c.drawString(bx + 15, by + 105, benefit["title"])
        
        # Description
        c.setFont("Helvetica", 11)
        c.setFillColor(COLOR_GREY)
        words = benefit["desc"].split()
        line = ""
        desc_y = by + 80
        for word in words:
            if len(line + " " + word) < 55:
                line += " " + word
            else:
                c.drawString(bx + 15, desc_y, line.strip())
                line = word
                desc_y -= 18
        if line:
            c.drawString(bx + 15, desc_y, line.strip())
            
    c.showPage()
    c.save()
    print("Presentation PDF generated successfully at:", PDF_PATH)

if __name__ == "__main__":
    create_presentation()

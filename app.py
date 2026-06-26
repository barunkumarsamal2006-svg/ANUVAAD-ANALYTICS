import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from datetime import datetime

# Import project modules
from config import settings
from database.db_handler import DatabaseHandler
from pipeline.translator import translate_odia_to_english
from pipeline.sentiment import analyze_sentiment
from pipeline.classifier import predict_department, train_classifier
from dashboard.metrics import display_metrics
import dashboard.charts as charts

# Page Config
st.set_page_config(
    page_title="Anuvaad Analytics - Public Grievance Management System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Initialize Database Handler (Self-heals and seeds database/CSVs if missing)
db = DatabaseHandler()

# Custom CSS for Premium Odisha Govt Theme
custom_css = """
<style>
    /* Main Layout Styling */
    .main {
        background-color: #0b0f19;
        color: #f8fafc;
    }
    
    /* Header & Branding */
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #0f172a 100%);
        border-bottom: 3px solid #ff8c00;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .header-title {
        color: #ffffff;
        font-family: 'Outfit', 'Inter', sans-serif;
        font-weight: 800;
        margin-left: 20px;
    }
    .header-subtitle {
        color: #ff8c00;
        font-size: 0.95rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-left: 20px;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #0f172a;
        padding: 8px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 600;
        transition: all 0.2s ease;
        padding: 10px 20px;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #f8fafc;
        background-color: rgba(255, 255, 255, 0.03);
    }
    .stTabs [aria-selected="true"] {
        background-color: #ff8c00 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(255, 140, 0, 0.3);
    }

    /* Cards and Containers */
    .content-card {
        background-color: #111827;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .accent-header {
        border-left: 4px solid #ff8c00;
        padding-left: 10px;
        margin-bottom: 15px;
        font-weight: 700;
        color: #f8fafc;
    }

    /* Badges */
    .badge {
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        display: inline-block;
    }
    .badge-pending { background-color: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); }
    .badge-progress { background-color: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.3); }
    .badge-resolved { background-color: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-rejected { background-color: rgba(100, 116, 139, 0.15); color: #64748b; border: 1px solid rgba(100, 116, 139, 0.3); }

    .badge-neg { background-color: rgba(225, 29, 72, 0.15); color: #e11d48; border: 1px solid rgba(225, 29, 72, 0.3); }
    .badge-neu { background-color: rgba(59, 130, 246, 0.15); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.3); }
    .badge-pos { background-color: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.image(
        "assets/logo.png" if os.path.exists("assets/logo.png") else "https://via.placeholder.com/150", 
        use_container_width=True
    )
    st.markdown("<h3 style='text-align: center; color: #ff8c00; margin-bottom: 0;'>ANUVAAD ANALYTICS</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>AI Public Grievance Portal - Odisha</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # App statistics quick view
    st.subheader("System Info")
    metrics = db.get_metrics_summary()
    st.write(f"🌐 **Translation backend:** `deep-translator`")
    st.write(f"🤖 **Department Classifier:** `TF-IDF + LogisticRegression`")
    st.write(f"📝 **Grievance Database:** `SQLite (Local)`")
    st.write(f"📊 **Total Active Records:** `{metrics['total']}`")
    
    st.markdown("---")
    # Quick Action: Train/Retrain model
    if st.button("🔄 Retrain ML Classifier"):
        with st.spinner("Retraining NLP model..."):
            train_classifier()
            st.success("Model trained successfully!")

# ----------------- MAIN TITLE HEADER -----------------
st.markdown(
    """
    <div class="main-header">
        <div>
            <span class="header-subtitle">Government of Odisha • Public Grievance Portal</span>
            <h1 class="header-title" style="margin: 5px 0 0 20px; font-size: 2.2rem;">ଅନୁବାଦ - ANUVAAD ANALYTICS</h1>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------- TABS SYSTEM -----------------
tab1, tab2 = st.tabs([
    "📝 CITIZEN PORTAL (SUBMIT GRIEVANCE)", 
    "📊 OFFICER DASHBOARD & ANALYTICS"
])

# ==========================================
# TAB 1: CITIZEN PORTAL
# ==========================================
with tab1:
    st.markdown("<h3 class='accent-header'>Submit a New Grievance / ଅଭିଯୋଗ ପଞ୍ଜିକରଣ</h3>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        with st.form("citizen_complaint_form", clear_on_submit=True):
            st.markdown("##### Fill Citizen Details")
            c_name = st.text_input("Full Name / ପୂରା ନାମ", placeholder="Enter your full name")
            c_phone = st.text_input("Contact Number / ମୋବାଇଲ୍ ନମ୍ବର", placeholder="10-digit mobile number")
            c_district = st.selectbox("Select District / ଜିଲ୍ଲା ଚୟନ କରନ୍ତୁ", settings.ODISHA_DISTRICTS, index=18) # default Khordha
            
            st.markdown("---")
            st.markdown("##### Describe Grievance in Odia / ଆପଣଙ୍କର ଅଭିଯୋଗ ଓଡ଼ିଆରେ ଲେଖନ୍ତୁ")
            st.caption("Tip: You can type in Odia or write using the Odia keyboard layout. Example: 'କାଳିଆ ଯୋଜନାର ଟଙ୍କା ମିଳିନି'")
            c_complaint = st.text_area(
                "Write complaint details / ଅଭିଯୋଗର ବିବରଣୀ", 
                height=150, 
                placeholder="ଏଠାରେ ଆପଣଙ୍କର ଅଭିଯୋଗ ଲେଖନ୍ତୁ..."
            )
            
            submit_btn = st.form_submit_button("🚀 Submit Grievance / ଅଭିଯୋଗ ଦାଖଲ କରନ୍ତୁ")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_right:
        st.markdown("<h5 style='color: #ff8c00;'>AI Translation & Processing Engine</h5>", unsafe_allow_html=True)
        st.write("When you click submit, the system automatically triggers the following pipeline:")
        
        # Timeline visualizer
        st.markdown(
            """
            <div style="background-color: #0f172a; padding: 15px; border-radius: 8px; border-left: 3px solid #3b82f6;">
                <ol style="margin-left: -15px; margin-bottom: 0; font-size: 0.9rem; line-height: 1.6;">
                    <li><b>Language Detection & Translation</b>: Translates Odia text to English via <i>IndicTrans/Google API</i>.</li>
                    <li><b>Department Classification</b>: NLP classifier assigns complaint to the correct government department.</li>
                    <li><b>Sentiment & Urgency Scoring</b>: Evaluates sentiment (Negative complaints are flagged as <b>Critical</b>).</li>
                    <li><b>Database Registration</b>: Logs data to secure SQLite storage for officer action.</li>
                </ol>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        if submit_btn:
            # Validations
            if not c_name:
                st.error("Please enter citizen name.")
            elif not c_phone or len(c_phone) < 10 or not c_phone.isdigit():
                st.error("Please enter a valid 10-digit contact number.")
            elif not c_complaint or len(c_complaint.strip()) < 5:
                st.error("Please enter detailed complaint description in Odia.")
            else:
                with st.spinner("Processing grievance through AI Translation and Classification Engine..."):
                    # 1. Translate
                    translated_text = translate_odia_to_english(c_complaint)
                    
                    # 2. Classify Department
                    pred_dept, confidence = predict_department(translated_text)
                    
                    # 3. Analyze Sentiment
                    sentiment_lbl, sentiment_val = analyze_sentiment(translated_text)
                    
                    # 4. Save to Database
                    grievance_id = db.insert_grievance(
                        citizen_name=c_name,
                        contact_number=c_phone,
                        district=c_district,
                        complaint_odia=c_complaint,
                        complaint_english=translated_text,
                        predicted_department=pred_dept,
                        assigned_department=pred_dept, # initial assignment
                        sentiment=sentiment_lbl,
                        sentiment_score=sentiment_val
                    )
                    
                    # Output Gorgeous Results Panel
                    st.balloons()
                    st.success(f"🎉 Grievance Submitted Successfully! ID: #{grievance_id}")
                    
                    st.markdown('<div class="content-card">', unsafe_allow_html=True)
                    st.markdown("#### 🔍 AI Processing Output")
                    st.markdown("---")
                    
                    st.write(f"🗣️ **Original Odia Complaint:**")
                    st.info(c_complaint)
                    
                    st.write(f"🔤 **English Translation:**")
                    st.code(translated_text, language="text")
                    
                    # Badges grid
                    c_col1, c_col2, c_col3 = st.columns(3)
                    with c_col1:
                        st.write("**Predicted Department:**")
                        st.markdown(f"<span style='color:#ff8c00; font-weight:700;'>{pred_dept}</span>", unsafe_allow_html=True)
                        st.caption(f"Confidence Score: {confidence*100}%")
                    with c_col2:
                        st.write("**Sentiment Analysis:**")
                        badge_class = "badge-neg" if "Negative" in sentiment_lbl else ("badge-pos" if "Positive" in sentiment_lbl else "badge-neu")
                        st.markdown(f"<span class='badge {badge_class}'>{sentiment_lbl}</span>", unsafe_allow_html=True)
                        st.caption(f"Score: {sentiment_val}")
                    with c_col3:
                        st.write("**Assigned Status:**")
                        st.markdown("<span class='badge badge-pending'>Pending</span>", unsafe_allow_html=True)
                        st.caption("Needs Officer Review")
                        
                    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# TAB 2: OFFICER PORTAL
# ==========================================
with tab2:
    # 1. Global KPIs
    st.markdown("<h3 class='accent-header'>Administrative Performance Overview</h3>", unsafe_allow_html=True)
    
    # Reload stats
    current_metrics = db.get_metrics_summary()
    display_metrics(current_metrics)
    
    st.write("")
    
    # 2. Charts Section
    col_chart1, col_chart2 = st.columns(2)
    
    # Get all records
    df_grievances = db.get_all_grievances()
    
    with col_chart1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        dept_fig = charts.plot_department_distribution(df_grievances)
        if dept_fig:
            st.plotly_chart(dept_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        sent_fig = charts.plot_sentiment_distribution(df_grievances)
        if sent_fig:
            st.plotly_chart(sent_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_chart2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        status_fig = charts.plot_status_distribution(df_grievances)
        if status_fig:
            st.plotly_chart(status_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        dist_fig = charts.plot_district_distribution(df_grievances)
        if dist_fig:
            st.plotly_chart(dist_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. Time Series trend
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    trend_fig = charts.plot_timeline_trend(df_grievances)
    if trend_fig:
        st.plotly_chart(trend_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. Grievance Management and Resolution Panel
    st.markdown("<h3 class='accent-header'>Grievance Redressal Control Panel</h3>", unsafe_allow_html=True)
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    
    # Filter controls in columns
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    with f_col1:
        dept_filter = st.selectbox("Filter Department", ["All"] + list(settings.DEPARTMENTS.keys()))
    with f_col2:
        dist_filter = st.selectbox("Filter District", ["All"] + settings.ODISHA_DISTRICTS)
    with f_col3:
        status_filter = st.selectbox("Filter Status", ["All", "Pending", "In Progress", "Resolved", "Rejected"])
    with f_col4:
        sentiment_filter = st.selectbox("Filter Sentiment", ["All", "Negative (Critical)", "Neutral", "Positive"])
        
    # Apply filters
    filtered_df = df_grievances.copy()
    if dept_filter != "All":
        filtered_df = filtered_df[filtered_df["assigned_department"] == dept_filter]
    if dist_filter != "All":
        filtered_df = filtered_df[filtered_df["district"] == dist_filter]
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["status"] == status_filter]
    if sentiment_filter != "All":
        filtered_df = filtered_df[filtered_df["sentiment"] == sentiment_filter]
        
    # Display table of grievances
    st.write(f"Showing **{len(filtered_df)}** matching grievances:")
    
    # Select columns for displaying
    display_cols = ["id", "citizen_name", "district", "assigned_department", "sentiment", "status", "date_submitted"]
    
    # Format table for high styling
    if not filtered_df.empty:
        st.dataframe(
            filtered_df[display_cols].rename(columns={
                "id": "ID", 
                "citizen_name": "Citizen", 
                "district": "District",
                "assigned_department": "Assigned Department", 
                "sentiment": "Sentiment",
                "status": "Status", 
                "date_submitted": "Date Submitted"
            }),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No grievances found matching the filters.")
        
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. Resolve Selected Grievance Form
    st.markdown("#### ⚙️ Manage & Resolve Grievance")
    if not filtered_df.empty:
        # Create a dropdown to select a grievance ID to update
        grievance_ids = filtered_df["id"].tolist()
        selected_id = st.selectbox("Select Grievance ID to Action", grievance_ids, format_func=lambda x: f"Grievance #{x} - {filtered_df[filtered_df['id']==x]['citizen_name'].values[0]} ({filtered_df[filtered_df['id']==x]['district'].values[0]})")
        
        # Load details of selected grievance
        g_details = db.get_grievance_by_id(selected_id)
        
        if g_details:
            # Display detailed view
            st.markdown('<div class="content-card" style="background-color: #0f172a;">', unsafe_allow_html=True)
            
            d_col1, d_col2 = st.columns(2)
            with d_col1:
                st.markdown(f"👥 **Citizen Name:** {g_details['citizen_name']} | 📞 **Contact:** {g_details['contact_number']}")
                st.markdown(f"📍 **District:** {g_details['district']}")
                st.markdown(f"📅 **Date Submitted:** {g_details['date_submitted']}")
                st.markdown(f"🔄 **Last Updated:** {g_details['last_updated']}")
                
                # Status Badges
                st.write("**Current status:**")
                s_badge = f"badge-{g_details['status'].lower().replace(' ', '')}"
                st.markdown(f"<span class='badge {s_badge}'>{g_details['status']}</span>", unsafe_allow_html=True)
                
            with d_col2:
                # Translation & sentiment
                st.write("**Sentiment Score:**")
                badge_class = "badge-neg" if "Negative" in g_details['sentiment'] else ("badge-pos" if "Positive" in g_details['sentiment'] else "badge-neu")
                st.markdown(f"<span class='badge {badge_class}'>{g_details['sentiment']}</span> (Score: {g_details['sentiment_score']})", unsafe_allow_html=True)
                
                st.write("**Original Odia Complaint:**")
                st.caption(g_details['complaint_odia'])
                
                st.write("**Translated English Complaint:**")
                st.text_area("English Translation (Read-only)", value=g_details['complaint_english'], height=60, disabled=True)
            
            st.markdown("---")
            
            # Action controls
            act_col1, act_col2 = st.columns(2)
            with act_col1:
                st.markdown("##### Administrative Action")
                new_status = st.selectbox(
                    "Update Status", 
                    ["Pending", "In Progress", "Resolved", "Rejected"], 
                    index=["Pending", "In Progress", "Resolved", "Rejected"].index(g_details['status'])
                )
                
                new_dept = st.selectbox(
                    "Re-assign Department (Correction)", 
                    list(settings.DEPARTMENTS.keys()),
                    index=list(settings.DEPARTMENTS.keys()).index(g_details['assigned_department'])
                )
                
            with act_col2:
                st.markdown("##### Action Taken / Resolution Remarks")
                remarks = st.text_area(
                    "Resolution Remarks", 
                    value=g_details['resolution_remarks'] or "",
                    placeholder="Describe resolution details or investigation progress...",
                    height=120
                )
            
            if st.button("💾 Apply Actions & Save Changes"):
                # Save changes
                db.update_grievance_status(selected_id, new_status, remarks)
                if new_dept != g_details['assigned_department']:
                    db.update_grievance_department(selected_id, new_dept)
                
                st.success(f"Grievance #{selected_id} successfully updated!")
                # Force rerun to reload graphs and table
                st.rerun()
                
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Select a different filter combination to view and action grievances.")

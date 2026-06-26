import plotly.express as px
import pandas as pd
import streamlit as st

# Color palettes for uniform premium look
STATUS_COLORS = {
    "Pending": "#ef4444",      # Soft Red
    "In Progress": "#f59e0b",   # Amber
    "Resolved": "#10b981",      # Emerald
    "Rejected": "#64748b"       # Slate
}

SENTIMENT_COLORS = {
    "Negative (Critical)": "#e11d48", # Rose
    "Neutral": "#3b82f6",             # Blue
    "Positive": "#10b981"             # Emerald
}

DEPT_COLORS = ["#3b82f6", "#10b981", "#8b5cf6", "#f59e0b", "#06b6d4", "#ec4899"]

def plot_department_distribution(df):
    """Plots interactive bar chart of grievances per department."""
    if df.empty:
        st.info("No data available for department distribution.")
        return None
        
    dept_counts = df["assigned_department"].value_counts().reset_index()
    dept_counts.columns = ["Department", "Grievance Count"]
    
    fig = px.bar(
        dept_counts,
        y="Department",
        x="Grievance Count",
        orientation="h",
        color="Department",
        color_discrete_sequence=DEPT_COLORS,
        title="<b>Grievance Distribution by Department</b>",
        text_auto=True
    )
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        showlegend=False,
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="Number of Grievances"),
        yaxis=dict(title=None, categoryorder="total ascending"),
        margin=dict(l=20, r=20, t=40, b=20),
        height=320
    )
    return fig

def plot_status_distribution(df):
    """Plots interactive donut chart of grievance statuses."""
    if df.empty:
        st.info("No data available for status distribution.")
        return None
        
    status_counts = df["status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    
    # Map colors
    colors = [STATUS_COLORS.get(s, "#94a3b8") for s in status_counts["Status"]]
    
    fig = px.pie(
        status_counts,
        names="Status",
        values="Count",
        hole=0.6,
        color="Status",
        color_discrete_map=STATUS_COLORS,
        title="<b>Resolution Status Breakdown</b>"
    )
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=40, b=20),
        height=320
    )
    fig.update_traces(textposition='inside', textinfo='percent+value')
    return fig

def plot_sentiment_distribution(df):
    """Plots interactive donut chart of grievance sentiments."""
    if df.empty:
        st.info("No data available for sentiment distribution.")
        return None
        
    sent_counts = df["sentiment"].value_counts().reset_index()
    sent_counts.columns = ["Sentiment", "Count"]
    
    fig = px.pie(
        sent_counts,
        names="Sentiment",
        values="Count",
        hole=0.6,
        color="Sentiment",
        color_discrete_map=SENTIMENT_COLORS,
        title="<b>Grievance Sentiment Split</b>"
    )
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=40, b=20),
        height=320
    )
    fig.update_traces(textposition='inside', textinfo='percent+value')
    return fig

def plot_timeline_trend(df):
    """Plots a line chart showing trends over time."""
    if df.empty:
        st.info("No timeline data available.")
        return None
        
    # Convert dates and extract day
    df_copy = df.copy()
    df_copy["date_parsed"] = pd.to_datetime(df_copy["date_submitted"])
    df_copy["Date"] = df_copy["date_parsed"].dt.strftime("%Y-%m-%d")
    
    timeline = df_copy.groupby("Date").size().reset_index(name="Complaints Submitted")
    timeline = timeline.sort_values("Date")
    
    fig = px.line(
        timeline,
        x="Date",
        y="Complaints Submitted",
        title="<b>Grievance Inflow Trend (Last 30 Days)</b>",
        markers=True,
        line_shape="linear"
    )
    
    # Stylize trace
    fig.update_traces(line_color="#3b82f6", line_width=3, marker=dict(size=8, color="#ff8c00"))
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", title=None, tickangle=-45),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="Complaints"),
        margin=dict(l=20, r=20, t=40, b=20),
        height=320
    )
    return fig

def plot_district_distribution(df):
    """Plots a horizontal bar chart showing grievance count by Odisha District."""
    if df.empty:
        st.info("No data available for district distribution.")
        return None
        
    dist_counts = df["district"].value_counts().reset_index()
    dist_counts.columns = ["District", "Count"]
    
    fig = px.bar(
        dist_counts.head(10), # Show top 10 districts for clarity
        x="Count",
        y="District",
        orientation="h",
        title="<b>Top Affected Districts (Grievance Counts)</b>",
        color="Count",
        color_continuous_scale=px.colors.sequential.Oranges,
        text_auto=True
    )
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        coloraxis_showscale=False,
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="Complaints"),
        yaxis=dict(title=None, categoryorder="total ascending"),
        margin=dict(l=20, r=20, t=40, b=20),
        height=320
    )
    return fig

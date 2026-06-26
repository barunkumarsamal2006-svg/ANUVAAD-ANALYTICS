import streamlit as st

def display_metrics(metrics):
    """
    Displays global KPIs for the government officers' dashboard.
    Uses custom CSS classes to achieve a premium dashboard appearance.
    """
    # 5-column layout for key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Custom HTML for cards with side-borders, shadows, and subtle hovering effects
    card_css = """
    <style>
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 12px;
        padding: 20px 15px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.05);
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .metric-title {
        color: #94a3b8;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    .metric-value {
        color: #f8fafc;
        font-size: 2rem;
        font-weight: 800;
        line-height: 1;
    }
    </style>
    """
    st.markdown(card_css, unsafe_allow_html=True)
    
    with col1:
        st.markdown(
            '<div class="metric-card" style="border-top: 4px solid #3b82f6;">'
            '<div class="metric-title">Total Grievances</div>'
            f'<div class="metric-value" style="color: #3b82f6;">{metrics["total"]}</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            '<div class="metric-card" style="border-top: 4px solid #ef4444;">'
            '<div class="metric-title">Pending</div>'
            f'<div class="metric-value" style="color: #ef4444;">{metrics["pending"]}</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            '<div class="metric-card" style="border-top: 4px solid #f59e0b;">'
            '<div class="metric-title">In Progress</div>'
            f'<div class="metric-value" style="color: #f59e0b;">{metrics["in_progress"]}</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with col4:
        st.markdown(
            '<div class="metric-card" style="border-top: 4px solid #10b981;">'
            '<div class="metric-title">Resolved</div>'
            f'<div class="metric-value" style="color: #10b981;">{metrics["resolved"]}</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with col5:
        st.markdown(
            '<div class="metric-card" style="border-top: 4px solid #8b5cf6;">'
            '<div class="metric-title">Resolution Rate</div>'
            f'<div class="metric-value" style="color: #c084fc;">{metrics["resolution_rate"]}%</div>'
            '</div>',
            unsafe_allow_html=True
        )

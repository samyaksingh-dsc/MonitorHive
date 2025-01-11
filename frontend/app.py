import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="Website Monitoring Dashboard",
    page_icon="🌐",
    layout="wide"
)

# Define navigation options
PAGES = {
    "Dashboard": "dashboard",
    "WHOIS Monitoring (Coming Soon)": "whois",
    "Ping/Port Monitoring (Coming Soon)": "ping_port",
    "AI Insights (Coming Soon)": "ai_insights",
    "Dark Web Monitoring (Coming Soon)": "dark_web",
    "SEO Metrics (Coming Soon)": "seo_metrics"
}

def render_dashboard():
    """Render the main dashboard."""
    st.title("🌐 Website Monitoring Dashboard")
    st.write("This is the main dashboard where users can view website metrics and trends.")
    st.info("🚀 Explore the upcoming features in the sidebar!")

def render_whois_monitoring():
    """Render WHOIS Monitoring placeholder."""
    st.title("🔍 WHOIS Monitoring (Coming Soon)")
    st.write("Track domain registration details, ownership changes, and expiry dates.")
    st.info("Example: You'll be able to monitor domains like `example.com` and receive alerts before they expire.")
    st.image("https://via.placeholder.com/800x400?text=WHOIS+Monitoring+Page")

def render_ping_port_monitoring():
    """Render Ping/Port Monitoring placeholder."""
    st.title("🌐 Ping/Port Monitoring (Coming Soon)")
    st.write("Monitor network connectivity and open ports for critical services.")
    st.info("Example: Check if ports like 80 (HTTP), 443 (HTTPS), or 22 (SSH) are open and accessible.")
    st.image("https://via.placeholder.com/800x400?text=Ping+and+Port+Monitoring+Page")

def render_ai_insights():
    """Render AI Insights placeholder."""
    st.title("🧠 AI Insights (Coming Soon)")
    st.write("Leverage AI for anomaly detection, predictive analytics, and intelligent recommendations.")
    st.info("Example: AI will detect unusual traffic spikes or predict SSL certificate expiry trends.")
    st.image("https://via.placeholder.com/800x400?text=AI+Insights+Page")

def render_dark_web_monitoring():
    """Render Dark Web Monitoring placeholder."""
    st.title("🌌 Dark Web Monitoring (Coming Soon)")
    st.write("Track mentions of your digital assets in dark web forums and marketplaces.")
    st.info("Example: Get notified if your brand or sensitive information appears on the dark web.")
    st.image("https://via.placeholder.com/800x400?text=Dark+Web+Monitoring+Page")

def render_seo_metrics():
    """Render SEO Metrics placeholder."""
    st.title("📈 SEO Metrics (Coming Soon)")
    st.write("Monitor Google Search Console data, search performance, and security issues.")
    st.info("Example: Track how your website ranks for key search terms and detect SEO issues.")
    st.image("https://via.placeholder.com/800x400?text=SEO+Metrics+Page")

def main():
    """Main application."""
    st.sidebar.title("Navigation")
    selected_page = st.sidebar.radio("Select a Page", list(PAGES.keys()))
    
    if PAGES[selected_page] == "dashboard":
        render_dashboard()
    elif PAGES[selected_page] == "whois":
        render_whois_monitoring()
    elif PAGES[selected_page] == "ping_port":
        render_ping_port_monitoring()
    elif PAGES[selected_page] == "ai_insights":
        render_ai_insights()
    elif PAGES[selected_page] == "dark_web":
        render_dark_web_monitoring()
    elif PAGES[selected_page] == "seo_metrics":
        render_seo_metrics()

# Constants
API_URL = "http://localhost:8000"

def get_token(email: str, password: str) -> str:
    """Get authentication token from API."""
    try:
        response = requests.post(
            f"{API_URL}/token",
            params={"email": email, "password": password}
        )
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            st.error("Invalid credentials. Please try again.")
            return None
    except Exception as e:
        st.error(f"Error connecting to the server: {str(e)}")
        return None

def api_request(endpoint: str, method="get", token=None, **kwargs):
    """Make authenticated API request."""
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        response = requests.request(method, f"{API_URL}{endpoint}", headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP Error: {http_err.response.status_code} - {http_err.response.reason}")
        return None
    except Exception as e:
        st.error("An unexpected error occurred. Please try again later.")
        return None

def login_form():
    """Display login form."""
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            token = get_token(email, password)
            if token:
                st.session_state.token = token
                st.session_state.logged_in = True
                st.rerun()

def add_website_form(token):
    """Form to add a new website."""
    with st.form("add_website"):
        st.subheader("Add New Website")
        url = st.text_input("Website URL", help="Include http:// or https://")
        name = st.text_input("Website Name")
        monitoring_interval = st.number_input(
            "Monitoring Interval (seconds)", 
            min_value=60, 
            value=300
        )
        
        if st.form_submit_button("Add Website"):
            if url and name:
                response = api_request(
                    "/monitor/websites/",
                    method="post",
                    token=token,
                    json={"url": url, "name": name, "monitoring_interval": monitoring_interval}
                )
                if response:
                    st.success("Website added successfully!")
                    st.rerun()

def display_website_metrics(website, token):
    """Display metrics for a specific website."""
    col1, col2, col3 = st.columns(3)
    
    # Fetch monitoring results, SSL checks, and security headers
    results = api_request(f"/monitor/websites/{website['id']}/results", token=token)
    ssl_checks = api_request(f"/monitor/websites/{website['id']}/ssl", token=token)
    security_headers = api_request(f"/monitor/websites/{website['id']}/security", token=token)
    
    # Display website status
    if results:
        latest_result = results[0]
        with col1:
            st.metric(
                "Website Status",
                "Online" if latest_result["is_up"] else "Offline",
                delta=f"{latest_result['response_time']:.2f}s"
            )
    else:
        st.warning("Unable to fetch website status.")

    # Display SSL status
    if ssl_checks and isinstance(ssl_checks, dict):
        with col2:
            st.metric(
                "SSL Certificate",
                "Valid" if ssl_checks.get("is_valid") else "Invalid",
                delta=f"Expires: {ssl_checks.get('expires_at')[:10]}" if ssl_checks.get("expires_at") else "Unknown"
            )
    else:
        st.warning("SSL data unavailable.")

    # Display security score
    if security_headers and isinstance(security_headers, dict):
        with col3:
            st.metric(
                "Website Security Score",
                f"{security_headers.get('score', 'N/A')}/65"
            )
    else:
        st.warning("Security score unavailable.")

    # Graphs for response time
    if results:
        df = pd.DataFrame(results)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Response Time Graph
        fig_response = px.line(
            df,
            x='timestamp',
            y='response_time',
            title='Response Time Over Time',
            labels={'response_time': 'Response Time (s)', 'timestamp': 'Time'}
        )
        st.plotly_chart(fig_response, use_container_width=True)

        # Uptime History Graph
        fig_uptime = px.scatter(
            df,
            x='timestamp',
            y='status_code',
            color='is_up',
            title='Uptime History',
            color_discrete_map={True: 'green', False: 'red'},
            labels={'status_code': 'Status Code', 'timestamp': 'Time'}
        )
        st.plotly_chart(fig_uptime, use_container_width=True)

def future_features():
    """Placeholders for future features."""
    st.sidebar.title("Future Features (Coming Soon)")
    st.sidebar.markdown("🚀 **WHOIS Monitoring**: Track domain registration details and expiry.")
    st.sidebar.markdown("🔍 **Ping/Port Monitoring**: Check network connectivity and open ports.")
    st.sidebar.markdown("🧠 **AI Insights**: Intelligent anomaly detection and predictions.")
    st.sidebar.markdown("🌌 **Dark Web Monitoring**: Monitor mentions of digital assets in dark web forums.")
    st.sidebar.markdown("📈 **SEO Metrics**: Google Search Console integration for search performance insights.")

def main():
    """Main application."""
    st.title("🌐 Website Monitoring Dashboard")
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        login_form()
    else:
        # Sidebar
        st.sidebar.title("Navigation")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.token = None
            st.rerun()
        
        # Add website form in sidebar
        add_website_form(st.session_state.token)
        
        # Future feature placeholders
        future_features()

        # Get user's websites
        websites = api_request("/monitor/websites/", token=st.session_state.token)
        
        if websites:
            # Website selector
            selected_website = st.selectbox(
                "Select Website",
                options=websites,
                format_func=lambda x: x['name']
            )
            
            if selected_website:
                st.header(selected_website['name'])
                st.write(f"URL: {selected_website['url']}")
                
                # Refresh button
                if st.button("Refresh Data"):
                    api_request(
                        f"/monitor/websites/{selected_website['id']}/check",
                        method="post",
                        token=st.session_state.token
                    )
                    st.success("Website check triggered!")
                    st.rerun()
                
                # Display metrics and graphs
                display_website_metrics(selected_website, st.session_state.token)
        else:
            st.info("No websites added yet. Add your first website using the form in the sidebar!")

if __name__ == "__main__":
    main()

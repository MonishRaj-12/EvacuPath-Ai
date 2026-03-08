import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval
from logic import get_evacuation_details, get_coords_from_address
import time
import math
import requests
import polyline
import numpy as np

st.set_page_config(
    page_title="Chennai Emergency Evacuation System", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for world-class UI
st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main container styling */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: 1px;
    }
    
    .sub-title {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* Card styling - FIXED EMPTY BOXES */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
        min-height: 200px;
        display: flex;
        flex-direction: column;
    }
    
    .info-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 25px rgba(0,0,0,0.15);
    }
    
    /* Metric styling - FIXED */
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
        min-width: 200px;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 500;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0.2rem 0;
        line-height: 1.2;
    }
    
    .metric-unit {
        font-size: 1rem;
        opacity: 0.8;
        font-weight: 400;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .status-safe {
        background: #28a745;
        color: white;
    }
    
    .status-danger {
        background: #dc3545;
        color: white;
    }
    
    .status-warning {
        background: #ffc107;
        color: #212529;
    }
    
    /* Step styling - IMPROVED */
    .step-container {
        background: #f8f9fa;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 10px 10px 0;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        cursor: pointer;
    }
    
    .step-container:hover {
        background: #e9ecef;
        transform: translateX(5px);
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .step-number {
        background: #28a745;
        color: white;
        width: 30px;
        height: 30px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        font-size: 0.9rem;
        font-weight: 600;
        margin-right: 1rem;
        flex-shrink: 0;
    }
    
    .step-text {
        flex-grow: 1;
        font-size: 1rem;
        color: #333;
    }
    
    .step-distance {
        background: #e9ecef;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        color: #666;
        margin-left: 0.5rem;
        flex-shrink: 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Map container */
    .map-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        background: white;
        padding: 1rem;
    }
    
    /* Direction panel - NEW */
    .direction-panel {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
        max-height: 300px;
        overflow-y: auto;
        border: 1px solid #e0e0e0;
    }
    
    .direction-step {
        padding: 0.8rem;
        border-bottom: 1px solid #e0e0e0;
        display: flex;
        align-items: flex-start;
    }
    
    .direction-step:last-child {
        border-bottom: none;
    }
    
    .direction-icon {
        background: #667eea;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 1rem;
        flex-shrink: 0;
        font-weight: 600;
    }
    
    .direction-text {
        flex-grow: 1;
    }
    
    .direction-instruction {
        font-weight: 500;
        color: #333;
    }
    
    .direction-detail {
        font-size: 0.8rem;
        color: #666;
        margin-top: 0.2rem;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 1rem;
        color: white;
        font-size: 0.9rem;
        margin-top: 2rem;
        background: rgba(0,0,0,0.2);
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    roads = pd.read_csv('chennai_road_status.csv')
    disasters = pd.read_csv('disaster_zones.csv')
    shelters = pd.read_csv('shelters.csv')
    return roads, disasters, shelters

roads_df, disasters_df, shelters_df = load_data()

# Function to get OSRM route (Open Source Routing Machine)
def get_osrm_route(start_lat, start_lon, end_lat, end_lon):
    """Get route from OSRM service (like Google Maps but free)"""
    try:
        # Using OSRM demo server (for production, use your own)
        url = f"http://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}"
        params = {
            'overview': 'full',
            'geometries': 'polyline',
            'steps': 'true'
        }
        
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 'Ok':
                route = data['routes'][0]
                # Decode polyline
                points = polyline.decode(route['geometry'])
                
                # Extract step-by-step directions
                steps = []
                for leg in route['legs']:
                    for step in leg['steps']:
                        steps.append({
                            'instruction': step['maneuver']['type'].replace('_', ' ').title(),
                            'name': step.get('name', 'Unknown road'),
                            'distance': step['distance'] / 1000,  # Convert to km
                            'duration': step['duration'] / 60  # Convert to minutes
                        })
                
                return {
                    'points': points,
                    'steps': steps,
                    'distance': route['distance'] / 1000,  # km
                    'duration': route['duration'] / 60  # minutes
                }
    except Exception as e:
        st.error(f"Route calculation error: {str(e)}")
        return None

# Function to calculate bearing for direction icons
def calculate_bearing(lat1, lon1, lat2, lon2):
    """Calculate bearing between two points"""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    bearing = math.degrees(math.atan2(x, y))
    bearing = (bearing + 360) % 360
    return bearing

def get_direction_symbol(bearing):
    """Convert bearing to direction symbol"""
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    idx = round(bearing / 45) % 8
    return directions[idx]

# Header Section
st.markdown("""
    <div class="main-header">
        <div class="main-title">Chennai Emergency Evacuation System</div>
        <div class="sub-title">Real-time Disaster Response and Evacuation Management</div>
    </div>
""", unsafe_allow_html=True)

# --- INPUT SECTION ---
with st.sidebar:
    st.markdown('<div class="sidebar-header">Location Settings</div>', unsafe_allow_html=True)
    
    search_query = st.text_input("Search Location", "T. Nagar", 
                                 help="Enter a place name in Chennai")
    
    track_gps = st.checkbox("Enable GPS Tracking", 
                           help="Use your device's GPS for precise location")
    
    # Route preference
    route_preference = st.selectbox(
        "Route Preference",
        ["Fastest", "Safest", "Shortest"],
        help="Choose your preferred route type"
    )
    
    # Default Coordinates (Chennai Center)
    u_lat, u_lon = 13.0827, 80.2707 

    if track_gps:
        try:
            if st.button("Get Current Location", key="gps_btn"):
                location = streamlit_js_eval(
                    js_expressions="""
                    new Promise((resolve) => {
                        if (navigator.geolocation) {
                            navigator.geolocation.getCurrentPosition(
                                (position) => {
                                    resolve({
                                        lat: position.coords.latitude,
                                        lon: position.coords.longitude,
                                        success: true
                                    });
                                },
                                (error) => {
                                    resolve({
                                        success: false,
                                        error: error.message
                                    });
                                }
                            );
                        } else {
                            resolve({
                                success: false,
                                error: "Geolocation not supported"
                            });
                        }
                    })
                    """,
                    key=f"gps_{int(time.time())}"
                )
                
                if location and location.get('success'):
                    u_lat, u_lon = location['lat'], location['lon']
                    st.success(f"Location acquired")
                    st.session_state['user_lat'] = u_lat
                    st.session_state['user_lon'] = u_lon
                else:
                    st.error("Unable to get GPS location")
            
            if 'user_lat' in st.session_state and 'user_lon' in st.session_state:
                u_lat = st.session_state['user_lat']
                u_lon = st.session_state['user_lon']
                st.info("Using stored GPS location")
                
        except Exception as e:
            st.error(f"GPS Error: {str(e)}")
    else:
        coords = get_coords_from_address(search_query)
        if coords:
            u_lat, u_lon = coords
            if 'user_lat' in st.session_state:
                del st.session_state['user_lat']
            if 'user_lon' in st.session_state:
                del st.session_state['user_lon']

# --- SYSTEM LOGIC ---
hazard, shelter, steps = get_evacuation_details(u_lat, u_lon, roads_df, shelters_df, disasters_df)

# Get route from OSRM
route_data = get_osrm_route(u_lat, u_lon, shelter['lat'], shelter['lon'])

# --- MAIN CONTENT ---
col1, col2 = st.columns([1, 2])

with col1:
    # Risk Analysis Card - FIXED EMPTY BOX
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.subheader("Risk Assessment")
    
    if hazard['dist'] < 0.8:
        st.markdown(f"""
            <div style="text-align: center; margin: 1rem 0;">
                <span class="status-badge status-danger">⚠ DANGER ZONE</span>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">Hazard Type</div>
                <div class="metric-value">{hazard['type'].title()}</div>
                <div class="metric-unit">Active Threat</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**Location:** {hazard['zone']}")
        st.markdown(f"**Distance:** {hazard['dist']:.2f} km")
        st.progress(min(hazard['dist'] / 2, 1.0), text="Risk Level")
    else:
        st.markdown(f"""
            <div style="text-align: center; margin: 1rem 0;">
                <span class="status-badge status-safe">✓ SAFE ZONE</span>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**Current Zone:** {hazard.get('zone', 'Unknown')}")
        st.markdown(f"**Distance to nearest hazard:** {hazard['dist']:.2f} km")
        st.progress(0.2, text="Risk Level")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Shelter Information Card - FIXED EMPTY BOX
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.subheader("Nearest Evacuation Center")
    
    distance = shelter.get('distance', shelter.get('dist', 0))
    if route_data:
        route_distance = route_data['distance']
        route_duration = route_data['duration']
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">{shelter['name']}</div>
                <div class="metric-value">{route_distance:.1f}</div>
                <div class="metric-unit">kilometers via route</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**Estimated Time:** {route_duration:.0f} minutes")
    else:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">{shelter['name']}</div>
                <div class="metric-value">{distance:.1f}</div>
                <div class="metric-unit">kilometers away</div>
            </div>
        """, unsafe_allow_html=True)
    
    if 'capacity' in shelter:
        st.markdown(f"**Capacity:** {shelter['capacity']} persons")
    if 'address' in shelter:
        st.markdown(f"**Address:** {shelter['address']}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation Steps Card - IMPROVED with clickable steps
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.subheader("Evacuation Route")
    
    if route_data and route_data['steps']:
        for i, step in enumerate(route_data['steps'][:5], 1):  # Show first 5 steps
            bearing = calculate_bearing(u_lat, u_lon, shelter['lat'], shelter['lon'])
            direction = get_direction_symbol(bearing)
            
            st.markdown(f"""
                <div class="step-container" onclick="alert('Navigating to: {step['name']}')">
                    <span class="step-number">{i}</span>
                    <span class="step-text">
                        <strong>{step['instruction']}</strong> on {step['name']}
                        <br>
                        <small>Direction: {direction} | {step['distance']:.2f} km</small>
                    </span>
                    <span class="step-distance">{step['duration']:.0f} min</span>
                </div>
            """, unsafe_allow_html=True)
    elif steps and len(steps) > 0:
        for i, s in enumerate(steps, 1):
            st.markdown(f"""
                <div class="step-container">
                    <span class="step-number">{i}</span>
                    <span class="step-text">{s}</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Proceed directly to the evacuation center")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    st.subheader("Evacuation Map")
    
    # Create map
    m = folium.Map(location=[u_lat, u_lon], zoom_start=14, tiles="cartodbpositron")
    
    # User Marker
    folium.Marker(
        [u_lat, u_lon], 
        tooltip="Your Location", 
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)
    
    # Shelter Marker
    folium.Marker(
        [shelter['lat'], shelter['lon']], 
        tooltip=f"Shelter: {shelter['name']}", 
        icon=folium.Icon(color='green', icon='home')
    ).add_to(m)
    
    # Draw route if available
    if route_data and route_data['points']:
        # Draw the main route
        folium.PolyLine(
            route_data['points'],
            color="#28a745",
            weight=6,
            opacity=0.8,
            popup=f"Route: {route_data['distance']:.2f} km, {route_data['duration']:.0f} min"
        ).add_to(m)
        
        # Add direction arrows along the route
        points = route_data['points']
        for i in range(0, len(points)-1, max(1, len(points)//10)):
            if i + 1 < len(points):
                p1, p2 = points[i], points[i+1]
                bearing = calculate_bearing(p1[0], p1[1], p2[0], p2[1])
                
                # Add arrow marker
                folium.RegularPolygonMarker(
                    location=[(p1[0] + p2[0])/2, (p1[1] + p2[1])/2],
                    color='white',
                    fill_color='#28a745',
                    fill_opacity=0.8,
                    number_of_sides=3,
                    rotation=bearing - 90,
                    radius=8,
                    popup=f"Direction: {get_direction_symbol(bearing)}"
                ).add_to(m)
    else:
        # Fallback straight line
        route_points = [[u_lat, u_lon], [shelter['lat'], shelter['lon']]]
        folium.PolyLine(
            route_points,
            color="#28a745",
            weight=5,
            opacity=0.8,
            popup="Direct Route (Simplified)"
        ).add_to(m)
    
    # Disaster Zones
    for _, z in disasters_df.iterrows():
        folium.Circle(
            [z['lat'], z['lon']], 
            radius=400, 
            color='#dc3545', 
            fill=True, 
            fill_opacity=0.3,
            popup=f"{z['type']} - {z['zone']}"
        ).add_to(m)
    
    # Blocked Roads
    for _, road in roads_df.iterrows():
        if road['status'] == 'Blocked':
            folium.Circle(
                [road['latitude'], road['longitude']],
                radius=200,
                color='#ffc107',
                fill=True,
                fill_opacity=0.3,
                popup=f"Blocked: {road['name']}"
            ).add_to(m)
    
    # Custom Legend
    legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; background-color: white; padding: 15px; border-radius: 10px; border: none; box-shadow: 0 2px 15px rgba(0,0,0,0.2); font-size: 12px;">
        <p style="margin: 5px 0; font-weight: 600; color: #333;">Map Legend</p>
        <p style="margin: 5px 0;"><span style="color: #007bff;">●</span> Your Location</p>
        <p style="margin: 5px 0;"><span style="color: #28a745;">●</span> Evacuation Center</p>
        <p style="margin: 5px 0;"><span style="color: #dc3545;">●</span> Danger Zone</p>
        <p style="margin: 5px 0;"><span style="color: #ffc107;">●</span> Blocked Road</p>
        <p style="margin: 5px 0;"><span style="color: #28a745;">━━</span> Evacuation Route</p>
        <p style="margin: 5px 0;"><span style="color: #28a745;">▶</span> Direction Arrow</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Display map
    st_folium(m, width=800, height=500)
    
    # Route summary
    if route_data:
        st.markdown(f"""
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin-top: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>Route Summary</strong><br>
                        <span style="color: #28a745;">▼ {route_data['distance']:.2f} km</span>
                    </div>
                    <div>
                        <strong>Est. Time</strong><br>
                        <span style="color: #667eea;">⏱ {route_data['duration']:.0f} min</span>
                    </div>
                    <div>
                        <strong>Preference</strong><br>
                        <span style="color: #764ba2;">{route_preference}</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Coordinates display
    st.markdown(f"""
        <div style="background: #f8f9fa; padding: 0.5rem; border-radius: 5px; text-align: center; font-size: 0.9rem; margin-top: 0.5rem;">
            <span style="color: #007bff;">📍 Your Location: {u_lat:.4f}, {u_lon:.4f}</span> | 
            <span style="color: #28a745;">🏠 Shelter: {shelter['lat']:.4f}, {shelter['lon']:.4f}</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Detailed Directions Panel - NEW
if route_data and route_data['steps']:
    with st.expander("🗺️ Detailed Step-by-Step Directions", expanded=False):
        st.markdown('<div class="direction-panel">', unsafe_allow_html=True)
        
        for i, step in enumerate(route_data['steps'], 1):
            # Get direction icon based on maneuver
            if 'left' in step['instruction'].lower():
                icon = "←"
            elif 'right' in step['instruction'].lower():
                icon = "→"
            elif 'straight' in step['instruction'].lower():
                icon = "↑"
            elif 'uturn' in step['instruction'].lower():
                icon = "↩"
            else:
                icon = "↓"
            
            st.markdown(f"""
                <div class="direction-step">
                    <div class="direction-icon">{icon}</div>
                    <div class="direction-text">
                        <div class="direction-instruction">
                            {step['instruction'].title()} on {step['name']}
                        </div>
                        <div class="direction-detail">
                            Distance: {step['distance']:.2f} km | Time: {step['duration']:.0f} min
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Emergency Information Expander
with st.expander("Emergency Protocols & Contact Information"):
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("""
        **Immediate Actions:**
        - Stay calm and assess your situation
        - Follow the marked evacuation route
        - Avoid blocked roads and danger zones
        - Proceed to the nearest evacuation center
        - Assist others if safely possible
        
        **Safety Guidelines:**
        - Keep emergency supplies ready
        - Follow official instructions
        - Stay away from hazardous areas
        - Help elderly and differently-abled
        - Maintain communication with authorities
        """)
    
    with col_b:
        st.markdown("""
        **Emergency Contacts:**
        - Police: 100
        - Fire Service: 101
        - Ambulance: 102
        - Disaster Management: 1070
        - NDRF: 011-24363260
        
        **Chennai Control Room:**
        - Phone: 044-25619200
        - Email: controlroom@chennaicorp.in
        - Website: www.chennaicorp.in/disaster
        """)

# Footer
st.markdown("""
    <div class="footer">
        <p>Chennai Emergency Evacuation System | Real-time Disaster Response | Version 3.0</p>
        <p style="font-size: 0.8rem; opacity: 0.8;">Powered by OSRM | For emergency use only</p>
    </div>
""", unsafe_allow_html=True)

# Refresh button in sidebar
with st.sidebar:
    st.markdown("---")
    if st.button("Refresh System Data", key="refresh"):
        st.cache_data.clear()
        st.rerun()
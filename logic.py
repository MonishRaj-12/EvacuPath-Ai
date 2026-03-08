import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim

# Initialize Geocoder for Place Name Search
geolocator = Nominatim(user_agent="chennai_evac_system")

def haversine(lat1, lon1, lat2, lon2):
    """Calculates distance in km between two points."""
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    return R * 2 * np.arcsin(np.sqrt(a))

def get_coords_from_address(address):
    """Converts a place name to (lat, lon) within Chennai."""
    try:
        # Adding Chennai ensures the search stays local
        location = geolocator.geocode(f"{address}, Chennai")
        if location:
            return location.latitude, location.longitude
        return None
    except:
        return None

def get_evacuation_details(u_lat, u_lon, roads, shelters, disasters):
    """Calculates risk and finds the nearest shelter and safe roads."""
    # 1. Identify Nearest Hazard
    disasters['dist'] = disasters.apply(lambda z: haversine(u_lat, u_lon, z['lat'], z['lon']), axis=1)
    nearest_hazard_idx = disasters['dist'].idxmin()
    nearest_hazard = disasters.loc[nearest_hazard_idx].to_dict()
    
    # 2. Find Nearest Shelter
    shelters['dist'] = shelters.apply(lambda s: haversine(u_lat, u_lon, s['lat'], s['lon']), axis=1)
    target_shelter_idx = shelters['dist'].idxmin()
    target_shelter = shelters.loc[target_shelter_idx].to_dict()
    
    # Add distance to shelter explicitly
    target_shelter['distance'] = target_shelter['dist']
    
    # 3. Find Nearby Safe Road Segments
    roads['dist_to_user'] = roads.apply(lambda r: haversine(u_lat, u_lon, r['latitude'], r['longitude']), axis=1)
    # Filter for safe roads and take the 3 closest to the user
    safe_nearby = roads[roads['status'] == 'Safe'].sort_values('dist_to_user').head(3)
    safe_steps = safe_nearby['name'].tolist()
    
    # If no safe roads found, provide a default step
    if not safe_steps:
        safe_steps = ["Proceed directly to shelter via main roads"]
    
    return nearest_hazard, target_shelter, safe_steps
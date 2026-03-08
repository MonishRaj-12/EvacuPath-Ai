import pandas as pd
import numpy as np
import os

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    return R * 2 * np.arcsin(np.sqrt(a))

def create_status_file():
    try:
        print("Checking for files...")
        # Check if files exist before loading
        if not os.path.exists('chennai_3000_roads.csv'):
            raise FileNotFoundError("Missing 'chennai_3000_roads.csv'")
        if not os.path.exists('disaster_zones.csv'):
            raise FileNotFoundError("Missing 'disaster_zones.csv'")

        roads = pd.read_csv('chennai_3000_roads.csv')
        disasters = pd.read_csv('disaster_zones.csv')

        print(f"Processing {len(roads)} roads against {len(disasters)} disaster zones...")

        blocked_indices = []
        high_risk = disasters[disasters['risk'].str.lower() == 'high']

        for idx, road in roads.iterrows():
            for _, zone in high_risk.iterrows():
                # Matching your uploaded CSV headers: 'lat'/'lon' for zones, 'latitude'/'longitude' for roads
                dist = haversine(road['latitude'], road['longitude'], zone['lat'], zone['lon'])
                if dist < 0.5: # 500m buffer
                    blocked_indices.append(idx)
                    break

        roads['status'] = 'Safe'
        roads.loc[blocked_indices, 'status'] = 'Blocked'
        
        roads.to_csv('chennai_road_status.csv', index=False)
        print("✅ SUCCESS: 'chennai_road_status.csv' created!")

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    create_status_file()
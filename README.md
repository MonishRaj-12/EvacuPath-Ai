# 
 EvacuPath AI — Smart Disaster Evacuation System


EvacuPath AI is an intelligent disaster evacuation support system designed to help people find the safest route to nearby shelters during emergencies.
 The system analyzes disaster zones, road networks, and shelter 
locations to generate optimized evacuation paths using geospatial data 
and routing algorithms.


The prototype focuses on disaster-prone regions like Chennai, where flooding and extreme weather events have impacted evacuation safety in the past.



 Problem Statement


During natural disasters such as 
floods and cyclones, people often struggle to locate safe evacuation 
routes. Traditional navigation systems do not consider disaster zones or
 emergency shelters, which can lead people into dangerous areas.


EvacuPath AI addresses this problem by providing real-time evacuation guidance using geospatial intelligence and pathfinding algorithms.



 Solution Overview


The system identifies disaster risk
 zones and calculates the safest evacuation route to nearby shelters. By
 combining geospatial datasets with routing algorithms, EvacuPath AI 
helps people reach safe locations quickly during emergencies.


Key capabilities include:




Detect disaster-affected areas




Identify nearest evacuation shelters




Generate safest route avoiding danger zones




Display evacuation paths on an interactive map





⚙️ Technology Stack


Backend




Python




Flask




Geospatial Processing




GeoPandas




NetworkX




Map Visualization




Leaflet




Data Source




OpenStreetMap





Algorithms Used


EvacuPath AI uses pathfinding algorithms to compute optimal evacuation routes:




Dijkstra's Algorithm




A* Search Algorithm




These algorithms help find the shortest and safest path while avoiding disaster zones

 How It Works




User enters location or enables GPS




System loads disaster and shelter datasets




Disaster risk zones are detected




Nearest safe shelter is identified




Road network is analyzed




Route optimization algorithm calculates safest path




Evacuation route is displayed on the map





 Proof of Concept (MVP)


The current prototype demonstrates:




Disaster zone visualization




Shelter identification




Safe route generation




Interactive evacuation map





 Future Improvements




Real-time disaster data integration




Mobile application for emergency evacuation




AI prediction for disaster risk zones




IoT sensor integration for flood monitoring





 Impact


EvacuPath AI aims to improve 
disaster preparedness and help people evacuate safely during 
emergencies, reducing risk and saving lives.



📹 Demo


Video demonstration:

(Add your hackathon demo video link here)



 Contributors




Monish Raj




Team Members (if any)





 License


This project is developed for the AI4Dev Hackathon and is intended for research and educational purposes

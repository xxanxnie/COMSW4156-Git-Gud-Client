import folium
import threading
import time
import pandas as pd
from geopy.geocoders import Nominatim
import requests
from flask import Flask, jsonify
import os
from dotenv import load_dotenv

app = Flask(__name__)
geolocator = Nominatim(user_agent="myGeocoder")

# Load environment variables from .env file
load_dotenv()

# Load the Bearer token from environment variables
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

# initial marker of New York City
markers = {
    'Counseling': [],
    'Food': [],
    'Healthcare': [],
    'Outreach': [],
    'Shelter': []
}
m = folium.Map(location=(40.7128, -74.0060), zoom_start=12)

category_colors = {
    'Counseling': 'blue',
    'Food': 'green',
    'Healthcare': 'red',
    'Outreach': 'purple',
    'Shelter': 'orange'
}

def create_map():
    # m = folium.Map(location=(40.7128, -74.0060), zoom_start=12) 
    m.save("GitGudMap.html")
    # print(f'markers are {markers}\n existing markers are {existing_markers}')

def update_markers(category):
    global markers, m

    print(f"Updating markers for {category}...")
    url = f"http://0.0.0.0:8080/resources/{category.lower()}/getAll"
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Clear the markers for the specified category
        markers[category] = []
        
        for item in data:
            if item["City"] == "NYC":
                if 'Address' in item:
                    address = item['Address']
                    geocoded_location = geolocator.geocode(address, timeout=10)
                    
                    if geocoded_location:
                        lat = geocoded_location.latitude
                        lon = geocoded_location.longitude
                        marker_key = (lat, lon)
                        
                        popup_info = f"""
                            <div style="font-size: 16px; font-weight: bold; color: #333; width: 400px; padding: 10px; line-height: 1.6;">
                                <p><strong>Name:</strong> {item['Name']}</p>
                                <p><strong>City:</strong> {item['City']}</p>
                                <p><strong>Address:</strong> {item['Address']}</p>
                                <p><strong>Description:</strong> {item['Description']}</p>
                                <p><strong>Contact Info:</strong> {item['ContactInfo']}</p>
                                <p><strong>Hours of Operation:</strong> {item['HoursOfOperation']}</p>
                                <p><strong>Category:</strong> {category}</p>
                            </div>
                        """
                        
                        marker_color = category_colors.get(category, 'gray')
                        markers[category].append((lat, lon, popup_info, marker_color))
                    else:
                        print(f"Address '{address}' could not be found or geocoded.")
                
                else:
                    print(f"Item does not contain 'Address' key: {item}")
            
        # Create a new map object
        m = folium.Map(location=(40.7128, -74.0060), zoom_start=12)
        
        # Add all markers from all categories to the map
        for cat, cat_markers in markers.items():
            for lat, lon, popup_info, marker_color in cat_markers:
                folium.Marker([lat, lon], popup=popup_info, icon=folium.Icon(color=marker_color)).add_to(m)
        
        m.save("GitGudMap.html")
        return jsonify({"status": "success", "message": f"{category} markers updated"}), 200
    except Exception as e:
        print(f"Error fetching data from API: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/update/counseling', methods=['POST'])
def update_counseling():
    return update_markers('Counseling')

@app.route('/update/food', methods=['POST'])
def update_food():
    return update_markers('Food')

@app.route('/update/healthcare', methods=['POST'])
def update_healthcare():
    return update_markers('Healthcare')

@app.route('/update/outreach', methods=['POST'])
def update_outreach():
    return update_markers('Outreach')

@app.route('/update/shelter', methods=['POST'])
def update_shelter():
    return update_markers('Shelter')

@app.route('/home', methods=['GET'])
def home():
    return jsonify({"status": "success", "message": "Welcome to the GitGudMap API!"}), 200

def subscribe():
    categories = ['Counseling', 'Food', 'Healthcare', 'Outreach', 'Shelter']
    url = "http://0.0.0.0:8080/resources/subscribe"
    headers = {
        "API-Key": "abc123NGO",
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    city = "NYC"  

    for category in categories:
        body = {
            "Resource": category.lower(),
            "City": city,
            "Contact": f"http://127.0.0.1:6000/update/{category.lower()}"
        }
        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            print(f"Subscribed to {category} updates successfully.")
        except Exception as e:
            print(f"Error subscribing to {category} updates: {e}")

if __name__ == "__main__":    
    create_map() # create an empty map
    subscribe()
    app.run(host='0.0.0.0', port=6000)

import folium
import threading
import time
import requests
from geopy.geocoders import Nominatim
from flask import Flask, jsonify

app = Flask(__name__)
geolocator = Nominatim(user_agent="myGeocoder")

ACCESS_TOKEN = "" 

# initial marker of New York City
markers = []
existing_markers = set()
m = folium.Map(location=(40.7128, -74.0060), zoom_start=12)

category_colors = {
    'Counseling': 'blue',
    'Food': 'green',
    'Healthcare': 'red',
    'Outreach': 'purple',
    'Shelter': 'orange'
}

# get API token from command line
def get_api_token():
    global ACCESS_TOKEN
    if not ACCESS_TOKEN:
        ACCESS_TOKEN = input("Please enter your API token: ").strip()
        if not ACCESS_TOKEN:
            print("Error: API token is required.")
            exit(1)  
    return ACCESS_TOKEN

# initial empty map at nyc
def create_map():
    m.save("GitGudMap.html")
    print(f'Markers are {markers}\n Existing markers are {existing_markers}')

def update_markers(category):
    global markers, existing_markers, m

    token = get_api_token()

    print(f'markers are {markers}\n existing markers are {existing_markers}')
    print(f"Updating markers for {category}...")
    url = f"http://0.0.0.0:8080/resources/{category.lower()}/getAll"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        # print(f'data is {data}\n')

        # Create a new map object
        last_marker = markers[-1] if markers else (40.7128, -74.0060)
        # m = folium.Map(location=last_marker, zoom_start=12)

        for item in data:
            # print(f'item is {item}\n')
            if 'Address' in item:
                address = item['Address']
                geocoded_location = geolocator.geocode(address, timeout=10)

                if geocoded_location:
                    lat = geocoded_location.latitude
                    lon = geocoded_location.longitude
                    marker_key = (lat, lon)

                    if marker_key not in existing_markers:
                        markers.append(marker_key)
                        existing_markers.add(marker_key)

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
                        folium.Marker([lat, lon], popup=popup_info, icon=folium.Icon(color=marker_color)).add_to(m)

                    else:
                        print(f"Marker at {lat}, {lon} already exists.")
                else:
                    print(f"Address '{address}' could not be found or geocoded.")
            else:
                print(f"Item does not contain 'Address' key: {item}")

        # create_map()
        m.save("GitGudMap.html")
        print(f'Markers updated for category: {category}')
        return jsonify({"status": "success", "message": f"{category} markers updated"}), 200
    
    except Exception as e:
        print(f"Error fetching data from API: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

def background_update():
    categories = ['counseling', 'food', 'healthcare', 'outreach', 'shelter']
    
    while True:
        for category in categories:
            update_markers(category)
            time.sleep(1)  

def start_thread():
    thread = threading.Thread(target=background_update, daemon=True)
    thread.start()

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

if __name__ == "__main__":
    create_map()   # create an empty map
    start_thread()  
    app.run(host='0.0.0.0', port=6000)

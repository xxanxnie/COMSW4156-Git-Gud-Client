import folium
import threading
import time
import pandas as pd
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="myGeocoder")

# data processing
counseling_df = pd.read_csv('data/Counseling.csv')
food_df = pd.read_csv('data/Food.csv')
healthcare_df = pd.read_csv('data/Healthcare.csv')
outreach_df = pd.read_csv('data/Outreach.csv')
shelter_df = pd.read_csv('data/Shelter.csv')  

counseling_df['Category'] = 'Counseling'
food_df['Category'] = 'Food'
healthcare_df['Category'] = 'Healthcare'
outreach_df['Category'] = 'Outreach'
shelter_df['Category'] = 'Shelter'

combined_df = pd.concat([counseling_df, food_df, healthcare_df, outreach_df, shelter_df])

# initial marker of New York City
markers = [(40.7128, -74.0060)]  

def create_map():
    last_marker = markers[-1]  
    m = folium.Map(location=last_marker, zoom_start=12) 

    # go through each row of the combined_df and add markers
    for index, row in combined_df.iterrows():
        address = row['Address']
        location = None
        
        # geocode the address input
        try:
            location = geolocator.geocode(address, timeout=10) 
        except Exception as e:
            print(f"Error geocoding address '{address}': {e}")
        
        if location:
            lat = location.latitude
            lon = location.longitude

            popup_info = f"""
                <div style="font-size: 16px; font-weight: bold; color: #333; width: 400px; padding: 10px; line-height: 1.6;">
                    <p><strong>Name:</strong> {row['Name']}</p>
                    <p><strong>Category:</strong> {row['Category']}</p>
                    <p><strong>Description:</strong> {row['Description']}</p>
                    <p><strong>Phone:</strong> {row['Phone Number']}</p>
                    <p><strong>Hours:</strong> {row['Hours of Operation']}</p>
                </div>
            """      

            if row['Category'] == 'Counseling':
                marker_color = 'blue'
            elif row['Category'] == 'Food':
                marker_color = 'green'
            elif row['Category'] == 'Healthcare':
                marker_color = 'red'
            elif row['Category'] == 'Outreach':
                marker_color = 'purple'
            elif row['Category'] == 'Shelter':
                marker_color = 'orange'

            folium.Marker([lat, lon], popup=popup_info, icon=folium.Icon(color=marker_color)).add_to(m)
        else:
            print(f"Address '{address}' could not be found or geocoded.")

    # add any new markers dynamically added during the process
    for lat, lon in markers:
        folium.Marker([lat, lon], popup=f'Marker at {lat}, {lon}').add_to(m)

    m.save("GitGudMap.html")
    print(f"Map updated and saved as 'GitGudMap.html' with center at {last_marker}")

# background thread to update the markers
def update_markers():
    global markers
    while True:
        # simulate adding a new marker
        # replace dummy data with api output
        new_marker = (40.7128 + len(markers)*0.01, -74.0060 + len(markers)*0.01) 
        markers.append(new_marker)  
        
        # check with subscription endpoint to update the data
        create_map()
        time.sleep(3)       # wait time before adding another marker

def start_thread():
    thread = threading.Thread(target=update_markers, daemon=True)
    thread.start()

if __name__ == "__main__":    
    create_map() # create the map in the beginning
    start_thread()
    time.sleep(90)  # make this longer for infinite if keep adding
    print("Map Generation Completed.")

# COMSW4156-Git-Gud-Client

Welcome to the Git Gud Client side of the service. The client is a web application that allows users to visualize essential social welfare resources on a Folium map. This client connects to the **Git Gud API**, which centralizes various social services to assist vulnerable groups, such as homeless individuals, refugees, veterans, and those recovering from substance use. By providing a dynamic map, users can access information about resources like shelter, food distribution, healthcare, counseling, and outreach services in real time.

To access the resources for them to display on the map, you must provide a valid API key. This key authenticates the user and ensures that the data shown on the map corresponds to the appropriate user permissions.

# How It Works

1. API Integration: The client communicates with the Git Gud API, subscribing to updates for social welfare resources. When new data is available (e.g., a new shelter, food distribution point, healthcare facility, etc.), the map is automatically updated to reflect the changes.

2. Color-Coded Markers: Each type of resource is displayed as a color-coded marker on the map:
- Blue: Counseling services
- Green: Food resources
- Red: Healthcare facilities
- Purple: Outreach programs
- Orange: Shelters

3. Resource Details: When a user clicks on a marker, detailed information about the resource is displayed, such as the name of the service, its address, and the city it is located in.

4. Dynamic Updates: The client listens for real-time updates from the API and automatically adds markers on the map as new resources become available.

The image below shows the map interface:

![Resource Map](docs/map.png)

# Libraries Used:
1. Folium: Used for creating interactive maps and visualizing resource locations with markers.
2. Pandas: Used for data manipulation and handling datasets related to resources.
3. Geopy: Used for geocoding addresses and coordinates to display resources on the map.
4. Requests: Used to interact with the Git Gud API and fetch resource data.
5. Flask: A lightweight web framework used for building the backend server.

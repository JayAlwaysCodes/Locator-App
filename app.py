import phonenumbers
import folium 
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
from phoneNumber import number, key  # Ensure this file contains `number` and `key`

# Parse and get location description
pepnumber = phonenumbers.parse(number)
location = geocoder.description_for_number(pepnumber, "en")
print("Location:", location)

# Get service provider
service_provider = phonenumbers.parse(number)
print("Service Provider:", carrier.name_for_number(service_provider, "en"))

# Use OpenCage Geocoder to get coordinates
geocoder = OpenCageGeocode(key)
query = str(location)
results = geocoder.geocode(query)

# Handle encoding issues when printing
if results and len(results):
    latitude = results[0]['geometry']['lat']
    longitude = results[0]['geometry']['lng']
    print(f"Coordinates: {latitude}, {longitude}")
else:
    print("No results found for the location.")

# Create a map
map = folium.Map(location=[latitude, longitude], zoom_start=9)
folium.Marker([latitude, longitude], popup=location).add_to(map)

# Save the map
map.save("Location.html")
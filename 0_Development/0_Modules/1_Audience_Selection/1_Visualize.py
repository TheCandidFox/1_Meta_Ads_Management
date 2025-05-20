# Using Folium to visualize (simple, yet lacking better UI and less modern -- likely not final setup)
"""
import json
import folium

# Load the GeoJSON
with open("isochrone_25min.geojson", "r") as f:
    geojson_data = json.load(f)

# Center the map around the first coordinate
center = geojson_data['features'][0]['geometry']['coordinates'][0][0]
center_lat = center[1]
center_lon = center[0]

# Create a Folium map
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# Add the GeoJSON as a layer
folium.GeoJson(geojson_data, name="25-minute isochrone").add_to(m)

# Save to HTML
m.save("map_visualization.html")
print("Map saved as map_visualization.html")
"""





# Pydeck (library wrapper for kepler.gl used by Uber? -- Production ready, highly customizable UX)
#"""
import json
import pydeck as pdk

pdk.settings.mapbox_api_key = "pk.eyJ1IjoiZHluYW1pY2ZveDIzIiwiYSI6ImNtYXQ0d2kxMDBzdm0ybnB5NWM2dmg3d20ifQ.dWdF5b8hDP5PNoHE5Wkg5g"

# Load the GeoJSON
with open("isochrone_25min.geojson", "r") as f:
    geojson_data = json.load(f)

# Create a GeoJsonLayer
geojson_layer = pdk.Layer(
    "GeoJsonLayer",
    data=geojson_data,
    stroked=True,
    filled=True,
    extruded=False,
    get_fill_color=[0, 150, 255, 80],   # RGBA
    get_line_color=[0, 0, 0, 200],
    line_width_min_pixels=2,
)

# Extract center from geojson
center = geojson_data["features"][0]["geometry"]["coordinates"][0][0]
center_lat = center[1]
center_lon = center[0]

# Setup deck.gl map
view_state = pdk.ViewState(latitude=center_lat, longitude=center_lon, zoom=11)

deck = pdk.Deck(
    layers=[geojson_layer],
    initial_view_state=view_state,
    
    # Base styles to maps
    #map_style="mapbox://styles/mapbox/light-v9"  # Optional
    map_style="mapbox://styles/mapbox/streets-v12"
    #map_style="mapbox://styles/mapbox/navigation-night-v1"
)

# Export to HTML
deck.to_html("isochrone_pydeck.html")
print("Map saved as isochrone_pydeck.html")
#"""
import pydeck as pdk

pdk.settings.mapbox_api_key = "pk.eyJ1IjoiZHluYW1pY2ZveDIzIiwiYSI6ImNtYXQ0d2kxMDBzdm0ybnB5NWM2dmg3d20ifQ.dWdF5b8hDP5PNoHE5Wkg5g"

# Empty map, no layers, just background style
deck = pdk.Deck(
    initial_view_state=pdk.ViewState(latitude=44.9537, longitude=-93.0900, zoom=10),
    map_style="mapbox://styles/mapbox/streets-v11"
)
deck.to_html("test_background.html")

import json

def write_route_geojson(route_places, output_path):
    """
    Writes a GeoJSON LineString of the route to the given file path.
    
    :param route_places: List of Place objects in order
    :param output_path: Output file path for the .geojson
    """
    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "name": "Optimized Route"
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [place.lon, place.lat] for place in route_places
                    ]
                }
            }
        ]
    }

    with open(output_path, "w", encoding='utf-8') as f:
        json.dump(geojson_data, f, indent=2)

    print(f"🗺️  GeoJSON route saved to: {output_path}")

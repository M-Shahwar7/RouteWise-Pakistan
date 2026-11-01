
import json
from pathlib import Path


DATA_FOLDER = Path(__file__).resolve().parent / "data"


def load_dataset(data_folder=None):

    folder = Path(data_folder) if data_folder else DATA_FOLDER

    cities_file = folder / "cities.json"
    roads_file = folder / "roads.json"

    # Read city data
    with open(cities_file, "r", encoding="utf-8") as file:
        city_data = json.load(file)

    # Read road data
    with open(roads_file, "r", encoding="utf-8") as file:
        road_data = json.load(file)

    cities = {}

    # Validate city records
    for city in city_data["cities"]:

        city_id = city["id"]

        if city_id in cities:
            raise ValueError(f"Duplicate city ID: {city_id}")

        lat = float(city["lat"])
        lon = float(city["lon"])

        if not -90 <= lat <= 90:
            raise ValueError(f"Invalid latitude: {city_id}")

        if not -180 <= lon <= 180:
            raise ValueError(f"Invalid longitude: {city_id}")

        cities[city_id] = city

    # Create empty graph
    graph = {
        city_id: {}
        for city_id in cities
    }

    # Add road connections
    for road in road_data["roads"]:

        source = road["from"]
        destination = road["to"]

        distance = float(road["distance_km"])

        if source not in cities:
            raise ValueError(f"Unknown city: {source}")

        if destination not in cities:
            raise ValueError(f"Unknown city: {destination}")

        if source == destination:
            raise ValueError("A road cannot connect a city to itself.")

        if distance <= 0:
            raise ValueError("Road distance must be positive.")

        if destination in graph[source]:
            raise ValueError("Duplicate road connection.")

        # Roads are treated as bidirectional
        graph[source][destination] = distance
        graph[destination][source] = distance

    return cities, graph

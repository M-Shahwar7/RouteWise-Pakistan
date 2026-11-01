
import math

EARTH_RADIUS_KM = 6371.0


def haversine_km(city_a, city_b):

    lat1 = math.radians(city_a["lat"])
    lon1 = math.radians(city_a["lon"])

    lat2 = math.radians(city_b["lat"])
    lon2 = math.radians(city_b["lon"])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    a = min(1.0, max(0.0, a))

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return EARTH_RADIUS_KM * c


def build_distance_heuristic(cities, goal):

    if goal not in cities:
        raise ValueError("Destination city does not exist.")

    return {
        city: haversine_km(coordinates, cities[goal])
        for city, coordinates in cities.items()
    }


def build_admissible_distance_heuristic(cities, graph, goal):

    if goal not in cities:
        raise ValueError("Destination city does not exist.")

    ratios = []

    for city, neighbours in graph.items():

        for neighbour, road_distance in neighbours.items():

            straight_distance = haversine_km(
                cities[city],
                cities[neighbour]
            )

            if straight_distance > 0:

                ratio = road_distance / straight_distance

                ratios.append(ratio)

    # Scale the straight-line heuristic so it
    # never overestimates the graph's shortest cost.
    scale = min(1.0, min(ratios)) if ratios else 0.0

    heuristic = {}

    for city, coordinates in cities.items():

        heuristic[city] = (
            scale *
            haversine_km(coordinates, cities[goal])
        )

    return heuristic


from flask import Flask, render_template, jsonify, request

from data_loader import load_dataset

from algorithms.ucs import uniform_cost_search
from algorithms.greedy import greedy_best_first_search
from algorithms.astar import a_star_search

from algorithms.heuristics import (
    build_distance_heuristic,
    build_admissible_distance_heuristic
)


# =====================================
# FLASK APPLICATION
# =====================================

app = Flask(__name__)


# =====================================
# LOAD PAKISTAN CITY DATASET
# =====================================

CITIES, GRAPH = load_dataset()


# =====================================
# ALGORITHM INFORMATION
# =====================================

ALGORITHMS = {

    "ucs": "Uniform Cost Search",

    "greedy": "Greedy Best-First Search",

    "astar": "A* Search"

}


# =====================================
# HOME PAGE
# =====================================

@app.route("/")
def home():

    return render_template("index.html")


# =====================================
# HEALTH CHECK API
# =====================================

@app.route("/api/health", methods=["GET"])
def health():

    return jsonify({

        "status": "success",

        "project": "RouteWise Pakistan",

        "message": "AI Route Planner is running!"

    })


# =====================================
# GET ALL PAKISTANI CITIES
# =====================================

@app.route("/api/cities", methods=["GET"])
def get_cities():

    city_list = []

    for city_id, city in CITIES.items():

        city_list.append({

            "id": city_id,

            "name": city["name"],

            "province": city["province"],

            "lat": city["lat"],

            "lon": city["lon"]

        })


    # Sort cities alphabetically

    city_list.sort(
        key=lambda city: city["name"]
    )


    return jsonify({

        "count": len(city_list),

        "cities": city_list

    })


# =====================================
# COMPARE THREE AI ALGORITHMS
# =====================================

@app.route("/api/compare", methods=["POST"])
def compare_routes():


    # Receive frontend data

    data = request.get_json(silent=True) or {}

    start = data.get("start")

    goal = data.get("goal")


    # Validate city selection

    if start not in CITIES or goal not in CITIES:

        return jsonify({

            "error": "Invalid starting or destination city."

        }), 400


    # =================================
    # GREEDY HEURISTIC
    # =================================

    greedy_heuristic = build_distance_heuristic(

        CITIES,

        goal

    )


    # =================================
    # A* ADMISSIBLE HEURISTIC
    # =================================

    astar_heuristic = build_admissible_distance_heuristic(

        CITIES,

        GRAPH,

        goal

    )


    # =================================
    # RUN ALL THREE ALGORITHMS
    # =================================

    results = {


        "ucs": uniform_cost_search(

            GRAPH,

            start,

            goal

        ),


        "greedy": greedy_best_first_search(

            GRAPH,

            start,

            goal,

            greedy_heuristic

        ),


        "astar": a_star_search(

            GRAPH,

            start,

            goal,

            astar_heuristic

        )

    }


    # =================================
    # PREPARE RESULTS FOR FRONTEND
    # =================================

    comparison = []


    for algorithm, result in results.items():


        route = []


        # Add city names and geographical coordinates

        for city_id in result["path"]:

            city = CITIES[city_id]


            route.append({

                "id": city_id,

                "name": city["name"],

                "lat": city["lat"],

                "lon": city["lon"]

            })


        # Prepare algorithm result

        comparison.append({

            "algorithm": algorithm,

            "algorithm_name": ALGORITHMS[algorithm],

            "found": result["found"],

            "path": route,

            "total_distance_km": result["total_cost"],

            "nodes_expanded": result["nodes_expanded"]

        })


    # =================================
    # SEND RESPONSE TO FRONTEND
    # =================================

    return jsonify({

        "start": CITIES[start]["name"],

        "destination": CITIES[goal]["name"],

        "results": comparison,

        "dataset_status": (

            "Prototype dataset: road distances are illustrative "
            "and are not verified real-world measurements."

        )

    })


# =====================================
# RUN FLASK APPLICATION
# =====================================

if __name__ == "__main__":

    app.run(debug=True)

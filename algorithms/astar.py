
import heapq
import itertools
import math


# =====================================
# NUMERICAL VALIDATION
# =====================================

def validate_number(value, label):

    if isinstance(value, bool):
        raise ValueError(
            f"{label} must be a valid number."
        )

    try:
        number = float(value)

    except (TypeError, ValueError):
        raise ValueError(
            f"{label} must be a valid number."
        )

    if not math.isfinite(number):
        raise ValueError(
            f"{label} must be finite."
        )

    if number < 0:
        raise ValueError(
            f"{label} cannot be negative."
        )

    return number


# =====================================
# A* SEARCH ALGORITHM
# =====================================

def a_star_search(graph, start, goal, heuristic):

    # STEP 1: VALIDATE START AND GOAL

    if start not in graph:
        raise ValueError(
            "Starting city does not exist."
        )

    if goal not in graph:
        raise ValueError(
            "Destination city does not exist."
        )


    # STEP 2: HANDLE SAME START AND GOAL

    # No search or heuristic calculation is needed.

    if start == goal:

        return {
            "found": True,
            "path": [start],
            "total_cost": 0.0,
            "nodes_expanded": 0
        }


    # STEP 3: VALIDATE GRAPH

    validated_graph = {}

    for city, neighbours in graph.items():

        validated_graph[city] = {}

        for neighbour, distance in neighbours.items():

            if neighbour not in graph:
                raise ValueError(
                    f"Neighbour {neighbour} is missing from graph."
                )

            validated_graph[city][neighbour] = (
                validate_number(
                    distance,
                    f"Road cost {city} to {neighbour}"
                )
            )


    # STEP 4: VALIDATE HEURISTIC

    validated_heuristic = {}

    for city in graph:

        if city not in heuristic:
            raise ValueError(
                f"Heuristic missing for {city}"
            )

        validated_heuristic[city] = (
            validate_number(
                heuristic[city],
                f"Heuristic for {city}"
            )
        )


    # Destination heuristic must be zero.

    if not math.isclose(
        validated_heuristic[goal],
        0.0,
        rel_tol=0.0,
        abs_tol=1e-12
    ):

        raise ValueError(
            "Heuristic at destination must be zero."
        )


    # STEP 5: INITIALIZE PRIORITY QUEUE

    counter = itertools.count()

    frontier = [

        (
            validated_heuristic[start],
            0.0,
            next(counter),
            start
        )

    ]


    # STEP 6: INITIALIZE TRACKING

    came_from = {
        start: None
    }

    g_score = {
        start: 0.0
    }

    nodes_expanded = 0


    # STEP 7: MAIN A* SEARCH LOOP

    while frontier:

        f_value, current_cost, _, current_city = (
            heapq.heappop(frontier)
        )


        # Ignore outdated queue entries.

        if current_cost != g_score[current_city]:
            continue


        # Destination reached.

        if current_city == goal:
            break


        nodes_expanded += 1


        # STEP 8: EXPLORE NEIGHBOURS

        for neighbor, distance in (
            validated_graph[current_city].items()
        ):

            new_cost = current_cost + distance

            if not math.isfinite(new_cost):
                raise ValueError(
                    "Accumulated path cost is not finite."
                )


            # Check for a better path.

            if new_cost < g_score.get(
                neighbor,
                float("inf")
            ):

                g_score[neighbor] = new_cost

                came_from[neighbor] = current_city


                # STEP 9: CALCULATE F SCORE

                f_score = (
                    new_cost +
                    validated_heuristic[neighbor]
                )

                if not math.isfinite(f_score):
                    raise ValueError(
                        "F-score is not finite."
                    )


                # Add improved path to priority queue.

                heapq.heappush(
                    frontier,
                    (
                        f_score,
                        new_cost,
                        next(counter),
                        neighbor
                    )
                )


    # STEP 10: CHECK DESTINATION

    if goal not in g_score:

        return {
            "found": False,
            "path": [],
            "total_cost": None,
            "nodes_expanded": nodes_expanded
        }


    # STEP 11: RECONSTRUCT PATH

    path = []

    current = goal

    while current is not None:

        path.append(current)

        current = came_from[current]

    path.reverse()


    # STEP 12: RETURN RESULTS

    return {
        "found": True,
        "path": path,
        "total_cost": g_score[goal],
        "nodes_expanded": nodes_expanded
    }

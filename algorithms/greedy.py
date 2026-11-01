
import heapq
import itertools


def greedy_best_first_search(graph, start, goal, heuristic):

    if start not in graph:
        raise ValueError("Starting city does not exist.")

    if goal not in graph:
        raise ValueError("Destination city does not exist.")

    # Priority queue: heuristic, path cost, counter, city
    counter = itertools.count()

    frontier = [
        (heuristic[start], 0, next(counter), start)
    ]

    came_from = {start: None}

    cost_so_far = {start: 0}

    visited = set()

    nodes_expanded = 0

    while frontier:

        h_value, current_cost, _, current_city = heapq.heappop(frontier)

        if current_cost != cost_so_far[current_city]:
            continue

        if current_city in visited:
            continue

        # Destination reached
        if current_city == goal:
            break

        visited.add(current_city)

        nodes_expanded += 1

        # Explore neighbouring cities
        for neighbor, distance in graph.get(current_city, {}).items():

            if distance < 0:
                raise ValueError("Road costs cannot be negative.")

            if neighbor in visited:
                continue

            new_cost = current_cost + distance

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:

                cost_so_far[neighbor] = new_cost

                came_from[neighbor] = current_city

                heapq.heappush(
                    frontier,
                    (
                        heuristic[neighbor],
                        new_cost,
                        next(counter),
                        neighbor
                    )
                )

    # Check destination
    if goal not in cost_so_far:

        return {
            "found": False,
            "path": [],
            "total_cost": None,
            "nodes_expanded": nodes_expanded
        }

    # Reconstruct path
    path = []

    current = goal

    while current is not None:

        path.append(current)

        current = came_from[current]

    path.reverse()

    return {
        "found": True,
        "path": path,
        "total_cost": cost_so_far[goal],
        "nodes_expanded": nodes_expanded
    }

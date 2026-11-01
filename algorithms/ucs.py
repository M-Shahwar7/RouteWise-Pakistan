
import heapq


def uniform_cost_search(graph, start, goal):

    if start not in graph:
        raise ValueError("Starting city does not exist.")

    if goal not in graph:
        raise ValueError("Destination city does not exist.")

    # Priority queue: (total cost, current city)
    frontier = [(0, start)]

    # Store the previous city
    came_from = {start: None}

    # Store the cheapest known cost
    cost_so_far = {start: 0}

    nodes_expanded = 0

    while frontier:

        current_cost, current_city = heapq.heappop(frontier)

        # Ignore outdated queue entries
        if current_cost != cost_so_far[current_city]:
            continue

        # Destination reached
        if current_city == goal:
            break

        nodes_expanded += 1

        # Explore connected cities
        for neighbor, distance in graph.get(current_city, {}).items():

            if distance < 0:
                raise ValueError("Road costs cannot be negative.")

            new_cost = current_cost + distance

            # Update if a cheaper path is found
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:

                cost_so_far[neighbor] = new_cost

                came_from[neighbor] = current_city

                heapq.heappush(
                    frontier,
                    (new_cost, neighbor)
                )

    # Check whether destination is reachable
    if goal not in cost_so_far:

        return {
            "found": False,
            "path": [],
            "total_cost": None,
            "nodes_expanded": nodes_expanded
        }

    # Reconstruct the route
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


# RouteWise Pakistan 🇵🇰

### AI-Based Inter-City Route Planner

RouteWise Pakistan is an interactive route-planning application that demonstrates three classical Artificial Intelligence search algorithms: Uniform Cost Search (UCS), Greedy Best-First Search, and A* Search.

The application compares algorithm performance using route distance and the number of expanded nodes across a prototype network of Pakistani cities.

## Features

- 65 Pakistani cities across different provinces and territories.
- 86 illustrative bidirectional graph connections.
- Uniform Cost Search (UCS).
- Greedy Best-First Search.
- A* Search.
- Haversine geographical distance calculation.
- Scaled distance heuristic for A*.
- Side-by-side algorithm comparison.
- Interactive map visualization.
- Flask-based backend and JSON APIs.
- Automated unit and API tests.

## Technologies Used

- Python
- Flask
- HTML5
- CSS3
- JavaScript
- JSON
- OpenStreetMap
- Python unittest

## AI Search Algorithms

### 1. Uniform Cost Search (UCS)

UCS explores paths according to their accumulated cost and finds an optimal path when edge costs are non-negative.

### 2. Greedy Best-First Search

Greedy Best-First Search selects the next city using its estimated distance to the destination.

It can explore fewer nodes but does not guarantee an optimal route.

### 3. A* Search

A* combines the actual accumulated path cost and the estimated remaining cost.

Formula:

f(n) = g(n) + h(n)

Where:

- g(n): Cost from the starting city.
- h(n): Estimated cost to the destination.
- f(n): Estimated total path cost.

The implementation uses a scaled Haversine heuristic designed to remain admissible for the current graph.

## Project Structure

```text
RouteWise-Pakistan/
│
├── algorithms/
│   ├── __init__.py
│   ├── astar.py
│   ├── greedy.py
│   ├── heuristics.py
│   └── ucs.py
│
├── data/
│   ├── cities.json
│   └── roads.json
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
├── templates/
│   └── index.html
│
├── tests/
│   ├── test_api.py
│   ├── test_astar.py
│   ├── test_data_loader.py
│   ├── test_greedy.py
│   ├── test_heuristics.py
│   └── test_ucs.py
│
├── app.py
├── data_loader.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Enter the project directory

```bash
cd RouteWise-Pakistan
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python app.py
```

Open your browser:

http://127.0.0.1:5000

## Running Tests

Run all automated tests:

```bash
python -m unittest discover -s tests -v
```

The current development version has 26 automated tests covering algorithms, dataset validation, heuristics, and API functionality.

## API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| /api/health | GET | Application health |
| /api/cities | GET | Retrieve available cities |
| /api/compare | POST | Compare search algorithms |

## Dataset Limitations

**This is an academic prototype, not a production navigation system.**

- City coordinates are approximate.
- Road distances are illustrative estimates, not verified road measurements.
- The current graph represents selected connections rather than the complete Pakistani road network.
- The map does not currently provide verified turn-by-turn road navigation.
- Live traffic, tolls, and verified travel times are not yet integrated.

These limitations will be addressed in future development.

## Future Improvements

- Integration with verified OpenStreetMap road-network data.
- Real road-route geometry.
- Travel-time optimization.
- Toll-aware route planning.
- Expanded algorithm performance evaluation.
- GitHub and cloud deployment.

## Project Purpose

The purpose of RouteWise Pakistan is to demonstrate and compare classical AI search algorithms through an interactive geographical route-planning application.

The project focuses on understanding algorithm efficiency, path costs, heuristic functions, and optimal search strategies.


document.addEventListener("DOMContentLoaded", function () {

    // =====================================
    // DOM ELEMENTS
    // =====================================

    const startSelect = document.getElementById("start");

    const destinationSelect =
        document.getElementById("destination");

    const routeForm =
        document.getElementById("route-form");

    const findButton =
        document.getElementById("find-route");

    const status =
        document.getElementById("status");

    const resultsSection =
        document.getElementById("results");

    const resultsGrid =
        document.getElementById("results-grid");

    const datasetNote =
        document.getElementById("dataset-note");


    // =====================================
    // GLOBAL VARIABLES
    // =====================================

    let citiesData = [];

    let map = null;

    let cityMarkers = null;

    let routeLayers = {};

    let routeLayerControl = null;


    // Different colors for AI algorithms

    const routeColors = {

        ucs: "#2563eb",

        greedy: "#f59e0b",

        astar: "#16a34a"

    };


    // =====================================
    // STEP 1: LOAD CITIES
    // =====================================

    async function loadCities() {

        try {

            status.textContent =
                "Loading Pakistani cities...";


            const response = await fetch("/api/cities");


            if (!response.ok) {

                throw new Error(
                    "Unable to load cities from backend."
                );

            }


            const data = await response.json();

            citiesData = data.cities;


            // Clear old options

            startSelect.replaceChildren();

            destinationSelect.replaceChildren();


            // Add cities to dropdowns

            citiesData.forEach(function (city) {


                const startOption =
                    document.createElement("option");

                startOption.value = city.id;

                startOption.textContent = city.name;

                startSelect.appendChild(startOption);


                const destinationOption =
                    document.createElement("option");

                destinationOption.value = city.id;

                destinationOption.textContent = city.name;

                destinationSelect.appendChild(
                    destinationOption
                );

            });


            // Default journey

            startSelect.value = "KHI";

            destinationSelect.value = "ISB";


            status.textContent =
                data.count +
                " Pakistani cities loaded successfully. Ready to plan!";


        } catch (error) {

            status.textContent = error.message;

            findButton.disabled = true;

        }

    }


    // =====================================
    // STEP 2: INITIALIZE LEAFLET MAP
    // =====================================

    function initializeMap() {


        // Prevent duplicate map initialization

        if (map) {

            map.invalidateSize();

            return;

        }


        // Check Leaflet library

        if (typeof L === "undefined") {

            throw new Error(
                "Leaflet map library could not load."
            );

        }


        // Create Pakistan map

        map = L.map("route-map").setView(

            [30.5, 69.3],

            5

        );


        // OpenStreetMap tiles

        L.tileLayer(

            "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",

            {

                maxZoom: 19,

                attribution:
                    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

            }

        ).addTo(map);


        // Create city marker group

        cityMarkers = L.layerGroup().addTo(map);


        // Add all city markers

        citiesData.forEach(function (city) {


            const marker = L.marker(

                [city.lat, city.lon]

            );


            // Safe popup content

            const popup = document.createElement("strong");

            popup.textContent = city.name;


            marker.bindPopup(popup);

            marker.addTo(cityMarkers);

        });

    }


    // =====================================
    // STEP 3: CREATE RESULT METRICS
    // =====================================

    function createMetric(label, value) {


        const container =
            document.createElement("div");

        container.className = "metric";


        const heading =
            document.createElement("span");

        heading.textContent = label;


        const result =
            document.createElement("strong");

        result.textContent = value;


        container.append(

            heading,

            result

        );


        return container;

    }


    // =====================================
    // STEP 4: DISPLAY ALGORITHM RESULTS
    // =====================================

    function displayResults(data) {


        resultsGrid.replaceChildren();


        // Get successful results

        const validResults = data.results.filter(

            function (result) {

                return result.found;

            }

        );


        // Find minimum route distance

        const minimumDistance = validResults.length

            ? Math.min(

                ...validResults.map(function (result) {

                    return Number(
                        result.total_distance_km
                    );

                })

            )

            : Infinity;


        // Display each algorithm

        data.results.forEach(function (result) {


            const card =
                document.createElement("article");

            card.className = "result-card";


            // Check whether route has minimum distance

            const isBest = result.found &&

                Math.abs(

                    Number(result.total_distance_km) -

                    minimumDistance

                ) < 0.000001;


            if (isBest) {

                card.classList.add("best-result");

            }


            // Algorithm heading

            const heading =
                document.createElement("h3");

            heading.textContent =
                result.algorithm_name;


            // Result badge

            const badge =
                document.createElement("span");

            badge.className = "result-badge";

            badge.textContent = isBest

                ? "Lowest Distance"

                : "Search Result";


            const header =
                document.createElement("div");

            header.className = "result-header";

            header.append(

                heading,

                badge

            );

            card.appendChild(header);


            // If route exists

            if (result.found) {


                // Route label

                const pathLabel =
                    document.createElement("p");

                pathLabel.className = "path-label";

                pathLabel.textContent =
                    "Calculated Route";


                // Route path

                const path =
                    document.createElement("p");

                path.className = "route-path";

                path.textContent = result.path

                    .map(function (city) {

                        return city.name;

                    })

                    .join(" → ");


                // Metrics container

                const metrics =
                    document.createElement("div");

                metrics.className = "metrics-grid";


                // Distance and nodes

                metrics.append(

                    createMetric(

                        "Distance",

                        Number(
                            result.total_distance_km
                        ).toFixed(1) + " km"

                    ),


                    createMetric(

                        "Nodes Expanded",

                        String(result.nodes_expanded)

                    )

                );


                card.append(

                    pathLabel,

                    path,

                    metrics

                );


            } else {


                const message =
                    document.createElement("p");

                message.textContent =
                    "No route found.";

                card.appendChild(message);

            }


            resultsGrid.appendChild(card);

        });


        // Dataset information

        datasetNote.textContent =
            data.dataset_status;


        // Show results section

        resultsSection.hidden = false;


        // Render interactive map

        try {

            renderMap(data);

        } catch (error) {

            console.error(
                "Map error:",
                error
            );

            const mapNote =
                document.querySelector(".map-note");

            if (mapNote) {

                mapNote.textContent =
                    "Map unavailable. Please check your internet connection and Leaflet library.";

            }

        }


        // Scroll to results

        resultsSection.scrollIntoView({

            behavior: "smooth",

            block: "start"

        });

    }


    // =====================================
    // STEP 5: DRAW AI ROUTES ON MAP
    // =====================================

    function renderMap(data) {


        // Initialize map if needed

        initializeMap();


        // Remove old layer control

        if (routeLayerControl) {

            map.removeControl(
                routeLayerControl
            );

            routeLayerControl = null;

        }


        // Remove previous routes

        Object.values(routeLayers).forEach(

            function (layer) {

                map.removeLayer(layer);

            }

        );


        routeLayers = {};


        // Store coordinates for zoom

        const allCoordinates = [];


        // Process each algorithm result

        data.results.forEach(function (result) {


            if (

                !result.found ||

                result.path.length < 2

            ) {

                return;

            }


            // Get route coordinates

            const coordinates = result.path.map(

                function (city) {

                    return [

                        city.lat,

                        city.lon

                    ];

                }

            );


            coordinates.forEach(function (point) {

                allCoordinates.push(point);

            });


            // Get algorithm color

            const color =
                routeColors[result.algorithm];


            // Route label

            const routeName =

                result.algorithm_name +

                " (" +

                Number(
                    result.total_distance_km
                ).toFixed(1) +

                " km)";


            // Create route line

            const polyline = L.polyline(

                coordinates,

                {

                    color: color,

                    weight: 5,

                    opacity: 0.85

                }

            );


            // Add popup to route

            const popup =
                document.createElement("strong");

            popup.textContent =

                result.algorithm_name +

                " - " +

                Number(
                    result.total_distance_km
                ).toFixed(1) +

                " km";


            polyline.bindPopup(popup);


            // Add route to map

            polyline.addTo(map);


            // Save route layer

            routeLayers[routeName] = polyline;

        });


        // Add route visibility controls

        routeLayerControl = L.control.layers(

            null,

            routeLayers,

            {

                collapsed: false

            }

        ).addTo(map);


        // Zoom map to selected routes

        if (allCoordinates.length > 0) {


            const bounds = L.latLngBounds(
                allCoordinates
            );


            map.fitBounds(

                bounds,

                {

                    padding: [30, 30],

                    maxZoom: 7

                }

            );

        }


        // Refresh map size

        map.invalidateSize();

    }


    // =====================================
    // STEP 6: SUBMIT ROUTE REQUEST
    // =====================================

    routeForm.addEventListener(

        "submit",

        async function (event) {


            event.preventDefault();


            const start =
                startSelect.value;

            const goal =
                destinationSelect.value;


            // Validate selection

            if (!start || !goal) {

                status.textContent =
                    "Please select both cities.";

                return;

            }


            // Prevent same city selection

            if (start === goal) {

                status.textContent =
                    "Starting city and destination must be different.";

                resultsSection.hidden = true;

                return;

            }


            // Loading state

            findButton.disabled = true;

            findButton.textContent =
                "Calculating Routes...";


            status.textContent =
                "Running UCS, Greedy and A* algorithms...";


            try {


                // Send request to Flask API

                const response = await fetch(

                    "/api/compare",

                    {

                        method: "POST",

                        headers: {

                            "Content-Type":
                                "application/json"

                        },

                        body: JSON.stringify({

                            start: start,

                            goal: goal

                        })

                    }

                );


                const data = await response.json();


                // Handle API errors

                if (!response.ok) {

                    throw new Error(

                        data.error ||

                        "Route calculation failed."

                    );

                }


                // Display all results

                displayResults(data);


                status.textContent =
                    "All three algorithms completed successfully!";


            } catch (error) {


                status.textContent =
                    error.message;


            } finally {


                // Restore button

                findButton.disabled = false;

                findButton.textContent =
                    "Compare AI Algorithms";

            }

        }

    );


    // =====================================
    // STEP 7: START APPLICATION
    // =====================================

    loadCities();

});

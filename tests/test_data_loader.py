
import unittest

from data_loader import load_dataset
from algorithms.heuristics import build_distance_heuristic
from algorithms.ucs import uniform_cost_search


class TestPakistanDataset(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.cities, cls.graph = load_dataset()


    def test_city_count(self):

        self.assertEqual(len(self.cities), 65)


    def test_every_city_has_graph_node(self):

        self.assertEqual(
            set(self.cities.keys()),
            set(self.graph.keys())
        )


    def test_all_cities_are_connected(self):

        start = next(iter(self.graph))

        visited = set()

        stack = [start]

        while stack:

            city = stack.pop()

            if city in visited:
                continue

            visited.add(city)

            for neighbour in self.graph[city]:

                if neighbour not in visited:

                    stack.append(neighbour)


        self.assertEqual(
            visited,
            set(self.cities.keys())
        )


    def test_heuristic_for_destination_is_zero(self):

        destination = "ISB"

        heuristic = build_distance_heuristic(
            self.cities,
            destination
        )

        self.assertEqual(
            heuristic[destination],
            0.0
        )


    def test_road_connections_are_bidirectional(self):

        for city, neighbours in self.graph.items():

            for neighbour, distance in neighbours.items():

                self.assertIn(
                    city,
                    self.graph[neighbour]
                )

                self.assertEqual(
                    distance,
                    self.graph[neighbour][city]
                )


    def test_ucs_finds_pakistan_route(self):

        result = uniform_cost_search(
            self.graph,
            "KHI",
            "ISB"
        )

        self.assertTrue(result["found"])

        self.assertEqual(
            result["path"][0],
            "KHI"
        )

        self.assertEqual(
            result["path"][-1],
            "ISB"
        )

        self.assertGreater(
            result["total_cost"],
            0
        )


if __name__ == "__main__":

    unittest.main()

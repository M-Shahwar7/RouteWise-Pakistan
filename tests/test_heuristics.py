
import unittest

from algorithms.heuristics import (
    haversine_km,
    build_distance_heuristic
)


class TestHaversine(unittest.TestCase):

    def setUp(self):

        self.cities = {

            "Lahore": {
                "lat": 31.5204,
                "lon": 74.3587
            },

            "Islamabad": {
                "lat": 33.6844,
                "lon": 73.0479
            },

            "Karachi": {
                "lat": 24.8607,
                "lon": 67.0011
            }
        }

    def test_lahore_islamabad_distance(self):

        distance = haversine_km(
            self.cities["Lahore"],
            self.cities["Islamabad"]
        )

        self.assertAlmostEqual(
            distance,
            270.14,
            delta=1
        )

    def test_same_city_distance(self):

        distance = haversine_km(
            self.cities["Lahore"],
            self.cities["Lahore"]
        )

        self.assertEqual(distance, 0)

    def test_distance_symmetry(self):

        distance_one = haversine_km(
            self.cities["Lahore"],
            self.cities["Islamabad"]
        )

        distance_two = haversine_km(
            self.cities["Islamabad"],
            self.cities["Lahore"]
        )

        self.assertEqual(distance_one, distance_two)

    def test_build_heuristic(self):

        heuristic = build_distance_heuristic(
            self.cities,
            "Islamabad"
        )

        self.assertEqual(
            heuristic["Islamabad"],
            0
        )

        self.assertAlmostEqual(
            heuristic["Lahore"],
            270.14,
            delta=1
        )

    def test_invalid_destination(self):

        with self.assertRaises(ValueError):

            build_distance_heuristic(
                self.cities,
                "Peshawar"
            )


if __name__ == "__main__":

    unittest.main()


import unittest

from algorithms.astar import a_star_search


class TestAStarSearch(unittest.TestCase):

    def setUp(self):

        self.graph = {

            "A": {
                "B": 4,
                "C": 1
            },

            "B": {
                "A": 4,
                "C": 2,
                "D": 1
            },

            "C": {
                "A": 1,
                "B": 2,
                "D": 5
            },

            "D": {
                "B": 1,
                "C": 5
            }
        }

        # Admissible heuristic values
        self.heuristic = {
            "A": 4,
            "B": 1,
            "C": 3,
            "D": 0
        }

    def test_optimal_path(self):

        result = a_star_search(
            self.graph,
            "A",
            "D",
            self.heuristic
        )

        self.assertTrue(result["found"])

        self.assertEqual(
            result["path"],
            ["A", "C", "B", "D"]
        )

        self.assertEqual(
            result["total_cost"],
            4
        )

    def test_same_start_and_destination(self):

        result = a_star_search(
            self.graph,
            "A",
            "A",
            self.heuristic
        )

        self.assertEqual(result["path"], ["A"])

        self.assertEqual(result["total_cost"], 0)

    def test_unreachable_destination(self):

        graph = {
            "A": {"B": 5},
            "B": {"A": 5},
            "C": {}
        }

        heuristic = {
            "A": 2,
            "B": 1,
            "C": 0
        }

        result = a_star_search(
            graph,
            "A",
            "C",
            heuristic
        )

        self.assertFalse(result["found"])


if __name__ == "__main__":

    unittest.main()

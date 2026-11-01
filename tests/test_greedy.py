
import unittest

from algorithms.greedy import greedy_best_first_search


class TestGreedySearch(unittest.TestCase):

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

        self.heuristic = {
            "A": 3,
            "B": 1,
            "C": 2,
            "D": 0
        }

    def test_greedy_path(self):

        result = greedy_best_first_search(
            self.graph,
            "A",
            "D",
            self.heuristic
        )

        self.assertTrue(result["found"])

        self.assertEqual(
            result["path"],
            ["A", "B", "D"]
        )

        self.assertEqual(
            result["total_cost"],
            5
        )

    def test_same_start_and_destination(self):

        result = greedy_best_first_search(
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

        result = greedy_best_first_search(
            graph,
            "A",
            "C",
            heuristic
        )

        self.assertFalse(result["found"])


if __name__ == "__main__":

    unittest.main()

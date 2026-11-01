
import unittest

from algorithms.ucs import uniform_cost_search


class TestUniformCostSearch(unittest.TestCase):

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

    def test_shortest_path(self):

        result = uniform_cost_search(
            self.graph, "A", "D"
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

        result = uniform_cost_search(
            self.graph, "A", "A"
        )

        self.assertEqual(result["path"], ["A"])

        self.assertEqual(result["total_cost"], 0)

    def test_unreachable_destination(self):

        graph = {
            "A": {"B": 5},
            "B": {"A": 5},
            "C": {}
        }

        result = uniform_cost_search(
            graph, "A", "C"
        )

        self.assertFalse(result["found"])


if __name__ == "__main__":

    unittest.main()

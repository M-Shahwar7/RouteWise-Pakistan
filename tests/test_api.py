
import unittest

from app import app


class TestRouteWiseAPI(unittest.TestCase):

    def setUp(self):

        self.client = app.test_client()


    def test_health_api(self):

        response = self.client.get("/api/health")

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.json["status"],
            "success"
        )


    def test_cities_api(self):

        response = self.client.get("/api/cities")

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.json["count"],
            65
        )

        self.assertEqual(
            len(response.json["cities"]),
            65
        )


    def test_compare_api(self):

        response = self.client.post(
            "/api/compare",
            json={
                "start": "KHI",
                "goal": "ISB"
            }
        )

        self.assertEqual(response.status_code, 200)

        results = response.json["results"]

        self.assertEqual(len(results), 3)

        for result in results:

            self.assertTrue(result["found"])

            self.assertEqual(
                result["path"][0]["id"],
                "KHI"
            )

            self.assertEqual(
                result["path"][-1]["id"],
                "ISB"
            )


    def test_astar_and_ucs_optimal_cost(self):

        response = self.client.post(
            "/api/compare",
            json={
                "start": "KHI",
                "goal": "ISB"
            }
        )

        results = {
            item["algorithm"]: item
            for item in response.json["results"]
        }

        self.assertAlmostEqual(
            results["ucs"]["total_distance_km"],
            results["astar"]["total_distance_km"]
        )


    def test_invalid_city(self):

        response = self.client.post(
            "/api/compare",
            json={
                "start": "ABC",
                "goal": "ISB"
            }
        )

        self.assertEqual(response.status_code, 400)


    def test_compare_api_includes_coordinates(self):

        response = self.client.post(
            "/api/compare",
            json={
                "start": "KHI",
                "goal": "ISB"
            }
        )

        self.assertEqual(response.status_code, 200)

        results = response.json["results"]

        for result in results:

            for city in result["path"]:

                self.assertIn("lat", city)

                self.assertIn("lon", city)

                self.assertIsInstance(
                    city["lat"],
                    (int, float)
                )

                self.assertIsInstance(
                    city["lon"],
                    (int, float)
                )


if __name__ == "__main__":

    unittest.main()

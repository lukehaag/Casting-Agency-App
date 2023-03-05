import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie
from datetime import datetime
import time

ASSISTANT_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJPMzdpNEhXc0drajNfVGlOMnpyaSJ9.eyJpc3MiOiJodHRwczovL2xraGcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYzZWU0ZmI2ZjA3NWFiMDI0YzIwMjllMSIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTY3ODAyNzAyNywiZXhwIjoxNjc4MTEzNDI3LCJhenAiOiJmWnJPdUxZRzkzamhBNmQ4N3dlWmRIRGZ4QzJ6RnBCZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.AxaWYnEBrXOcbGETVZU4f7nqx_omIQW_3zZeNjdoLzI2JzH0uzrgZzZlD_TvBwo1TylTcfQNVGkU-m2bFWYfbmvGBEDnZGetaKt-rquS97kmGJJsEpwVW4-9_Ut3OuhCAqxfieScy1d6apjdtECu3AdWlrcD8WOoeJ_9kfE1H8eyLifiZtY2ik0ZB-SuMNCpHcuUICyJgAq8QDHzVz-rtglkhEg6ujmZNorhMWEnjVDfawANA4HhmWM0vMpV6mKRfKjj1HiddgZ6-C20CgvVeVhpzdsperGm568a8lDwnDs7NhCcE--lWA7nXbS9mH-mX1HyPhFMDuJlnkW_hCeWNQ"
DIRECTOR_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJPMzdpNEhXc0drajNfVGlOMnpyaSJ9.eyJpc3MiOiJodHRwczovL2xraGcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYzZWU0ZjI4ZjA3NWFiMDI0YzIwMjlkMyIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTY3ODAyNjk0MCwiZXhwIjoxNjc4MTEzMzQwLCJhenAiOiJmWnJPdUxZRzkzamhBNmQ4N3dlWmRIRGZ4QzJ6RnBCZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.aVZ13y4H0cNwIgWaD8dyltyQ2upPFhBYQkutZaHlPFKYS2lEwHRhFyvwZuhXd5Rv_C80b8F2wzQb1YJg1hZBww920jVnqcpuFK16D77Bvm4CphFnqH6FnfWLM3kHqeii2Z6xypnBqEmBUvZmbs1WNgZ3B05LnFKjmFI-eoX3xeXkMTRJoMTdgqJUa3nnwyAvuuQpodDFavz_xr20pJ-_eVrRZlWO7zVFayaHe6JgUmZKzzuJTdOolAOnuMdQlmpzJcugFQ06gg1JpL-LZVTXj9AKEUwf5eSieip8yILofB5faZ435dslkk8RhLstukhBqy571DNFm0mtEhkeHPY7IQ"
PRODUCER_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJPMzdpNEhXc0drajNfVGlOMnpyaSJ9.eyJpc3MiOiJodHRwczovL2xraGcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYzZmNhZjM1YjRkZjU1YTViMzhiNTMzYiIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTY3ODAyNjc0MywiZXhwIjoxNjc4MTEzMTQzLCJhenAiOiJmWnJPdUxZRzkzamhBNmQ4N3dlWmRIRGZ4QzJ6RnBCZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.KQZVyC_jQnOTc2RDS4FeYKqOqwRblPO6jxX1kYWTXQP_No_fzM9aAfmtkp-kmD2aIcve6p9Q8RvJOYutkzroEsEfDjw5WgsTiYktH_TYLvp0HqFKNrHUFYwAVbTtDLVhWE37ZJWy1gz1TmyBAQDVvlwAm-61YLfWvFIafOjMU2wpdlhEaUZuutFY3HWVzJoKsL1QUh8STRGZQjJWSwufDhoCdBn-g2QF6A5cMJApbXJmxM9JghHFdV9BnZxC_6nwFIvCh6t6Rh4WIF5Cc5vw6NsFAJyVUv1-ta2xvdP3BjRRdnUbUOXVC4635XGTaRcQIlBBr86l4MUJqKtd_yzcuA"


class CastingAgencyCase(unittest.TestCase):
    """This class represents the test case"""

    def setUp(self):
        """Define test variables and initialise app"""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "postgres_test"
        self.database_path = "postgresql://lukehaag@localhost:5432/{}".format(
            self.database_name
        )

        setup_db(self.app, self.database_path)

        # Test data for actors

        self.actor_to_post = {
            "id": 1,
            "name": "Samantha Grey",
            "age": 37,
            "gender": "Female",
        }

        self.actor_to_patch = {"name": "Max"}

        # Test data for movies

        self.movie_to_post = {"title": "Jurassic Park", "release_date": datetime.now()}

        self.movie_to_patch = {"title": "Jurassic Noob"}

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test Cases for actor endpoints

    def test_post_actor(self):
        res = self.client().post(
            "/actors",
            json=self.actor_to_post,
            headers={"Authorization": f"Bearer {DIRECTOR_TOKEN}"},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])

    def test_post_actor_unauthorized(self):
        res = self.client().post(
            "/actors",
            json=self.actor_to_post,
            headers={"Authorization": f"Bearer {ASSISTANT_TOKEN}"},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["code"], "forbidden")
        self.assertTrue(data["description"], "Permission not found.")

    def test_get_actors(self):
        res = self.client().get(
            "/actors", headers={"Authorization": f"Bearer {ASSISTANT_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])

    def test_patch_actor(self):
        res = self.client().patch(
            "/actors/3",
            json=self.actor_to_patch,
            headers={"Authorization": f"Bearer {DIRECTOR_TOKEN}"},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])

    def test_404_actor_not_found_patch(self):
        res = self.client().patch(
            "/actors/100",
            json=self.actor_to_patch,
            headers={"Authorization": f"Bearer {PRODUCER_TOKEN}"},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # def test_delete_actor(self):
    #     res = self.client().delete(
    #         "/actors/2", headers={"Authorization": f"Bearer {PRODUCER_TOKEN}"}
    #     )
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["delete"])

    def test_422_delete_non_existing_actor(self):
        res = self.client().delete(
            "/actors/1000", headers={"Authorization": f"Bearer {PRODUCER_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    # Test cases for movies

    def test_post_movie(self):
        res = self.client().post(
            "/movies",
            json=self.movie_to_post,
            headers={"Authorization": f"Bearer {PRODUCER_TOKEN}"},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

    def test_post_movie_unauthorized(self):
        res = self.client().post(
            "/movies",
            json=self.movie_to_post,
            headers={"Authorization": f"Bearer {ASSISTANT_TOKEN}"},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["code"], "forbidden")
        self.assertTrue(data["description"], "Permission not found.")

    def test_get_movies(self):
        res = self.client().get(
            "/movies", headers={"Authorization": f"Bearer {DIRECTOR_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

    # def test_patch_movie(self):
    #     res = self.client().patch(
    #         "/movies/1",
    #         json=self.patch_movie,
    #         headers={"Authorization": f"Bearer {PRODUCER_TOKEN}"},
    #     )
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["movies"])

    def test_404_movie_not_found_patch(self):
        res = self.client().patch(
            "/movies/100",
            json=self.movie_to_patch,
            headers={"Authorization": f"Bearer {PRODUCER_TOKEN}"},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # def test_delete_movie(self):
    #     res = self.client().delete(
    #         "/movies/2", headers={"Authorization": f"Bearer {PRODUCER_TOKEN}"}
    #     )
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["delete"])

    def test_422_delete_non_existing_movie(self):
        res = self.client().delete(
            "/movies/1000", headers={"Authorization": f"Bearer {PRODUCER_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")


if __name__ == "__main__":
    unittest.main()

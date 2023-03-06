import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie
from datetime import datetime
import time

ASSISTANT_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJPMzdpNEhXc0drajNfVGlOMnpyaSJ9.eyJpc3MiOiJodHRwczovL2xraGcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYzZWU0ZmI2ZjA3NWFiMDI0YzIwMjllMSIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTY3ODA5MDU2NSwiZXhwIjoxNjc4MTc2OTY1LCJhenAiOiJmWnJPdUxZRzkzamhBNmQ4N3dlWmRIRGZ4QzJ6RnBCZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.YzUqk67JzUnMWRNJn5YP0QCNoDVr91hjPbrKIfz-a_WbWYtp-iIuM5ZnueLdRLDEWr2gaCtwBhOw1FEWgMEkhRYM8rQse0CSeJ8_Xk2wnpTuCBVBrys5GzGxtpVQneH2YauhWy7ebnUzyrcaRCAtIguGNDnpShPnlRyF8N6oNUAITs-AO6PH36Xzs8MVA5MsHZw2SUlwDb9PLSj7mZbgHeqXWNYmNbNSBKyZvD2ZA0K7u6iuWRZ-3YeoCL3OHxjD8gikY7j8NmA1xqKzSGzFrFSF-eKRHRyOwaDM-LFvH3Zfsh9XgvYDv05utyKzUH-6zVBGV61ZKp46Uh_sTSxRwQ"
DIRECTOR_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJPMzdpNEhXc0drajNfVGlOMnpyaSJ9.eyJpc3MiOiJodHRwczovL2xraGcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYzZWU0ZjI4ZjA3NWFiMDI0YzIwMjlkMyIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTY3ODA5MDUyMSwiZXhwIjoxNjc4MTc2OTIxLCJhenAiOiJmWnJPdUxZRzkzamhBNmQ4N3dlWmRIRGZ4QzJ6RnBCZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.i3ro4WKzRzOzGL2YAlhX8OaX9aMw9HnTvcgO0dY8SHbY_EcPbOStedzF-z2DEQHDcKNEUplGrea7pOo834eQJVG0hoJLUMd_n0FhFYmlWJYXN91HMMhCbWLSVU-gxYQ56m1cxq8DZQrerA245_2L954jOwM_8jVn3EwCaGUkL73z4ieV2mD0HVKnr84ZuOfOlgvK2Bn8Xm_bNYehUdamAZ93GugzyCPQgPZn9LHEi1YJoVCe-Pv3TIRj_qDX-615h67t3VFrSbqpdKZWa3PHTWV7oPRfmsAFW2M55p3bXBR3_mh1P4kiWNLyqfkNv253A5VomMO5pPQDYnxQX3z19g"
PRODUCER_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJPMzdpNEhXc0drajNfVGlOMnpyaSJ9.eyJpc3MiOiJodHRwczovL2xraGcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYzZmNhZjM1YjRkZjU1YTViMzhiNTMzYiIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTY3ODA5MDQ2NSwiZXhwIjoxNjc4MTc2ODY1LCJhenAiOiJmWnJPdUxZRzkzamhBNmQ4N3dlWmRIRGZ4QzJ6RnBCZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.FdOE9NB-_iwSRdmiemsEsJS4ToxG4Ma1LwMyLhPJFbEaUfwdTKeC-BK0GIdtLkznpY_ibk2qmcaZAY1ooUx-7eydBkTv3HUSTDT4jOjLplYESbJ756TMe56-r9FMPnZ_ziNeVl6hK4KS2hwjIbGIM_vudJllzwFdSmROwjIewYbOM5Tlh7ZDRGn2tnQEnygRfd7cXfiuP3uCn5Riy_wQfOxDWH48qL5Cnk0iiI1QNPGyMiNorJNHqdT5r64nuRQuCQQLVeE9p4FOj-xOc2-7uQiYP41AlGE1v-xdcQKGCeE8pHEGLW0lsTphPeJ_UshlZC6CMOf7VnNBk4x_5x1i1A"


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

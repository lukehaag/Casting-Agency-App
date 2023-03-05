import os
from flask import Flask, jsonify, abort, request
from models import setup_db, Actor, Movie
from flask_cors import CORS
from auth import requires_auth, AuthError
import json

# from flask import render_template, session, url_for, redirect


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    app.app_context().push()

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )

        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS"
        )
        return response

    @app.route("/actors", methods=["GET"])
    @requires_auth("get:actors")
    def get_actors(jwt):
        actors = Actor.query.all()

        return (
            jsonify({"success": True, "actors": [actor.format() for actor in actors]}),
            200,
        )

    @app.route("/actors", methods=["POST"])
    @requires_auth("post:actors")
    def post_actor(jwt):
        body = request.get_json()

        try:
            new_name = body["name"]
            new_age = body["age"]
            new_gender = body["gender"]

            actor = Actor(name=new_name, age=new_age, gender=new_gender)
            actor.insert()

            return jsonify({"success": True, "actors": [actor.format()]}), 200

        except Exception as e:
            print(e)
            abort(422)

    @app.route("/actors/<int:actor_id>", methods=["PATCH"])
    @requires_auth("patch:actors")
    def edit_actor(jwt, actor_id):
        body = request.get_json()
        actor = Actor.query.filter(actor_id == Actor.id).one_or_none()

        if not actor:
            abort(404)

        try:
            new_name = body.get("name")
            new_age = body.get("age")
            new_gender = body.get("gender")

            if new_name:
                actor.name = new_name

            if new_age:
                actor.age = new_age

            if new_gender:
                actor.gender = new_gender

            actor.update()

            return jsonify({"success": True, "actors": actor.format()}), 200

        except Exception as e:
            print(e)
            abort(422)

    @app.route("/actors/<int:actor_id>", methods=["DELETE"])
    @requires_auth("delete:actors")
    def delete_actor(jwt, actor_id):
        actor = Actor.query.filter(actor_id == Actor.id).one_or_none()

        if actor is None:
            abort(404)

        try:
            actor.delete()

            return jsonify({"success": True, "delete": actor_id}), 200

        except Exception as e:
            print(e)
            abort(422)

    @app.route("/movies", methods=["GET"])
    @requires_auth("get:movies")
    def get_movies(jwt):
        movies = Movie.query.all()

        return (
            jsonify({"success": True, "movies": [movie.format() for movie in movies]}),
            200,
        )

    @app.route("/movies", methods=["POST"])
    @requires_auth("post:movies")
    def new_movie(jwt):
        body = request.get_json()

        try:
            new_title = body["title"]
            new_release_date = body["release_date"]

            movie = Movie(title=new_title, release_date=new_release_date)
            movie.insert()

            return jsonify({"success": True, "movies": movie.format()}), 200

        except Exception as e:
            print(e)
            abort(422)

    @app.route("/movies/<int:movie_id>", methods=["PATCH"])
    @requires_auth("patch:movies")
    def edit_movie(jwt, movie_id):
        body = request.get_json()
        movie = Movie.query.filter(movie_id == Movie.id).one_or_none()

        if not movie:
            abort(404)

        try:
            new_title = body.get("title")
            new_release_date = body.get("release_date")

            if new_title:
                movie.title = new_title

            if new_release_date:
                movie.release_date = new_release_date

            movie.update()

            return jsonify({"success": True, "movies": movie.format()}), 200

        except Exception as e:
            print(e)
            abort(422)

    @app.route("/movies/<int:movie_id>", methods=["DELETE"])
    @requires_auth("delete:movies")
    def delete_movie(jwt, movie_id):
        movie = Movie.query.filter(movie_id == Movie.id).one_or_none()

        if movie is None:
            abort(404)

        try:
            movie.delete()

            return jsonify({"success": True, "delete": movie_id}), 200

        except Exception as e:
            print(e)
            abort(422)

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(AuthError)
    def handle_auth_error(e):
        response = jsonify(e.error)
        response.status_code = e.status_code
        return response

    return app


app = create_app()

if __name__ == "__main__":
    app.run()

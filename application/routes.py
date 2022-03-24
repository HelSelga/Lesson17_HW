from flask import current_app as app, request
from flask_restx import Resource, Api
from application.models import db
from application import models
from application.schema import *

api: Api = app.config['api']


movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        movies_query = db.session.query(models.Movie)
        args = request.args
        director_id = args.get('director_id')
        if director_id is not None:
            movies_query = movies_query.filter(models.Movie.director_id == director_id)

        genre_id = args.get('genre_id')
        if genre_id is not None:
            movies_query = movies_query.filter(models.Movie.genre_id == genre_id)

        movies = movies_query.all()

        return movies_schema.dump(movies), 200

    def post(self):
        req_json = request.json
        new_movie = models.Movie(**req_json)
        #new_movie = movie_schema.load(req_json)
        with db.session.begin():
            db.session.add(new_movie)
            #db.session.add(models.Movie(**new_movie))
        return None, 201


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid: int):
        try:
            movie = db.session.query(models.Movie).filter(models.Movie.id == mid).first()
            return movie_schema.dump(movie), 200
        except Exception as e:
            return str(e), 404

    def put(self, mid: int): # Далее закомменчены мои варианты решения
        #movie = db.session.query(models.Movie).get(mid)
        req_json = request.json

        # movie.title = req_json.get("title")
        # movie.description = req_json.get("description")
        # movie.trailer = req_json.get("trailer")
        # movie.year = req_json.get("year")
        # movie.rating = req_json.get("rating")
        # movie.genre_id = req_json.get("genre_id")
        # movie.director_id = req_json.get("director_id")

        updated_movie = db.session.query(models.Movie).filter(models.Movie.id == mid).update(req_json)

        if updated_movie != 1:
            return None, 400

        db.session.add(updated_movie)
        db.session.commit()

        return None, 204

    def delete(self, mid: int):
        movie = db.session.query(models.Movie).filter(models.Movie.id == mid).first()
        deleted_row = db.session.delete(movie)
        if deleted_row != 1:
            return None, 400
        db.session.commit()
        return None


# @movie_ns.route('/search')
# class MovieSearch(Resource):
#     def get_by_director(self, director_id: int):
#         query = request.args.get('director_id')
#         if query:
#             movies = db.session.query(models.Movie).filter(models.Movie.director_id == director_id).first()
#             return movie_schema.dump(movies), 200
#         else:
#             return "По вашему запросу ничего не найдено", 404
#
#     def get_by_genre(self, genre_id: int):
#         query = request.args.get('genre_id')
#         if query:
#             movies = db.session.query(models.Movie).filter(models.Movie.genre_id == genre_id).first()
#             return movie_schema.dump(movies), 200
#         else:
#             return "По вашему запросу ничего не найдено", 404


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        all_directors = db.session.query(models.Director).all()
        return directors_schema.dump(all_directors), 200

    def post(self):
        req_json = request.json
        new_director = models.Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
        return None, 201


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did: int):
        try:
            director = db.session.query(models.Director).filter(models.Director.id == did).first()
            return director_schema.dump(director), 200
        except Exception as e:
            return str(e), 404

    def put(self, did: int):
        # director = db.session.query(models.Director).get(did)
        req_json = request.json

        # director.name = req_json.get("name")
        updated_director = db.session.query(models.Director).filter(models.Director.id == did).update(req_json)

        if updated_director != 1:
            return None, 400

        db.session.add(updated_director)
        db.session.commit()

        return None, 204

    def delete(self, did: int):
        director = db.session.query(models.Director).filter(models.Director.id == did).first()
        deleted_row = db.session.delete(director)
        if deleted_row != 1:
            return None, 400
        db.session.commit()
        return None


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        all_genres = db.session.query(models.Genre).all()
        return genres_schema.dump(all_genres), 200

    def post(self):
        req_json = request.json
        new_genre = models.Genre(**req_json)
        with db.session.begin():
            db.session.add(new_genre)
        return None, 201


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid: int):
        try:
            genre = db.session.query(models.Genre).filter(models.Genre.id == gid).first()
            return director_schema.dump(genre), 200
        except Exception as e:
            return str(e), 404

    def put(self, gid: int):
        #genre = db.session.query(models.Genre).get(gid)
        req_json = request.json

        #genre.name = req_json.get("name")
        updated_genre = db.session.query(models.Genre).filter(models.Genre.id == gid).update(req_json)

        if updated_genre != 1:
            return None, 400

        db.session.add(updated_genre)
        db.session.commit()

        return None, 204

    def delete(self, gid: int):
        genre = db.session.query(models.Genre).filter(models.Genre.id == gid).first()
        deleted_row = db.session.delete(genre)
        if deleted_row != 1:
            return None, 400
        db.session.commit()
        return None

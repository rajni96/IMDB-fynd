import json
import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from .serializers import MovieSerializer, GenreSerializer, DirectorSerializer
from .models import Director, Genre, Movies as MoviesModel


# Create your views here.
class Movies(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        """[Add the movie with the name, director, genre etc provided in request.Same movie name and director can't be added if already exist]

        Args:
            request ([dict]):
               {
                name(str): Movies name,
                director(int): pass director id which is already saved in db e.g 6,
                genre(list[int]): pass genre list which are already saved in db e.g [21,22],
                popularity(float): pass popularity rate e.g 82.0
                imdb_score(float): pass movie score rate e.g 8.2
               }
        Returns:
            [dict]: [return passed dict if successfully saved]
        """
        try:
            request = request.data
            serializer = MovieSerializer(data=request)
            if serializer.is_valid():
                serializer.save()
                response = {"response": serializer.data, "status": status.HTTP_200_OK}
            else:
                response = {
                    "message": serializer.errors,
                    "status": status.HTTP_400_BAD_REQUEST,
                }

        except Exception as e:
            response = {
                "message": f"Something went wrong while adding movie Error:{str(e)}.",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
        return Response(response, status=response.get("status"))

    def patch(self, request):
        try:
            request = request.data
            movie = MoviesModel.objects.get(id=request.get("id"))
            serializer = MovieSerializer(movie, data=request, partial=True)
            if serializer.is_valid():
                serializer.save()
                response = {"response": serializer.data, "status": status.HTTP_200_OK}
            else:
                response = {
                    "message": serializer.errors,
                    "status": status.HTTP_400_BAD_REQUEST,
                }

        except MoviesModel.DoesNotExist:
            response = {
                "message": "Movie not found.",
                "status": status.HTTP_404_NOT_FOUND,
            }
        except Exception as e:
            response = {
                "message": f"Something went wrong while updating movie Error:{str(e)}.",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
        return Response(response, status=response.get("status"))

    def delete(self, request):
        try:
            request = request.GET
            MoviesModel.objects.get(id=request.get("id")).delete()
            response = {"response": "movie deleted successfully."}
            return Response(response, status=status.HTTP_200_OK)
        except MoviesModel.DoesNotExist:
            response = {
                "message": "Movie not found.",
                "status": status.HTTP_404_NOT_FOUND,
            }
        except Exception as e:
            response = {
                "message": f"Something went wrong while deleting movie Error:{str(e)}.",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
        return Response(response, status=response.get("status"))


@api_view(["GET"])
def get_movies(request):
    try:
        movies = []
        request = request.GET
        limit = int(request.get("limit", 10))
        offset = int(request.get("offset", 0))
        count = MoviesModel.objects.count()
        if request.get("_search"):
            movies_obj = MoviesModel.objects.filter(
                name__contains=request.get("_search")
            )[offset:limit]
        else:
            movies_obj = MoviesModel.objects.all()[offset:limit]
        for movie in movies_obj:
            genres = movie.genre.all()
            movie = {
                "id": movie.id,
                "name": movie.name,
                "imdb_score":movie.imdb_score,
                "popularity": movie.popularity,
                "director_id": movie.director.id,
                "director_name": movie.director.name,
                "genre": [],
            }
            movie["genre"].extend(
                [{"id": genre.id, "name": genre.name} for genre in genres]
            )
            movies.append(movie)
        response = {"response": movies, "total": count, "status": status.HTTP_200_OK}

    except Exception as e:
        response = {
            "message": f"Something went wrong while fetching movies Error:{str(e)}.",
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
        }
    return Response(response, status=response.get("status"))


@api_view(["GET"])
def get_director_list(request):
    try:
        directors = Director.objects.all().values("id", "name")
        response = {"response": directors, "status": status.HTTP_200_OK}
    except Exception as e:
        response = {
            "message": f"Something went wrong while fetching director list Error:{str(e)}.",
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
        }
    return Response(response, status=response.get("status"))


@api_view(["GET"])
def get_genre_list(request):
    try:
        genres = Genre.objects.all().values("id", "name")
        response = {"response": genres, "status": status.HTTP_200_OK}

    except Exception as e:
        response = {
            "message": f"Something went wrong while fetching genre list Error:{str(e)}.",
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
        }
    return Response(response, status=response.get("status"))


@api_view(["POST"])
def uploadMovieJson(request):
    try:
        file_path = os.path.join(os.path.dirname(__file__), "./imdb.jsont.json")
        data = open(file_path)
        movies = json.load(data)
        for movie in movies:
            # updateGenreInDb(movie.get("genre"))  # to add genre in genre table
            # updateDirectorInDb(
            #     movie.get("director")
            # )  # to add director in director table
            updateMovieIndb(movie)  # to add movie in movie table

        return Response("movies uploaded", status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def updateMovieIndb(movie):
    try:
        director_id = Director.objects.get(name=movie.get("director"))
        genres_list = [genre.strip() for genre in movie.get("genre")]
        genres = Genre.objects.filter(name__in=genres_list).values("id")
        genre_ids = [genre.get("id") for genre in genres]
        movie["genre"] = genre_ids
        movie["director"] = director_id.id
        movie["popularity"] = movie.get("99popularity")
        serializer = MovieSerializer(data=movie)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
            pass
    except Director.DoesNotExist:
        pass


def updateGenreInDb(genres: list):
    for name in genres:
        genre_serializer = GenreSerializer(data={"name": name.strip()})
        if genre_serializer.is_valid():
            genre_serializer.save()
        else:
            print(genre_serializer.errors)
            pass


def updateDirectorInDb(director: str):
    dir_serializer = DirectorSerializer(data={"name": director.strip()})
    if dir_serializer.is_valid():
        dir_serializer.save()
    else:
        print(dir_serializer.errors)
        pass

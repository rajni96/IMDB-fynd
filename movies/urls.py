from django.urls import path

from .views import (
    Movies,
    get_movies,
    uploadMovieJson,
    get_genre_list,
    get_director_list,
)

urlpatterns = [
    path("list", get_movies, name="movies_list"),
    path("add", Movies.as_view(), name="movies_add"),
    path("update", Movies.as_view(), name="movies_update"),
    path("delete", Movies.as_view(), name="movies_delete"),
    path("genre/list", get_genre_list, name="genre_list"),
    path("director/list", get_director_list, name="director_list"),
    # path("upload", uploadMovieJson, name="movies_delete"),
]


from django.urls import path
from . import views


urlpatterns = [
    path("all_movies/",  views.all_movies, name="all-movies"),
    path("all_movies/<int:movie_id>/",  views.movie_info, name="movie-info"),
    path("add_movie/<int:movie_id>",  views.add_movie, name="add-movie"),
    path("movies_to_watch/",  views.my_movies, name="my-movies"),
    ]

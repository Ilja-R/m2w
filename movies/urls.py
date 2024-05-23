from django.urls import path
from . import views


urlpatterns = [
    path("all_movies/",  views.all_movies, name="all-movies"),
    path("all_movies/<int:movie_id>/",  views.movie_info, name="movie-info"),
    path("add_movie/<int:movie_id>",  views.add_movie, name="add-movie"),
    path("rate_movie/<int:movie_id>",  views.rate_movie, name="rate-movie"),
    path("delete_movie/<int:movie_id>",  views.delete_movie, name="delete-movie"),
    path("advice-to-friends/<int:movie_id>",  views.advice_to_friends, name="advice-to-friends"),
    path("advice-to-friends/<int:movie_id>/<int:friend_id>",  views.advice_movie_to_friend, name="advice-movie-to-friend"),
    path("movies_to_watch/",  views.my_movies, name="my-movies"),
    path("my_advices/", views.my_advices, name="my-advices"),
    path("delete_advice/<int:advice_id>", views.delete_advice, name="delete-advice"),
    ]

from django.urls import path
from . import views


urlpatterns = [
    path("movies_to_watch/",  views.my_movies, name="my-profile"),
    ]

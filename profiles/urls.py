from django.urls import path
from . import views

# app_name = "profiles" # TODO: change to profiles (add profiles in main url.py)

urlpatterns = [
    path("",  views.my_profile, name="my-profile"),
    path("myprofile/", views.my_profile, name="my-profile"),
    path("friends/", views.my_friends, name="friends"),
    path("delete_request/<int:pk>/", views.delete_request, name="delete-request"),
    path("accept_request/<int:pk>/", views.accept_request, name="accept-request"),
    path("delete_friend/<int:pk>", views.delete_friend, name="delete-friend"),
    ]

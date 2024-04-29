from django.urls import path
from . import views

# app_name = "profiles" # TODO: change to profiles (add profiles in main url.py)

urlpatterns = [
    path("",  views.my_profile, name="my-profile"),
    path("myprofile/", views.my_profile, name="my-profile"),
    path("friends/", views.my_friends, name="friends"),
    ]

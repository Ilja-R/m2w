from django.contrib.auth.decorators import login_required
from django.shortcuts import render



@login_required
def my_cinema_view(request):
    return render(request, 'My_cinema.html')


def welcome_view(request):
    return render(request, 'Welcome.html')



from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from movies.models import MovieToWatch


@login_required(login_url='login')
def my_movies(request):
    movies = MovieToWatch.objects.filter(user=request.user)
    context = {
        'movies': movies,
    }
    return render(request, 'movies/my_movies.html', context)

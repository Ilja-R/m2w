from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from movies.models import MovieToWatch, Movie


@login_required(login_url='login')
def my_movies(request):
    movies = MovieToWatch.objects.filter(user=request.user)
    context = {
        'movies': movies,
    }
    return render(request, 'movies/my_movies.html', context)


@login_required(login_url='login')
def all_movies(request):
    movies = Movie.objects.all()
    added_movies_id = MovieToWatch.objects.filter(user=request.user).values_list('movie_id', flat=True)

    print([movie.id for movie in movies])
    print(added_movies_id)

    context = {
        'all_movies': movies,
        'added_movies_id': added_movies_id,
    }
    return render(request, 'movies/all_movies.html', context)


@login_required(login_url='login')
def movie_info(request, movie_id):
    movie = Movie.objects.all().get(id=movie_id)
    is_added = MovieToWatch.objects.filter(user=request.user, movie=movie).exists()
    context = {
        'movie': movie,
        'is_added': is_added,
    }
    return render(request, 'movies/movie.html', context)


@login_required(login_url='login')
def add_movie(request, movie_id):
    movie = Movie.objects.all().get(id=movie_id)
    if MovieToWatch.objects.filter(user=request.user, movie=movie).exists():
        message = 'You have already added this movie to your list'
        messages.error(request, message)
    else:
        MovieToWatch.objects.create(user=request.user, movie=movie)
        message = f'Movie {movie.title} added to your list'
        messages.success(request, message)
    return redirect('all-movies')

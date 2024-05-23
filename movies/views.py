from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

from movies.forms import RatingForm
from movies.models import MovieToWatch, Movie, MovieAdvice
from profiles.models import Profile


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

    context = {
        'all_movies': movies,
        'added_movies_id': added_movies_id,
    }
    return render(request, 'movies/all_movies.html', context)


@login_required(login_url='login')
def movie_info(request, movie_id):
    movie = Movie.objects.all().get(id=movie_id)
    is_added = MovieToWatch.objects.filter(user=request.user, movie=movie).exists()
    is_watched = MovieToWatch.objects.filter(user=request.user, movie=movie, watched=True).exists()

    context = {
        'movie': movie,
        'is_added': is_added,
        'is_watched': is_watched,
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


@login_required(login_url='login')
def rate_movie(request, movie_id):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['personal_rating']
            movie = get_object_or_404(MovieToWatch, user=request.user, movie_id=movie_id)
            movie.personal_rating = rating
            movie.watched = True
            movie.save()
            messages.success(request, 'Your rating has been saved')
            return redirect('my-movies')
        else:
            messages.error(request, 'Something went wrong')
    else:
        form = RatingForm()
    return render(request, 'movies/rate_movie.html', {'form': form})


@login_required(login_url='login')
def delete_movie(request, movie_id):
    movie = get_object_or_404(MovieToWatch, user=request.user, movie_id=movie_id)
    movie.delete()
    messages.success(request, 'Movie has been deleted')
    return redirect('my-movies')


@login_required(login_url='login')
def advice_to_friends(request, movie_id):
    profile = Profile.objects.get(user=request.user)
    all_friends = profile.friends.all()
    movie = Movie.objects.get(id=movie_id)
    friends_to_advice = []
    for friend in all_friends:
        if (not MovieToWatch.objects.filter(user=friend, movie=movie).exists() and not MovieAdvice.objects.filter(
                receiver=friend, movie=movie).exists()):
            friends_to_advice.append(friend)
    context = {
        'friends': friends_to_advice,
        'movie': movie,
    }

    return render(request, 'movies/advice_to_friends.html', context)


def advice_movie_to_friend(request, friend_id, movie_id):
    friend = Profile.objects.get(id=friend_id)
    movie = Movie.objects.get(id=movie_id)
    MovieAdvice.objects.create(sender=request.user, receiver=friend.user, movie=movie)
    messages.success(request, 'Movie has been advised to your friend')
    return redirect('advice-to-friends', movie_id=movie_id)


def my_advices(request):
    all_advices = MovieAdvice.objects.filter(receiver=request.user, status='send').all()

    for advice in all_advices:
        if MovieToWatch.objects.filter(user=advice.receiver, movie=advice.movie).exists():
            advice.status = 'accepted'
            advice.save()

    all_advices.filter(status='send')

    context = {
        'advices': all_advices,
    }
    return render(request, 'movies/advices.html', context)


def delete_advice(request, advice_id):
    advice = get_object_or_404(MovieAdvice, id=advice_id)
    advice.delete()
    messages.success(request, 'Advice has been deleted')
    return redirect('my-advices')
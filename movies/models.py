from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name='movies')
    director = models.CharField(max_length=255)
    plot = models.TextField()
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class MovieToWatch(models.Model):
    user = models.ForeignKey('authentication.AppUser', on_delete=models.CASCADE, related_name='movies_to_watch')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movies_to_watch')
    watched = models.BooleanField(default=False)
    personal_rating = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}-{self.movie}'

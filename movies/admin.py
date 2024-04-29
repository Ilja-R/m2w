from django.contrib import admin

# Register your models here.
from .models import MovieToWatch, Genre, Movie

admin.site.register(MovieToWatch)
admin.site.register(Genre)
admin.site.register(Movie)

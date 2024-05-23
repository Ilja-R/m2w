# movies/management/commands/add_movies.py
import os
import random
from django.core.management.base import BaseCommand
from django.conf import settings
from movies.models import Movie, Genre
from faker import Faker
from PIL import Image, ImageDraw, ImageFont


class Command(BaseCommand):
    help = 'Add 100 movie objects to the database'

    def handle(self, *args, **kwargs):
        movie_genres = [
            "Action",
            "Adventure",
            "Comedy",
            "Drama",
            "Fantasy",
            "Horror",
            "Mystery",
            "Romance",
            "Sci-Fi",
            "Thriller",
            "Western",
            "Documentary",
            "Animation",
            "Biography",
            "Crime"
        ]

        for genre in movie_genres:
            new_genre = Genre.objects.create(name=genre)
            new_genre.save()

        fake = Faker()
        genres = list(Genre.objects.all())  # Ensure you have some genres created in your database

        for i in range(100):
            # Generate fake movie data
            title = fake.sentence(nb_words=3)
            year = random.randint(1950, 2023)
            director = fake.name()
            plot = fake.paragraph(nb_sentences=5)

            # Create a placeholder poster image
            poster_path = self.generate_poster(i, title)

            # Create the movie object
            movie = Movie.objects.create(
                title=title,
                year=year,
                director=director,
                plot=plot,
                poster=poster_path
            )

            # Add random genres to the movie
            movie.genres.set(random.sample(genres, k=min(3, len(genres))))  # Assign up to 3 random genres
            movie.save()

        self.stdout.write(self.style.SUCCESS('Successfully added 100 movie objects'))

    def generate_poster(self, index, title):
        # Create a blank image with white background
        width, height = 200, 300
        image = Image.new('RGB', (width, height), color = (255, 255, 255))

        # Draw text on the image
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        # Add the title text to the image
        text = f"Movie {index + 1}\n{title}"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (width - text_width) / 2
        text_y = (height - text_height) / 2
        draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)

        # Save the image to the 'posters' directory
        poster_dir = os.path.join(settings.MEDIA_ROOT, 'posters')
        os.makedirs(poster_dir, exist_ok=True)
        poster_filename = f"poster_{index + 1}.png"
        poster_path = os.path.join(poster_dir, poster_filename)
        image.save(poster_path)

        # Return the relative path to the saved poster image
        return f'posters/{poster_filename}'

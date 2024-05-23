from django import forms
from movies.models import MovieToWatch


RATING_CHOICES = [(i, str(i)) for i in range(11)]  # Choices from 0 to 10


class RatingForm(forms.ModelForm):

    class Meta:
        model = MovieToWatch
        fields = ['personal_rating']
        widgets = {
            'personal_rating': forms.RadioSelect(choices=RATING_CHOICES)
        }
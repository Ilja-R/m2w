from django.contrib.auth import get_user_model
from django.db import models


class MovieAppUser(models.Model):
    user = models.OneToOneField(get_user_model(), unique=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.user}'

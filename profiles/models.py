from django.contrib.auth import get_user_model
from django.db import models

from authentication.models import AppUser


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), unique=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100)
    avatar = models.ImageField(default='movie.png', upload_to='avatars/')

    friends = models.ManyToManyField(AppUser, blank=True, related_name='friends')

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # TODO: IR maybe add slag?

    def __str__(self):
        return f'{self.user}-{self.created.date()}'


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='send')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender}-{self.receiver}-{self.status}'

    class Meta:
        unique_together = ['sender', 'receiver']
        index_together = ['sender', 'receiver']

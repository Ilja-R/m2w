import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from authentication.models import AppUser
from .models import Profile, Relationship

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AppUser)
def post_save_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, email=instance.email)


@receiver(post_save, sender=Profile)
def post_create_profile(sender, instance, created, **kwargs):
    if created:
        logger.info(f'Profile for user {instance} successfully created')


@receiver(post_save, sender=Relationship)
def post_relationship_save(sender, instance, created, **kwargs):
    the_sender = instance.sender
    the_receiver = instance.receiver
    if instance.status == 'accepted':
        the_sender.friends.add(the_receiver.user)
        the_receiver.friends.add(the_sender.user)
        the_sender.save()
        the_receiver.save()
        logger.info(f'{the_sender} and {the_receiver} are now friends')

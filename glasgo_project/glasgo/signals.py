from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

from glasgo.models import Vote, Attraction


@receiver(post_save, sender=Vote)
def save_vote(sender, instance, created, **kwargs):
    if created:
        if instance.like:
            instance.attraction.rating += 1
        else:
            instance.attraction.rating -= 1
        instance.attraction.save()


@receiver(post_save, sender=Attraction)
def save_added_time(sender, instance, created, **kwargs):
    if created:
        instance.added = datetime.now()
        instance.save()

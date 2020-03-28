import pytz
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from datetime import datetime

from glasgo.models import Vote, Attraction


# Adds a vote to the current attraction and updates the total rating
@receiver(post_save, sender=Vote)
def save_vote(sender, instance, created, **kwargs):
    if created:
        if instance.like:
            instance.attraction.rating += 1
        else:
            instance.attraction.rating -= 1
    else:
        if instance.like:
            instance.attraction.rating += 2
        else:
            instance.attraction.rating -=2
    instance.attraction.save()


# Removes a vote from the current attraction and updates the total rating
@receiver(pre_delete, sender=Vote)
def delete_vote(sender, instance, **kwargs):
    if instance.like:
        instance.attraction.rating -= 1
    else:
        instance.attraction.rating += 1
    instance.attraction.save()


# Records the time the current attraction was submitted (in the Attraction's added field)
@receiver(post_save, sender=Attraction)
def save_added_time(sender, instance, created, **kwargs):
    if created:
        instance.added = datetime.now(pytz.utc)
        instance.save()

from django.db.models.signals import post_save
from django.dispatch import receiver

from glasgo.models import Vote


@receiver(post_save, sender=Vote)
def save_vote(sender, instance, created, **kwargs):
    if created:
        if instance.like:
            instance.attraction.rating += 1
        else:
            instance.attraction.rating -= 1
        instance.attraction.save()

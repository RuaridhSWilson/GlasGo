from django.db.models import Q

from glasgo.models import Attraction, Tag


def get_attractions(contains="", tags=None):
    if tags:
        attractions = [Tag.objects.get(slug=tag).attraction_set.all() for tag in tags]
        attractions = attractions[0].intersection(*attractions[1:])
    else:
        attractions = Attraction.objects.all()

    if contains:
        attractions = attractions.intersection(Attraction.objects.filter(title__icontains=contains))

    return attractions.order_by("-added")

from glasgo.models import Attraction


def get_attractions(contains=""):
    if contains:
        return Attraction.objects.filter(title__icontains=contains).order_by("added")
    else:
        return Attraction.objects.order_by("added")

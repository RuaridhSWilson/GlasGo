from glasgo.models import Attraction


def get_attractions(starts_with=""):
    if starts_with:
        return Attraction.objects.filter(title__istartswith=starts_with).order_by(
            "added"
        )
    else:
        return Attraction.objects.order_by("added")
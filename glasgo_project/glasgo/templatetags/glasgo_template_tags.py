from django import template

from glasgo.models import Attraction, Vote

register = template.Library()


@register.inclusion_tag("glasgo/top_ten.html")
def get_top_ten():
    return {"top_ten": Attraction.objects.filter(approved=True).order_by("-rating")[:10]}

@register.inclusion_tag("glasgo/attractions.html")
def get_attractions():
    return {"attractions": Attraction.objects.filter(approved=True).order_by("-added")}
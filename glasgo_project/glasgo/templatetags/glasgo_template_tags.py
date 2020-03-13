from django import template

from glasgo.models import Attraction, Vote

register = template.Library()


@register.inclusion_tag("glasgo/top_ten.html")
def get_top_ten():
    return {"top_ten": Attraction.objects.order_by("-rating")[:10]}

@register.inclusion_tag("glasgo/attractions.html")
def get_attractions():
    return {"attractions": Attraction.objects.order_by("-added")}
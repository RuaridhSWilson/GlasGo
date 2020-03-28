from django.db.models import Q

from glasgo.models import Attraction, Tag


# Returns a list of Attraction objects which are filtered by text and tags if given
# Note the approved=True filter prevents unapproved attractions from being displayed
def get_attractions(contains="", tags=None):
    # If tags are given filter attractions with those tags
    if tags:
        attractions = [Tag.objects.get(slug=tag).attraction_set.filter(approved=True) for tag in tags]
        attractions = attractions[0].intersection(*attractions[1:])
    else:
        attractions = Attraction.objects.filter(approved=True)

    # If text is given filter attractions whose title contains that text
    if contains:
        attractions = attractions.intersection(Attraction.objects.filter(title__icontains=contains, approved=True))

    # Return the list of attractions ordered by date added descending (most recent first)
    return attractions.order_by("-added")

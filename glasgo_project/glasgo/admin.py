from django.contrib import admin
from glasgo.models import Attraction, Tag, Vote

admin.site.register(Attraction)
admin.site.register(Tag)
admin.site.register(Vote)
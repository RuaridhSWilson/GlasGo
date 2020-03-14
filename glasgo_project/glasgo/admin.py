from django.contrib import admin
from glasgo.models import Attraction, Tag, Vote


class AttractionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("approved", "title", "price_range", "added", "rating")


admin.site.register(Attraction, AttractionAdmin)


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Tag, TagAdmin)


class VoteAdmin(admin.ModelAdmin):
    list_display = ("attraction", "user", "like")


admin.site.register(Vote, VoteAdmin)

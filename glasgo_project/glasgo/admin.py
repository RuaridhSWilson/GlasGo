from django.contrib import admin
from glasgo.models import Attraction, Tag, Vote

# Approve attraction action - sets approved field of selected attractions to True
def approve_attraction(modeladmin, request, queryset):
    queryset.update(approved=True)

approve_attraction.short_description = "Approve selected attractions"


# AttractionAdmin class - for admins to view & edit attractions
class AttractionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("approved", "title", "price_range", "added", "rating")
    actions = [approve_attraction]

admin.site.register(Attraction, AttractionAdmin)


# TagAdmin class - for admins to view & edit tags
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Tag, TagAdmin)


# VoteAdmin class - for admins to view & edit votes
class VoteAdmin(admin.ModelAdmin):
    list_display = ("attraction", "user", "like")


admin.site.register(Vote, VoteAdmin)

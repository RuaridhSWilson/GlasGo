from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from glasgo.forms import AttractionForm
from glasgo.helper_functions import get_attractions
from glasgo.models import Attraction, Vote, Tag


# Home View
class HomeView(View):
    def get(self, request):
        return render(
            request,
            "glasgo/home.html",
            context={"attractions": Attraction.objects.order_by("added")},
        )


# About View
class AboutView(View):
    def get(self, request):
        return render(request, "glasgo/about.html")


# Attraction View
class AttractionView(View):
    def get(self, request, slug):
        # Get the attraction to render
        try:
            attraction = Attraction.objects.get(slug=slug)
        except Attraction.DoesNotExist:
            attraction = None

        vote = None
        # If the user is logged in render the page with their current vote on the attraction
        if request.user.is_authenticated:
            try:
                vote = Vote.objects.get(attraction=attraction, user=request.user)
            except Vote.DoesNotExist:
                pass

        return render(
            request,
            "glasgo/attraction.html",
            context={"attraction": attraction, "vote": vote},
        )


# Add Attraction View
class AddAttractionView(View):
    # GET - render the Add Attraction page initially
    @method_decorator(login_required)
    def get(self, request):
        return render(
            request, "glasgo/add_attraction.html", context={"form": AttractionForm()},
        )

    # POST - redirect to the new attraction after it has been submitted successfully
    # If form was invalid render the Add Attraction page with error messages
    @method_decorator(login_required)
    def post(self, request):
        form = AttractionForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the new attraction if the form was valid and add the Price,
            # Accessibility and Event tags if applicable
            attraction = form.save(commit=True)
            attraction.add_price_tag()
            attraction.add_access_tags()
            attraction.add_event_tag()
            # Redirect to the new attraction's page
            return redirect(
                reverse("glasgo:attraction", kwargs={"slug": attraction.slug})
            )
        else:
            # If the form was invalid render the form with error messages
            print(form.errors)
            return render(
                request, "glasgo/add_attraction.html", {"form": AttractionForm()},
            )


# Search View
class SearchView(View):
    def get(self, request):
        tags = Tag.objects.all()
        return render(request, "glasgo/search.html", {"tags": tags})


# SearchAttractions View - display the Attractions searched for
class SearchAttractionsView(View):
    def get(self, request):
        if "search" in request.GET:
            search = request.GET["search"]
        else:
            search = ""

        tags = request.GET.getlist("tags[]")
        print(tags)

        attractions = get_attractions(search, tags)
        return render(request, "glasgo/attractions.html", {"attractions": attractions})


# Vote View
class VoteView(View):
    @method_decorator(login_required)
    def get(self, request):
        # Get the vote's fields (associated attraction & user and like/dislike)
        attraction_title = request.GET["attraction"]
        username = request.GET["user"]
        like = request.GET["like"]
        try:
            attraction = Attraction.objects.get(title=attraction_title)
            user = User.objects.get(username=username)
        except (Attraction.DoesNotExist, User.DoesNotExist):
            return redirect(reverse("glasgo:home"))

        if like == "None":
            # If the vote has no associated like/dislike value try and delete it
            try:
                vote = Vote.objects.get(user=user, attraction=attraction)
                vote.delete()
                vote = None
            except Vote.DoesNotExist:
                return render(
                    request,
                    "glasgo/rating.html",
                    {"attraction": attraction, "vote": None},
                )
        else:
            # If the vote is a like or dislike save the vote object
            like = like == "True"
            try:
                vote = Vote.objects.get(user=user, attraction=attraction)
                if vote.like != like:
                    vote.like = like
                    vote.save()
            except Vote.DoesNotExist:
                vote = Vote.objects.create(user=user, attraction=attraction, like=like)

        # The attraction has to be reloaded to get the updated rating
        try:
            attraction = Attraction.objects.get(title=attraction_title)
        except Attraction.DoesNotExist:
            return redirect(reverse("glasgo:home"))

        return render(
            request, "glasgo/rating.html", {"attraction": attraction, "vote": vote}
        )

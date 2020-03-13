from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from glasgo.forms import AttractionForm
from glasgo.helper_functions import get_attractions
from glasgo.models import Attraction, Vote, Tag


# Home view
class HomeView(View):
    def get(self, request):
        return render(
            request,
            "glasgo/home.html",
            context={"attractions": Attraction.objects.order_by("added")},
        )


class AboutView(View):
    def get(self, request):
        return render(request, "glasgo/about.html")


class AttractionView(View):
    def get(self, request, slug):
        try:
            attraction = Attraction.objects.get(slug=slug)
        except Attraction.DoesNotExist:
            attraction = None

        try:
            vote = Vote.objects.get(attraction=attraction, user=request.user)
        except Vote.DoesNotExist:
            vote = None

        return render(
            request,
            "glasgo/attraction.html",
            context={"attraction": attraction, "vote": vote},
        )


class AddAttractionView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(
            request, "glasgo/add_attraction.html", context={"form": AttractionForm()},
        )

    @method_decorator(login_required)
    def post(self, request):
        form = AttractionForm(request.POST, request.FILES)
        if form.is_valid():
            attraction = form.save(commit=True)
            return redirect(
                reverse("glasgo:attraction", kwargs={"slug": attraction.slug})
            )
        else:
            print(form.errors)
            return render(
                request, "glasgo/add_attraction.html", {"form": AttractionForm()},
            )


class SearchView(View):
    def get(self, request):
        tags = Tag.objects.all()
        return render(request, "glasgo/search.html", {"tags": tags})


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


class VoteView(View):
    @method_decorator(login_required)
    def get(self, request):
        attraction_title = request.GET["attraction"]
        username = request.GET["user"]
        like = request.GET["like"]
        try:
            attraction = Attraction.objects.get(title=attraction_title)
            user = User.objects.get(username=username)
        except (Attraction.DoesNotExist, User.DoesNotExist):
            return redirect(reverse("glasgo:home"))

        if like == "None":
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
            like = like == "True"
            try:
                vote = Vote.objects.get(user=user, attraction=attraction)
                if vote.like != like:
                    vote.like = like
                    vote.save()
            except Vote.DoesNotExist:
                vote = Vote.objects.create(user=user, attraction=attraction, like=like)

        # attraction has to be reloaded to get the updated rating
        try:
            attraction = Attraction.objects.get(title=attraction_title)
        except Attraction.DoesNotExist:
            return redirect(reverse("glasgo:home"))

        return render(
            request, "glasgo/rating.html", {"attraction": attraction, "vote": vote}
        )

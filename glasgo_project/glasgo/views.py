from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from glasgo.forms import AttractionForm
from glasgo.helper_functions import get_attractions
from glasgo.models import Attraction

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

        return render(
            request, "glasgo/attraction.html", context={"attraction": attraction}
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
                request,
                "glasgo/add_attraction.html",
                context={"form": AttractionForm()},
            )


class SearchView(View):
    def get(self, request):
        return render(request, "glasgo/search.html")


class SearchAttractionsView(View):
    def get(self, request):
        if "search" in request.GET:
            search = request.GET["search"]
        else:
            search = ""

        attractions = get_attractions(search)
        return render(request, "glasgo/attractions.html", {"attractions": attractions})
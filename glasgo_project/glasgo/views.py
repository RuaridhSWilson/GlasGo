from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from glasgo.forms import AttractionForm
from glasgo.models import Attraction


def get_top_ten():
    return Attraction.objects.order_by("-score")[:10]


class TestView(View):
    def get(self, request):
        return render(request, "glasgo/test.html")


class HomeView(View):
    def get(self, request):
        context = {}
        context["attractions"] = Attraction.objects.order_by("added")
        context["top_ten"] = get_top_ten()

        return render(request, "glasgo/home.html", context=context)


class AboutView(View):
    def get(self, request):
        render(request, "glasgo/about.html", {"top_ten": get_top_ten()})


class AttractionView(View):
    def get(self, request, slug):
        context = {}
        try:
            attraction = Attraction.objects.get(slug=slug)
            context["attraction"] = attraction
        except Attraction.DoesNotExist:
            context["attraction"] = None

        context["top_ten"] = get_top_ten()

        return render(request, "glasgo/attraction.html", context=context)


class AddAttractionView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(
            request,
            "glasgo/add_attraction.html",
            context={"form": AttractionForm(), "top_ten": get_top_ten()},
        )

    @method_decorator(login_required)
    def post(self, request):
        form = AttractionForm(request.POST)
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
                context={"form": AttractionForm(), "top_ten": get_top_ten()},
            )

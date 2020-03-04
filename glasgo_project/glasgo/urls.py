from django.urls import path

from glasgo import views

app_name = "glasgo"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("attraction/<slug:slug>/", views.AttractionView.as_view(), name="attraction"),
    path("add/", views.AddAttractionView.as_view(), name="add"),
    path("search/", views.SearchView.as_view(), name="search"),
    path(
        "search_attractions/",
        views.SearchAttractionsView.as_view(),
        name="search_attractions",
    ),
]

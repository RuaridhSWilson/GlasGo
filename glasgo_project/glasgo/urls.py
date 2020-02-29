from django.urls import path

from glasgo import views

app_name = "glasgo"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("attraction/<slug:slug>/", views.AttractionView.as_view(), name="attraction"),
    path("add/", views.AddAttractionView.as_view(), name="add"),
]

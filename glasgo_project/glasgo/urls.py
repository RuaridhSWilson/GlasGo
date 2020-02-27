from django.urls import path

from glasgo import views

app_name = "glasgo"

urlpatterns = [
    path("", views.TestView.as_view(), name="test"),
]

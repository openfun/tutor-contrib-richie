from django.urls import path

from . import views

urlpatterns = [
    path("<path:subpath>", views.redirect_to_richie, name="redirect_to_richie"),
]

from django.urls import path
from . import views

urlpatterns = [
    path("compare/", views.compare, name="dna_compare"),
    path("likelihood/", views.likelihood, name="dna_likelihood"),
]

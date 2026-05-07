from django.urls import path
from . import views

urlpatterns = [
    path("models/", views.models, name="dna_models"),
    path("cds-completion/", views.cds_completion, name="cds_completion"),
    path("promoter-extension/", views.promoter_extension, name="promoter_extension"),
    path("intron-generation/", views.intron_generation, name="intron_generation"),
]

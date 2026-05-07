from django.urls import path
from . import views

urlpatterns = [
    path('datasetlist/', views.dataset_list),
    path('files/<int:file_id>/preview/', views.file_preview),
    path('files/<int:file_id>/download/', views.file_download),
    path('datasetupdate/', views.dataset_update),  # New endpoint for dataset update
]

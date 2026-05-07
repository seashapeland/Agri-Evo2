# dataset/admin.py
from django.contrib import admin
from .models import Dataset, GenomeFile

admin.site.register(Dataset)
admin.site.register(GenomeFile)

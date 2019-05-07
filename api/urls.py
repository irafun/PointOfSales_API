# Django
from django.contrib import admin
from django.urls import path, include

# local
from core import views


urlpatterns = [
    # List of PATH API Object was refactoring to urls.py file in core folder
    path('', include('core.urls'))
]

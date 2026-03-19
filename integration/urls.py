from django.urls import path
from .views import environment_summary

urlpatterns = [
    path("environment-summary/", environment_summary),
]
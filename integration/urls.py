from django.urls import path
from .views import environment_summary

app_name = "environment"

urlpatterns = [
    path("environment-summary/", environment_summary),
]
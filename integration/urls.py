from django.urls import path
from .views import environment_summary

urlpatterns = [
    path("environment-summary/<str:country>/", environment_summary, name="environment-summary"),
]
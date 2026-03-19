from django.urls import path
from . import views

app_name = "environment"  

urlpatterns = [
    path(
        "environment-summary/",
        views.environment_summary,
        name="environment_summary"  
    ),
]
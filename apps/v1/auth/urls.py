from django.urls import path
from apps.v1.auth import views

urlpatterns = [
    path('token/', views.CustomAuthToken.as_view()),
]
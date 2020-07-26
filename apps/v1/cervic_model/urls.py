from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.v1.cervic_model import views

router = DefaultRouter()
router.register('', views.ClassificationViewSet, 'classifications')

urlpatterns = [
    path('classifications/', include(router.urls)),
]
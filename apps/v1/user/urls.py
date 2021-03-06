from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.v1.user import views

router = DefaultRouter()
router.register('', views.UserViewSet, 'user')

urlpatterns = [
    path('', include(router.urls)),
]
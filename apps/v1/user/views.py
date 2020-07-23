from django.shortcuts import render
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework_api_key.permissions import HasAPIAccess

from apps.v1.common.pagination import DefaultLimitOffsetPagination
from apps.v1.user import serializers, models, permissions

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    permission_classes = [
        HasAPIAccess,
        permissions.UserPermission,
    ]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "account__username",
        "account__is_active",
        "name",
    ]

    search_fields = [
        "account__username",
        "name",
        "degree__instance_name",
        "degree__name",
        "place__country",
        "place__province",
        "place__city",
        "place__street_name",
        "place__postal_code",
    ]

    ordering_fields = [
        "account__username",
        "name",
        "updated_at",
        "created_at",
    ]

    pagination_class = DefaultLimitOffsetPagination

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created and instance != None:
        Token.objects.create(user = instance)
    
    
    
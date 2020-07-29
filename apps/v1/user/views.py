from django.shortcuts import render
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework_api_key.permissions import HasAPIAccess

from apps.v1.common.tools import get_user_or_none
from apps.v1.user import serializers, models, permissions

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    permission_classes = [
        HasAPIAccess,
        permissions.UserPermission,
    ]

    def get_queryset(self):
        account = self.request.user
        if account.is_staff:
            return models.User.objects.all()
        else:
            return models.User.objects.filter(account = account)

    def list(self, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, pk, *args, **kwargs):
        user = get_user_or_none(request)
        user_id = str(user.id)
        if pk.lower() == 'me' or pk == user_id:
            self.kwargs['pk'] = user_id
            return super().retrieve(request, *args, **kwargs)

        else:
            return Response(status = status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        if request.method == 'PATCH':
            return super().update(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None, *args, **kwargs):
        user = get_user_or_none(request)
        user_id = str(user.id)
        if pk.lower() == 'me' or user_id == pk:
            self.kwargs['pk'] = user_id
            return super().partial_update(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk, *args, **kwargs):
        user = get_user_or_none(request)
        user_id = str(user.id)
        if pk.lower() == 'me' or user_id == pk:
            self.kwargs['pk'] = user_id
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created and instance != None:
        Token.objects.create(user = instance)
    
    
    
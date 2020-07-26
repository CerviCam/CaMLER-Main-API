from rest_framework.response import Response
from django.conf import settings
from asgiref.sync import async_to_sync
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIAccess

from apps.v1.common import tools
from apps.v1.user.models import User
from apps.v1.cervic_model import serializers, models

# Create your views here.
class ClassificationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CervicSerializer
    queryset = models.CervicClassification.objects.all()
    permission_classes = [IsAuthenticated, HasAPIAccess]

    def get_queryset(self):
        user = User.objects.get(account = self.request.user)
        return models.CervicClassification.objects.filter(creator = user)

    def create(self, request, *args, **kwargs):
        serializer = serializers.CervicSerializer(data = request.data, context = {'request': request})

        if serializer.is_valid():
            classification = serializer.save()
            # send_classification_request(classification)
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def update(self, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)

def send_classification_request(instance):
    response = tools.fetch(
        url = '{}/predict'.format(settings.APIS['AI']['DOMAIN']),
        method = 'POST',
        body = {
            'image_url': settings.APIS['MAIN']['DOMAIN'] + instance.image.url,
        }
    )
    
    instance.status = models.CervicClassification.Status.DONE
    instance.save()
        

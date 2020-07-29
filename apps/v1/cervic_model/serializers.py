from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from apps.v1.cervic_model import models
from apps.v1.user.models import User

class CervicSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = models.CervicClassification
        fields = (
            'id',
            'created_at',
            'updated_at',
            'creator',
            'image',
            'status',
            'result',
        )
        depth = 1
        extra_kwargs = {
            'creator': {
                'read_only': True,
            },
            'status': {
                'read_only': True,
            },
            'result': {
                'read_only': True,
            }
        }

    def save(self):
        account = self.context.get('request').user
        user = account.user
        return super(CervicSerializer, self).save(creator = user)
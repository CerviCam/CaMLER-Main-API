from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from apps.v1.cervic_model import models
from apps.v1.user.models import User

class CervicSerializer(serializers.ModelSerializer):
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
            'image': {
                'write_only': True,
            },
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

    def to_representation(self, instance, *args, **kwargs):
        representation = {
            'image_url': self.context.get('request').build_absolute_uri(instance.image.url),
            'creator': {
                'id': instance.creator.id,
                'name': instance.creator.name,
            },
            'status': {
                'code': instance.status,
                'label': instance.get_status_display(),
            },
            'result': {
                'code': instance.result,
                'label': instance.get_result_display(),
            },
        }

        return {
            **super().to_representation(instance, *args, **kwargs),
            **representation,
        }
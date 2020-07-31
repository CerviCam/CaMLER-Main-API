from rest_framework import serializers
from django.contrib.auth.models import User as DjangoUser
from apps.v1.user import models
from apps.v1.common import tools

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Place
        fields = (
            "id",
            "created_at",
            "updated_at",   
            "country",
            "province",
            "city",
            "street_name",
            "postal_code",
        )

class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Degree
        fields = (
            "id",
            "created_at",
            "updated_at",
            "instance_name",
            "name",
        )

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DjangoUser
        fields = (
            "username",
            "is_staff",
            "is_active",
            "password",
        )
        extra_kwargs = {
            "is_staff": {
                "read_only": True
            },
            "is_active": {
                "read_only": True
            },
            "password": {
                'write_only': True,
            }
        }

    def create(self, validated_data):
        user = self.Meta.model.objects.create(
            username = validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class UserSerializer(serializers.ModelSerializer):
    degree = DegreeSerializer(many = False)
    workplace = PlaceSerializer(many = False)
    account = AccountSerializer(many = False)

    class Meta:
        model = models.User
        fields = (
            "id",
            "created_at",
            "updated_at",
            "name",
            "gender",
            "account",
            "degree",
            "workplace",
        )

    def create(self, validated_data):
        ModelClass = self.Meta.model
        for field_name in self.Meta.fields:
            field = self.fields[field_name]
            if isinstance(field, serializers.BaseSerializer):
                SerializerClass = field.__class__

                serializer_field = SerializerClass(data = validated_data.pop(field_name), many = False)
                serializer_field.is_valid(raise_exception = True)
                validated_data[field_name] = serializer_field.save()

        user = ModelClass.objects.create(
            **validated_data,
        )

        return user

    def update(self, instance, validated_data):
        for field_name in self.Meta.fields:
            field = self.fields[field_name]
            if isinstance(field, serializers.BaseSerializer):
                SerializerClass = field.__class__

                instance_child_data = validated_data.pop(field_name, None)
                if instance_child_data == None:
                    continue

                serializer_field = SerializerClass(
                    getattr(instance, field_name),
                    data = instance_child_data,
                    many = False,
                )
                serializer_field.is_valid(raise_exception = True)
                serializer_field.save()
            else:
                setattr(instance, field_name, validated_data.get(field_name, getattr(instance, field_name)))

        instance.save()
        return instance

    def to_representation(self, instance, *args, **kwargs):
        representation = {
            'gender': {
                'code': instance.gender,
                'label': instance.get_gender_display(),
            }
        }

        return {
            **super().to_representation(instance, *args, **kwargs),
            **representation,
        }

from django.contrib import admin
from rest_framework_api_key.admin import ApiKeyAdmin
from rest_framework_api_key.models import APIKey

# Override API Key admin
class MyApiKeyAdmin(ApiKeyAdmin):
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


admin.site.unregister(APIKey)
admin.site.register(APIKey, MyApiKeyAdmin)
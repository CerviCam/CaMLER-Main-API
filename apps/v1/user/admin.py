from django.contrib import admin
from apps.v1.user.models import User, Degree, Place

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "gender", "account", "created_at", "updated_at")
admin.site.register(User, UserAdmin)

admin.site.register(Degree)
admin.site.register(Place)

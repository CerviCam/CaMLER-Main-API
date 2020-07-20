from django.contrib import admin
from apps.v1.user.models import User, Degree, Place

# Register your models here.
admin.site.register(User)
admin.site.register(Degree)
admin.site.register(Place)

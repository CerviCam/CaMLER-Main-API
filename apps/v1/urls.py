from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.v1.auth.urls')),
    path('users/', include('apps.v1.user.urls')),
]
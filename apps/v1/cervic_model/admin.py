from django.contrib import admin
from apps.v1.cervic_model import models

# Register your models here.
class CervicClassificationAdmin(admin.ModelAdmin):
    list_display = ("creator", "status", "result", "created_at", "updated_at")
admin.site.register(models.CervicClassification, CervicClassificationAdmin)

class AIModelAdmin(admin.ModelAdmin):
    list_display = ("name", "model", "is_chosen")
admin.site.register(models.AIModel, AIModelAdmin)
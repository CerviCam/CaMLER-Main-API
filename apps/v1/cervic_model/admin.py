from django.contrib import admin
from apps.v1.cervic_model import models

# Register your models here.
def send_instance_to_ai_api(instance):
    if instance.status == models.CervicClassification.Status.WAITING:
        return 

    models.classify_instance(instance) 

def classify_selected_instances(modeladmin, request, queryset):
    for instance in queryset:
        send_instance_to_ai_api(instance)

classify_selected_instances.short_description = "Classify instances"


class CervicClassificationAdmin(admin.ModelAdmin):
    list_display = ("creator", "status", "result", "created_at", "updated_at")
    list_filter = ("status", "result")
    search_fields = ("creator__name",)
    readonly_fields = ("status", "result")
    actions = (classify_selected_instances,)

admin.site.register(models.CervicClassification, CervicClassificationAdmin)

class AIModelAdmin(admin.ModelAdmin):
    list_display = ("name", "model", "is_chosen")

admin.site.register(models.AIModel, AIModelAdmin)
from django.contrib import admin
from .models import Mandate


# Register your models here.
@admin.register(Mandate)
class MandateAdmin(admin.ModelAdmin):
    list_display = ("mandateCode", "branch", "accountNumber", "subscriberCode", "created_at")
    list_filter = ("branch",)

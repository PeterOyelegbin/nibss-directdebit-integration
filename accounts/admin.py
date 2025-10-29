from django.contrib import admin
from .models import UserModel, AuditLog


# Register your models here.
@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_active")
    filter_horizontal = ('groups', 'user_permissions')
    list_filter = ("role",)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("user", "action", "details", "created_at")
    
from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from .managers import UserModelManager


# Create your models here.
class Role(models.TextChoices):
    CSO = 'CSO', "CSO"
    CREDIT = 'CREDIT', "Credit"
    IT = 'IT', "IT"
    OTHERS = 'OTHERS', "Others"
    

class UserModel(AbstractUser):
    """
    This model will serve as the default authentication model via AUTH_USER_MODEL in settings.py
    """
    username = None
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(choices=Role.choices, max_length=50)
    is_active = models.BooleanField(verbose_name="Active")
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserModelManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['-date_joined']


class AuditLog(models.Model):
    """
    This model will serve as the audit trail to log users activity
    """
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    user = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
    
    def __str__(self):
        return f"{self.action} by {self.user} at {self.created_at}"
    
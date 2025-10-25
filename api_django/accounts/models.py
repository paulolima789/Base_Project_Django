from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.conf import settings
try:
    from django.contrib.postgres.fields import ArrayField
except Exception:
    ArrayField = None

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Usuário deve ter um email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_social_account = models.BooleanField(default=False)
    totp_secret = models.CharField(max_length=128, blank=True, null=True)
    route_permissions = models.JSONField(default=list, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class SocialAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='social_accounts')
    provider = models.CharField(max_length=50)
    social_id = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.URLField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    raw_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('provider', 'social_id')

    def __str__(self):
        return f"{self.provider} - {self.email or self.name}"

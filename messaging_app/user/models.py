from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db.models import BooleanField, CharField, DateTimeField, EmailField


class UserManager(BaseUserManager):
    def create_user(self, username: str, password=None, **extra_fields):
        if not username:
            raise ValueError("Username field is required")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username: str, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(username, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    username = CharField(max_length=250, unique=True, blank=False)
    email = EmailField(blank=False, unique=True)
    first_name = CharField(max_length=100, blank=False)
    last_name = CharField(max_length=100, blank=False)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"

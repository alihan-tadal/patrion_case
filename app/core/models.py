from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppors using email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    surname = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    factory = models.ForeignKey(
        "Factory", on_delete=models.CASCADE, blank=True, null=True
    )

    objects = UserManager()

    USERNAME_FIELD = "email"


class Equipment(models.Model):
    """Equipment object"""

    name = models.CharField(max_length=255, unique=True)
    factory = models.ForeignKey(
        "Factory", related_name="equipments", on_delete=models.CASCADE
    )
    description = models.CharField(max_length=255)
    price = models.FloatField()
    date = models.DateField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Property(models.Model):
    """Property object"""

    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    equipment = models.ForeignKey("Equipment", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Factory(models.Model):
    """Factory object"""

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    @property
    def first_user_id(self):
        return self.user_set.first().id

    def __str__(self):
        return self.name

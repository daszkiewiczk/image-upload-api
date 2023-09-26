from django.db import models

# from django.contrib.auth.models import User
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class AccountTier(models.Model):
    name = models.CharField(max_length=100)
    thumbnail_sizes = models.ManyToManyField("ThumbnailSize")
    original_link = models.BooleanField(default=False)
    expiring_link = models.BooleanField(default=False)


class ThumbnailSize(models.Model):
    height = models.PositiveIntegerField()


class UploadedImage(models.Model):
    user = models.ForeignKey("MyUser", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="uploaded_images/")
    upload_time = models.DateTimeField(auto_now_add=True)


class ImageLink(models.Model):
    uploaded_image = models.ForeignKey(UploadedImage, on_delete=models.CASCADE)
    link = models.URLField()
    expiration_time = models.DateTimeField(null=True, blank=True)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    tier = models.ForeignKey(
        AccountTier, on_delete=models.CASCADE, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
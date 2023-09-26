from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import FileExtensionValidator
import os
import uuid


def extension(filename):
    """Return file extension"""
    return filename.rsplit(".", 1)[1].lower()


def image_file_path(instance, filename):
    """Generate file path for new image"""
    ext = extension(filename)
    filename = f"{uuid.uuid4()}.{ext}"

    return os.path.join("images/", filename)


class AccountTier(models.Model):
    name = models.CharField(max_length=100)
    thumbnail_sizes = models.ManyToManyField("ThumbnailSize")
    original_link = models.BooleanField(default=False)
    expiring_link = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ThumbnailSize(models.Model):
    height = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.height}px"


class UploadedImage(models.Model):
    user = models.ForeignKey("MyUser", on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=image_file_path,
        validators=[FileExtensionValidator(["png", "jpg", "jpeg"])],
    )
    upload_time = models.DateTimeField(auto_now_add=True)


class ImageLink(models.Model):
    class LinkType(models.TextChoices):
        ORIGINAL = "original"
        EXPIRING = "expiring"
        THUMBNAIL = "thumbnail"

    uploaded_image = models.ForeignKey(
        UploadedImage, on_delete=models.CASCADE, related_name="links"
    )
    link = models.URLField()
    expiration_time = models.DateTimeField(null=True, blank=True)
    type = models.CharField(
        max_length=10, choices=LinkType.choices, default=LinkType.THUMBNAIL
    )


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
        user.tier = AccountTier.objects.get(name="Enterprise")
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

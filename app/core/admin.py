from django.contrib import admin
from .models import AccountTier, ThumbnailSize, MyUser

admin.site.register(MyUser)
admin.site.register(AccountTier)
admin.site.register(ThumbnailSize)

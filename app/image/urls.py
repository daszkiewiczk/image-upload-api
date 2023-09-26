from django.urls import path, include

from .views import ImageView, CreateExpiringImageLinkView
from .views import expiring_link_view

urlpatterns = [
    path("", ImageView.as_view(), name="images"),
    path("links/", CreateExpiringImageLinkView.as_view(), name="make-expiring-link"),
    path("expiring/<int:link_id>/", expiring_link_view, name="expiring-link"),
]

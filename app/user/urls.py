from django.urls import path
from user import views

urlpatterns = [
    path("token/", views.CreateTokenView.as_view(), name="token"),
]

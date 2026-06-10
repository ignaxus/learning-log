from django.urls import path, include

from . import views

app_name = "users"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
    path("my_account/", views.my_account, name="my_account")
]

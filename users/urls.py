from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import path, include, reverse_lazy

from . import views

app_name = "users"

urlpatterns = [
    path("password_change/", 
        auth_views.PasswordChangeView.as_view(success_url=reverse_lazy("users:password_change_done")),
        name="password_change",),

    path("", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
    path("my_account/", views.my_account, name="my_account")
]

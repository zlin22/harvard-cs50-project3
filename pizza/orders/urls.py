from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    # path("create_account_view", views.create_account_view, name="create_account_view"),
    path("create_account", views.create_account, name="create_account"),
]

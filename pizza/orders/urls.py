from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("create_account", views.create_account, name="create_account"),
    path("add_to_cart_item/<int:menu_item_id>", views.add_to_cart_item, name="add_to_cart_item"),
    path("add_to_cart_addition/<int:order_item_id>", views.add_to_cart_addition, name="add_to_cart_addition"),
    path("cart", views.view_cart, name="view_cart"),
    path("order/<int:order_id>", views.order_confirmation, name="order_confirmation"),
    path("pay", views.pay, name="pay"),
]

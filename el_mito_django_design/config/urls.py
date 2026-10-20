from django.contrib import admin
from django.urls import path
from store import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("shop/", views.shop, name="shop"),
    path("product/<slug:slug>/", views.product_detail, name="product"),
    path("cart/", views.cart, name="cart"),
    path("cart/add/<slug:slug>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<slug:slug>/", views.update_cart, name="update_cart"),
    path("cart/remove/<slug:slug>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("login/", views.login_page, name="login"),
    path("verify/", views.verify_page, name="verify"),
    path("orders/", views.orders_page, name="orders"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]

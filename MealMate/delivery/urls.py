from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),

    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("logout/", views.signout, name="logout"),

    path(
        "customer-home/",
        views.customer_home,
        name="customer_home",
    ),
    path(
        "customer-restaurants/",
        views.customer_restaurants,
        name="customer_restaurants",
    ),
    path(
        "customer-restaurants/<int:restaurant_id>/",
        views.restaurant_detail,
        name="restaurant_detail",
    ),

    path("profile/", views.profile, name="profile"),
    path(
        "profile/edit/",
        views.edit_profile,
        name="edit_profile",
    ),
    path(
        "profile/change-password/",
        views.change_password,
        name="change_password",
    ),

    path(
        "admin-dashboard/restaurants/",
        views.restaurant_list,
        name="restaurant_list",
    ),
    path(
        "admin-dashboard/restaurants/add/",
        views.add_restaurant,
        name="add_restaurant",
    ),
    path(
        "admin-dashboard/restaurants/<int:restaurant_id>/update/",
        views.update_restaurant,
        name="update_restaurant",
    ),
    path(
        "admin-dashboard/restaurants/<int:restaurant_id>/delete/",
        views.delete_restaurant,
        name="delete_restaurant",
    ),

    path(
        "admin-dashboard/menu/add/",
        views.add_menu_item,
        name="add_menu_item",
    ),
    path(
        "admin-dashboard/menu/",
        views.menu_item_list,
        name="menu_item_list",
    ),
    path(
        "admin-dashboard/menu/<int:menu_item_id>/update/",
        views.update_menu_item,
        name="update_menu_item",
    ),
    path(
        "admin-dashboard/menu/<int:menu_item_id>/delete/",
        views.delete_menu_item,
        name="delete_menu_item",
    ),

    path(
        "cart/add/<int:menu_item_id>/",
        views.add_to_cart,
        name="add_to_cart",
    ),
    path("cart/", views.view_cart, name="view_cart"),
    path(
        "cart/increase/<int:cart_item_id>/",
        views.increase_cart_item,
        name="increase_cart_item",
    ),
    path(
        "cart/decrease/<int:cart_item_id>/",
        views.decrease_cart_item,
        name="decrease_cart_item",
    ),
    path(
        "cart/remove/<int:cart_item_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),

    path("checkout/", views.checkout, name="checkout"),
    path(
        "payment/verify/",
        views.verify_payment,
        name="verify_payment",
    ),
    path(
        "payment/failed/",
        views.mark_payment_failed,
        name="mark_payment_failed",
    ),
path("checkout/", views.checkout, name="checkout"),
    path(
        "place-order/",
        views.place_order,
        name="place_order",
    ),
    path(
        "order-success/<int:order_id>/",
        views.order_success,
        name="order_success",
    ),

    path("my-orders/", views.my_orders, name="my_orders"),
    path(
        "my-orders/<int:order_id>/",
        views.order_detail,
        name="order_detail",
    ),

    path(
        "admin-dashboard/orders/",
        views.admin_orders,
        name="admin_orders",
    ),
    path(
        "admin-dashboard/orders/<int:order_id>/status/",
        views.update_order_status,
        name="update_order_status",
    ),
]


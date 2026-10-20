from django.contrib import admin
from .models import PaymentAttempt
admin.site.register(PaymentAttempt)
from .models import (
    CustomerProfile,
    Restaurant,
    MenuItem,
    Order,
    OrderItem
)


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "mobile",
        "address",
    )


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "cuisine",
        "rating",
        "location",
    )


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "restaurant",
        "price",
        "is_vegetarian",
        "is_available",
    )

    list_filter = (
        "restaurant",
        "is_vegetarian",
        "is_available",
    )

    search_fields = (
        "name",
        "restaurant__name",
    )
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "total_amount",
        "status",
        "payment_status",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_status",
        "created_at",
    )

    search_fields = (
        "user__username",
        "id",
    )
    

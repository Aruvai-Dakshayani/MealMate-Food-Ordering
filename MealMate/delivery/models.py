from django.db import models
from django.contrib.auth.models import User


class CustomerProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    mobile = models.CharField(
        max_length=15
    )

    address = models.TextField()

    def __str__(self):
        return self.user.username


class Restaurant(models.Model):

    name = models.CharField(
        max_length=200
    )

    picture = models.URLField(
        blank=True
    )

    cuisine = models.CharField(
        max_length=100
    )

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1
    )

    description = models.TextField(
        blank=True
    )

    location = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return self.name
    
    
class MenuItem(models.Model):

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="menu_items"
    )

    name = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    image = models.URLField(
        blank=True
    )

    is_vegetarian = models.BooleanField(
        default=False
    )

    is_available = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name
    
    
class Cart(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    added_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["cart", "menu_item"],
                name="unique_cart_menu_item"
            )
        ]

    def get_total_price(self):

        return self.menu_item.price * self.quantity

    def __str__(self):

        return f"{self.menu_item.name} x {self.quantity}"
    
    
class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Preparing", "Preparing"),
        ("Out for Delivery", "Out for Delivery"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Failed", "Failed"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    delivery_address = models.TextField()

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="Pending"
    )

    razorpay_order_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True
    )

    razorpay_payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    razorpay_signature = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    item_name = models.CharField(
        max_length=200
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField()

    def get_total_price(self):

        return self.price * self.quantity

    def __str__(self):

        return f"{self.item_name} x {self.quantity}"
    
    
    
class PaymentAttempt(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="payment_attempts"
    )

    payment_id = models.CharField(
        max_length=100,
        blank=True
    )

    status = models.CharField(
        max_length=30,
        default="Reported failed"
    )

    failure_reason = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Payment attempt for Order {self.order_id} - "
            f"{self.status}"
        )
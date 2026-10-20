
import razorpay

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db import transaction

from .models import (
    CustomerProfile,
    Restaurant,
    MenuItem,
    Cart,
    CartItem,
    Order,
    OrderItem,
    PaymentAttempt,
)

from .forms import (
    SignUpForm,
    RestaurantForm,
    MenuItemForm,
    ProfileForm,
)

User = get_user_model()


# -----------------------------
# MealMate Landing Page
# -----------------------------
def home(request):
    return render(request, "delivery/index.html")


# -----------------------------
# Customer Signup
# -----------------------------
def signup(request):
    if request.user.is_authenticated:
        return redirect("customer_home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        mobile = request.POST.get("mobile", "").strip()
        address = request.POST.get("address", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not all([
            username,
            email,
            mobile,
            address,
            password,
            confirm_password,
        ]):
            messages.error(request, "Please fill in all fields.")
            return render(request, "delivery/signup.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "delivery/signup.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "This username is already taken.")
            return render(request, "delivery/signup.html")

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "This email is already registered.")
            return render(request, "delivery/signup.html")

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                )

                CustomerProfile.objects.create(
                    user=user,
                    mobile=mobile,
                    address=address,
                )

            login(request, user)
            return redirect("customer_home")

        except Exception:
            messages.error(
                request,
                "We could not create your account. "
                "Please check your details and try again.",
            )
            return render(request, "delivery/signup.html")

    return render(request, "delivery/signup.html")


# -----------------------------
# Customer Sign In
# -----------------------------
def signin(request):
    if request.user.is_authenticated:
        return redirect("customer_home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect("customer_home")

        messages.error(request, "Invalid username or password.")
        return redirect("signin")

    return render(request, "delivery/signin.html")


# -----------------------------
# Customer Home
# -----------------------------
@login_required
def customer_home(request):
    restaurants = Restaurant.objects.all().order_by("name")

    return render(
        request,
        "delivery/customer_home.html",
        {"restaurants": restaurants},
    )


# -----------------------------
# Logout
# -----------------------------
def signout(request):
    logout(request)
    return redirect("signin")


# -----------------------------
# Admin - Restaurant List
# -----------------------------
@staff_member_required
def restaurant_list(request):
    restaurants = Restaurant.objects.all().order_by("name")

    return render(
        request,
        "delivery/restaurant_list.html",
        {"restaurants": restaurants},
    )


# -----------------------------
# Admin - Add Restaurant
# -----------------------------
@staff_member_required
def add_restaurant(request):
    if request.method == "POST":
        form = RestaurantForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("restaurant_list")
    else:
        form = RestaurantForm()

    return render(
        request,
        "delivery/add_restaurant.html",
        {"form": form},
    )


# -----------------------------
# Admin - Update Restaurant
# -----------------------------
@staff_member_required
def update_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(
        Restaurant,
        id=restaurant_id,
    )

    if request.method == "POST":
        form = RestaurantForm(
            request.POST,
            request.FILES,
            instance=restaurant,
        )

        if form.is_valid():
            form.save()
            return redirect("restaurant_list")
    else:
        form = RestaurantForm(instance=restaurant)

    return render(
        request,
        "delivery/update_restaurant.html",
        {
            "form": form,
            "restaurant": restaurant,
        },
    )


# -----------------------------
# Admin - Delete Restaurant
# -----------------------------
@staff_member_required
def delete_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(
        Restaurant,
        id=restaurant_id,
    )

    if request.method == "POST":
        restaurant.delete()
        return redirect("restaurant_list")

    return render(
        request,
        "delivery/delete_restaurant.html",
        {"restaurant": restaurant},
    )


# -----------------------------
# Admin - Add Menu Item
# -----------------------------
@staff_member_required
def add_menu_item(request):
    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("menu_item_list")
    else:
        form = MenuItemForm()

    return render(
        request,
        "delivery/add_menu_item.html",
        {"form": form},
    )


# -----------------------------
# Admin - Menu Item List
# -----------------------------
@staff_member_required
def menu_item_list(request):
    menu_items = MenuItem.objects.select_related(
        "restaurant"
    ).all()

    return render(
        request,
        "delivery/menu_item_list.html",
        {"menu_items": menu_items},
    )


# -----------------------------
# Admin - Update Menu Item
# -----------------------------
@staff_member_required
def update_menu_item(request, menu_item_id):
    menu_item = get_object_or_404(
        MenuItem,
        id=menu_item_id,
    )

    if request.method == "POST":
        form = MenuItemForm(
            request.POST,
            request.FILES,
            instance=menu_item,
        )

        if form.is_valid():
            form.save()
            return redirect("menu_item_list")
    else:
        form = MenuItemForm(instance=menu_item)

    return render(
        request,
        "delivery/update_menu_item.html",
        {
            "form": form,
            "menu_item": menu_item,
        },
    )


# -----------------------------
# Customer - Restaurant List
# -----------------------------

@login_required
def customer_restaurants(request):
    restaurants = Restaurant.objects.all()

    restaurant_images = {
        "Andhra Spice Kitchen": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=900&auto=format&fit=crop",
        "Burger House": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=900&auto=format&fit=crop",
        "Domino's Pizza": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=900&auto=format&fit=crop",
        "Fresh Bowl": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=900&auto=format&fit=crop",
        "Green Leaf Kitchen": "https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=900&auto=format&fit=crop",
        "Spice Route": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=900&auto=format&fit=crop",
        "Sweet Treats Cafe": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=900&auto=format&fit=crop",
        "Tandoori Flames": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=900&auto=format&fit=crop",
        "Urban Slice": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=900&auto=format&fit=crop",
    }

    for restaurant in restaurants:
        restaurant.image_url = restaurant_images.get(
            restaurant.name,
            "https://images.unsplash.com/photo-1546549032-9571cd6b27df?w=900&auto=format&fit=crop"
        )

    return render(
        request,
        "delivery/customer_restaurants.html",
        {"restaurants": restaurants}
    )



# -----------------------------
# Customer - Restaurant Details
# -----------------------------
@login_required
def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(
        Restaurant,
        id=restaurant_id,
    )

    menu_items = MenuItem.objects.filter(
        restaurant=restaurant
    )

    return render(
        request,
        "delivery/restaurant_detail.html",
        {
            "restaurant": restaurant,
            "menu_items": menu_items,
        },
    )


# -----------------------------
# Customer - Add Item to Cart
# -----------------------------
@login_required
def add_to_cart(request, menu_item_id):
    menu_item = get_object_or_404(
        MenuItem,
        id=menu_item_id,
    )

    cart, created = Cart.objects.get_or_create(
        user=request.user,
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        menu_item=menu_item,
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("view_cart")


# -----------------------------
# Customer - View Cart
# -----------------------------
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user,
    )

    cart_items = cart.items.select_related("menu_item")

    total_price = sum(
        item.get_total_price()
        for item in cart_items
    )

    return render(
        request,
        "delivery/cart.html",
        {
            "cart_items": cart_items,
            "total_price": total_price,
        },
    )


# -----------------------------
# Customer - Increase Cart Item
# -----------------------------
@login_required
def increase_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=cart_item_id,
        cart__user=request.user,
    )

    cart_item.quantity += 1
    cart_item.save()

    return redirect("view_cart")


# -----------------------------
# Customer - Decrease Cart Item
# -----------------------------
@login_required
def decrease_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=cart_item_id,
        cart__user=request.user,
    )

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect("view_cart")


# -----------------------------
# Customer - Remove Item from Cart
# -----------------------------
@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=cart_item_id,
        cart__user=request.user,
    )

    cart_item.delete()

    return redirect("view_cart")


# -----------------------------
# Customer - Checkout
# -----------------------------
@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user,
    )

    cart_items = cart.items.select_related("menu_item")

    if not cart_items.exists():
        return redirect("view_cart")

    subtotal = sum(
        item.get_total_price()
        for item in cart_items
    )

    delivery_fee = 40
    total_amount = subtotal + delivery_fee

    profile, created = CustomerProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "mobile": "",
            "address": "",
        },
    )

    pending_order = None
    pending_order_id = request.session.get("pending_order_id")

    if pending_order_id:
        try:
            pending_order = Order.objects.get(
                id=pending_order_id,
                user=request.user,
                payment_status="Pending",
            )
        except Order.DoesNotExist:
            pending_order = None

    if pending_order is None:
        pending_order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            delivery_address=profile.address,
            status="Pending",
            payment_status="Pending",
        )

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=pending_order,
                menu_item=cart_item.menu_item,
                item_name=cart_item.menu_item.name,
                price=cart_item.menu_item.price,
                quantity=cart_item.quantity,
            )

        request.session["pending_order_id"] = pending_order.id

    if not pending_order.razorpay_order_id:
        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET,
            )
        )

        razorpay_order = client.order.create(
            data={
                "amount": int(total_amount * 100),
                "currency": "INR",
                "payment_capture": 1,
            }
        )

        pending_order.razorpay_order_id = razorpay_order["id"]
        pending_order.save(update_fields=["razorpay_order_id"])

    return render(
        request,
        "delivery/checkout.html",
        {
            "cart_items": cart_items,
            "subtotal": subtotal,
            "delivery_fee": delivery_fee,
            "total_amount": total_amount,
            "profile": profile,
            "razorpay_order_id": pending_order.razorpay_order_id,
            "razorpay_key_id": settings.RAZORPAY_KEY_ID,
            "razorpay_amount": int(total_amount * 100),
        },
    )


# -----------------------------
# Customer - Place Order
# -----------------------------
@login_required
def place_order(request):
    if request.method != "POST":
        return redirect("checkout")

    cart, created = Cart.objects.get_or_create(
        user=request.user,
    )

    cart_items = cart.items.select_related("menu_item")

    if not cart_items.exists():
        return redirect("view_cart")

    subtotal = sum(
        item.get_total_price()
        for item in cart_items
    )

    delivery_fee = 40
    total_amount = subtotal + delivery_fee

    profile = get_object_or_404(
        CustomerProfile,
        user=request.user,
    )

    order = Order.objects.create(
        user=request.user,
        total_amount=total_amount,
        delivery_address=profile.address,
        status="Pending",
    )

    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            menu_item=cart_item.menu_item,
            item_name=cart_item.menu_item.name,
            price=cart_item.menu_item.price,
            quantity=cart_item.quantity,
        )

    cart_items.delete()

    return redirect("order_success", order_id=order.id)


# -----------------------------
# Customer - Order Success
# -----------------------------
@login_required
def order_success(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    return render(
        request,
        "delivery/order_success.html",
        {"order": order},
    )


# -----------------------------
# Customer - My Orders
# -----------------------------
@login_required
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "delivery/my_orders.html",
        {"orders": orders},
    )


# -----------------------------
# Admin - Orders
# -----------------------------
@staff_member_required
def admin_orders(request):
    orders = Order.objects.select_related(
        "user"
    ).order_by("-created_at")

    return render(
        request,
        "delivery/admin_orders.html",
        {
            "orders": orders,
            "status_choices": Order.STATUS_CHOICES,
        },
    )


# -----------------------------
# Admin - Update Order Status
# -----------------------------
@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
    )

    if request.method == "POST":
        new_status = request.POST.get("status")

        valid_statuses = [
            choice[0]
            for choice in Order.STATUS_CHOICES
        ]

        if new_status in valid_statuses:
            order.status = new_status
            order.save(update_fields=["status"])

    return redirect("admin_orders")


# -----------------------------
# Customer - Order Details
# -----------------------------
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    return render(
        request,
        "delivery/order_detail.html",
        {"order": order},
    )


# -----------------------------
# Admin - Delete Menu Item
# -----------------------------
@staff_member_required
def delete_menu_item(request, menu_item_id):
    menu_item = get_object_or_404(
        MenuItem,
        id=menu_item_id,
    )

    if request.method == "POST":
        menu_item.delete()
        return redirect("menu_item_list")

    return render(
        request,
        "delivery/delete_menu_item.html",
        {"menu_item": menu_item},
    )


# -----------------------------
# Customer - Profile
# -----------------------------
@login_required
def profile(request):
    customer_profile, created = CustomerProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "mobile": "",
            "address": "",
        },
    )

    return render(
        request,
        "delivery/profile.html",
        {"customer_profile": customer_profile},
    )


# -----------------------------
# Customer - Edit Profile
# -----------------------------
@login_required
def edit_profile(request):
    profile, created = CustomerProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "mobile": "",
            "address": "",
        },
    )

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(
        request,
        "delivery/edit_profile.html",
        {"form": form},
    )


# -----------------------------
# Customer - Change Password
# -----------------------------
@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(
            request.user,
            request.POST,
        )

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")
    else:
        form = PasswordChangeForm(request.user)

    return render(
        request,
        "delivery/change_password.html",
        {"form": form},
    )


# -----------------------------
# Razorpay - Payment Verification
# -----------------------------
@login_required
def verify_payment(request):
    if request.method != "POST":
        return redirect("checkout")

    payment_id = request.POST.get("razorpay_payment_id")
    razorpay_order_id = request.POST.get("razorpay_order_id")
    razorpay_signature = request.POST.get("razorpay_signature")

    if not payment_id or not razorpay_order_id or not razorpay_signature:
        return render(
            request,
            "delivery/order_success.html",
            {
                "payment_failed": True,
                "error_message": "Payment information was incomplete.",
            },
        )

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET,
        )
    )

    try:
        client.utility.verify_payment_signature(
            {
                "razorpay_payment_id": payment_id,
                "razorpay_order_id": razorpay_order_id,
                "razorpay_signature": razorpay_signature,
            }
        )
    except razorpay.errors.SignatureVerificationError:
        return render(
            request,
            "delivery/order_success.html",
            {
                "payment_failed": True,
                "error_message": "Payment verification failed.",
            },
        )

    order = get_object_or_404(
        Order,
        razorpay_order_id=razorpay_order_id,
        user=request.user,
    )

    order.razorpay_payment_id = payment_id
    order.razorpay_signature = razorpay_signature
    order.payment_status = "Paid"

    order.save(
        update_fields=[
            "razorpay_payment_id",
            "razorpay_signature",
            "payment_status",
        ]
    )

    cart, created = Cart.objects.get_or_create(
        user=request.user,
    )
    cart.items.all().delete()

    request.session.pop("pending_order_id", None)

    return redirect("order_success", order_id=order.id)


# -----------------------------
# Razorpay - Payment Failure
# -----------------------------
@login_required
def mark_payment_failed(request):
    if request.method != "POST":
        return redirect("checkout")

    razorpay_order_id = request.POST.get("razorpay_order_id")
    payment_id = request.POST.get(
        "razorpay_payment_id",
        "",
    ).strip()

    if not razorpay_order_id:
        return redirect("checkout")

    order = get_object_or_404(
        Order,
        razorpay_order_id=razorpay_order_id,
        user=request.user,
    )

    if order.payment_status == "Paid":
        return redirect("my_orders")

    attempt = PaymentAttempt.objects.create(
        order=order,
        payment_id=payment_id,
        status="Reported failed",
        failure_reason=(
            "Razorpay Checkout reported a failed payment attempt. "
            "This attempt has not yet been verified with Razorpay."
        ),
    )

    if not payment_id:
        return redirect("checkout")

    try:
        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET,
            )
        )

        payment = client.payment.fetch(payment_id)

        if payment.get("order_id") != order.razorpay_order_id:
            attempt.failure_reason = (
                "Payment order ID did not match the MealMate order."
            )
            attempt.save(update_fields=["failure_reason"])
            return redirect("checkout")

        if payment.get("status") == "failed":
            attempt.status = "Verified failed"
            attempt.failure_reason = (
                payment.get("error_description")
                or "Razorpay confirmed that this payment failed."
            )
        else:
            attempt.status = "Not confirmed failed"
            attempt.failure_reason = (
                "Razorpay did not confirm a failed payment status."
            )

        attempt.save(
            update_fields=["status", "failure_reason"]
        )

    except Exception:
        attempt.failure_reason = (
            "Could not verify this attempt with Razorpay."
        )
        attempt.save(update_fields=["failure_reason"])

    return redirect("checkout")

from django import forms
from django.contrib.auth.models import User

from .models import CustomerProfile, Restaurant, MenuItem


class SignUpForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    mobile = forms.CharField(
        max_length=15
    )

    address = forms.CharField(
        widget=forms.Textarea
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
        ]

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:

            if password != confirm_password:

                raise forms.ValidationError(
                    "Passwords do not match."
                )

        return cleaned_data

class ProfileForm(forms.ModelForm):

    class Meta:
        model = CustomerProfile
        fields = [
            "mobile",
            "address",
        ]

        widgets = {
            "address": forms.Textarea(attrs={
                "rows": 4
            }),
        }
class RestaurantForm(forms.ModelForm):

    class Meta:
        model = Restaurant

        fields = [
            "name",
            "picture",
            "cuisine",
            "rating",
            "description",
            "location",
        ]
        
class MenuItemForm(forms.ModelForm):

    class Meta:
        model = MenuItem

        fields = [
            "restaurant",
            "name",
            "description",
            "price",
            "image",
            "is_vegetarian",
            "is_available",
        ]
# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from django.core.validators import MaxValueValidator, MinValueValidator
# from .models import Profile
#
#
# class RegisterForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     balance = forms.DecimalField(max_digits=7, decimal_places=2,
#                                  validators=[MinValueValidator(100.00), MaxValueValidator(1000.00)],
#                                  help_text="Enter an initial balance between £100.00 and £1000.00.")
#
#     class Meta:
#         model = User
#         fields = ("username", "email", "password1", "password2", "balance")
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         if commit:
#             user.save()
#             user.profile.balance = self.cleaned_data['balance']
#             user.profile.save()
#         return user

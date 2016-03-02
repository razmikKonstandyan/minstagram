from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserPageData, UserProfileData

# from django.contrib.auth.models import User

"""
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            msg = "Passwords don't match"
            raise forms.ValidationError("Password mismatch")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
"""


class MakePostForm(forms.ModelForm):
    class Meta:
        model = UserPageData
        fields = [
            "title",
            "image",
        ]


class EditInfo(forms.ModelForm):
    class Meta:
        model = UserProfileData
        fields = [
            "status",
            "avatar",
            "age",
        ]


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")

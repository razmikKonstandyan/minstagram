from django import forms

from .models import UserPage


# Create form for a new post

class MakePostForm(forms.ModelForm):
    class Meta:
        model = UserPage
        fields = [
            "title",
            "image"
        ]

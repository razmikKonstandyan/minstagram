from django import forms

from .models import UserPageData


# Create form for a new post

class MakePostForm(forms.ModelForm):
    class Meta:
        model = UserPageData
        fields = [
            "title",
            "image",
        ]
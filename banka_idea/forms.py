from django import forms
from django.contrib.auth.forms import UserCreationForm

from banka_idea.models import Idea, User, IdeaTags


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=("Email",),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete":"email"})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = "__all__"
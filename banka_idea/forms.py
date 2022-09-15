from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import UserCreationForm

from banka_idea.models import Idea, User, IdeaTags, Solution


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=("Email",),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "avatar"]


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'avatar', 'first_name', 'last_name']


class IdeaForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Idea
        fields = "__all__"


class SolutionForm(forms.ModelForm):
    text = forms.CharField(max_length=100, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Solution
        fields = "__all__"

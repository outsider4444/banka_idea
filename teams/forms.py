from django import forms

from .models import Team


class TeamCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'border-radius:25px'}))

    slug = forms.CharField(max_length=100, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'border-radius:25px'}))

    class Meta:
        model = Team
        fields = "__all__"


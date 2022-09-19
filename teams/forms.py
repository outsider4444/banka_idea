from django import forms

from .models import Team


class TeamCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Team
        fields = "__all__"


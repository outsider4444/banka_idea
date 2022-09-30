from django import forms

from report.models import Report


class ReportForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = ['message', 'image']
